#rm -rf results resources
snakemake -jall --use-conda --conda-frontend mamba
snakemake --dag | dot -Tsvg > dag.svg


