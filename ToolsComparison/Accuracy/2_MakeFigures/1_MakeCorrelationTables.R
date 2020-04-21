library(RColorBrewer)
library(gplots)

MakeTable1Tool = function(toolName,DataMatrix){
    justTool = DataMatrix[DataMatrix$Tool == toolName,]
    ctNames = names(which(table(justTool[,2]) > 0))
    corMat = data.frame(c("AllCells",ctNames))
    corMat[,2] = cor(justTool[,4],justTool[,5])
        
    names(corMat) = c("RefMat",toolName)
    for (i in 1:length(ctNames)){
  	  relData = justTool[justTool$CellType==ctNames[i],]
          corMat[i+1,2] = cor(relData[,4],relData[,5])}
return(corMat)}


MakeTableAllTools = function(AllPredictions){
   toolList = names(table(AllPredictions[,1]))
   outMat = MakeTable1Tool(toolList[1],AllPredictions)
   for (i in 2:length(toolList)){
	    nextMat = MakeTable1Tool(toolList[i],AllPredictions)
   outMat = merge(outMat,nextMat, by="RefMat", all = T)}
return(outMat)}

DoCorrs = function(fname, outName){
  outName = paste("CorrelationTables",outName,sep="/")
  print(outName)
  Data = read.table(fname, header = TRUE, sep = "\t")
  Corrs = MakeTableAllTools(Data)
  row.names(Corrs) = Corrs[,1]
  Corrs = Corrs[,2:dim(Corrs)[[2]]]
  flipped = as.data.frame(t(Corrs))
  names(flipped) = row.names(Corrs)
  row.names(flipped) = names(Corrs)
  write.table(flipped, paste(outName,"Corrs.tsv", sep = "-"), sep = "\t", quote =FALSE, row.names = TRUE)
  print(outName)
  png(paste(outName,"CorrHM.png", sep = "-"), 1000,1000)
  heatmap.2(as.matrix(flipped), trace = "none", dendrogram = "none", Rowv = FALSE, Colv = FALSE, breaks = c(.4,.5, .6,.7,.8,.9,1.0),
  cexRow = 2, cexCol = 2, col = brewer.pal(9,"Blues")[1:6], cellnote = round(flipped,2), notecol = "black", margins = c(15,25), 
  main = "Correlation between Prediction and Actual Preportions", rowsep = c(4,8,12,16,20), sepcol = "black", density.info = "none")
  dev.off()}

DoCorrs("UnrolledCellMix.tsv", "CellMix")
DoCorrs("UnrolledBothTCellMix.tsv", "CellMixT_Subtypes")
DoCorrs("UnrolledHoek.tsv", "Hoek")
DoCorrs("UnrolledAscites.tsv", "Ascites")
DoCorrs("UnrolledCombined.tsv", "Combined")
