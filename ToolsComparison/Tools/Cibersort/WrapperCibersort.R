args <- commandArgs(trailingOnly = TRUE)
print(args)

class(args)

n <- length(args)

if ( n < 3){
	print("Please provide two input files and the number of permutations")
	stop("Did not get enough arguments, exiting...")
}

# check whether files exists:
for (i in 1:(n-1)) {
	if(!file.exists(args[i])){
		print("File ",args[i],"does not exist in the current directory")
		stop("No valid file given. Exiting!")	
	}
}


source("CIBERSORT_Modified.R")
CIBERSORT(args[2],args[1],args[3], perm=0)
