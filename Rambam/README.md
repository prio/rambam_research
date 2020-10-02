# Rambam

This repo contains notebooks that process the Rambam data first released as part of a study by [Armory et al. (2015)](https://doi.org/10.1287/14-SSY153). 

This data is available for download from [SEELab](https://see-center.iem.technion.ac.il/databases/HomeHospital/) and was used by Whitt & Zhang in two papers which are reproduced in this repo.

* Whitt, Ward, and Xiaopei Zhang. "A Data-Driven Model of an Emergency Department". Operations Research for Health Care 12 (1 March 2017): 1–15. [https://doi.org/10.1016/j.orhc.2016.11.001](https://doi.org/10.1016/j.orhc.2016.11.001).
* Whitt, Ward, and Xiaopei Zhang. "Forecasting Arrivals and Occupancy Levels in an Emergency Department". Operations Research for Health Care 21 (1 June 2019): 1–18. [https://doi.org/10.1016/j.orhc.2019.01.002](https://doi.org/10.1016/j.orhc.2019.01.002).

## Notebooks

All notebooks can be viewed directly on Github. The notebooks can also be executed and edited using [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/prio/research/main).

### [01. Process MDB](https://github.com/prio/research/blob/main/Rambam/notebooks/01.%20Process%20MDB.ipynb)

The original SEELab files are stored in Microsoft Access format. This notebook uses an open source set of tools to export the information into a more open CSV and Sqlite formats.

The Sqlite format also contains the metadata contained in the original data dictionaries to make queries and exploration easier. An example of how to query the database [sql](/../../../blob/main/Rambam/notebooks/sql.ipynb) is also provided.


### [02. Datasets for 2017](https://github.com/prio/research/blob/main/Rambam/notebooks/02.%20Datasets%20for%202017.ipynb)

This covers section 2 of the paper and focuses on the visits table recreating the datasets described in the 2017 paper. It creates a number of CSV and [parquet](https://parquet.apache.org/) files that are used by subsequent notebooks.

### [03. Section 3 - The ED arrival process](https://github.com/prio/research/blob/main/Rambam/notebooks/03.%20Section%203%20-%20The%20ED%20arrival%20process.ipynb)

This notebook roughly corresponds to Section 3 of the 2017 paper.

### [Section 4 Length of stay](https://github.com/prio/research/blob/main/Rambam/notebooks/Section%204%20Length%20of%20stay.ipynb)

This notebook roughly corresponds to Section 4 of the 2017 paper.

### Miscellaneous

* [Presentation](https://github.com/prio/research/blob/main/Rambam/notebooks/Presentation.ipynb) Some of my rough note
* [Simulation](https://github.com/prio/research/blob/main/Rambam/simulation/simulation.py) a simple simulation of a $G_t/GI/\infty$ queue model based on the length of stay data.