# SDC2 HI-FRIENDS results

## Our solution

For our solution we used this configuration file:

```yaml
# General
threads: 31

# Cube selection
#incube: '/mnt/scratch/sdc2/data/evaluation/sky_eval.fits'
#incube: '/mnt/scratch/sdc2/data/development/sky_dev_v2.fits'
#incube: '/mnt/scratch/sdc2/data/development_large/sky_ldev_v2.fits'
incube: '/mnt/sdc2-datacube/sky_full_v2.fits'

# Splitting
subcube_id: 'all'
coord_file: results/plots/coord_subcubes.csv
grid_plot: results/plots/subcube_grid.png
num_subcubes: 36
pixel_overlap: 40

# Sofia
sofia_param: "config/sofia_12.par"
scfind_threshold: 4.5
reliability_fmin: 5.0
reliability_threshold: 0.5
```

The 36 subcubes were gridded following this pattern:
![Example of subcube grid](figures/subcube_grid.png)

The distribution of sources in the sky was:
![Detected catalog](figures/sky_detected_sources.png)

We detected 22346 sources (once duplicates in the overlapping regions are removed).

This is the distribution of parameters in our catalog (blue), and how does it compare with the truth catalog of the large development cube (in grey), which covers a smaller area and therefore contains fewer sources. Please, note the different binning and the log scale used in some cases.

![Parameters distribution](figures/output_params_distribution.png)

We then filtered the catalog to exclude sources that deviate significantly from the  Wang et al. 2016 ([2016MNRAS.460.2143W](https://ui.adsabs.harvard.edu/abs/2016MNRAS.460.2143W/abstract)) correlation between HI size in kpc ($D_HI$) and HI mass in solar masses ($M_HI$). This is the resulting catalog:

![Filtered by D-M correlation](figures/filtered_sources.png)

These results will be uploaded to Zenodo.

## Score

The solution presented by HI-FRIENDS obtained a total score of 13902.62 points in the challenge. This is the final [leaderboard](https://sdc2.astronomers.skatelescope.org/sdc2-challenge/leaderboard) from the SDC2 website. 

![leaderboard](figures/leaderboard.png)
