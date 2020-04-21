library(preprocessCore)

args = commandArgs(TRUE)
UnNormed = read.table(args[1], header = TRUE, row.names =1, sep = "\t")
Normed = as.data.frame(normalize.quantiles(as.matrix(UnNormed)))
row.names(Normed) = row.names(UnNormed)
names(Normed) = names(UnNormed)
print(args[2])
write.table(Normed, file = args[2], sep = "\t", quote = FALSE)
