
import ROOT
import sys

ROOT.gROOT.SetBatch()

infile = ROOT.TFile(sys.argv[1])
outfileName = sys.argv[2]
canv = ROOT.TCanvas()

canv.Print(outfileName+'[')

for key in infile.GetListOfKeys():
    print key.GetName()
    obj = infile.Get(key.GetName())
    if obj.Class().InheritsFrom(ROOT.TDirectory.Class()):
        continue

    #get canvases and write 'em to PDF.
    if obj.Class().InheritsFrom(ROOT.TCanvas.Class()):
        print "Found canvas. Writing ..."
        canv = obj
        #canv.GetYAxis().SetRangeUser(0.5,1.0)
        list = canv.GetListOfPrimitives()
        hist = 0
        for item in list:
            hist = canv.GetPrimitive(item.GetName())
            if hist.Class().InheritsFrom(ROOT.TH1.Class()):
                print "found first histogram on canvas"
                break
        if 'data' in hist.GetName():
            print "found signal histo"
            hist.GetYaxis().SetRangeUser(0.5,1.0)
        if 'bkgd' in hist.GetName():
            print "found background histo"
            hist.GetYaxis().SetRangeUser(0.0,0.04)

        canv.Print(outfileName)


canv.Print(outfileName+']')
