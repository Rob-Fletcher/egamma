from ROOT import *
import rootlogon
import re
import PyPlotHelper as p

pph = p.PyPlotHelper()
var_names_list = [ #  'el_rhad',
                     'el_reta',
                     'el_deltaeta1',
                     'el_weta2',
                     'el_f1',
                     'el_rphi',
                     'el_f3',
                     'el_TRTHighTOutliersRatio',
                    # 'el_eratio',       # --> see getERatio() below
                    # 'el_DeltaPoverP',  # --> see getDeltaPoverP() below
                     'el_deltaphiRescaled',
                    # 'el_d0significance',    # --> see below.
                     'el_trackd0pvunbiased',
                    # 'el_isConv',            # --> see below.
                    # 'el_EoverP',     # --> see below.
                    ]


full_MC_files = [ '~/egamma/Data/June19_2013_LHSignal_mu40_bs25_Iso_TIBALE_MC.root',
                  '~/egamma/Data/June19_2013_LHSignal_mu60_bs25_Iso_TIBALE_MC.root',
                  '~/egamma/Data/June19_2013_LHSignal_mu80_bs25_Iso_TIBALE_MC.root',
                  '~/egamma/Data/June19_2013_LHSignal_mu80_bs50_Iso_TIBALE_MC.root'
                ]

outfile = TFile('~/egamma/rootfiles/2013_June/all_var_overlay.root', 'recreate')

def getHistos( name ):
   print 'Opening file: ', name
   m = re.search('mu\d\d_bs\d\d', name)
   label = m.group(0)
   f = TFile(name)
   t = f.Get('photon')
   outfile.mkdir(label)
   outfile.cd(label)
   histos = [ TH1F( var, var, pph.getBins(var), pph.getLow(var), pph.getHi(var)) for var in var_names_list ]
   for var in var_names_list:
      t.Draw(var+'>>'+var, '', 'goff')
   [h.GetXaxis().SetTitle( str(h.GetTitle()).lstrip('el_')) for h in histos]
   f.Close()
   return histos

if __name__=='__main__':
   all_plots = [ getHistos( name ) for name in full_MC_files]
   outfile.Write()
   gROOT.SetBatch(kTRUE)
   gStyle.SetOptTitle(0)
   outfile.cd()
   keys = [a.GetName() for a in outfile.GetListOfKeys()]
   for var in var_names_list:
      canvas = TCanvas(var+'_overlay', var+'_overlay')
      for i, mu in enumerate(keys): 
         dir = outfile.Get(mu)
         hist = dir.Get(var)
         hist.SetLineColor(i+1)
         hist.SetTitle(mu)
         if i == 0:
            hist.DrawNormalized()
         else:
            hist.DrawNormalized('same')
      gPad.BuildLegend()
      canvas.Write()
       









