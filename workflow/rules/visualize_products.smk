
rule visualize:
    input:
        "results/catalogs/final_catalog.csv"
    output:
        "results/plots/output_params_distribution.png"
    log:
        "results/logs/visualize/visualize.log",
        # optional path to the processed notebook
        notebook="results/notebooks/sdc2_hi-friends.ipynb"
    conda:
        "../envs/analysis.yml"
    notebook:
        "../notebooks/sdc2_hi-friends.ipynb"
