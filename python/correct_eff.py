from ROOT import TFile, TTree, TH2, TH1, TGraph
import rootlogon
import argparse
from array import array

def correctEff(args):
   # loop over all the things
   infile = TFile(args.input)
   tree   = TTree('t1', 'tree')
   h2     = infile.Get(args.histo)

   Xaxis = array('i',[0])
   cuts  = array('f',[0.])

   tree.Branch( 'mu', Xaxis, 'mu/I' )
   tree.Branch( args.histo, cuts, args.histo+'/F' )

   target_Eff = 0.94

   for bin in xrange(1, h2.GetNbinsX()): 
      h1 = h2_mu_Rhad.ProjectionY('h1', bin, bin)
      
      if h1.Integral(1, h1.GetNbinsX()) < 100:
         continue

      corrected_cut_bin = getCut(h1, target_Eff)

      final_cut = h1.GetBinCenter(corrected_cut_bin)

      Xaxis[0] = bin
      cuts[0]  = final_cut
      tree.Fill()



   outfile = TFile(args.output, 'update')
   gFile = outfile
   tree.Write()
   outfile.Close()

def getCut(histo, target_Eff):
   """Find the value of the cut that preserves the efficiency

      \param histo 1D histogram to cut on
      \param target_Eff the efficiency the function should try to get closest too
      \param cut_bin what bin should be used to cut the histogram
      \return The bin that was used to get closest to the target efficiency

   """ 
   for bin in xrange(1, histo.GetNbinsX()):

      current_Eff = getEff(histo, bin) 

   # if the current cut is within the range of efficiency
   # then return the current cut bin
      if abs(current_Eff - target_Eff) < 0.005:
         return bin

   print 'no cut bin found. Current EFF: ', current_Eff, '\n'

def getEff(histo, Cut):
   """Get Efficiency of the cut

   Integrates the histo after the cut then divides by the 
   uncut histo integral to get the fraction of electrons
   that pass the cut.

   \param histo the histogram to integrate
   \param Cut the cut to make on the histogram
   \return The Efficiency
   """
   maxBin = histo.GetNbinsX()
   total = histo.Integral(1, maxBin)
   if total == 0:  # get rid of division by zero
      return 0
   elif gCUTLOW:
      return histo.Integral(Cut, maxBin) / total  
   else:
      return histo.Integral(1, Cut) / total


if __name__=='__main__':

   pars = argparse.ArgumentParser()
   pars.add_argument('--input','-i', required=True, help='input root file')
   pars.add_argument('--histo', required=True, help='2d histo to parameterize')
   pars.add_argument('--output','-o', help='ouput root file', default='output.root')
   pars.add_argument('--cutLow','-c', default=False, type=bool, help='Set True if the cut should be made to the left, False for right')
   args = pars.parse_args()

   gCUTLOW = args.cutLow

   correctEff(args)





