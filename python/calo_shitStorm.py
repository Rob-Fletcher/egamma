from ROOT import *
import PyPlotHelper

infile = TFile('~/egamma/rootfiles/2013_July/NTUP_PHOTON.root')
tree = infile.Get('photon')
outfile = TFile('calo_shitStorm_output.root', 'recreate')
pph = PyPlotHelper.PyPlotHelper()
detectors = [
             'lar_em', #EM calorimeter
             #'lar_hec', #Hadronic Endcap
             #'lar_fcal',
             'tile'   # tile calorimeter
            ]
detKeys={ 
          (0b0001): 'lar_em',
          (0b0010): 'lar_hec',
          (0b0100): 'lar_fcal',
          (0b1000): 'tile'
        }

decoder = {
            'lar_em':{
                       0b00100 : 'PS'     ,
                       0b00101 : 'layer_1',
                       0b00110 : 'layer_2',
                       0b00111 : 'layer_3',
                       0b01000 : 'ec_in_PS',
                       0b01001 : 'ec_in_l1',
                       0b01010 : 'ec_in_l2',
                       0b01011 : 'ec_in_l3',
                       0b10000 : 'ec_out_PS',
                       0b10001 : 'ec_out_l1',
                       0b10010 : 'ec_out_l2',
                       0b10011 : 'ec_out_l3'
                     },
            
            'tile':{
                      0b00001000 : 'sample_a', 
                      0b00001001 : 'sample_b', 
                      0b00001010 : 'sample_d', 
                      0b00001011 : 'sample_e', 
                      0b00001100 : 'sample_x' 
                   } 
          }

def plotItAll():
    for event in range(tree.GetEntries()):
        tree.GetEvent(event)
        outfile.mkdir('Event '+str(event))
        outfile.cd('Event '+str(event))
        for det in detectors:
            gDirectory.mkdir(det)
            gDirectory.cd(det)
            for layer in decoder[det].items(): 
                gDirectory.mkdir(layer[1])
                gDirectory.cd(layer[1])
                try:
                    eta_phi_h2 = TH2F('eta_phi_h2_'+det+'_'+layer[1], 'eta_phi_h2_'+det+'_'+layer[1],
                                                                     pph.getDetBins(det, layer[1], 'eta'),
                                                                     pph.getDetLow(det, layer[1], 'eta'),
                                                                     pph.getDetHi(det, layer[1], 'eta'),
                                                                     pph.getDetBins(det,layer[1], 'phi'),
                                                                     pph.getDetLow(det, layer[1], 'phi'),
                                                                     pph.getDetHi(det, layer[1], 'phi'))
                    E_eta_phi_h2 = TH2F('E_eta_phi_h2_'+det+'_'+layer[1], 'E_eta_phi_h2_'+det+'_'+layer[1],
                                                                     pph.getDetBins(det, layer[1], 'eta'),
                                                                     pph.getDetLow(det, layer[1], 'eta'),
                                                                     pph.getDetHi(det, layer[1], 'eta'),
                                                                     pph.getDetBins(det,layer[1], 'phi'),
                                                                     pph.getDetLow(det, layer[1], 'phi'),
                                                                     pph.getDetHi(det, layer[1], 'phi'))
                except KeyError:
                    print "key error on: ", det, layer[1]
                    gDirectory.cd('../')
                    continue
                for n in range(tree.cell_n):
                    if getDet(tree.cell_DetCells[n]) == det:
                        if getBarelLayer(n, det, tree.cell_DetCells[n]) == layer[1]:
                            # now this entry of the vector holds the right info
                            eta_phi_h2.Fill(tree.cell_eta[n], tree.cell_phi[n])
                            if E_eta_phi_h2.GetBinContent( E_eta_phi_h2.FindBin(tree.cell_eta[n], tree.cell_phi[n])) != 0:
                                print "Warning. Bin not empty. Overwriting contents"
                            E_eta_phi_h2.SetBinContent( E_eta_phi_h2.FindBin(tree.cell_eta[n], tree.cell_phi[n]), tree.cell_E[n])
                eta_phi_h2.Write()
                E_eta_phi_h2.Write()
                gDirectory.cd('../')
            gDirectory.cd('../')
        gDirectory.cd('../')
    outfile.Write()
                
def getDet(detCells):

    return detKeys[detCells & 0b1111]  ## get the first 4 bits

def getBarelLayer(n, det, detCells):
   if det == 'lar_em':
      try:
        return decoder['lar_em'][(detCells & 0b11111<<4) >> 4]
      except KeyError:
        print "cell_n: ", n
        print "Key Error: ",bin((detCells & 0b11111<<4) >> 4)
        print "Detector: ", det
        print "DetCells: ", bin(detCells)
        return 0

   if det == 'tile':
      if ((detCells & 0b00001111<<13) >> 13) == 0:
          return 0 
      try:
        return decoder['tile'][(detCells & 0b00001111<<13) >> 13]
      except KeyError:
        print "cell_n: ", n
        print "key Error: ",bin((detCells & 0b00001111<<13) >> 13)
        print "Detector: ", det
        print "DetCells: ", bin(detCells)
        return 0     





if __name__ == '__main__':
   plotItAll()




