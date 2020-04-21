library(gplots)
library(RColorBrewer)

CorrHM = function(flipped,outName){png(paste(outName,"CorrHM.png", sep = "-"), 1000,1000)
     heatmap.2(as.matrix(flipped), trace = "none", dendrogram = "none", Rowv = FALSE, Colv = FALSE, breaks = c(.4,.5, .6,.7,.8,.9,1.0),
               cexRow = 2, cexCol = 2, col = brewer.pal(9,"Blues")[1:6], cellnote = round(flipped,2), notecol = "black", margins = c(15,25), 
               main = "Correlation between Prediction and Actual Preportions", rowsep = c(5,10,15,20,25), sepcol = "black", density.info = "none")
     dev.off()}
ErrorHM = function(flipped,outName){ png(paste(outName,"ErrorHM.png", sep = "-"), 1000,1000)
     heatmap.2(as.matrix(flipped), trace = "none", dendrogram = "none", Rowv = FALSE, Colv = FALSE, 
               cexRow = 2, cexCol = 2, col = brewer.pal(9,"Reds")[1:6], cellnote = trunc(flipped*100)/100, notecol = "black", margins = c(15,25),
               main = "Errors By Tool, Reference, and Cell Type", rowsep = c(5,10,15,20,25), sepcol = "black", breaks = c(0.0,.05,.1,.15,.2,.25,.3), key.title = "Error", density.info = "none")}


AllCorrs = read.table("AllCorrs.tsv", header = TRUE, row.names = 1, sep = "\t")
AllErrors = read.table("AllErrors.tsv", header = TRUE, row.names = 1, sep = "\t")

CorrHM(AllCorrs, "AllCorrs.png")
ErrorHM(AllErrors, "AllErrors.png")
