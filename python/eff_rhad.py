import ROOT



def eff_rhad():
   infile = ROOT.TFile('LHSignal_plots.root')
   outfile = ROOT.TFile('rhad_effic.root', 'recreate')

   cut = 0.014 
   
   h2_mu_Rhad_eff = ROOT.TH2F('h2_mu_Rhad_eff', 'Mu vs. Rhad Eff', 50, 0, 50, 200, 0, 1)
   h2_mu_Rhad = infile.Get('h2_mu_Rhad')
   nBins = h2_mu_Rhad.GetNbinsX()

   for bin in range(nBins):
      h1_mu_temp = h2_mu_Rhad.ProjectionY( "temp", bin, bin)
      h2_mu_Rhad_eff.Fill(bin, getEff( h1_mu_temp, cut))


   gFile = outfile
   h2_mu_Rhad_eff.Write()
   infile.Close()
   outfile.Close()     
    

def getEff( h_Rhad, Cut ):
   maxBin = h_Rhad.GetNbinsX()
   cutBin = h_Rhad.GetXaxis().FindBin(Cut)
   total = h_Rhad.Integral(1, maxBin)
   if total == 0:
      return 0
   else:    
      return h_Rhad.Integral(1, cutBin) / total  

if __name__ == '__main__':
    eff_rhad()
