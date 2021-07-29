import os
import sys

import subprocess as sp
from tempfile import TemporaryDirectory
import shutil
from pathlib import Path, PurePosixPath

sys.path.insert(0, os.path.dirname(__file__))

import common


def test_sofia2cat():

    with TemporaryDirectory() as tmpdir:
        workdir = Path(tmpdir) / "workdir"
        data_path = PurePosixPath(".tests/unit/sofia2cat/data")
        expected_path = PurePosixPath(".tests/unit/sofia2cat/expected")
        config_path = PurePosixPath(".tests/unit/config")
        workflow_path = PurePosixPath(".tests/unit/workflow")

        # Copy data to the temporary workdir.
        shutil.copytree(data_path, workdir)
        shutil.copytree(config_path, workdir / "config")
        shutil.copytree(workflow_path, workdir / "workflow")

        # dbg
        print("results/sofia/0/subcube_0_final_catalog.csv", file=sys.stderr)

        # Run the test job.
        sp.check_output([
            "python",
            "-m",
            "snakemake", 
            "results/sofia/0/subcube_0_final_catalog.csv",
            #"-F", 
            "-j1",
            "--keep-target-files",
            "--use-conda",
            "--conda-frontend","mamba",
            "--config","incube='interim/sofia_test_datacube.fits'",
            "subcube_id=[0]",
            "num_subcubes=16",
            "pixel_overlap=0",
    
            "--use-conda",
            "--directory",
            workdir,
        ])

        # Check the output byte by byte using cmp.
        # To modify this behavior, you can inherit from common.OutputChecker in here
        # and overwrite the method `compare_files(generated_file, expected_file), 
        # also see common.py.
        common.OutputChecker(data_path, expected_path, workdir).check()
