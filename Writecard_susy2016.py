#!/usr/bin/env python

import CombineHarvester.CombineTools.ch as ch
import ROOT as R
import glob
import os

cb = ch.CombineHarvester()

auxiliaries  = os.environ['CMSSW_BASE'] + '/src/CombineHarvester/CombineTools/SUSY2016ana/'
aux_shapes   = auxiliaries +'inputshapes/'
aux_pruning  = auxiliaries +'pruning/'

masses=open(aux_shapes+'scanpointname.txt').read().splitlines()
#input_dir    = os.environ['CMSSW_BASE'] + '/src/CombineHarvester/CombineTools/input';

chns = ['eg', 'egg', 'mg', 'mgg']

infile = {'eg':'Oct16_ELE.root', 'egg':'Oct16_ELE.root', 'mg':'Oct16_Mu.root','mgg':'Oct16_Mu.root'}

bkg_procs = { 'eg':["TT", "WJets", "ZJets","ST","Vgamma","TTV","TTG","VV"],
#              'egg':["TT", "WJets", "ZJets","ST","Vgamma","TTV","TTG","VV"],
              'egg':["TT", "ST","Vgamma","TTV","TTG","ZJets"],
              'mg':["TT", "WJets", "ZJets","ST","Vgamma","TTV","TTG","VV"],
              'mgg':["TT", "ST","Vgamma","TTV","TTG"]
#              'mgg':["TT", "WJets", "ZJets","ST","Vgamma","TTV","TTG","VV"],
}

sig_procs = ['SMS_T6ttZg']

#cats = [
#   (1, "Aug2_ELE_pfMET_SR1_ele_bjj"),
#   (2, "Aug2_ELE_pfMET_SR2_ele_bjj"),
#]
cats = {
'eg':[(1, "Oct16_ELE_pfMET_SR1_ele_bjj")],
'egg':[(1, "Oct16_ELE_pfMET_SR2_ele_bjj")],
'mg':[(1, "Oct16_Mu_pfMET_SR1_mu_bjj")],
'mgg':[(1, "Oct16_Mu_pfMET_SR2_mu_bjj")] 
}



print '>> Creating processes and observations...'

for era in ['13TeV']:
    for chn in chns:
        cb.AddObservations(   ['*'], ['FX'], [era], [chn],                 cats[chn]         )
        cb.AddProcesses(      ['*'], ['FX'], [era], [chn], bkg_procs[chn], cats[chn], False  )
        cb.AddProcesses(     masses, ['FX'], [era], [chn], sig_procs,      cats[chn], True   )

#    cb.AddObservations(   ['*'], ['MU'], [era], ["MET"],                 cats['MU']         )
#    cb.AddProcesses(      ['*'], ['MU'], [era], ["MET"], bkg_procs, cats['MU'], False  )
#    cb.AddProcesses(     masses, ['MU'], [era], ["MET"], sig_procs,      cats['MU'], True   )


#Have to drop ZL from tautau_vbf category
#cb.FilterProcs(lambda p : p.bin() == 'tauTau_vbf' and p.process() == 'ZL')

print '>> Adding systematic uncertainties...'
# get the xsec uncert. for signal
stopxsfile=aux_shapes+'stop_pair_13TeVxs.dat'
stopxslist=[[float(element) for element in line.strip().split()] for line in open(stopxsfile).read().strip().split('\n')]
stopxsdic={i[0]:i[1:] for i in stopxslist}
for m in masses:
    xserr=(stopxsdic[float(filter(str.isdigit,m.split('_')[0]))][1]+100)/100.
    cb.cp().signals().AddSyst(cb, "sig_xsecErr","lnN",ch.SystMap()(xserr))
cb.cp().process(sig_procs).AddSyst(cb, 'genMET', "shape", ch.SystMap()(1.0))



# lumi uncertainty
cb.cp().process(sig_procs+["TT", "WJets", "ZJets","ST","Vgamma","TTV","TTG","VV"]).AddSyst(cb, 'lumi_$ERA', "lnN", ch.SystMap()(1.025))
cb.cp().process(["TT", "WJets", "ZJets","ST","Vgamma","TTV","TTG","VV"]).AddSyst(cb, 'pileup_$ERA', "lnN", ch.SystMap()(1.046))
#cb.cp().signals().AddSyst(cb, "lumi_$ERA", "lnN", ch.SystMap('era')(["13TeV"],1.026))
#cb.cp().signals().AddSyst(cb, "lumi_$ERA", "lnN", ch.SystMap()(1.026))

