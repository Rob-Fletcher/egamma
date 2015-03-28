import ROOT

dataPDFs = '~/egamma/PDFs/April_2014/ElectronLikelihoodPdfs.root'
#mcPDFs = '~/egamma/PDFs/April_2014/ElectronLikelihoodPdfs.root'
#mcPDFs   = '~/egamma/PDFs/2015/March/Shifted_PDFs_Full_Et/output/out.root'
mcPDFs   = '~/egamma/PDFs/April_2014/21April2014.LHSignal_Iso_TIBALE_MC.jf17_LikelihoodBackground.PDF.ec0.OFFL.SHIFT.root'
targetPDFs = '~/egamma/PDFs/2015/March/15March2015.ElectonLikelihoodPdfs.LHSignal_Iso_TIBALE_MC.jf17_LikelihoodBackground.PDF.ec0.OFFL.MUTANT.root'

MC_list = [
          'el_rhad',
          'el_reta',
          'el_wstot',
          'el_deltaeta1',
          'el_weta2',
          'el_f1',
          'el_rphi',
          #'el_f3',
          #'el_deltaEmax2',
          #'el_TRTHighTHitsRatio',
          'el_d0significance',
          #'el_trackd0',
          'el_TRTHighTOutliersRatio',
          'el_eratio',
          'el_d0significance',
          'el_trackd0pvunbiased',
          'el_ws3',
          'el_DeltaPoverP',
          'el_deltaphiRescaled',
          ]

stype = ['sig']  # type to replace with MC

if __name__=="__main__":
    print "Making Mutant PDFs..."
    print "Data file:", dataPDFs
    print "MC file:", mcPDFs
    print "Target file:", targetPDFs
    dataFile = ROOT.TFile(dataPDFs)
    MCFile = ROOT.TFile(mcPDFs)
    targetFile = ROOT.TFile(targetPDFs, 'RECREATE')

    for key in dataFile.GetListOfKeys():
        print "Getting", key.GetName()
        targetFile.cd()
        target_var_dir = targetFile.mkdir(key.GetName())
        target_var_dir.cd()
        data_var_dir = dataFile.Get(key.GetName())
        mc_var_dir   = MCFile.Get(key.GetName())

        for sample in data_var_dir.GetListOfKeys():
            source = data_var_dir.Get(sample.GetName())
            target_sample_dir = target_var_dir.mkdir(sample.GetName())
            target_sample_dir.cd()
            if key.GetName() in MC_list:
                if sample.GetName() in stype:
                    source = mc_var_dir.Get(sample.GetName())

            for histo in source.GetListOfKeys():
                T = source.Get(histo.GetName())
                T.Write()

            ROOT.gDirectory.cd('../')
        ROOT.gDirectory.cd('../')


            






      


