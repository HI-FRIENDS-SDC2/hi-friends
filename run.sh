#rm -rf results resources
snakemake -j32 --use-conda --conda-frontend mamba --default-resources tmpdir=tmp  --resources bigfile=1

#snakemake -j32 --use-conda --conda-frontend mamba --default-resources tmpdir=tmp  --resources bigfile=1 --edit-notebook results/plots/plot1.png
#snakemake -j1 --use-conda --conda-frontend mamba --default-resources tmpdir=tmp  --resources bigfile=1 --configfile config/verification_config.yaml
snakemake --dag | dot -Tsvg > dag.svg
snakemake --report results/report.html
rm -rf tmp
