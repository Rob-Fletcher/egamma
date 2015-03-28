import json

aod = open("/home/robflet/egamma/misc/AODelecInfo2.txt")
#dpd = open("~/egamma/misc/D3PDelecInfo.txt")
dpd = open("/home/robflet/egamma/misc/elecInfo_MyD3PD.txt")

def getDifference(aod, dpd, key):
    try:
        return 100*abs(aod[key] - dpd[key]) / dpd[key]
    except ZeroDivisionError:
        return aod[key], dpd[key], "Zero Division"


for i, aodline in enumerate(aod):
    aodevent = json.loads(aodline)
    dpd.seek(0)

    for dpdline in dpd:
        dpdevent = json.loads(dpdline)
        aodeventNumber = aodevent.keys()[0]
        dpdeventNumber = dpdevent.keys()[0]
        #keep looping until you find matching event numbers
        if not (aodeventNumber == dpdeventNumber):
            continue

        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        print "============= Next Event ==============================================="
        print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
        print "Num of AOD elec: ", len(aodevent[aodeventNumber])
        print "Num of DPD elec: ", len(dpdevent[dpdeventNumber])
        tot = len(aodevent[aodeventNumber])
        totMatched = 0
        for k, aodElec in enumerate(aodevent[aodeventNumber]):
            numMatched = 0
            print "Matching AOD Elec #: ", k+1
            for dpdElec in dpdevent[dpdeventNumber]:
                
                EtDiff = abs(aodElec['et'] - dpdElec['et']) / abs(dpdElec['et'])
                try:
                    etaDiff = 100*abs(aodElec['eta'] - dpdElec['eta']) / abs(dpdElec['eta'])
                except ZeroDivisionError:
                    print "Eta diff is Zero."
                    continue

                if etaDiff < 0.005:
                    print "======================================================================="
                    print "Event Number: ", aodeventNumber, dpdeventNumber
                    print "Electron Number: ", k+1, "/", len(aodevent[aodeventNumber])
                    print "    Emaxs1:    ", getDifference(aodElec, dpdElec, 'Emaxs1')
                    print "    clusterET: ", getDifference(aodElec, dpdElec, 'clusterET')
                    print "    d0: ", getDifference(aodElec, dpdElec, 'd0')
                    print "    d0sigma: ", getDifference(aodElec, dpdElec, 'd0sigma')
                    print "    deltaEta: ", getDifference(aodElec, dpdElec, 'deltaEta')
                    print "    deltaPhiRescaled: ",getDifference(aodElec, dpdElec, 'deltaPhiRescaled')
                    print "    dpOverp: ", getDifference(aodElec, dpdElec, 'dpOverp')
                    print "    e237: ", getDifference(aodElec, dpdElec, 'e237')
                    print "    e277: ", getDifference(aodElec, dpdElec, 'e277')
                    print "    et: ", getDifference(aodElec, dpdElec, 'et')
                    print "    eta: ", getDifference(aodElec, dpdElec, 'eta')
                    print "    ethad: ", getDifference(aodElec, dpdElec, 'ethad')
                    print "    ethad1: ", getDifference(aodElec, dpdElec, 'ethad1')
                    print "    f1: ", getDifference(aodElec, dpdElec, 'f1')
                    print "    f3: ", getDifference(aodElec, dpdElec, 'f3')
                    print "    rTRT: ", getDifference(aodElec, dpdElec, 'rTRT')
                    print "    reta: ", getDifference(aodElec, dpdElec, 'reta')
                    print "    rhad: ", getDifference(aodElec, dpdElec, 'rhad'), aodElec['rhad'], dpdElec['rhad']
                    print "    rhad1: ", getDifference(aodElec, dpdElec, 'rhad1'), aodElec['rhad1'], dpdElec['rhad1']
                    print "    rphi: ", getDifference(aodElec, dpdElec, 'rphi')
                    print "    w2: ", getDifference(aodElec, dpdElec, 'w2')
                    print "    ws3: ", getDifference(aodElec, dpdElec, 'ws3')
                    print "\n"

                    numMatched += 1
                    totMatched += 1

            print ">> Number of electrons Matched to AOD electron:", numMatched, " <<\n"
        print "Total AOD electrons matched:",totMatched,"/",tot,"\n\n"


         
