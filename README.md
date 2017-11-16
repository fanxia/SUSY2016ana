# SUSY2016ana(Limit Setting)
###########################################
## Get Limits
1, This repo need to be installed under **CombineHarvester**, follow the instructions here (http://cms-analysis.github.io/CombineHarvester/index.html)

2, 
```
cd CombineHarvester/CombineTools
git clone git@github.com:fanxia/SUSY2016ana.git
```

3,
put the root file containing all the MET hists to `inputshapes`

4, Write datacards:
```
python Writecard_susy2016.py
```

5, build workspace:
```
cd output/datacards/ 
combineTool.py -M T2W -i Mst*/* -o workspace.root 
```

6, Run limits by using the above workspace:
```
combineTool.py -M Asymptotic -d */*/workspace.root --there -n .limit 
```

7, Collect the limits values(first modify the filenames in collectlimits.py):
```
emacs collectlimits.py
python collectlimits.py TAG
```

###########################################
## Plot limits

1, Plot the obs and expected limits contours and save them into a root file.(can find the tag from previous output. Eg. LimitTable_ALLNov9.txt, then use `ALLNov9` as tag in the command, output will be `Contourplots/ALLNov9.root`)
```
cd plotMacro/
python plotcontour.py tag
```

2, Get the SUSY formatted plots.
```
cd PlotsSMS
cp ../Contourplots/ALLNov9.root fx2016/
emacs fx2016/T6ttZg_fx2016.cfg
python python/makeSMSplots.py fx2016/T6ttZg_fx2016.cfg T6ttZg
```

EXTRA: change the limit plots axis range...
```
emacs python/sms.py
```

ALL DONE!
