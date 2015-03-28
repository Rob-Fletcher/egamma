import ROOT as r

branches = ['el_n', 'el_eta','el_cl_eta', 'el_cl_E', 'el_etas2', 'el_Ethad', 'el_Ethad1', 'el_reta', 'PV_n', 'PV_trk_n', 'averageIntPerXing']

def makeTree():
   f = r.TFile('~/egamma/Data/March9_2013_LHSignal_Iso_TIBALE.root')
   tree = f.Get('photon')

   tree.SetBranchStatus('*', 0)

   for name in branches:
      tree.SetBranchStatus( name, 1)

   outfile = r.TFile('trimmed_tree.root', 'recreate')
   newTree = tree.CloneTree()

   newTree.Print()
   outfile.Write()

   del f
   del outfile


if __name__ == '__main__':
   makeTree()
