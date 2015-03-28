from ROOT import *
gROOT.SetBatch(kTRUE)
gStyle.SetOptStat(0)

sigfile = TFile('~/egamma/rootfiles/2014_January/LHSignal_plots.root')
bkgfile = TFile('~/egamma/rootfiles/2014_January/Bkg_plots.root')

outfile = TFile('rhad_f3_mu_15-25.root', 'recreate')

h2_rhad_sig = sigfile.Get('h2_mu_Rhad') 
h2_rhad_bkg = bkgfile.Get('h2_mu_Rhad') 

h2_f3_sig = sigfile.Get('h2_mu_f3')
h2_f3_bkg = bkgfile.Get('h2_mu_f3')

rhad_low_mu_sig = h2_rhad_sig.ProjectionY('rhad_low_mu_sig', 1, 15)
rhad_low_mu_sig.Rebin(4)
rhad_low_mu_sig.SetTitle('Rhad #mu < 15')
rhad_low_mu_sig.GetXaxis().SetTitle('Rhad')
rhad_high_mu_sig = h2_rhad_sig.ProjectionY('rhad_high_mu_sig', 25, 45)
rhad_high_mu_sig.Rebin(4)
rhad_high_mu_sig.SetTitle('Rhad #mu > 25')

rhad_low_mu_bkg = h2_rhad_bkg.ProjectionY('rhad_low_mu_bkg', 1, 15)
rhad_high_mu_bkg = h2_rhad_bkg.ProjectionY('rhad_high_mu_bkg', 25, 45)
rhad_low_mu_bkg.Rebin(4) 
rhad_high_mu_bkg.Rebin(4)


f3_low_mu_sig = h2_f3_sig.ProjectionY('f3_low_mu_sig', 1, 15)
f3_high_mu_sig = h2_f3_sig.ProjectionY('f3_high_mu_sig', 25, 45)
f3_low_mu_sig.Rebin(4) 
f3_low_mu_sig.SetTitle('f3 #mu < 15')
f3_low_mu_sig.GetXaxis().SetTitle('f3')
f3_high_mu_sig.Rebin(4)
f3_high_mu_sig.SetTitle('f3 #mu > 25')
f3_high_mu_sig.GetXaxis().SetTitle('f3')


f3_low_mu_bkg = h2_f3_bkg.ProjectionY('f3_low_mu_bkg', 1, 15)
f3_high_mu_bkg = h2_f3_bkg.ProjectionY('f3_high_mu_bkg', 25, 45)
f3_low_mu_bkg.Rebin(4) 
f3_high_mu_bkg.Rebin(4)


c_rhad_low_mu = TCanvas('Rhad_low_mu', 'Rhad Low Mu')
c_rhad_high_mu = TCanvas('Rhad_high_mu', 'Rhad High Mu')
c_f3_low_mu = TCanvas('f3_low_mu', 'f3 Low Mu')
c_f3_high_mu = TCanvas('f3_high_mu', 'f3 high Mu')

#####Draw rhad low mu canvas
rhad_low_mu_sig.SetFillColor(kBlue)
rhad_low_mu_bkg.SetFillColor(kRed)
rhad_low_mu_bkg.SetFillStyle(3004)
low_cut = TLine(0.01,0,0.01,0.15)
low_cut.SetLineWidth(2)
high_cut = TLine(0.02425, 0, 0.02425, 0.15)
high_cut.SetLineWidth(2)
high_cut.SetLineColor(kRed)

c_rhad_low_mu.cd()
rhad_low_mu_sig.SetAxisRange(-0.03, 0.05)
rhad_low_mu_sig.DrawNormalized()
rhad_low_mu_bkg.DrawNormalized('same')
low_cut.Draw('same')
high_cut.Draw('same')

c_rhad_low_mu.Write()

#####Draw rhad high mu canvas
rhad_high_mu_sig.SetFillColor(kBlue)
rhad_high_mu_bkg.SetFillColor(kRed)
rhad_high_mu_bkg.SetFillStyle(3004)
low_cut = TLine(0.01,0,0.01,0.13)
low_cut.SetLineWidth(2)
high_cut = TLine(0.02425, 0, 0.02425, 0.13)
high_cut.SetLineWidth(2)
high_cut.SetLineColor(kRed)

c_rhad_high_mu.cd()
rhad_high_mu_sig.SetAxisRange(-0.03, 0.05)
rhad_high_mu_sig.DrawNormalized()
rhad_high_mu_bkg.DrawNormalized('same')
low_cut.Draw('same')
high_cut.Draw('same')

c_rhad_high_mu.Write()

#####Draw f3 low mu canvas
f3_low_mu_sig.SetFillColor(kBlue)
f3_low_mu_bkg.SetFillColor(kRed)
f3_low_mu_bkg.SetFillStyle(3004)
high_cut = TLine(0.0215, 0, 0.0215, 0.08)
high_cut.SetLineWidth(2)
high_cut.SetLineColor(kRed)

c_f3_low_mu.cd()
f3_low_mu_sig.SetAxisRange(0.001, 0.1)
f3_low_mu_sig.DrawNormalized()
f3_low_mu_bkg.DrawNormalized('same')
high_cut.Draw('same')

c_f3_low_mu.Write()

#####Draw rhad high mu canvas
f3_high_mu_sig.SetFillColor(kBlue)
f3_high_mu_bkg.SetFillColor(kRed)
f3_high_mu_bkg.SetFillStyle(3004)
high_cut = TLine(0.0215, 0, 0.0215, 0.08)
high_cut.SetLineWidth(2)
high_cut.SetLineColor(kRed)

c_f3_high_mu.cd()
f3_high_mu_sig.SetAxisRange(0.001, 0.1)
f3_high_mu_sig.DrawNormalized()
f3_high_mu_bkg.DrawNormalized('same')
high_cut.Draw('same')

c_f3_high_mu.Write()
