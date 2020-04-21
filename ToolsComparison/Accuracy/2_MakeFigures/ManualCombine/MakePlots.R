library(gplots)
library(RColorBrewer)

CorrHM = function(flipped,outName){png(paste(outName,"CorrHM.png", sep = "-"), 4000,4000)
     heatmap.2(as.matrix(flipped), trace = "none", dendrogram = "none", Rowv = FALSE, Colv = FALSE, breaks = c(-.5,-.01,.25,.5,.75,.8,.9,1.0),
               cexRow = 2, cexCol = 2, col = c("#FCBBA1",brewer.pal(9,"Blues")[1:6]), cellnote = trunc(flipped*100)/100, notecex = 7, notecol = "black", margins = c(15,25), 
               main = "Correlation between Prediction and Actual Preportions", sepcol = "black", density.info = "none",rowsep = c(4,9,14,19,24))
     dev.off()}
ErrorHM = function(flipped,outName){ png(paste(outName,"ErrorHM.png", sep = "-"), 4000,4000)
     heatmap.2(as.matrix(flipped), trace = "none", dendrogram = "none", Rowv = FALSE, Colv = FALSE, notecex = 7, rowsep = c(4,9,14,19,24),
               cexRow = 2, cexCol = 2, col = brewer.pal(9,"Reds")[1:6], cellnote = trunc(flipped*100)/100, notecol = "black", margins = c(15,25),
               main = "Errors By Tool, Reference, and Cell Type", sepcol = "black", breaks = c(0.0,.05,.1,.15,.2,.25,.3), key.title = "Error")}


AllCorrs = read.table("AllCorrs.tsv", header = TRUE, row.names = 1, sep = "\t")
AllErrors = read.table("AllErrors.tsv", header = TRUE, row.names = 1, sep = "\t")

CorrHM(AllCorrs, "AllCorrs.png")
ErrorHM(AllErrors, "AllErrors.png")
