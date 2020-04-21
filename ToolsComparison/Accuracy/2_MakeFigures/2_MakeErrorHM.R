library(RColorBrewer)
library(gplots)

MakeTable1Tool = function(toolName,DataMatrix){
    justTool = DataMatrix[DataMatrix$Tool == toolName,]
    ctNames = names(which(table(justTool[,2]) > 0))
    corMat = data.frame(c("AllCells",ctNames))
    corMat[,2] = mean(justTool[,6])
    
    names(corMat) = c("RefMat",toolName)
    for (i in 1:length(ctNames)){
  	  relData = justTool[justTool$CellType==ctNames[i],]
    corMat[i+1,2] = mean(relData[,6])}
return(corMat)}


MakeTableAllTools = function(AllPredictions){
   toolList = names(table(AllPredictions[,1]))
   outMat = MakeTable1Tool(toolList[1],AllPredictions)
   for (i in 2:length(toolList)){
	    nextMat = MakeTable1Tool(toolList[i],AllPredictions)
   outMat = merge(outMat,nextMat, by="RefMat", all = T)}
return(outMat)}

DoCorrs = function(fname, outName){
  outName = paste("ErrorTables",outName,sep="/")
  Data = read.table(fname, header = TRUE, sep = "\t")
  Errors = MakeTableAllTools(Data)
  print(Errors)
  row.names(Errors) = Errors[,1]
  Errors = Errors[,2:dim(Errors)[[2]]]
  flipped = as.data.frame(t(Errors))
  names(flipped) = row.names(Errors)
  row.names(flipped) = names(Errors)
  write.table(flipped, paste(outName,"Error.tsv", sep = "-"), sep = "\t", quote =FALSE, row.names = TRUE)

  png(paste(outName,"ErrorHM.png", sep = "-"), 800,800)
  heatmap.2(as.matrix(flipped), trace = "none", dendrogram = "none", Rowv = FALSE, Colv = FALSE, 
  cexRow = 2, cexCol = 2, col = brewer.pal(9,"Reds")[1:6], cellnote = round(flipped,2), notecol = "black", margins = c(15,25),
  main = "Errors By Tool, Reference, and Cell Type", rowsep = c(4,8,12,16,20), sepcol = "black", breaks = c(0.0,.05,.1,.15,.2,.25,.3), key.title = "Error", density.info = "none")
  dev.off()}

DoCorrs("UnrolledCellMix.tsv", "CellMix")
DoCorrs("UnrolledBothTCellMix.tsv", "CellMixTSubtypes")
DoCorrs("UnrolledHoek.tsv", "Hoek")
DoCorrs("UnrolledAscites.tsv", "Ascites")
DoCorrs("UnrolledCombined.tsv", "Combined")
