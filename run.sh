#rm -rf results resources
snakemake -j10 --use-conda --conda-frontend mamba
snakemake --dag | dot -Tsvg > dag.svg
snakemake --report results/report.html
