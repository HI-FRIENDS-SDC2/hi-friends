rule define_chunks:
    input:
    output:
        "results/coord_subcubes.csv"
    conda:
        "../envs/chunk_data.yml"
    log:
        "results/logs/define_chunks/define_chunks.log"
    params:
        incube = config['incube'],
        grid_plot = config['grid_plot'],
        num_subcubes = config['num_subcubes'],
        pixel_overlap = config['pixel_overlap']
    shell:
        "python workflow/scripts/define_chunks.py -d {params.incube} -g {params.grid_plot} -n {params.num_subcubes} -o {params.pixel_overlap} | tee {log}"

rule split_subcube:
    input:
        "results/coord_subcubes.csv"
    output:
        #temp("results/subcubes/subcube_{idx}.fits")
        "interim/subcubes/subcube_{idx}.fits"
    log:
        "results/logs/split_subcube/subcube_{idx}.log"
    resources:
        bigfile=1
    conda:
        "../envs/chunk_data.yml"
    params:
        incube = config['incube'],
        coord_file = config['coord_file']
    shell:
        "python workflow/scripts/split_subcube.py -d {params.incube} -c {params.coord_file} -i {wildcards.idx} | tee {log}"
