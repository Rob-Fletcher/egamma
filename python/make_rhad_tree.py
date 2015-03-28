############################################################################
# This script only generates the el_rhad branch to be used as a 
# friend of the main data to make rhad available for analysis
###########################################################################

from ROOT import TFile, TH1, TH2, TTree
from array import array
import math
import argparse
from sys import stdout

def runIt():
    nEntries = tree.GetEntries()
    for i in range(nEntries):
        if i%1000==0:
           perc = int((float(i)/nEntries)*100)
           stdout.write("\r Scanning Event %d /" %i)
           stdout.write(" %d" %nEntries)
           stdout.write("   %d%%" %perc)
           stdout.flush()

        tree.GetEntry(i)

        a_rhad[0] = getRhad()
        a_Et[0]   = get_Et()
        a_Nvtx[0] = getNvtx()

        rhad_tree.Fill()

    rhad_tree.Write()
    stdout.write("\r")

def get_Et():
    return tree.el_cl_E[0]/math.cosh(tree.el_etas2[0])

def getRhad0():
    return tree.el_Ethad[0]/(tree.el_cl_E[0]/math.cosh(tree.el_etas2[0])) 

def getRhad1():
    return tree.el_Ethad1[0]/(tree.el_cl_E[0]/math.cosh(tree.el_etas2[0])) 

def getRhad():
    if (0.8 <= abs(tree.el_cl_eta[0]) and abs(tree.el_cl_eta[0]) < 1.37):
        return getRhad0()
    else:
        return getRhad1()

def getNvtx():
    nGoodVertices = 0
    VtxMin = 3
    for i in range( tree.PV_n ):
        if (tree.PV_trk_n[i] >= VtxMin):
            nGoodVertices = nGoodVertices + 1
    return nGoodVertices


if __name__ == '__main__':
    
    p = argparse.ArgumentParser()
    p.add_argument('-i', required=True, help='input root file')
    p.add_argument('-o', required=True, help='output root file')
    args = p.parse_args()
    #f=TFile('~/egamma/Data/March9_2013_LHSignal_Iso_TIBALE.root')
    #f=TFile('~/egamma/Data/March9_2013_LHBkg_z100.root')
    f = TFile(args.i)
    tree = f.Get('photon')
    tree.SetBranchStatus('*', 0)
    tree.SetBranchStatus('el_cl_eta', 1)
    tree.SetBranchStatus('el_Ethad', 1)
    tree.SetBranchStatus('el_Ethad1', 1)
    tree.SetBranchStatus('el_etas2', 1)
    tree.SetBranchStatus('el_cl_E', 1)
    tree.SetBranchStatus('PV_n', 1)
    tree.SetBranchStatus('PV_trk_n', 1)

    a_rhad = array('f', [0])
    a_Et   = array('f', [0])
    a_Nvtx = array('i', [0])

    outfile = TFile(args.o, 'recreate')
#    outfile = TFile('trimmed_rhad.root', 'recreate')
    rhad_tree = TTree('rhad_tree', 'rhad_tree')
    rhad_branch = rhad_tree.Branch('el_rhad', a_rhad, 'el_rhad/F')
    Et_branch   = rhad_tree.Branch('el_Et',   a_Et,   'el_Et/F')
    Nvtx_branch= rhad_tree.Branch('el_Nvtx', a_Nvtx,  'el_Nvtx/I')
   
    runIt()

