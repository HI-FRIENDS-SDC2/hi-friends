
rule visualize:
    input:
        "results/catalogs/final_catalog.csv",
        "results/catalogs/catalog_w_duplicates.csv",
        "results/catalogs/unfiltered_catalog_logMD.csv",
        "results/catalogs/unfiltered_catalog_logMD_filtered.csv",
	"resources/sky_ldev_truthcat_v2.txt",
	config['coord_file']
    output:
        "results/plots/output_params_distribution.png",
	"results/notebooks/sdc2_hi-friends.ipynb",
	"results/plots/sky_detected_sources.png",
	"results/plots/filtered_sources.png"
    log:
        "results/logs/visualize/visualize.log",
        # optional path to the processed notebook
        notebook="results/notebooks/sdc2_hi-friends.ipynb"
    conda:
        "../envs/analysis.yml"
    notebook:
        "../notebooks/sdc2_hi-friends.ipynb"
