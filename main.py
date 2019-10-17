from data_etl import pipeline

if __name__ == '__main__':
    print("Running data pipeline .... " )
    try:
        pipeline()
        print("Completed")
    except:
        print("Error while running pipeline")
    
