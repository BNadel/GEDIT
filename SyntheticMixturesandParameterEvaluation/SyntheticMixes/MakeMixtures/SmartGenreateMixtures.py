import random
from sys import *

for line in range(1,1001):
   elsLeft = int(argv[1])
   growingList = []
   while elsLeft > 1:
     remainingWeight = 100 - sum(growingList)
     growingList.append(random.randrange(0,remainingWeight))
     elsLeft = elsLeft -1
   growingList.append(100- sum(growingList))
   shuffled = random.shuffle(growingList)
   total = float(sum(growingList)) 
   print"\t".join([str(x/total) for x in growingList])
   
