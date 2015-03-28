
import root
import argparse
import os



def main():
    """Dump all plots and canvases to pdf.

    Dump all plots to pdf up to specified depth
    in a root file.
    """
    for object in Dir.GetListOfKeys():
















if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--depth', type=int, default=1 )
    parser.add_argument('-t','--tag', type=str, default='')

    args = parser.parse_args()
