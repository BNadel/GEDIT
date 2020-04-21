from sys import *
ToolRan = None
size = argv[1].split("/")[-1].split("_")[1]
for line in open(argv[1],"r"):
   if line[0:5] == "Tool:":
       ToolRan = line.strip().split()[1]
   if "Mar" in line and ("PDT 2020" in line or "PST 2020" in line):
       timeParts = line.split()[3].split(":")
       hourSeconds = float(timeParts[0])*60*60
       minuteSeconds = float(timeParts[1])*60
       secondSeconds = float(timeParts[2])
       TotalSeconds = hourSeconds+minuteSeconds+secondSeconds
       if ToolRan != None:
           print ToolRan + "\t" + size + "\t" + str(TotalSeconds - prevTime)
           ToolRan = None
       prevTime = TotalSeconds
