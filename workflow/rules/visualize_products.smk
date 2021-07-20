
rule visualize:
    input:
        "results/final_catalog.csv"
    output:
        "results/plots/plot1.png"
    log:
        "results/logs/visualize/visualize.log",
        # optional path to the processed notebook
        notebook="results/notebooks/sdc2_hi-friends.ipynb"
    conda:
        "../envs/analysis.yml"
    notebook:
        "../notebooks/sdc2_hi-friends.ipynb"
