# Workflow execution

Please, follow the instructions in section [Workflow installation](installation.md) to make sure you have snakemake available in your path. You may also be working inside one the proposed containers described in the section.

Follow these commands to run the pipeline on a small dataset to verify everything works:
```bash
python run.py --check
```
First, this will create all the conda environments needed for the different stages of the pipeline. Then, they will be executed.

To execute the pipeline on your own dataset, first remove the directories `results` and `interim` if you have created them. You may want to edit `config/config.yml` to define your configuration, including the dataset to process. Run the pipeline with:
```bash
python run.py
```

# Snapshots of what the user will see 

