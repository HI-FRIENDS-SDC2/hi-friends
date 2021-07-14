rule run_sofia:
    input:
        "results/subcubes/subcube_{idx}.fits"
    output:
        "results/sofia/{idx}/subcube_{idx}_cat.txt"
    log:
        "results/logs/run_sofia/subcube_{idx}.log"
    threads:
        config['threads']
    conda:
        "../envs/process_data.yml"
    params:
        sofia_param = config['sofia_param']
    shell:
        "python workflow/scripts/run_sofia.py --parfile {params.sofia_param} --outname {wildcards.idx} --datacube {input} -r results/sofia"

checkpoint sofia2cat:
    input:
        "results/sofia/{idx}/subcube_{idx}_cat.txt"
    output:
        "results/sofia/{idx}/subcube_{idx}_final_catalog.csv"
    log:
        "results/logs/sofia2cat/subcube_{idx}.log"
    conda:
        "../envs/process_data.yml"
    params:
        sofia_param = config['sofia_param']
    shell:
        "python workflow/scripts/sofia2cat.py --outname {wildcards.idx} -r results/sofia --incatalog {input}"
