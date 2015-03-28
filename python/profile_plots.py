import ROOT
import array
from math import sqrt

def makePlots():
    infile = ROOT.TFile('~/egamma/rootfiles/LHSignal_plots_finer_bins.root')
    outfile = ROOT.TFile('sig_eff.root', 'recreate')

    Rhad_cut = 0.018
    reta_cut = 0.92

    # Get some histograms from the root file    
    h2_mu_Rhad = infile.Get('h2_mu_Rhad')
    h2_Nvtx_Rhad = infile.Get('h2_Nvtx_Rhad')
    h2_mu_reta = infile.Get('h2_mu_el_reta')
    h2_Nvtx_reta = infile.Get('h2_Nvtx_el_reta')

    #number of bins to loop over
    nBins = h2_mu_Rhad.GetNbinsX()

    #make some new histograms that we want to see
    # pileup vs. Rhad RMS
    h2_mu_Rhad_RMS   = ROOT.TH2F('h2_mu_Rhad_RMS', 'mu vs. Rhad RMS', 50, 0, 50, 500, 0, 0.05)
    h2_Nvtx_Rhad_RMS = ROOT.TH2F('h2_Nvtx_Rhad_Nvtx', 'Nvtx vs. Rhad RMS', 50, 0, 50, 500, 0, 0.02)
   
    #pileup vs. efficiencies calculated by getEff
    h2_mu_reta_eff   = ROOT.TH2F('h2_mu_reta_eff', 'mu vs. reta Eff', 50, 0, 50, 2000, 0, 1)
    h2_Nvtx_reta_eff = ROOT.TH2F('h2_Nvtx_reta_eff', 'Nvtx vs. reta Eff', 50, 0, 50, 2000, 0, 1)

    h2_mu_Rhad_eff   = ROOT.TH2F('h2_mu_Rhad_eff', 'Mu vs. Rhad Eff', 50, 0, 50, 2000, 0, 1)
    h2_Nvtx_Rhad_eff = ROOT.TH2F('h2_Nvtx_Rhad_eff', 'Nvtx vs. Rhad Eff', 50, 0, 50, 2000, 0, 1)

    h1_mu_Rhad_eff = ROOT.TH1F('h1_mu_Rhad_eff', 'Mu vs. Rhad Eff', 50, 0, 50)
    h1_mu_reta_eff = ROOT.TH1F('h1_mu_reta_eff', 'Mu vs. reta Eff', 50, 0, 50)

    h1_Nvtx_Rhad_eff = ROOT.TH1F('h1_Nvtx_Rhad_eff', 'Nvtx vs. Rhad Eff', 50, 0, 50)
    h1_Nvtx_reta_eff = ROOT.TH1F('h1_Nvtx_reta_eff', 'Nvtx vs. reta Eff', 50, 0, 50)


    mu = array.array('d',[])
    RMS_mu = array.array('d',[])
    RMS_Nvtx = array.array('d',[])
    Nvtx = array.array('d',[])

    for bin in range(nBins):
        h1_Rhad_mu_temp = h2_mu_Rhad.ProjectionY( "temp_Rhad", bin, bin)
        h1_Rhad_Nvtx_temp = h2_Nvtx_Rhad.ProjectionY( "temp_Nvtx", bin, bin)

        h1_reta_mu_temp = h2_mu_reta.ProjectionY( "temp_mu_reta", bin, bin)
        h1_reta_Nvtx_temp = h2_Nvtx_reta.ProjectionY( "temp_Nvtx_reta", bin, bin)

        h2_mu_Rhad_RMS.Fill( bin, h1_Rhad_mu_temp.GetRMS())
        h2_Nvtx_Rhad_RMS.Fill( bin, h1_Rhad_Nvtx_temp.GetRMS() )     

        #print bin, getEff( h1_Rhad_mu_temp, Rhad_cut, False )
        h2_mu_Rhad_eff.Fill( bin, getEff( h1_Rhad_mu_temp, Rhad_cut, False ))
        h2_Nvtx_Rhad_eff.Fill( bin, getEff( h1_Rhad_Nvtx_temp, Rhad_cut, False) )

        h2_mu_reta_eff.Fill( bin, getEff( h1_reta_mu_temp, reta_cut, True ))
        h2_Nvtx_reta_eff.Fill( bin, getEff( h1_reta_Nvtx_temp, reta_cut, True) )

        h1_mu_Rhad_eff.SetBinContent( bin, getEff( h1_Rhad_mu_temp, Rhad_cut, False ))
        if h1_Rhad_mu_temp.GetEntries() != 0:
           h1_mu_Rhad_eff.SetBinError( bin, 1./sqrt( h1_Rhad_mu_temp.GetEntries() ))
        
        h1_mu_reta_eff.SetBinContent( bin, getEff( h1_reta_mu_temp, reta_cut, True ))
        if h1_reta_mu_temp.GetEntries() != 0:
           h1_mu_reta_eff.SetBinError( bin, 1./sqrt( h1_reta_mu_temp.GetEntries() ))
         
        h1_Nvtx_Rhad_eff.SetBinContent( bin, getEff( h1_Rhad_Nvtx_temp, Rhad_cut, False ))
        if h1_Rhad_Nvtx_temp.GetEntries() != 0:
           h1_Nvtx_Rhad_eff.SetBinError( bin, 1./sqrt( h1_Rhad_Nvtx_temp.GetEntries() ))
        
        h1_Nvtx_reta_eff.SetBinContent( bin, getEff( h1_reta_Nvtx_temp, reta_cut, True ))
        if h1_reta_Nvtx_temp.GetEntries() != 0:
           h1_Nvtx_reta_eff.SetBinError( bin, 1./sqrt( h1_reta_Nvtx_temp.GetEntries() ))

        mu.append(bin)
        RMS_mu.append( h1_Rhad_mu_temp.GetRMS())
        RMS_Nvtx.append( h1_Rhad_Nvtx_temp.GetRMS())
        Nvtx.append(bin)
  #  gr_mu_Rhad_RMS   = ROOT.TGraph(nBins, mu, RMS_mu)
  #  gr_Nvtx_Rhad_RMS = ROOT.TGraph(nBins, Nvtx, RMS_Nvtx)
  #  gr_mu_Rhad_RMS.SetTitle("Mu vs. Rhad RMS")
  #  gr_Nvtx_Rhad_RMS.SetTitle("Nvtx vs. Rhad RMS")

    h1_Rhad_mu_temp.Delete()
    h1_Rhad_Nvtx_temp.Delete()
    h1_reta_mu_temp.Delete()
    h1_reta_Nvtx_temp.Delete()
    outfile.Write()


    
def getEff( h_Rhad, Cut, cutLow ):
   maxBin = h_Rhad.GetNbinsX()
   cutBin = h_Rhad.GetXaxis().FindBin(Cut)
   total = h_Rhad.Integral(1, maxBin)
   if total == 0:
      return 0
   elif cutLow:
      return h_Rhad.Integral(cutBin, maxBin) / total  
   else:
      return h_Rhad.Integral(1, cutBin) / total


if __name__=='__main__':
    makePlots()
 
