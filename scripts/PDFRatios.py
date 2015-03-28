### Overlay shifted and unshifted PDFS
import ROOT
import re

ROOT.gROOT.SetBatch(ROOT.kTRUE)
vars = [ 'reta'
        ,'rhad'
        ,'deltaeta1'
        ,'weta2'
        ,'f1'
        ,'rphi'
        ,'f3'
        ,'TRTHighTOutliersRatio'
        ,'eratio'
        ,'DeltaPoverP'
        ,'deltaphiRescaled'  
        ,'d0significance'
        ,'trackd0pvunbiased'
        ]                    



outfile_path = '~/egamma/Likelihoods/ratios/'
file_head = 'PDF_Ratio'

for name in vars:
    var = 'el_'+name
    print "Overlaying", var
    datafile = ROOT.TFile('~/egamma/PDFs/ElectronLikelihoodPdfs.root')  #data PDF file
    shfile = ROOT.TFile('~/egamma/PDFs/April_2014/21April2014.LHSignal_Iso_TIBALE_MC.jf17_LikelihoodBackground.PDF.ec0.OFFL.SHIFT.root') #shifted PDF file
    MCfile = ROOT.TFile('~/egamma/PDFs/April_2014/21April2014.LHSignal_Iso_TIBALE_MC.jf17_LikelihoodBackground.PDF.ec0.OFFL.root')  #Unshifted MC PDFs
    outfile = ROOT.TFile('~/egamma/Likelihoods/ratios/'+file_head+'_'+name+'_overlay.root', 'recreate')

    for sample in ['sig','bkg']:
        datadir = datafile.Get(var+'/'+sample)
        outfile.cd('/')
        outfile.mkdir(sample)
        outfile.cd(sample)
        last = len(datadir.GetListOfKeys())
        canvas = ROOT.TCanvas('c1')
        #canvas.Print(outfile_path+file_head+'_'+var+'_'+sample+'_dump.pdf[')
        for i,histo in enumerate(datadir.GetListOfKeys(), start=1): 
            if 'KDE' in histo.GetName():
                print histo.GetName() 
                h_un = datadir.Get(histo.GetName())
                #print type(h_un)
                #sh_name = re.sub('hist_from_KDE_', '', histo.GetName())
                #print sh_name
                h_sh = shfile.Get(var+'/'+sample+'/'+histo.GetName())
                if not h_sh.Class().InheritsFrom(ROOT.TH1.Class()):
                    continue
                h_mc = MCfile.Get(var+'/'+sample+'/'+histo.GetName())

                div = h_un.Clone()
                div.Divide(h_sh)

                h_un.SetFillStyle(3004)
                h_un.SetFillColor(ROOT.kBlack)
                

                #h_sh.SetLineColor(ROOT.kRed)
                #h_sh.SetTitle('Pass Data, Fail Shifted MC')
                div.SetLineColor(ROOT.kRed)
                div.SetTitle('Data PDF / Shifted PDF')

                #h_sh.DrawNormalized('same')
                div.Draw()
                line = ROOT.TLine(canvas.GetUxmin(), 1, canvas.GetUxmax(), 1)
                line.Draw('same')
                h_un.DrawNormalized("same", div.Integral()/2)
                leg = ROOT.TLegend(0.5,0.67,0.88,0.88,'',"NDC")
                leg.AddEntry(h_un, 'Data PDF')
                leg.AddEntry(div, 'Data PDF / Shifted PDF')
                #leg.AddEntry(h_sh, 'Pass Data, Fail Shifted MC')
                leg.Draw()
                leg.SetFillColor(0)
                leg.SetBorderSize(0)
                #leg = canvas.BuildLegend()
                #canvas.SetName(histo.GetName())
                canvas.Write()
               # canvas.Print(outfile_path+file_head+'_'+var+'_'+sample+'_dump.pdf')

        print "Close PDF print"
        #canvas.Update()
        #canvas.Print(outfile_path+file_head+'_'+var+'_'+sample+'_dump.pdf]')


    datafile.Close()
    shfile.Close()
    MCfile.Close()
    outfile.Close()




#loop throuh the directories and get PDFs








