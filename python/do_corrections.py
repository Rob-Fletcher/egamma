from ROOT import * 
import argparse
from sys import stdout
import math

gCUTLOW = False
#Et_bins_l = ['0-5', '5-10', '10-15', '15-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-1000000']
Et_bins_l = ['0-1000000']
eta_bins_l = ['0-10']
#eta_bins_l = ['0-0.1', '0.1-0.6', '0.6-0.8', '0.8-1.15', '1.15-1.37', '1.37-1.52', '1.52-1.81', '1.81-2.01', '2.01-2.37', '2.37-2.47']
#fits      = [ [0]*len(Et_bins_l) ]*len(eta_bins_l)
cuts   = {} 
target_Eff = 0.94

#infile_bkg = TFile('~/egamma/Data/June19_2013_jf17_mu80_bs25_z100.root')
#infile_sig = TFile('~/egamma/Data/June19_2013_LHSignal_mu80_bs25_Iso_TIBALE_MC.root')
infile_sig = TFile('~/egamma/Data/March9_2013_LHSignal_Iso_TIBALE.root')
infile_bkg = TFile('~/egamma/Data/March9_2013_LHBkg_z100.root')
tree_sig = infile_sig.Get('photon')
tree_sig.SetBranchStatus('*',0)
tree_sig.SetBranchStatus('el_Et', 1)
tree_sig.SetBranchStatus('el_eta', 1)
tree_sig.SetBranchStatus('averageIntPerXing', 1)
tree_sig.SetBranchStatus('PV_n', 1)
tree_sig.SetBranchStatus('PV_trk_n', 1)

tree_bkg = infile_bkg.Get('photon')
tree_bkg.SetBranchStatus('*',0)
tree_bkg.SetBranchStatus('el_Et', 1)
tree_bkg.SetBranchStatus('el_eta', 1)
tree_bkg.SetBranchStatus('averageIntPerXing', 1)
tree_bkg.SetBranchStatus('PV_n', 1)
tree_bkg.SetBranchStatus('PV_trk_n', 1)

#tree_sig.AddFriend('rhad_tree', '~/egamma/rootfiles/2013_June/rhad_tree_signal_mu80.root')
#tree_bkg.AddFriend('rhad_tree', '~/egamma/rootfiles/2013_June/rhad_tree_background_mu80.root')
tree_sig.AddFriend('rhad_tree', '~/egamma/rootfiles/2013_June/rhad_tree.root')
tree_bkg.AddFriend('rhad_tree', '~/egamma/rootfiles/2013_June/rhad_tree_bkg.root')

outfile = TFile('rhad_eff_Nvtx.root','recreate')


def runIt():
   """Populate and array of cuts as a function of mu

   run the corrections. Loop over all Et and eta bins defined in a list and make 2d histo.
   Then project along the Y axis to get a 1d histo corresponding to one value of mu. For 
   each value of mu find the cut that preserves the efficiency then put that number in
   a histogram. Then fit a line to the histogram that defines a cut on rhad parameterized by mu.
   These parameters go into an dictionary of lambda functions. To get a cut for a specific Et, eta and mu:

         cut = fits[ Et_bin ][ eta_bin ]( mu ) 
   """  
   for Et_index, Et_bin in enumerate(Et_bins_l):
      cuts[Et_bin] = {}
      for eta_index, eta_bin in enumerate(eta_bins_l):
         print 'evaluating bin: ', Et_bin, eta_bin
         h2_temp = makeHisto( Et_bin, eta_bin, eta_index, 'sig' )
         h2_temp_bkg = makeHisto( Et_bin, eta_bin, eta_index, 'bkg')

         hist_to_fit = TH1F('hist_fit', 'hist_fit', 90, 0, 90) 
         count = 0 
         for mu in range( h2_temp.GetNbinsX() ):
            h1 = h2_temp.ProjectionY('h1', mu, mu)

            if h1.Integral(1, h1.GetNbinsX()) < 100:
               continue

            corrected_cut_bin = getCut(h1, target_Eff)

            final_cut = h1.GetBinCenter(corrected_cut_bin)
            hist_to_fit.SetBinContent( mu, final_cut )
            print 'Filling hist to fit with [mu, cut]: ', mu, final_cut, h1.Integral(1, h1.GetNbinsX())
            count = count+1

         if count > 1: 
            hist_to_fit.Fit('pol1','0','goff',5, 88)
            this_fit = hist_to_fit.GetFunction('pol1') 
            param1 = this_fit.GetParameter(1)
            param0 = this_fit.GetParameter(0)

            cuts[Et_bin][eta_bin] = lambda x : param1*x + param0
            print 'putting fit in ', Et_bin, eta_bin

         elif count == 1:
            cuts[Et_bin][eta_bin] = lambda x: final_cut
            print 'Not enough points for fit.'
            print 'Using single cut: ', final_cut

         gROOT.ProcessLine('delete h2_rhad_mu'+str(eta_index)+'sig')
         #gROOT.ProcessLine('delete hist_fit')
         gROOT.ProcessLine('delete h1')
   print 'Dictionary of Fits completed'
   outfile.Write()

