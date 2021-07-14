
rule concatenate_catalogs:
    input:
        expand("results/sofia/{idx}/subcube_{idx}_final_catalog.csv", idx=IDX, allow_missing=True)
        #aggregate_input
    output:
        "results/final_catalog.csv"
    log:
        "results/logs/concatenate/concatenate_catalogs.log"
    shell:
        "cat {input} > {output} | tee {log}"

