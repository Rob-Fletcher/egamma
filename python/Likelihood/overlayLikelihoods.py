
import ROOT

ROOT.gROOT.SetBatch(True)
data_file    = ROOT.TFile('/home/robflet/egamma/rootfiles/April_2014/2014April22.LHSignal_Iso_TIBALE.LHBkg_z100.LH.ec0.OFFL.root')
MC_file      = ROOT.TFile('/home/robflet/egamma/rootfiles/April_2014/2014April22.LHSignal_Iso_TIBALE.LHBkg_z100.LH.ec0.OFFL.MCPDFs.root')
shifted_file = ROOT.TFile('/home/robflet/egamma/rootfiles/April_2014/2014April22.LHSignal_Iso_TIBALE.LHBkg_z100.LH.ec0.OFFL.MCPDFs.SHIFT.root')
#shifted_file = ROOT.TFile('/home/robflet/egamma/rootfiles/April_2014/2014April24.LHSignal_Iso_TIBALE.LHBkg_z100.LH.ec0.OFFL.MCPDFs.SHIFTreta.root')

data_dir = data_file.Get('PyLikelihoodMakerAlg/Tight-Likelihood')
MC_dir   = MC_file.Get('PyLikelihoodMakerAlg/Tight-Likelihood')
shifted_dir = shifted_file.Get('PyLikelihoodMakerAlg/Tight-Likelihood')
#data_dir = data_file.Get('PyLikelihoodMakerAlg/Latest-Tightpp')
#MC_dir   = MC_file.Get('PyLikelihoodMakerAlg/Latest-Tightpp')
#shifted_dir = shifted_file.Get('PyLikelihoodMakerAlg/Latest-Tightpp')

out_file = ROOT.TFile('LH_compare_out.root', 'RECREATE')

def recursiveGetHisto(object):
    if type(object) == ROOT.TDirectory:
        pass


def overlayHistos():
    for item in data_dir.GetListOfKeys():
        histo = data_dir.Get(item.GetName())
        #print type(histo), histo.GetName()
        if type(histo) == ROOT.TH1F:
            print 'getting histos', item.GetName()
            out_histo_data = histo.Clone()
            out_histo_MC = MC_dir.Get(item.GetName())
            out_histo_shifted = shifted_dir.Get(item.GetName())

            cvs = ROOT.TCanvas(item.GetName())
            cvs.cd()

            print 'drawing histos'
            out_histo_data.Draw()
            out_histo_MC.Draw('same')
            out_histo_shifted.Draw('same')

            out_histo_data.SetLineColor(ROOT.kBlack)
            out_histo_data.SetTitle('Data')
            out_histo_MC.SetLineColor(ROOT.kBlue)
            out_histo_MC.SetTitle('MC')
            out_histo_shifted.SetLineColor(ROOT.kRed)
            out_histo_shifted.SetTitle('Shifted MC')
            print 'Writing histos'
            cvs.Write()
            
            #print type(histo), histo.GetName()
        
if __name__=='__main__':
    overlayHistos()
    

