### Overlay shifted and unshifted PDFS
import sys
import ROOT
import rootlogon

ROOT.gROOT.SetBatch(ROOT.kTRUE)
vars = [ 'reta'
       # ,'rhad'
       # ,'deltaeta1'
        ,'weta2'
        ,'f1'
       # ,'rphi'
       ,'f3'
       # ,'TRTHighTOutliersRatio'
       # ,'eratio'
       # ,'DeltaPoverP'
       # ,'deltaphiRescaled'  
       # ,'d0significance'
       # ,'trackd0pvunbiased'
        ]                    



outfile_path = '~/egamma/plots/2015/March/'
file_head = 'FullShiftTest'

for name in vars:
    var = 'el_'+name
    print "Overlaying", var
    usfile = ROOT.TFile('~/egamma/PDFs/DC14/ElectronLikelihoodPdfs.root')  #data PDF file
    #shfile = ROOT.TFile('~/egamma/PDFs/July_2014/11July2014.ElectonLikelihoodPdfs.LHSignal_Iso_TIBALE_MC.jf17_LikelihoodBackground.PDF.ec0.OFFL.MUTANT.SIG.ONLY.reta.root') #shifted PDF file
    shfile = ROOT.TFile(sys.argv[1])
    MCfile = ROOT.TFile('~/egamma/PDFs/September_2014/15September2014.ElectonLikelihoodPdfs.LHSignal_Iso_TIBALE_MC.jf17_LikelihoodBackground.PDF.ec0.OFFL.MUTANT.sigOnly.root')  #Unshifted MC PDFs
    #MCfile = ROOT.TFile('~/egamma/PDFs/June_2014/fixed_stretch_reta_only.root')  #Unshifted MC PDFs
    #MCfile = ROOT.TFile('~/testarea/anotherone/egammaCore/macros/PDF_test_dir/output/out.root')  #Unshifted MC PDFs
    #MCfile = ROOT.TFile(sys.argv[1])
    outfile = ROOT.TFile('~/egamma/PDFs/2015/March/'+file_head+'_'+name+'_overlay.root', 'recreate')

    for sample in ['sig','bkg']:
        usdir = usfile.Get(var+'/'+sample)
        outfile.cd('/')
        outfile.mkdir(sample)
        outfile.cd(sample)
        last = len(usdir.GetListOfKeys())
        canvas = ROOT.TCanvas('c1')
        canvas.Print(outfile_path+file_head+'_'+var+'_'+sample+'_dump.pdf[')
        for i,histo in enumerate(usdir.GetListOfKeys(), start=1): 
            if 'KDE' in histo.GetName():
                print histo.GetName() 
                h_un = usdir.Get(histo.GetName())
                #print type(h_un)
                h_sh = shfile.Get(var+'/'+sample+'/'+histo.GetName())
                if not h_sh.Class().InheritsFrom(ROOT.TH1.Class()):
                    continue
                h_mc = MCfile.Get(var+'/'+sample+'/'+histo.GetName())
                if not h_mc.Class().InheritsFrom(ROOT.TH1.Class()):
                    continue

                h_un.SetFillStyle(3004)
                h_un.SetFillColor(ROOT.kBlack)
                h_sh.SetLineColor(ROOT.kRed)
                h_sh.SetTitle('Shifted MC')
                h_mc.SetLineColor(ROOT.kBlue)
                h_mc.SetTitle('MC Unshifted')

                h_un.DrawNormalized()
                h_un.SetTitle('Data')
                h_sh.DrawNormalized('same')
                h_mc.DrawNormalized('same')
                canvas.BuildLegend()
                canvas.SetName(histo.GetName())
                canvas.Write()
                canvas.Print(outfile_path+file_head+'_'+var+'_'+sample+'_dump.pdf')

        print "Close PDF print"
        #canvas.Update()
        canvas.Print(outfile_path+file_head+'_'+var+'_'+sample+'_dump.pdf]')


    usfile.Close()
    shfile.Close()
    MCfile.Close()
    outfile.Close()





