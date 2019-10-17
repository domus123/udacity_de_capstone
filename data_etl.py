import pandas as pd 
import configparser 
import boto3
import pyarrow as pa
import pyarrow.parquet as pq
import fastparquet as fp
from s3fs import S3FileSystem

def load_csv(csv_file): 
    """ 
        Load an CSV file into a pandas DF
        params:
            csv_file: string with file name
        return:pandas dataframe
    """ 
    dataframe = pd.read_csv(csv_file)
    #Data Validation when loading 
    assert len(dataframe), f"Error while loading file:{csv_file}! Empty dataframe"
    return dataframe

def data_cleaning(dataframe, drop_nan=False): 
    """
        Basic processing of the files
        params:
            dataframe: pandas dataframe
            drop_nan: boolean for dropping null columns
        return: cleaned dataframe
    """
    dataframe = dataframe.drop_duplicates() 
    #Validating if dataframe has values after dropping duplicates
    assert len(dataframe), f"Empty dataframe after removing duplicated values"
    if (drop_nan) :
        dataframe = dataframe.dropna() 
    #Validating if dataframe is not empty after drop null values
    assert len(dataframe), f"Empty dataframe after removing null values"
    return dataframe

def timestamp_into_date(dataframe):
    """
        Get the dataframe timestamp field and break into day,month and year
        This function will probably be not used
        params: 
            dataframe 
        return : pd_dataframe
    """
    dataframe['date'] = pd.to_datetime(dataframe['timestamp'])
    dataframe['day'] = [ d.day for d in dataframe['date']]
    dataframe['month'] = [d.month for d in dataframe['date']]
    dataframe['year'] = [d.year for d in dataframe['date']]

    #Not necessary keep date
    try :
        dataframe = dataframe.drop(columns=['date'])
    except Exception as e:
        print(f"Exception {e} while dropping column")
    return dataframe

def save_training_data(dataframe, path):
    """ Convert dataframe into pyarrow table and save it on s3 """
    s3 = S3FileSystem()
    table = pa.Table.from_pandas(dataframe)
    print(f"Saving for machine learning team on {path}")
    pq.write_to_dataset(table, root_path=path, filesystem=s3)
    print("OK")


def pipeline(): 
    """
        Will load and handle all the data, passing then step by step.
        Will also handle memory    
    """

    #Read configurations 
    parser = configparser.ConfigParser()
    parser.read('.config')

    #data_paths
    data_path = parser['PATH']['DATA']
    build_path = parser['PATH']['BUILD_DATA']
    weather_path = parser['PATH']['WEATHER_DATA']

    data = load_csv(data_path)
    data = data_cleaning(data)

    building_data = load_csv(build_path)
    building_data = data_cleaning(building_data)

    #Merging both
    #data = data.set_index('building_id').join(building_data.set_index('building_id'))
    print("Merging data and build data ...")
    data = data.merge(building_data, left_on='building_id', right_on='building_id')
    #memory cleaning
    del building_data

    weather_data = load_csv(weather_path)
    weather_data = data_cleaning(weather_data)

    print("Merging data and weather data ...")
    data = data.merge(weather_data, left_on='site_id_x', right_on='site_id')
    del weather_data

    output_machine_learning = parser['PATH']['OUTPUT_PATH']
    save_training_data(data, output_machine_learning)

pipeline()
    




