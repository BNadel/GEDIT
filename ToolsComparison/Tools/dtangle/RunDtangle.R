library(dtangle)
args = commandArgs(TRUE)
getCoreFileName = function(LongFName){
   parts = strsplit(LongFName,"/")[[1]]
   end = parts[length(parts)]
   core = strsplit(end,"\\.")[[1]][1]
   return(core)}

mixMat = read.table(args[1], header = TRUE, row.names =1, sep = "\t")
refMat = read.table(args[2], header = TRUE, row.names =1, sep = "\t")
SharedNames = intersect(row.names(mixMat),row.names(refMat))
readyMix = log2(1+mixMat[SharedNames,])
readyRef = log2(1+refMat[SharedNames,])
outMat = dtangle(t(readyMix), references = t(readyRef))
mixString = getCoreFileName(args[1])
refString = getCoreFileName(args[2])
outFName = args[3]
print(outFName)
write.table(outMat[[1]], file = outFName, sep = "\t", quote = FALSE)
