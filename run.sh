#rm -rf results resources
snakemake -j32 --use-conda --conda-frontend mamba --default-resources tmpdir=tmp  --resources bigfile=1 #--edit-notebook results/plots/plot1.png
snakemake --dag | dot -Tsvg > dag.svg
snakemake --report results/report.html
