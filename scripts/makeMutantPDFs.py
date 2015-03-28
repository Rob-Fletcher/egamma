import ROOT

dataPDFs = '~/egamma/PDFs/April_2014/ElectronLikelihoodPdfs.root'
#mcPDFs = '~/egamma/PDFs/April_2014/ElectronLikelihoodPdfs.root'
mcPDFs   = '~/egamma/PDFs/2015/March/Shifted_PDFs_Full_Et/output/out.root'
#dataPDFs   = '~/egamma/PDFs/April_2014/21April2014.LHSignal_Iso_TIBALE_MC.jf17_LikelihoodBackground.PDF.ec0.OFFL.root'
targetPDFs = '~/egamma/PDFs/2015/March/15March2015.ElectonLikelihoodPdfs.LHSignal_Iso_TIBALE_MC.jf17_LikelihoodBackground.PDF.ec0.OFFL.MUTANT.EtBinned.root'
MC_list = [
          'el_rhad',
          'el_reta',
          'el_wstot',
          'el_deltaeta1',
          'el_weta2',
          'el_f1',
          'el_rphi',
          'el_f3',
          'el_deltaEmax2',
          'el_TRTHighTHitsRatio',
          'el_d0Sig',
          'el_trackd0',
          'el_TRTHighTOutliersRatio',
          'el_eratio',
          'el_d0significance',
          'el_trackd0pvunbiased',
          'el_ws3',
          'el_DeltaPoverP',
          'el_deltaphiRescaled',
          ]

def copyObj( source, target, dataFile, MCFile ):
    """Copy an object from one file to a new root file.

    """
    for key in source.GetListOfKeys():
        #print type(source)
        #print source.GetPath()
        #print key.GetName()
        path = source.GetPath().split(':')[1]
        if key.GetName() == 'bkg':
            source = dataFile.Get( path+"/bkg" )
            print "Background key found."
            print source.GetPath()
        elif key.GetName() == 'sig':
            print path
            source = MCFile.Get( path+"/sig" )
            print "Signal key found."
            print source.GetPath()

        print source.GetName()
        print "source.Get(", key.GetName(), ")"
        subObj = source.Get(key.GetName())
        print subObj.GetPath()

        if subObj.Class().InheritsFrom(ROOT.TDirectory.Class()):
            newDir = target.mkdir(subObj.GetName())
            newDir.cd()
            copyObj(subObj, ROOT.gDirectory, dataFile, MCFile)
            target.cd('../')
        elif subObj.Class().InheritsFrom(ROOT.TTree.Class()):
            target.cd()
            T = subObj.CloneTree()
            T.Write()
        else:
           # print "Found histo:", key.GetName()
            target.cd()
            subObj.Write()
           # ROOT.gROOT.ProcessLine('delete '+subObj.GetName())

if __name__=='__main__':
    #do the copy stuff
    print "Making Mutant PDFs..."
    print "Data file:", dataPDFs
    print "MC file:", mcPDFs
    print "target file:", targetPDFs
    dataFile = ROOT.TFile(dataPDFs)
    MCFile = ROOT.TFile(mcPDFs)
    targetFile = ROOT.TFile(targetPDFs, 'RECREATE')

    for key in dataFile.GetListOfKeys():
        print key.GetName()
        if key.GetName() in MC_list:
            print "********Using MC PDFs for", key.GetName()
            source = MCFile.Get(key.GetName())
        else:
            source = dataFile.Get(key.GetName())

        if source.Class().InheritsFrom(ROOT.TDirectory.Class()):
            varDir = targetFile.mkdir(source.GetName())
            varDir.cd()
            copyObj( source, ROOT.gDirectory, dataFile, MCFile)
            varDir.cd()
        else:
            targetFile.cd()
            source.Write()


