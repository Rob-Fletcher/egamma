from ROOT import TFile, TTree, TH2, TH1, TGraph, gROOT
import rootlogon
from array import array
import datetime, time

gROOT.SetBatch()
histo_names = ['h2_mu_Rhad', 'h2_mu_el_reta', 'h2_Nvtx_Rhad', 'h2_Nvtx_el_reta']
target_Eff = 0.95

def runIt():
   histo_list = [ correctEff(signal.Get(histo), histo) for histo in histo_names ]

   a_xAxis = array('f', range(len(histo_list[0])))

   mu_Rhad = TGraph( len(a_xAxis), a_xAxis, histo_list[0])
   mu_Rhad.SetDrawOption('P')
   mu_Rhad.SetTitle('mu vs. Rhad cuts')
   mu_Rhad.GetXaxis().SetTitle('mu')
   mu_Rhad.GetYaxis().SetTitle('Cut on Rhad')
   mu_Rhad.SetName('mu_Rhad_cuts')

   mu_reta = TGraph( len(a_xAxis), a_xAxis, histo_list[1])
   mu_reta.SetDrawOption('P')
   mu_reta.SetTitle('mu vs. reta cuts')
   mu_reta.GetXaxis().SetTitle('mu')
   mu_reta.GetYaxis().SetTitle('Cut on reta')
   mu_reta.SetName('mu_reta_cuts')


   Nvtx_Rhad = TGraph( len(a_xAxis), a_xAxis, histo_list[2])
   Nvtx_Rhad.SetDrawOption('P')
   Nvtx_Rhad.SetTitle('Nvtx vs. Rhad cuts')
   Nvtx_Rhad.GetXaxis().SetTitle('Nvtx')
   Nvtx_Rhad.GetYaxis().SetTitle('Cut on Rhad')
   Nvtx_Rhad.SetName('Nvtx_Rhad_cuts')

   Nvtx_reta = TGraph( len(a_xAxis), a_xAxis, histo_list[3])
   Nvtx_reta.SetDrawOption('P')
   Nvtx_reta.SetTitle('Nvtx vs. reta cuts')
   Nvtx_reta.GetXaxis().SetTitle('Nvtx')
   Nvtx_reta.GetYaxis().SetTitle('Cut on reta')
   Nvtx_reta.SetName('Nvtx_reta_cuts')

   gFile = outfile
   mu_Rhad.Write()
   mu_reta.Write()
   Nvtx_Rhad.Write()
   Nvtx_reta.Write()


   graph1 = makeCuts( background.Get(histo_names[0]), histo_list[0] )
   graph1.SetTitle('mu vs. Background rejection using calculated Rhad signal cuts')
   graph1.GetXaxis().SetTitle('mu')
   graph1.GetYaxis().SetTitle('Rhad Rejection')
   graph1.SetName('mu_Rhad_rejection')

   graph2 = makeCuts( background.Get(histo_names[2]), histo_list[2] )
   graph2.SetTitle('Nvtx vs. Background rejection using calculated Rhad signal cuts')
   graph2.GetXaxis().SetTitle('Nvtx')
   graph2.GetYaxis().SetTitle('Rhad Rejection')
   graph2.SetName('Nvtx_Rhad_rejection')

   gFile = outfile
   #graph1.Draw('AP')
   #graph2.Draw('P')
   graph1.Write()
   graph2.Write()

def makeCuts( histo_2d, cuts):
  
   eff = []
   bins = []
   for bin in xrange(histo_2d.GetNbinsX() ):
      proj = histo_2d.ProjectionY(histo_2d.GetName(), bin, bin)
      cut_bin = proj.FindBin( cuts[bin] )
      eff.append(1-getEff( proj, cut_bin, False ) )
      bins.append(bin)

   a_eff = array('f', eff)
   a_xaxis = array('f', bins)

   return TGraph( len(a_xaxis), a_xaxis, a_eff) 


def correctEff(histo_2, name):

   cuts = []
   print 'correcting efficiency\n'
   
   if 'reta' in name: 
      gCUTLOW = True
   else:
      gCUTLOW = False

   for bin in xrange( histo_2.GetNbinsX() ):
      proj = histo_2.ProjectionY(name+'_temp', bin, bin)
   
      if proj.Integral( 1, proj.GetNbinsX() - 1 ) < 100: 
         cuts.append( 0 ) 
         continue

      cut_bin = getCut( proj, target_Eff, gCUTLOW)

      cut_val = proj.GetBinCenter( cut_bin )

      cuts.append( cut_val )
      proj.Delete()

   return array('f', cuts)


def getCut(histo, target_Eff, gCUTLOW):
   """Find the value of the cut that preserves the efficiency

      \param histo 1D histogram to cut on
      \param target_Eff the efficiency the function should try to get closest too
      \return The bin that was used to get closest to the target efficiency

   """ 
   for bin in xrange(1, histo.GetNbinsX()):

      current_Eff = getEff(histo, bin, gCUTLOW) 

      # if the current cut is within the range of efficiency
      # then return the current cut bin
      if abs(current_Eff - target_Eff) < 0.005:
         return bin

def getEff(histo, Cut, gCUTLOW):
   """Get Efficiency of the cut

   Integrates the histo after the cut then divides by the 
   uncut histo integral to get the fraction of electrons
   that pass the cut.

   \param histo the histogram to integrate
   \param Cut the cut bin to make on the histogram
   \return The Efficiency
   """
   maxBin = histo.GetNbinsX()
   total = histo.Integral(1, maxBin)
   if total == 0:  # get rid of division by zero
      return 0
   elif gCUTLOW:
      return histo.Integral(Cut, maxBin) / total  
   else:
      return histo.Integral(1, Cut) / total

if __name__=='__main__':

   signal = TFile('~/egamma/rootfiles/LHSignal_plots_finer_bins.root')
   background = TFile('~/egamma/rootfiles/Bkg_plots_finer_bins.root')
   outfile = TFile(datetime.date.today().strftime('cuts_%B_%d.root'), 'recreate')
   gFile = outfile
   runIt()





