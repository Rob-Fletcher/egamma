from ROOT import *

gROOT.SetBatch(kTRUE)
gStyle.SetLegendBorderSize(0)
gStyle.SetLegendFillColor(0)

DataFile = TFile('/home/robflet/egamma/Likelihoods/2015/March/FullShiftMCPDFs-DataInput/output/out.root')
MCFile   = TFile('/home/robflet/egamma/Likelihoods/2015/March/FullShiftMCPDFs-MCInput/output/out.root')

outfile = TFile('/home/robflet/egamma/plots/2015/March/SFPlots_March_2015_FullShiftMCPDFs_UnshiftedInput.root','recreate')


#histo_list = ['TightppNoTRT','TightppNoF3','TightppNoRhad','TightppNoReta','TightppNoWeta2','TightppNoF1','TightppNoWstot','TightppNoEratio','TightppNoDeltaEta','TightppNonPixelHits','TightppNoEOverP','TightppNoDeltaPhi','TightppNoConv','TightppNoRTW']
histo_list = ['_bkgd_et_Efficiency','_bkgd_eta_Efficiency'
             ,'_data_et_Efficiency','_data_eta_Efficiency']

dir_data = DataFile.Get('PyLikelihoodMakerAlg/FullShiftMCPDFs-DataInput')
dir_MC   = MCFile.Get('PyLikelihoodMakerAlg/FullShiftMCPDFs-MCInput')

dataNamePrefix = 'FullShiftMCPDFs-DataInput'
mcNamePrefix   = 'FullShiftMCPDFs-MCInput'

dir_data.pwd()
#tpp_SF   = infile.Get('TightppSF')
#tpp_SF.SetTitle('')

for name in histo_list:
    canvas = TCanvas('c'+name, 'c'+name)
    upad = TPad('upad'+name, 'upad'+name, .00, .35, 1, 1) 
    lpad = TPad('dpad'+name, 'dpad'+name, .00, .00, 1, .35)
    upad.Draw()
    upad.SetTitle(name)
    lpad.Draw()
    upad.cd()
    print dataNamePrefix + name
    histo_data = dir_data.Get(dataNamePrefix + name) 
    histo_data.SetTitle(dataNamePrefix + name +' Data')
    histo_data.Draw()
    gStyle.SetOptTitle(0)
    histo_data.GetYaxis().SetTitle('Efficiency')
    histo_data.GetYaxis().CenterTitle()
    histo_data.GetYaxis().SetTitleOffset(0.6)
    histo_data.GetYaxis().SetTitleSize(0.06)
    histo_data.GetXaxis().SetLabelSize(0)
    #histo_data.SetMinimum(0.51)
    #histo_data.SetMaximum(0.93)

    histo_MC = dir_MC.Get(mcNamePrefix + name)
    histo_MC.SetTitle('MC')
    histo_MC.Draw('same')
    histo_MC.SetMarkerColor(kRed)
    histo_MC.SetLineColor(kRed)

    #histo_data = infile.Get(name+'_signal')
    #histo_data.SetTitle(name+' Data')
    #histo_data.Draw('same')
    #histo_data.SetMarkerColor(kBlack)
    #histo_data.SetLineColor(kBlack)
    #histo_data.SetMarkerStyle(kOpenTriangleUp)
    #histo_MC = infile.Get(name+'_MC')
    #histo_MC.SetTitle(name+' MC')
    #histo_MC.Draw('same')
    #histo_MC.SetMarkerColor(kRed)
    #histo_MC.SetLineColor(kRed)
    #histo_MC.SetMarkerStyle(kOpenTriangleUp)
    histo_data.SetTitle('Data')
    upad.BuildLegend(0.2,0.2,0.4,0.4)
    histo_data.SetTitle(dataNamePrefix + name)

    histo_SF = histo_data.Clone()
    histo_SF.Divide(histo_MC)
    lpad.cd()
    histo_SF.SetTitle('')
    histo_SF.Draw()
    if '_et_' in name:
        histo_SF.GetXaxis().SetTitle('Et')
    if '_eta_' in name:
        histo_SF.GetXaxis().SetTitle('#eta')

    histo_SF.GetXaxis().SetTitleSize(0.12)
    histo_SF.GetXaxis().SetTitleOffset(0.65)
    histo_SF.GetXaxis().SetLabelSize(0.1)
    histo_SF.GetYaxis().SetTitle('Data/MC')
    histo_SF.GetYaxis().CenterTitle()
    histo_SF.GetYaxis().SetTitleSize(0.1)
    histo_SF.GetYaxis().SetTitleOffset(0.33)
    histo_SF.GetYaxis().SetLabelSize(0.08)
    #histo_SF.SetMinimum(0.95)
    #histo_SF.SetMaximum(1.0)
    #histo_SF = infile.Get(name+'SF')
    #histo_SF.SetTitle(name)
    #histo_SF.Draw('same')
    #histo_SF.SetMarkerColor(46)
    #histo_SF.SetLineColor(46)
    #lpad.BuildLegend(0.2,0.58, 0.55,0.85)
    if '_et_' in name:
        line = TLine(7,1,50,1)
    if '_eta_' in name:
        line = TLine(0,1,2.46,1)
    line.Draw('same')

    canvas.Write()




    
