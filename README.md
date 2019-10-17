# Udacity capstone

# Project description 
* We have a database of energy efficience given by https://www.kaggle.com/c/ashrae-energy-prediction/data . We want to make it possible for our team of Machine Learning Engineering to run tests and build models and enther Kaggle competition.
* The data has more then 20mi rows and consist in the following files 

## Project Files

  The project contain a few files, description bellow: 
  
  * Dataexploratory.ipynb: Python notebook used for exploring the data and trying to find patterns, cleaning and joining
  * Loading_from_s3_debug: Python notebook used for debuging the s3 write part.
  * data_etl.py: Python pipeline and modules are all here
  * main.py: main function to be runned 
  * requirements.txt: python requirements


## Data Files 

##### train.csv 
* building_id - Foreign key for the building metadata.
* meter - The meter id code. Read as {0: electricity, 1: chilledwater, 2: steam, 3: hotwater}. Not every building has all meter types.
* timestamp - When the measurement was taken
* meter_reading - The target variable. Energy consumption in kWh (or equivalent). Note that this is real data with measurement error, which we expect will impose a baseline level of modeling error.

##### building_meta.csv 
* site_id - Foreign key for the weather files.
* building_id - Foreign key for training.csv
* primary_use - Indicator of the primary category of activities for the building based on EnergyStar property type definitions
* square_feet - Gross floor area of the building
* year_built - Year building was opened
* floor_count - Number of floors of the building

##### weather_[train/test].csv 
 Weather data from a meteorological station as close as possible to the site.
* site_id
* air_temperature - Degrees Celsius
* cloud_coverage - Portion of the sky covered in clouds, in oktas
* dew_temperature - Degrees Celsius
* precip_depth_1_hr - Millimeters
* sea_level_pressure - Millibar/hectopascals
* wind_direction - Compass direction (0-360)
* wind_speed - Meters per second

### Projects steps
The project was done in a few steps: 
1. Scope 
2. Data exploration (in the notebook Data exploratory.ipynb) 
3. Defining our data model
4. Developing and running the ETL

### Tools 
* We decided to go with Pandas for loading and processing the data, since our files weren't considered big data and Spark would be a overkill
* We decided to save in parquet format to save space in S3.

### Writeups 
* How to scale the project to 100x data: We would have to have a cluster architecture with Spark for processing that much data, since pandas can hold low volume of data (compare to spark)
* Pipeline running on 7AM: We would have to have an scheduler, beeing Airflow an possible solution
* The database needed to be accesed by 100+ peoples: We havent use database in this solution, but, we saved the file as parquet in order to speed up and reduce the memory used, beeing faster for multiple HTTP GET request on S3.

### Data quality checks 

##### We tested the data for quality in 3 steps, for all the data that we have, meaning that our data is checked 9 times before saving, and not passing this, would cause an error and stop the data flow.

### Final data schema
In the starting phase, we have a fact table with two dimensions table. Since our team wants to run machine learning model, they need to research and experiment with all the fields, in the end we ended up with the following datas :
```
'meter', 'timestamp_x', 'meter_reading', 'site_id', 'primary_use',
       'square_feet', 'year_built', 'floor_count', 'timestamp_y',
       'air_temperature', 'cloud_coverage', 'dew_temperature',
       'precip_depth_1_hr', 'sea_level_pressure', 'wind_direction',
       'wind_speed'
```

That can be found in dataexploratory.ipinb

### Considerations 

For running this project, we use s3fs. This use an configuration file with AWS credentials at ~/.aws/credentials
