#!/bin/bash

if [ -z ${ROOTSYS:+x} ]
  then
    echo "Root not setup. Doing it now."
    localSetupROOT
fi

if [ -z ${ROOTCOREDIR:+x} ]
  then
    echo "RootCore not setup. Doing it now."
    cd ~/testarea/anotherone
    source RootCore/scripts/setup.sh
fi

cd ~/testarea/anotherone/egammaCore/macros

python studyPDFs.py --dir ~/egamma/scripts/PDF_test_dir

cd ~/egamma/scripts/
python ~/egamma/scripts/overlayPDFs.py ~/egamma/scripts/PDF_test_dir/output/out.root

root ~/egamma/plots/August_2014/fixed-stretch-test_reta_overlay.root 



