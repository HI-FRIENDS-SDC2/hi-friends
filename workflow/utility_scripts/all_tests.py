import os

scfind_threshold = [3.5, 4.0, 4.5]
reliability_fmin = [5.0, 6.0, 7.0]
reliability_threshold = [0.3, 0.4, 0.5]
#scfind_threshold = [3.5, 4.0]
#reliability_fmin = [5.0, 7.0]
#reliability_threshold = [0.3, 0.5]

for scf in scfind_threshold:
    for rf in reliability_fmin:
        for rt in reliability_threshold:
            print(f'scfind_threshold = {scf}')
            print(f'reliability_fmin = {rf}')
            print(f'reliability_threshold = {rt}')
            test_name = f'test_{scf}_{rf}_{rt}'
            os.system(f'mkdir tests/{test_name}')
            command = f"snakemake -j 32 --use-conda --conda-frontend mamba --default-resources tmpdir=tmp  --resources bigfile=1 --config scfind_threshold={scf} reliability_fmin={rf} reliability_threshold={rt}"
            print(command)
            os.system(command)
            os.system(f"mv summary results/sofia results/catalogs tests/{test_name}")


