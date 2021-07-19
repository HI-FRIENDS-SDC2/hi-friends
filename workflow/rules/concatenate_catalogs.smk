
rule concatenate_catalogs:
    input:
        expand("results/sofia/{idx}/subcube_{idx}_final_catalog.csv", idx=IDX, allow_missing=True)
        #aggregate_input
    output:
        "results/catalog_w_duplicates.csv"
    log:
        "results/logs/concatenate/concatenate_catalogs.log"
    run:
        shell("awk 'FNR>1' {input} > {output} | tee {log}")
	shell("sed -i '1i id_subcube ra dec hi_size line_flux_integral central_freq pa i w20 rms subcube' {output}")


rule eliminate_duplicates:
    input:
        "results/catalog_w_duplicates.csv"
    output:
        "results/final_catalog.csv"
    conda:
        "../envs/xmatch_catalogs.yml"
    log:
        "results/logs/concatenate/eliminate_duplicates.log"
    shell:
        "python workflow/scripts/eliminate_duplicates.py -i {input} -o {output} | tee {log}"

