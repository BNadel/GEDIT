library(ggplot2)
library(RColorBrewer)

Hoek = read.table("UnrolledHoek.tsv", header = TRUE, sep = "\t")
Ascites = read.table("UnrolledAscitesDouble.tsv", header = TRUE, sep = "\t")
CellMixtures = read.table("UnrolledCellMix.tsv", header = TRUE, sep = "\t")

png("HoekHM.png",1000,1000)

ggplot(Hoek[order(Hoek$Cell.Type),], aes(fill=Cell.Type, y=Value, x=Sample)) + geom_bar(position = position_stack(), stat = "identity") + scale_fill_manual(values = c('#084594','#7a0177','#33a02c','#fb9a99','#bdbdbd')) + theme(legend.text = element_text(size = 20)) + theme(legend.position="left")

dev.off()
png("CellMixturesHM.png",1000,1000)

ggplot(CellMixtures[order(CellMixtures$Cell.Type),], aes(fill=Cell.Type, y=Value, x=Sample)) + geom_bar(position = position_stack(), stat = "identity") + scale_fill_manual(values = c('#084594','#fbb4ae','#e41a1c','#7a0177','#b2df8a','#33a02c','#fb9a99','#fdbf6f')) + theme(legend.text = element_text(size = 12)) + theme(legend.position="left")

dev.off()
png("AscitesHM.png",1000,1000)

ggplot(Ascites[order(Ascites$Cell.Type),], aes(fill=Cell.Type, y=Value, x=Sample)) + geom_bar(position = position_stack(), stat = "identity") + scale_fill_manual(values = c('#084594','#d95f02','#7a0177','#b2df8a','#33a02c','#fb9a99','#bdbdbd')) + theme(legend.text = element_text(size = 12)) + theme(legend.position="left") + xlab("")

dev.off()
