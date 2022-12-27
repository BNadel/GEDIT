#!/usr/bin/Rscript
args = commandArgs(TRUE)

library(gplots)
library(RColorBrewer)

predictions = read.table(args[1], header = TRUE, row.names = 1, sep = "\t")
numSamples = dim(predictions)[1]
numCTs = dim(predictions)[2]
rowClust = FALSE
colClust = FALSE

pdf(file = paste(args[1],".pdf", sep = ""), width = .5*numSamples + 5, height = .4*numCTs + 7)

heatmap.2(as.matrix(predictions), Rowv = rowClust, Colv = colClust, trace = "none", col = brewer.pal(9, "Oranges"), margins = c(30,30), colsep = 0:dim(predictions)[2], rowsep = 0:dim(predictions)[1],cellnote = round(predictions,2),notecol = "black", key = FALSE, lhei = c(.5,4), lwid = c(.5,4), main = "Predicted Sample Composition", dendrogram = "none")
dev.off()

png(filename = paste(args[1],".png", sep = ""), width = 50 * numSamples +250 , height = 60 * numCTs +350)

heatmap.2(as.matrix(predictions), Colv = rowClust, Rowv = colClust, trace = "none",
col = brewer.pal(9, "Oranges"), margins = c(20,20),
colsep = 0:dim(predictions)[2], rowsep = 0:dim(predictions)[1],cellnote = round(predictions,2),notecol = "black",
key = FALSE, lhei = c(.5,4), lwid = c(.5,4),
main = "Predicted Sample Composition", dendrogram = "none")

dev.off()
