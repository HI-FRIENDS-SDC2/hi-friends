rule run_sofia:
    input:
        "interim/subcubes/subcube_{idx}.fits"
    output:
        "results/sofia/{idx}/subcube_{idx}_cat.txt"
    log:
        "results/logs/run_sofia/subcube_{idx}.log"
    threads:
        config['threads']
    conda:
        "../envs/process_data.yml"
    params:
        sofia_param = config['sofia_param'],
        scfind_threshold = config['scfind_threshold'],
        reliability_fmin = config['reliability_fmin'],
        reliability_threshold = config['reliability_threshold']
    shell:
        "python workflow/scripts/run_sofia.py --parfile {params.sofia_param}\
	--outname {wildcards.idx} --datacube {input} -r results/sofia\
        --scfind_threshold {params.scfind_threshold}\
	--reliability_fmin {params.reliability_fmin}\
	--reliability_threshold {params.reliability_threshold}\
        | tee {log}"

rule sofia2cat:
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
        "python workflow/scripts/sofia2cat.py --outname {wildcards.idx} -r results/sofia --incatalog {input} | tee {log}"