#cb.cp().process([sig_procs+["TT", "WJets", "ZJets","ST","Vgamma","TTV","TTG","VV"]]).AddSyst(
cb.cp().process(sig_procs+["TT", "WJets", "ZJets","ST","Vgamma","TTV","TTG","VV"]).AddSyst(cb, 'BbtagWeight', "shape", ch.SystMap()(1.0))
cb.cp().process(["TT", "WJets", "ZJets","ST","Vgamma","TTV","TTG","VV"]).AddSyst(cb, 'BphoWeight', "shape", ch.SystMap()(1.0))
cb.cp().channel(['mg','mgg']).process(["TT","TTV","TTG"]).AddSyst(cb, 'BtopPtWeight',"shape",ch.SystMap()(1.0))
cb.cp().channel(['mg','mgg']).process(["TT", "WJets", "ZJets","ST","Vgamma","TTV","TTG","VV"]).AddSyst(cb, 'BJES',"shape",ch.SystMap()(1.0))
#cb.cp().channel(['mgg']).process(["TT", "WJets", "ZJets","ST","Vgamma","TTV","TTG","VV"]).AddSyst(cb, 'BJES',"shape",ch.SystMap()(1.0))
cb.cp().channel(['mg','mgg']).process(["TT", "WJets", "ZJets","ST","Vgamma","TTV","TTG","VV"]).AddSyst(cb, 'BmuWeight',"shape",ch.SystMap()(1.0))
#cb.cp().channel(['mg','mgg']).process(["TT", "WJets", "ZJets","ST","Vgamma","TTV","TTG","VV"]).AddSyst(cb, 'BmuWeight',"shape",ch.SystMap()(1.0))

##cb.cp().channel(['mg']).process(["TT"]).AddSyst(cb,"gpuritysf","lnN",ch.SystMap()(1.1))
##cb.cp().channel(['mgg']).process(["TT"]).AddSyst(cb,"gpuritysf","lnN",ch.SystMap()(1.14))
cb.cp().channel(['mg']).process(["TTG"]).AddSyst(cb,"gpuritysf","lnN",ch.SystMap()(1.14))
cb.cp().channel(['mgg']).process(["TTG"]).AddSyst(cb,"gpuritysf","lnN",ch.SystMap()(1.46))
#cb.cp().channel(['mgg']).process(["TTG"]).AddSyst(cb,"gpuritysf","lnN",ch.SystMap()(1.2))
cb.cp().channel(['mg','mgg']).process(["WJets"]).AddSyst(cb,"jetm3_wSF","lnN",ch.SystMap()(1.18))
##cb.cp().channel(['mg','mgg']).process(["TT"]).AddSyst(cb,"jetm3_wSF","lnN",ch.SystMap()(1.08))

cb.cp().channel(['mg']).process(["TT"]).AddSyst(cb,"comb","lnN",ch.SystMap()(1.13))
cb.cp().channel(['mgg']).process(["TT"]).AddSyst(cb,"comb","lnN",ch.SystMap()(1.17))

#### for >1bjets###
#cb.cp().channel(['mg']).process(["TTG"]).AddSyst(cb,"gpuritysf","lnN",ch.SystMap()(1.17))
#cb.cp().channel(['mgg']).process(["TTG"]).AddSyst(cb,"gpuritysf","lnN",ch.SystMap()(1.39))
#cb.cp().channel(['mg','mgg']).process(["WJets"]).AddSyst(cb,"jetm3_wSF","lnN",ch.SystMap()(1.5))
#cb.cp().channel(['mg']).process(["TT"]).AddSyst(cb,"comb","lnN",ch.SystMap()(1.17))
#cb.cp().channel(['mgg']).process(["TT"]).AddSyst(cb,"comb","lnN",ch.SystMap()(1.26))
#### END for >1bjets### 

cb.cp().channel(['eg','egg']).process(["TT","TTV","TTG"]).AddSyst(cb, 'BtopPtWeight',"shape",ch.SystMap()(1.0))
cb.cp().channel(['eg','egg']).process(["TT", "WJets", "ZJets","ST","Vgamma","TTV","TTG","VV"]).AddSyst(cb, 'BJES',"shape",ch.SystMap()(1.0))
#cb.cp().channel(['egg']).process(["TT", "WJets", "ZJets","ST","Vgamma","TTV","TTG","VV"]).AddSyst(cb, 'BJES',"shape",ch.SystMap()(1.0))
cb.cp().channel(['eg','egg']).process(["TT", "WJets", "ZJets","ST","Vgamma","TTV","TTG","VV"]).AddSyst(cb, 'BeleWeight',"shape",ch.SystMap()(1.0))
#cb.cp().channel(['egg']).process(["TT", "WJets", "ZJets","ST","Vgamma","TTV","TTG","VV"]).AddSyst(cb, 'BeleWeight',"shape",ch.SystMap()(1.0))

