
import ROOT
import sys



infile = ROOT.TFile(sys.argv[1])
outfileName = sys.argv[2]
canv = ROOT.TCanvas()

canv.Print(outfileName+'[')

for key in infile.GetListOfKeys():
    obj = infile.Get(key)
    if obj.Class().InheritsFrom(ROOT.TDirectory.Class()):
        continue

    #get canvases and write 'em to PDF.
    if obj.Class().InheritsFrom(ROOT.TCanvas.Class()):
        canv = obj
        canv.Print(outfileName)


canv.Print(outfileName+']')
