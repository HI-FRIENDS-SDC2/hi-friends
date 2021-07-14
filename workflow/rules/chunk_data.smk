rule define_chunks:
    input:
    output:
        "results/coord_subcubes.csv"
    conda:
        "../envs/chunk_data.yml"
    params:
        incube = config['incube'],
        grid_plot = config['grid_plot']
    shell:
        "python workflow/scripts/define_chunks.py -d {params.incube} -g {params.grid_plot}"


rule split_subcube:
    input:
        "results/coord_subcubes.csv"
    output:
        "results/subcubes/subcube_{idx}.fits"
    log:
        "results/logs/split_subcube/subcube_{idx}.log"
    threads:
        config['threads']
    conda:
        "../envs/chunk_data.yml"
    params:
        incube = config['incube'],
        coord_file = config['coord_file']
    shell:
        "python workflow/scripts/split_subcube.py -d {params.incube} -c {params.coord_file} -i {wildcards.idx} | tee {log}"
