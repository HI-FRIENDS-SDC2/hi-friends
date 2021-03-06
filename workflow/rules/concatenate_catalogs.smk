
rule concatenate_catalogs:
    input:
        expand("results/sofia/{idx}/subcube_{idx}_final_catalog.csv", idx=IDX, allow_missing=True)
        #aggregate_input
    output:
        "results/catalogs/catalog_w_duplicates.csv"
    log:
        "results/logs/concatenate/concatenate_catalogs.log"
    run:
        shell("awk 'FNR>1' {input} > {output} | tee {log}")
	shell("sed -i '1i id_subcube ra dec hi_size line_flux_integral central_freq pa i w20 rms subcube' {output}")


rule eliminate_duplicates:
    input:
        "results/catalogs/catalog_w_duplicates.csv"
    output:
        "results/catalogs/unfiltered_catalog.csv"
    conda:
        "../envs/xmatch_catalogs.yml"
    log:
        "results/logs/concatenate/eliminate_duplicates.log"
    shell:
        "python workflow/scripts/eliminate_duplicates.py -i {input} -o {output} | tee {log}"

rule final_catalog:
    input:
        "results/catalogs/unfiltered_catalog.csv"
    output:
        "results/catalogs/final_catalog.csv",
	"results/catalogs/unfiltered_catalog_logMD.csv",
        "results/catalogs/unfiltered_catalog_logMD_filtered.csv"
    conda:
        "../envs/filter_catalog.yml"
    log:
        "results/logs/concatenate/filter_catalog.log"
    shell:
        "python workflow/scripts/filter_catalog.py -i {input} -o {output[0]} | tee {log}"

