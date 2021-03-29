# multi-species-PBTK

This project repository is connected to the journal article ‘*A Novel Multi-Species Toxicokinetic Modeling Approach in Support of Chemical Risk Assessment*’ by Mangold-Döring et al. (submitted to ES&T in March 2021). The key element of this repository is the Jupyter Notebook with the model code (`Multi-species-PBTK-model.ipynb`), in which you will find a more detailed description of instructions and its function. <br>
Furthermore, this repository contains:<br>  

`Derive-parameter-distributions.ipynb` : Jupyter notebook to derive statistical underlying parameter distributions <br><br>
`distribution_fitting.py` : Module for fitting the statistical underlying distributions <br><br>
`mySQL_PBTK.py` : Module to load data out of the mySQL database <br><br>
`config_PBTK.ini` : Configuration file for Python-mySQL connector used in mySQL_PBTK.py <br><br>
`pbtk-fishbase.sql` : Database of physiological parameters of freshwater fish found in Canada

## **Dependencies**: (Latest versions tested)
| Package         |         Version |
| :---            |            ---: |
| numpy           |          1.16.2 |
| pandas          |          0.24.2 |
| scipy           |           1.2.1 |
| seaborn         |           0.9.0 |
| progressbar     |             2.5 |
| statsmodels     |           0.9.0 |
