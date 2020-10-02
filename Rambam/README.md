# Rambam

This repo contains notebooks that process the Rambam data first released as part of a study by [Armory et al. (2015)](https://doi.org/10.1287/14-SSY153). 

This data is available for download from [SEELab](https://see-center.iem.technion.ac.il/databases/HomeHospital/) and was used by Whitt & Zhang in two papers which are reporoduced in this repo.

* Whitt, Ward, and Xiaopei Zhang. ‘A Data-Driven Model of an Emergency Department’. Operations Research for Health Care 12 (1 March 2017): 1–15. [https://doi.org/10.1016/j.orhc.2016.11.001](https://doi.org/10.1016/j.orhc.2016.11.001).
* Whitt, Ward, and Xiaopei Zhang. ‘Forecasting Arrivals and Occupancy Levels in an Emergency Department’. Operations Research for Health Care 21 (1 June 2019): 1–18. [https://doi.org/10.1016/j.orhc.2019.01.002](https://doi.org/10.1016/j.orhc.2019.01.002).

# Notebooks

## 01. Process MDB

The orginal SEELab files are stored in Microsoft Access format. This notebook uses an open source set of tools to export the information into a more open CSV format.

## 02. Datasets for 2017

This covers section 2 of the paper and focuses on the visits table recreating the datasets described in the 2017 paper.
