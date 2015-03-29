
import root
import argparse
import os



def plotObject(args, Dir):
    """Dump all plots and canvases to pdf.

    Dump all plots to pdf up to specified depth
    in a root file.
    """
    pathName = Dir.GetName()
    for key in Dir.GetListOfKeys():
        object = Dir.Get(key)
        if object.Class().InheritsFrom(ROOT.TDirectory.Class()):
            if args.currentDepth < args.depth:
                try:
                    os.mkdir(pathName)
                except OSError:
                    #dir already exists. Open a new pdf for appending.

                args.currentDepth = args.currentDepth + 1
                plotObject(args, object) #Directory recursion
                args.currentDepth = args.currentDepth -1

        if object.Class().InheritsFrom(ROOT.TTree.Class())
            continue

        if object.Class() == ROOT.TCanvas.Class()
                        or object.Class().InheritsFrom(ROOT.TH1.Class())
            #Print the canvas or histogram















if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--depth', type=int, default=0 )
    parser.add_argument('-t','--tag', type=str, default='')

    args = parser.parse_args()
    args.currentDepth = 0