def plotWithCuts():
   """Plot rhad vs. Nvtx using cuts with mu


   """

   print'Making plots of Nvtx with cuts on mu'
   for Et_index, Et_bin in enumerate(Et_bins_l):
      outfile.mkdir('Et bin '+Et_bin)
      outfile.cd('Et bin '+Et_bin)
      histo_eff_list = [ TH1F(eta_bin, 'h1', 50, 0, 50) for eta_bin in eta_bins_l ]
      histo_pass_list = [ TH1I(eta_bin+'_pass', 'h1', 50, 0, 50) for eta_bin in eta_bins_l ]
      histo_total_list = [ TH1I(eta_bin+'_total', 'h1', 50, 0, 50) for eta_bin in eta_bins_l ]

      for i in range(tree.GetEntries()):
         tree.GetEntry(i)

         for eta_index, eta_bin in enumerate(eta_bins_l):
       
            Et_cut = [float(x) for x in Et_bin.split('-')]
            eta_cut = [float(x) for x in eta_bin.split('-')]

            if (Et_cut[0] < tree.el_Et and tree.el_Et <= Et_cut[1] and 
               eta_cut[0] < tree.el_eta and tree.el_eta <= eta_cut[1]):  #if this entry makes the cut then fill the total histogram corresponding to eta_index

               histo_total_list[eta_index].Fill(tree.el_Nvtx)

               if tree.rhad_tree.el_rhad < cuts[Et_bin][eta_bin](tree.averageIntPerXing):
                  histo_pass_list[eta_index].Fill( tree.el_Nvtx )  #if this entry passes the cut calculated earlier fill histo corresponding to eta_index
                  print 'Filled pass histo with ', tree.el_Nvtx
       
      for eta_index in range(len(eta_bins_l)):
         histo_eff_list[eta_index].Divide(histo_pass_list[eta_index], histo_total_list[eta_index])      
         histo_eff_list[eta_index].Write()


#   outfile.Write()
   outfile.Close()
             
