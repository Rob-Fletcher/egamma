#!/bin/bash

if [ -n "$ROOTSYS" ]
    then
        export PKG="my_packages"

        while getopts ":p:ul:" opt; do
            case $opt in
                p)
                  echo "Using package list $OPTARG..."
                  export PKG=$OPTARG
                  ;;
                u)
                  echo "Updating all packages and recompiling..."
                  ;;
                l)
                  echo "Using name: $OPTARG"
                  export LN=$OPTARG
                  ;;
                \?)
                  echo "Invalid option: -$OPTARG." >&2
                  return
                  ;;
                :)
                  echo "Option -$OPTARG requires a file with packages listed." >&2
                  return
                  ;;
            esac
        done

        echo "Setting up RootCore and egammaCore packages..."

        #Checkout needed Packages
        svn export svn+ssh://svn.cern.ch/reps/penn/brendlin/egammaCore/trunk/share/my_packages
        svn co svn+ssh://svn.cern.ch/reps/atlasoff/PhysicsAnalysis/D3PDTools/RootCore/tags/RootCore-00-02-99 RootCore

        #Configure RootCore
        cd RootCore
        ./configure
        source scripts/setup.sh
        cd ..

        #Compile Root core and packages
        $ROOTCOREDIR/scripts/manage_all.sh checkout $PKG
        $ROOTCOREDIR/scripts/find_packages.sh
        $ROOTCOREDIR/scripts/compile.sh
        $ROOTCOREDIR/scripts/make_par.sh

        echo "RootCore compilation done."

    else
        echo "Root has not been setup. Need to run localSetupROOT."
fi
