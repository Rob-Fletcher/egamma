import ROOT
import re

ROOT.gROOT.SetBatch(ROOT.kTRUE)
colors = [ ROOT.kRed,
           ROOT.kOrange,
           ROOT.kYellow,
           ROOT.kGreen,
           ROOT.kCyan,
           ROOT.kBlue,
           ROOT.kViolet,
           ROOT.kMagenta,
           ROOT.kBlack,
           ]

var = 'el_weta2'
file_head = 'weta2'
outfile_path = '~/egamma/plots/february_2014/'

infile = ROOT.TFile('~/egamma/PDFs/february_2014/'+file_head+'_shifted_PDFs.root')
outfile = ROOT.TFile('~/egamma/plots/february_2014/'+file_head+'_grouped_PDFs.root', 'recreate')

indir = infile.Get(var+'/sig') 
et_dict = {}
eta_dict = {}

#make a dictionary of all histos where each Et key is a list of etas.
for histo in indir.GetListOfKeys():
    name = histo.GetName()
    if not 'KDE' in name:
        continue
    m = re.search('et(\d+)eta(\d.\d+)', name)
    if m:
        search_string = m.group()
        et_label = m.group(1)
        eta_label = m.group(2)

        if not et_dict.get( et_label, False):
            et_dict[et_label] = []
        et_dict[et_label].append(indir.Get(name))

        if not eta_dict.get( eta_label, False):
            eta_dict[eta_label] = []
        eta_dict[eta_label].append(indir.Get(name))

for item in et_dict:
    et_canvas = ROOT.TCanvas(item, item)
    et_canvas.cd()
    i = 0
    for num, histo in enumerate(et_dict[item]):
        histo.SetLineColor(colors[num])
        if i == 0:
            histo.DrawNormalized()
            i = 1
        else:
            histo.DrawNormalized('same')

    et_canvas.Write()
            
for item in eta_dict:
    eta_canvas = ROOT.TCanvas(item, item)
    eta_canvas.cd()
    j = 0
    for num, histo in enumerate(eta_dict[item]):
        histo.SetLineColor(colors[num])
        if j == 0:
            histo.DrawNormalized()
            j = 1
        else:
            histo.DrawNormalized('same')

    eta_canvas.Write()