def plotSimple():

   hist_Nvtx = TH1F('histo_Nvtx', 'Rhad efficiency vs. Nvtx ('+args.c+' cuts)', 90, 0, 90)
   hist_Nvtx.GetYaxis().SetTitle('Rhad Efficiency')
   hist_Nvtx.GetXaxis().SetTitle('Nvtx')
   hist_mu = TH1F('histo_mu', 'Rhad efficiency vs. mu ('+args.c+' cuts)', 90, 0, 90)
   hist_mu.GetYaxis().SetTitle('Rhad Efficiency')
   hist_mu.GetXaxis().SetTitle('mu')
   hist_pass_mu   = TH1F('histo_pass_mu', 'histo_pass_mu', 90, 0, 90)
   hist_pass_Nvtx = TH1F('histo_pass_Nvtx', 'histo_pass_Nvtx', 90, 0, 90)
   hist_total_mu   = TH1F('histo_total_mu', 'histo_total_mu', 90, 0, 90)
   hist_total_Nvtx = TH1F('histo_total_Nvtx', 'histo_total_Nvtx', 90, 0, 90)

   h1_bkg_mu = TH1F('histo_bkg_mu', 'Background efficiency vs. Mu('+args.c+' cuts)', 90, 0, 90)
   h1_bkg_mu.GetYaxis().SetTitle('Rhad Efficiency')
   h1_bkg_mu.GetXaxis().SetTitle('Mu')
   h1_bkg_Nvtx = TH1F('histo_bkg_Nvtx', 'Background efficiency vs. Nvtx('+args.c+' cuts)', 90, 0, 90)
   h1_bkg_Nvtx.GetYaxis().SetTitle('Rhad Efficiency')
   h1_bkg_Nvtx.GetXaxis().SetTitle('Nvtx')
   hist_pass_mu_bkg   = TH1F('histo_pass_mu_bkg', 'histo_pass_mu_bkg', 90, 0, 90)
   hist_pass_Nvtx_bkg = TH1F('histo_pass_Nvtx_bkg', 'histo_pass_Nvtx_bkg', 90, 0, 90)
   hist_total_mu_bkg   = TH1F('histo_total_mu_bkg', 'histo_total_mu_bkg', 90, 0, 90)
   hist_total_Nvtx_bkg = TH1F('histo_total_Nvtx_bkg', 'histo_total_Nvtx_bkg', 90, 0, 90)

   print 'Making signal Histograms with ', args.c, ' cuts.'
   for event in range(tree_sig.GetEntries()):
      if event%10000 == 0:
           perc = int((float(event)/tree_sig.GetEntries())*100)
           stdout.write("\r****** Scanning Event %d /" %event)
           stdout.write(" %d" %tree_sig.GetEntries())
           stdout.write("   %d%%" %perc)
           stdout.flush()

      tree_sig.GetEntry(event)
      hist_total_mu.Fill(tree_sig.averageIntPerXing)
      hist_total_Nvtx.Fill(tree_sig.el_Nvtx)
      if args.c == 'mu':
         if tree_sig.el_rhad <= cuts['0-1000000']['0-10'](tree_sig.averageIntPerXing):
            hist_pass_mu.Fill(tree_sig.averageIntPerXing)
            hist_pass_Nvtx.Fill(tree_sig.el_Nvtx)
      if args.c == 'Nvtx':
         if tree_sig.el_rhad <= cuts['0-1000000']['0-10'](tree_sig.el_Nvtx):
            hist_pass_mu.Fill(tree_sig.averageIntPerXing)
            hist_pass_Nvtx.Fill(tree_sig.el_Nvtx)

   hist_Nvtx.Divide(hist_pass_Nvtx, hist_total_Nvtx)
   setEffErrors( hist_Nvtx, hist_total_Nvtx)
   hist_mu.Divide(hist_pass_mu, hist_total_mu)
   setEffErrors( hist_mu, hist_total_mu)

   print "\nMaking Background Histograms"
   for event in range(tree_bkg.GetEntries()):
      if event%10000 == 0:                            # This just does some status output
           perc = int((float(event)/tree_bkg.GetEntries())*100)
           stdout.write("\r***** Scanning Event %d /" %event)
           stdout.write(" %d" %tree_bkg.GetEntries())
           stdout.write("   %d%%" %perc)
           stdout.flush()
      tree_bkg.GetEntry(event)
      hist_total_mu_bkg.Fill(tree_bkg.averageIntPerXing)
      hist_total_Nvtx_bkg.Fill(tree_bkg.el_Nvtx)
      if args.c == 'mu':                #  cut on either mu or Nvtx as defined on the command line
         if tree_bkg.el_rhad <= cuts['0-1000000']['0-10'](tree_bkg.averageIntPerXing):
            hist_pass_mu_bkg.Fill(tree_bkg.averageIntPerXing)
            hist_pass_Nvtx_bkg.Fill(tree_bkg.el_Nvtx)
      if args.c == 'Nvtx':
         if tree_bkg.el_rhad <= cuts['0-1000000']['0-10'](tree_bkg.el_Nvtx):
            hist_pass_mu_bkg.Fill(tree_bkg.averageIntPerXing)
            hist_pass_Nvtx_bkg.Fill(tree_bkg.el_Nvtx)


   h1_bkg_Nvtx.Divide(hist_pass_Nvtx_bkg, hist_total_Nvtx_bkg)
   setEffErrors( h1_bkg_Nvtx, hist_total_Nvtx_bkg)
   h1_bkg_mu.Divide(hist_pass_mu_bkg, hist_total_mu_bkg)
   setEffErrors( h1_bkg_mu, hist_total_mu_bkg)

   print "\r\r"
   outfile.Write()