##cb.cp().channel(['eg']).process(["TT"]).AddSyst(cb,"gpuritysf","lnN",ch.SystMap()(1.14))
##cb.cp().channel(['egg']).process(["TT"]).AddSyst(cb,"gpuritysf","lnN",ch.SystMap()(1.22))
cb.cp().channel(['eg']).process(["TTG"]).AddSyst(cb,"gpuritysf","lnN",ch.SystMap()(1.18))
cb.cp().channel(['egg']).process(["TTG"]).AddSyst(cb,"gpuritysf","lnN",ch.SystMap()(1.5))
#cb.cp().channel(['egg']).process(["TTG"]).AddSyst(cb,"gpuritysf","lnN",ch.SystMap()(1.2))
cb.cp().channel(['eg','egg']).process(["ZJets"]).AddSyst(cb,"zjetsf","lnN",ch.SystMap()(1.45))
cb.cp().channel(['eg','egg']).process(["WJets"]).AddSyst(cb,"jetm3_wSF","lnN",ch.SystMap()(1.17))
##cb.cp().channel(['eg','egg']).process(["TT"]).AddSyst(cb,"jetm3_wSF","lnN",ch.SystMap()(1.09))

cb.cp().channel(['eg']).process(["TT"]).AddSyst(cb,"comb","lnN",ch.SystMap()(1.16)) 
cb.cp().channel(['egg']).process(["TT"]).AddSyst(cb,"comb","lnN",ch.SystMap()(1.24)) 

#### for >1bjets###
#cb.cp().channel(['eg']).process(["TTG"]).AddSyst(cb,"gpuritysf","lnN",ch.SystMap()(1.19))
#cb.cp().channel(['egg']).process(["TTG"]).AddSyst(cb,"gpuritysf","lnN",ch.SystMap()(1.66))
#cb.cp().channel(['eg','egg']).process(["ZJets"]).AddSyst(cb,"zjetsf","lnN",ch.SystMap()(1.45))
#cb.cp().channel(['eg','egg']).process(["WJets"]).AddSyst(cb,"jetm3_wSF","lnN",ch.SystMap()(1.46))
#cb.cp().channel(['eg']).process(["TT"]).AddSyst(cb,"comb","lnN",ch.SystMap()(1.19))
#cb.cp().channel(['egg']).process(["TT"]).AddSyst(cb,"comb","lnN",ch.SystMap()(1.36))
#### END for >1bjets###


#xsec error
#cb.cp().process(["TT"]).AddSyst(cb,"xsec_err","lnN",ch.SystMap()(1.05))
#cb.cp().process(["TTV"]).AddSyst(cb,"xsec_err","lnN",ch.SystMap()(1.01))

######
print '>> Extracting histograms from input root files...'
for era in ['13TeV']:
  for chn in chns:
    file = aux_shapes  + infile[chn]
    cb.cp().channel([chn]).backgrounds().ExtractShapes(
        file, '$BIN_$PROCESS', '$BIN_$SYSTEMATIC_$PROCESS')
    cb.cp().channel([chn]).signals().ExtractShapes(
        file, '$BIN__$PROCESS_$MASS', '$BIN_$SYSTEMATIC__$PROCESS_$MASS')


print '>> Merging bin errors and generating bbb uncertainties...'
bbb = ch.BinByBinFactory()
bbb.SetAddThreshold(0.1).SetFixNorm(True)

bbb.AddBinByBin(cb.cp().backgrounds(), cb);
print '>> Setting standardised bin names...'
ch.SetStandardBinNames(cb)
bins = cb.bin_set()

#output=R.TFile("SUSYtest.input.root", "RECREATE")

 
writer = ch.CardWriter('$TAG/$ANALYSIS_$CHANNEL_$BINID_$ERA_$MASS.txt',
                       '$TAG/$ANALYSIS_$CHANNEL.input.root')   
#cmb for all datacards
#writer.WriteCards('outputest/datacards/cmb', cb)

#store datacards according to their bin...
#for b in bins :
for m in masses :
#        print "Writing datacard for bin: " +b + " and mass: " + m+"\n" 
        writer.WriteCards('outputest/datacardsOct16/'+m+'/All', cb.cp().mass([m,"*"]))
        # for b in bins[0:2]:
        #     writer.WriteCards('outputest/datacardsMay41/'+m+'/ELE', cb.cp().mass([m,"*"]).bin([b]))
        # for b in bins[2:4]:
        #     writer.WriteCards('outputest/datacardsMay41/'+m+'/MU', cb.cp().mass([m,"*"]).bin([b]))
        # for b in [bins[0],bins[2]]:
        #     writer.WriteCards('outputest/datacardsJul10/'+m+'/SR1', cb.cp().mass([m,"*"]).bin([b]))
        # for b in [bins[1],bins[3]]:
        #     writer.WriteCards('outputest/datacardsMay41/'+m+'/SR2', cb.cp().mass([m,"*"]).bin([b]))

        # for b in bins:
        #     writer.WriteCards('outputest/datacardsMay41/'+m+'/'+b, cb.cp().mass([m,"*"]).bin([b]))


print '>> Done!'
