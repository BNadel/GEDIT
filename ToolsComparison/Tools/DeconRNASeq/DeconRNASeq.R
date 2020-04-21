#!/usr/bin/Rscript
library(DeconRNASeq)

args = commandArgs(TRUE)

mixture = read.table(args[1], header = TRUE, row.names = 1, sep = "\t")
ref = read.table(args[2], header = TRUE, row.names = 1, sep = "\t")
outFile = args[3]

#flipped = as.data.frame(t(mixture))
#names(flipped) = row.names(mixture)
#row.names(flipped) = names(mixture)
#mixture = flipped

predictions = DeconRNASeq(mixture, ref)[[1]]
row.names(predictions) = names(mixture)

write.table(x = predictions, file = outFile, quote = FALSE, sep = ",")