def setEffErrors(th, den):
   for i in range(th.GetNbinsX()):
      eff = th.GetBinContent(i+1)
      if eff < 0: eff = 0
      if eff > 1: eff = 1
      n = den.GetBinContent(i+1)
      if n != 0 and 0 <= eff and eff <=1:
         err = math.sqrt(eff*(1-eff)/n)
         th.SetBinError(i+1, err)
   
def getNvtx():
   nGoodVertices = 0
   VtxMin = 3 
   for i in len(tree.PV_n):
      if tree.PV_trk_n[i] >= Vtxmin:
         nGoodVertices = nGoodVertices + 1
   return nGoodVertices


def makeHisto(Et_bin, eta_bin, eta_index, sig):
   Et_str = Et_bin.split('-') 
   eta_str = eta_bin.split('-')
   h_temp = TH2F('h2_rhad_mu'+str(eta_index)+sig, 'h2_rhad_mu'+str(eta_index), 90, 0, 90, 10000, -1,1)
   Et_cut1 = TCut( Et_str[0] + '<el_Et' )    
   eta_cut1 = TCut( eta_str[0] + '<el_eta' )    
   
   Et_cut2 = TCut(Et_str[1]+'>=el_Et' )    
   eta_cut2 = TCut(eta_str[1]+'>=el_eta' )    
   if args.c == 'mu':
      draw_str = 'rhad_tree.el_rhad:averageIntPerXing'
   if args.c == 'Nvtx':
      draw_str = 'rhad_tree.el_rhad:rhad_tree.el_Nvtx'
   if sig=='sig':
     tree_sig.Draw(draw_str+'>>h2_rhad_mu'+str(eta_index)+sig, Et_cut1 and Et_cut2 and eta_cut1 and eta_cut2, 'goff')
     h_temp.Write()
   if sig=='bkg':
     tree_bkg.Draw(draw_str+'>>h2_rhad_mu'+str(eta_index)+sig, Et_cut1 and Et_cut2 and eta_cut1 and eta_cut2, 'goff')
     h_temp.Write()

   return h_temp


def getCut(histo, target_Eff):
   """Find the value of the cut that preserves the efficiency

      \param histo 1D histogram to cut on
      \param target_Eff the efficiency the function should try to get closest too
      \return The bin that was used to get closest to the target efficiency

   """ 
   for bin in xrange(1, histo.GetNbinsX()):

      current_Eff = getEff(histo, bin) 

   # if the current cut is within the range of efficiency
   # then return the current cut bin
      if abs(current_Eff - target_Eff) < 0.005:
         return bin

   print 'no cut bin found. Current EFF: ', current_Eff, '\n'
   print 'Number of entries ', histo.Integral(1, histo.GetNbinsX())

def getEff(histo, Cut):
   """Get Efficiency of the cut

   Integrates the histo after the cut then divides by the 
   uncut histo integral to get the fraction of electrons
   that pass the cut.

   \param histo the histogram to integrate
   \param Cut the cut to make on the histogram
   \return The Efficiency
   """
   gCUTLOW = False
   if 'reta' in histo.GetName():
      gCUTLOW = True
   maxBin = histo.GetNbinsX()
   total = histo.Integral(2, maxBin-2)
   if total == 0:  # get rid of division by zero
      return 0
   elif gCUTLOW:
      return histo.Integral(Cut, maxBin) / total  
   else:
      return histo.Integral(2, Cut) / total


if __name__=='__main__':

   p = argparse.ArgumentParser()
   p.add_argument('-c',type=str, required=True, help='var to cut with', choices=['mu', 'Nvtx'])
   args = p.parse_args()

   runIt()
   plotSimple()

   infile_sig.Close()
   infile_bkg.Close()
