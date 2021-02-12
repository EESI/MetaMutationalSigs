install.packages('BiocManager', repos = 'https://cloud.r-project.org')
BiocManager::install('deconstructSigs' )
BiocManager::install( 'MutationalPatterns' )
BiocManager::install( 'remotes')
BiocManager::install( 'data.table')
BiocManager::install( 'dplyr')
BiocManager::install( 'purrr')
BiocManager::install( 'tidyr')
BiocManager::install( 'furrr')
BiocManager::install( 'Rcpp')
BiocManager::install( 'cowplot')
BiocManager::install( 'NMF')
BiocManager::install( 'ggpubr')
BiocManager::install( 'cli')
BiocManager::install( 'reticulate')
BiocManager::install( 'roxygen2')
# BiocManager::install('BSgenome')
# BiocManager::install('BSgenome.Hsapiens.UCSC.hg19')
# BiocManager::install('BSgenome.Hsapiens.UCSC.hg38')
BiocManager::install('ShixiangWang/sigminer@v1.2.3', dependencies = TRUE)