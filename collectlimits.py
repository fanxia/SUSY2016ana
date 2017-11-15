#!/bin/python
import math,sys
import ROOT
from ROOT import *
from commands import getoutput
from array import array
import os, string, math

Channel=sys.argv[1]
datadir='outputest/datacardsNov9/'
stopxsfile='inputshapes/stop_pair_13TeVxs.dat'
stopxslist=[[float(element) for element in line.strip().split()] for line in open(stopxsfile).read().strip().split('\n')]
stopxsdic={i[0]:i[1:] for i in stopxslist}

if Channel=='ALL':
    ch='/All/'
elif Channel=='ELE':
    ch='/ELE/'
elif Channel=='ELE_SR1':
    ch='/FX_eg_1_13TeV/'
elif Channel=='ELE_SR2':
    ch='/FX_egg_1_13TeV/'
elif Channel=='MU':
    ch='/MU/'
elif Channel=='MU_SR1':
    ch='/FX_mg_1_13TeV/'
elif Channel=='MU_SR2':
    ch='/FX_mgg_1_13TeV/'
elif Channel=='SR1':
    ch='/SR1/'
elif Channel=='SR2':
    ch='/SR2/'

else:
    print 'There is NOT this Channel, check again! '


outfile=open("LimitTable_"+Channel+"Nov9.txt","w")

masslist=getoutput('ls '+datadir).split('\n')

for mass in masslist:
    if not 'Mst' in mass: continue
    mstop=int(filter(str.isdigit,mass.split('_')[0]))
    mnlsp=int(filter(str.isdigit,mass.split('_')[1]))
    xsec=stopxsdic[mstop][0]
    xsecErr=stopxsdic[mstop][1]

    limitfile=TFile.Open(datadir+mass+ch+"higgsCombine.limit.Asymptotic.mH120.root")
    limitree=limitfile.Get("limit")
    
    for lim in limitree:


        cl=lim.quantileExpected

        if cl == -1:
            obs=lim.limit
            up_obs=obs*1.0/(1-(float(xsecErr)/100.))
            dn_obs=obs*1.0/(1+(float(xsecErr)/100.))

        elif abs(cl-0.025) < 1E-4:
            m2s_exp=lim.limit
        elif abs(cl - 0.16) < 1E-4:
            m1s_exp=lim.limit
        elif abs(cl - 0.5) < 1E-4:
            exp=lim.limit
        elif abs(cl- 0.84) < 1E-4:
            p1s_exp=lim.limit
        elif abs(cl- 0.975) < 1E-4:
            p2s_exp=lim.limit

        else: continue


    outfile.write('mstop=%s\n'%mstop)
    outfile.write('mnlsp=%s\n'%mnlsp)
    outfile.write('xsec=%s\n'%xsec)
    outfile.write('xsecErr=%s\n'%xsecErr)
    outfile.write('obsLimit=%s\n'%obs)
    outfile.write('obs_up=%s\n'%up_obs)
    outfile.write('obs_dn=%s\n'%dn_obs)
    outfile.write('expLimit=%s\n'%exp)
    outfile.write('exp_m2s=%s\n'%m2s_exp)
    outfile.write('exp_m1s=%s\n'%m1s_exp)
    outfile.write('exp_p1s=%s\n'%p1s_exp)
    outfile.write('exp_p2s=%s\n'%p2s_exp)
    outfile.write('#####################################\n')

outfile.close()
