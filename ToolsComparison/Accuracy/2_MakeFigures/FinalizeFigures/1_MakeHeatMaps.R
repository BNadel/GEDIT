library(RColorBrewer)
library(gplots)

GenErrorMap = function(outName, flipped){
  png(paste(outName,"ErrorHM.png", sep = "-"), 1600,1600)
  heatmap.2(as.matrix(flipped), trace = "none", dendrogram = "none", Rowv = FALSE, Colv = FALSE, 
  cexRow = 2.6, notecex= 2.5, cexCol = 2.8, col = brewer.pal(9,"Reds")[1:6], cellnote = round(flipped,2), notecol = "black", margins = c(20,28),
  main = "Errors By Tool, Reference, and Cell Type", rowsep = c(5,10,15,20,25), sepcol = "black", breaks = c(0.0,.05,.1,.15,.2,.25,.3), key.title = "", key.ylab = "", key.xlab = "")
  dev.off()}

GenCorrMap = function(outName, flipped){
  png(paste(outName,"CorrHM.png", sep = "-"), 1600,1600)
  heatmap.2(as.matrix(flipped), trace = "none", dendrogram = "none", Rowv = FALSE, Colv = FALSE, breaks = c(.4,.5, .6,.7,.8,.9,1.0),
  cexRow = 2.6, notecex = 2.5, cexCol = 2.8, col = brewer.pal(9,"Blues")[1:6], cellnote = round(flipped,2), notecol = "black", margins = c(20,28), 
  main = "Correlation between Prediction and Actual Preportions", rowsep = c(5,10,15,20,25), sepcol = "black", key.title = "", key.ylab = "", key.xlab = "")
  dev.off()}



AscitesError = read.table("Ascites-Error.tsv", header = TRUE, row.names = 1, sep = "\t")
AscitesCorr = read.table("Ascites-Corrs.tsv", header = TRUE, row.names = 1, sep = "\t")

CellMixError = read.table("CellMix-Error.tsv", header = TRUE, row.names = 1, sep = "\t")
CellMixCorr = read.table("CellMix-Corrs.tsv", header = TRUE, row.names = 1, sep = "\t")

HoekError = read.table("Hoek-Error.tsv", header = TRUE, row.names = 1, sep = "\t")
HoekCorr = read.table("Hoek-Corrs.tsv", header = TRUE, row.names = 1, sep = "\t")


names(AscitesError) = c("All Predictions", "B Cells", "Dendritic", "Mono/Macro","Neutrophils", "NK", "T Cells")
names(AscitesCorr) = c("All Predictions", "B Cells", "Dendritic", "Mono/Macro","Neutrophils", "NK", "T Cells")

names(CellMixError) = c("All Predictions", "B Cells", "CD4 T Cells", "CD8 T Cells", "Monocytes", "Neutrophils", "NK")
names(CellMixCorr) = c("All Predictions", "B Cells", "CD4 T Cells", "CD8 T Cells", "Monocytes", "Neutrophils", "NK")

names(HoekError) = c("All Predictions", "B Cells", "Monocytes", "NK", "T Cells") 
names(HoekCorr) = c("All Predictions", "B Cells", "Monocytes", "NK", "T Cells") 

GenErrorMap("Ascites-Error.tsv", AscitesError)
GenErrorMap("CellMix-Error.tsv", CellMixError)
GenErrorMap("Hoek-Error.tsv", HoekError)

GenCorrMap("Ascites-Corrs.tsv", AscitesCorr)
GenCorrMap("CellMix-Corrs.tsv", CellMixCorr)
GenCorrMap("Hoek-Corrs.tsv",HoekCorr)
