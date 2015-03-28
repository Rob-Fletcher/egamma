#import ROOT
import argparse

file_list = [ 
             'file1.root',
             'file2.root',
             'file3.root'
            ]
          
configs = {}

configs.update(files=file_list)









if __name__=="__main__":

    #parse arguments
    parser = argparse.ArgumentParser(description='Overlay corresponding histograms in several root files.')
    parser.add_argument('--files', nargs='*', help='Root files to overlay.')

    args = p.parse_args() 

    config.update(args.__dict__) #append command line args to the config dictionary
    print configs

