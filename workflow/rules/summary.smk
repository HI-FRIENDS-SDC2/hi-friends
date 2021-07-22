rule rulegraph:
    input:
        "results/catalogs/final_catalog.csv"
    output:
        "summary/rulegraph.svg"
    log:
        "results/logs/summary/rulegraph.log"
    conda:
        "../envs/snakemake.yml"
    shell:
        "snakemake --rulegraph | dot -Tsvg > {output}"

rule dag:
    input:
        "results/catalogs/final_catalog.csv"
    output:
        "summary/dag.svg"
    log:
        "results/logs/summary/dag.log"
    conda:
        "../envs/snakemake.yml"
    shell:
        "snakemake --dag | dot -Tsvg > {output}"

