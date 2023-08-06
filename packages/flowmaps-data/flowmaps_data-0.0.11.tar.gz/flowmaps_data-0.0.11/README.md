# flowmaps-data

A tool for downloading COVID-19 and mobility datasets for Spain. 

The database integrates two main types of data:

1. Time dependent population **mobility networks** across Spain (provided by MITMA and INE)

2. Daily reports of **COVID-19** cases in Spain, at different levels of spatial resolution (provided by the CNE and the different Autonomous Communities)

All the data records are associated with a specific area from a geographic layer:

3. **Geographic layers** for Spain, in geojson format, at different levels of spatial resolution.

All the data has been gather from official access points.

More info about the data: https://flowmaps.life.bsc.es/flowboard/data

API: https://flowmaps.life.bsc.es/api

Contact us: https://flowmaps.life.bsc.es/flowboard/contact


## Installation


### Install using pip:

    pip install flowmaps-data


### Install manually:

Create virtual environment:
	
	virtualenv env --python=python3
	source env/bin/activate


Install python dependencies:

	pip3 install -r requirements.txt



## Usage


### Python module

```
from flowmaps_data import geolayer, covid19, dataset, daily_mobility_matrix, population, zone_movements

# Geojson layers
geojson = geolayer('cnig_provincias')

# Consolidated COVID-19 data
df = covid19(ev='ES.covid_cpro')

# Raw health datasets
df = dataset(ev='ES.covid_cpro')

# Origin-destination daily mobility (from MITMA)
df = daily_mobility_matrix(source_layer='cnig_provincias', target_layer='cnig_provincias', date='2020-10-10')

# Daily zone movements (from MITMA)
df = zone_movements(layer='cnig_provincias')

# Population
df = population('cnig_provincias')
```


### Command line utility

```
usage: flowmaps-data [-h] COLLECTION [list describe download]

examples: 

    # Geojson layers
    flowmaps-data layers list
    flowmaps-data layers describe --layer cnig_provincias --provenance
    flowmaps-data layers describe --layer cnig_provincias --plot
    flowmaps-data layers download --layer cnig_provincias

    # Consolidated COVID-19 data
    flowmaps-data covid19 list
    flowmaps-data covid19 describe --ev ES.covid_cpro
    flowmaps-data covid19 download --ev ES.covid_cpro --output-file out.csv --output-type csv

    # Population
    flowmaps-data population list
    flowmaps-data population describe --layer cnig_provincias
    flowmaps-data population download --layer zbs_15 --output-file out.csv

    # Origin-destination daily mobility (from MITMA)
    flowmaps-data daily_mobility_matrix list
    flowmaps-data daily_mobility_matrix describe
    flowmaps-data daily_mobility_matrix download --source-layer cnig_provincias --target-layer cnig_provincias --date 2020-10-10 --output-file out.csv

    # Daily zone movements (from MITMA)
    flowmaps-data zone_movements list
    flowmaps-data zone_movements describe
    flowmaps-data zone_movements download --layer cnig_provincias --output-file out.csv --start-date 2020-10-10 --end-date 2020-10-10

    # Raw health datasets
    flowmaps-data datasets list
    flowmaps-data datasets describe --ev ES.covid_cpro
    flowmaps-data datasets download --ev ES.covid_cpro --output-file out.csv --output-type csv
```
