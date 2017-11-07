# plot the contour limits, use the txt limit input file
import math,sys
import ROOT
import time
import datetime
from ROOT import *
from array import array
import os, string, math


tag=sys.argv[1]
##############################################################
def GetContourTG(graph2d):
    hist2d=graph2d.GetHistogram()
#    ctest=ROOT.TCanvas("ctest","ctest",1000,1000);

    contours=array('d',[0.,1.0])
    hist2d.SetContour(2,contours)
    hist2d.Draw("SAME CONT LIST")

    gPad.Update()

#    contsM = TObjArray()
    contsM=gROOT.GetListOfSpecials().FindObject("contours");
    print contsM
    contLevel = contsM.At(0);
    print contLevel
    curv = contLevel.First().Clone("exclusion_contour");
    
    return curv


###############################################################

file_in=open("../LimitTable_"+tag+".txt","r")
os.system('mkdir Contourplots')
file_out=TFile("Contourplots/"+tag+".root","recreate")

Gr2D_sigxsec=ROOT.TGraph2D()  #origin theory xsec, only depends on stop mass
Gr2D_obsxsec=ROOT.TGraph2D()  #observed xsec, is theory_xsec*obsLimit, used as base color in limit plots
Gr2D_expxsec=ROOT.TGraph2D()  #exp. xsec, is theory_xsec*expLimit
Gr2D_obslimit=ROOT.TGraph2D() #observed limit, is obsLimit, compare with 1. link all the points of value 1, that's the contour
Gr2D_obsmlimit=ROOT.TGraph2D()
Gr2D_obsplimit=ROOT.TGraph2D()
Gr2D_explimit=ROOT.TGraph2D()
Gr2D_expm1limit=ROOT.TGraph2D()
Gr2D_expp1limit=ROOT.TGraph2D()

ind=0
for line in file_in:
    if 'mstop' in line:
        mstop=float(filter(str.isdigit, line))
    elif 'mnlsp' in line:
        mnlsp=float(filter(str.isdigit, line))
    elif 'xsec=' in line:
        xsec=float(line.split('=')[1])
    elif 'obsLimit' in line:
        obsLimit=float(line.split('=')[1])
    elif 'expLimit' in line:
        expLimit=float(line.split('=')[1])
    elif 'exp_m1s' in line:
        exp_m1s=float(line.split('=')[1])
    elif 'exp_p1s' in line:
        exp_p1s=float(line.split('=')[1])


    elif '##' in line:
        # end reading this masspoint, and fill graphs
        print "get mass point:", mstop, mnlsp,xsec, obsLimit, expLimit
        Gr2D_sigxsec.SetPoint(ind,mstop,mnlsp,xsec)
        Gr2D_obsxsec.SetPoint(ind,mstop,mnlsp,xsec*obsLimit)
        Gr2D_expxsec.SetPoint(ind,mstop,mnlsp,xsec*expLimit)
        Gr2D_obslimit.SetPoint(ind,mstop,mnlsp,obsLimit)
        Gr2D_explimit.SetPoint(ind,mstop,mnlsp,expLimit)
        Gr2D_expm1limit.SetPoint(ind,mstop,mnlsp,exp_m1s)
        Gr2D_expp1limit.SetPoint(ind,mstop,mnlsp,exp_p1s)
        ind+=1
        

# get contour tgraph: tgraph2d->getTH2F->getcontour
contour_obslimit=GetContourTG(Gr2D_obslimit)
contour_explimit=GetContourTG(Gr2D_explimit)
contour_expm1limit=GetContourTG(Gr2D_expm1limit)
contour_expp1limit=GetContourTG(Gr2D_expp1limit)








#########
#graph=Gr2D_obsxsec
graph=Gr2D_expxsec
c=ROOT.TCanvas("c","c",1000,800);
c.SetRightMargin(0.12)
gStyle.SetPalette(1)

# special palette setting for susy plots
stops = array("d",[0.00, 0.34, 0.61, 0.84, 1.00])
red= array("d",[0.50, 0.50, 1.00, 1.00, 1.00])
green = array("d",[ 0.50, 1.00, 1.00, 0.60, 0.50])
blue = array("d",[1.00, 1.00, 0.50, 0.40, 0.50])
TColor.CreateGradientColorTable(5,stops,red,green,blue,255)



virtualLineA = ROOT.TLine(300, 300, 1400, 1400);
virtualLineA.SetLineStyle(2);
virtualLineA.SetLineWidth(2);
nlspCommentA = ROOT.TLatex(650, 670, "m_{ #tilde{t}} < m_{ Bino}");
nlspCommentA.SetTextAngle(40);
nlspCommentA.SetTextSize(0.025);
# top mass=172                                                                                                                         
virtualLineB = ROOT.TLine(300, 128, 1500, 1328);
virtualLineB.SetLineStyle(2);
virtualLineB.SetLineWidth(2);
nlspCommentB = ROOT.TLatex(650, 500, "m_{ #tilde{t}} < m_{ Bino}+m_{ t}");
nlspCommentB.SetTextAngle(35);
nlspCommentB.SetTextSize(0.025);

comment = ROOT.TLatex(400, 1000, 'MU');
#      comment.SetTextAngle(40);                                                                                                             
comment.SetTextSize(0.05);



#graph.SetTitle(title)
graph.SetMaximum(0.07)
graph.SetMinimum(0.003)
#graph.GetXaxis().SetTitle(xtitle)
#graph.GetXaxis().SetLabelSize(0.025)
#graph.GetYaxis().SetLabelSize(0.025)
#graph.GetZaxis().SetLabelSize(0.03)
#graph.GetYaxis().SetTitle(ytitle)
#graph.GetYaxis().SetTitleOffset(1.3)
graph.Draw("colz")
graph.Write("name")
gPad.SetLogz(1)
#contour_obslimit.Draw("same")
contour_explimit.SetLineStyle(7)
contour_explimit.Draw("same")
contour_expm1limit.SetLineStyle(2)
contour_expp1limit.SetLineStyle(2)
#contour_expm1limit.Draw("same")
#contour_expp1limit.Draw("same")


virtualLineA.Draw("same")
virtualLineB.Draw("same")
nlspCommentA.Draw("same")
nlspCommentB.Draw("same")
comment.Draw("same")
c.Print("Contourplots/contour"+tag+".pdf")


file_out.Write()
file_out.Close()        
