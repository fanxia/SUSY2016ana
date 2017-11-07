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

7, Collect the limits values:
```
python collectlimits.py TAG
```

###########################################
## Plot limits
