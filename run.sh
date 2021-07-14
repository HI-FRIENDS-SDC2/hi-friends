#rm -rf results resources
snakemake -j8 --use-conda --conda-frontend mamba
snakemake --dag | dot -Tsvg > dag.svg


