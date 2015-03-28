from ROOT import *

l_files = ['~/egamma/rootfiles/2013_June/rhad_tree_signal_mu40.root','~/egamma/rootfiles/2013_June/rhad_tree_signal_mu60.root','~/egamma/rootfiles/2013_June/rhad_tree_signal_mu80.root','~/egamma/rootfiles/2013_June/rhad_tree_signal_mu80_bs50.root']

full_MC_files = ['~/egamma/Data/June19_2013_LHSignal_mu40_bs25_Iso_TIBALE_MC.root','~/egamma/Data/June19_2013_LHSignal_mu60_bs25_Iso_TIBALE_MC.root',
                  '~/egamma/Data/June19_2013_LHSignal_mu80_bs25_Iso_TIBALE_MC.root','~/egamma/Data/June19_2013_LHSignal_mu80_bs50_Iso_TIBALE_MC.root']



files = [ TFile( name ) for name in full_MC_files]

def getHistos( name, i ):
   print 'opening file: ', name
   hist = TH1F('histo'+str(i), 'histo'+str(i), 500, -0.2, 0.2)
   t = files[i].Get('photon')
#   t.Draw('el_rhad>>histo'+str(i),'1<2', 'goff')
   t.Draw('el_reta>>histo'+str(i),'1<2', 'goff')
   return hist


histos = [ getHistos(name, i) for i, name  in enumerate(full_MC_files)]

histos[0].SetLineColor(kRed)
histos[1].SetLineColor(kBlue)
histos[2].SetLineColor(kGreen)
histos[3].SetLineColor(kBlack)

histos[0].SetTitle('mu=40')
histos[1].SetTitle('mu=60')
histos[2].SetTitle('mu=80')
histos[3].SetTitle('mu=80 bs=50')

histos[0].GetXaxis().SetTitle('Reta')
histos[1].GetXaxis().SetTitle('Reta')
histos[2].GetXaxis().SetTitle('Reta')
histos[3].GetXaxis().SetTitle('Reta')

histos[3].DrawNormalized()
for n in range(len(histos)-1):
   histos[n].DrawNormalized('same')
raw_input("press any key to Exit")
