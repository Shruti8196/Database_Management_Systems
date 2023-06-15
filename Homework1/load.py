import pandas as pd
import requests
import sys

def get_df(cars:str):
    df = pd.read_csv(cars,index_col="car_ID")
    df.insert(0,column='car_ID',value=df.index)
    return df

def load_data(cars:str):
    '''Takes the CSV file cars.csv and loads it to Firebase real time database. Loads the entire data set to Firebase. 
    Every car is stored as a JSON object in Firebase. Each Car is represented by its Car ID.'''
    df = get_df(cars)
    url = "https://durable-fact-274310-default-rtdb.firebaseio.com/"
    response = requests.put(url + "cars.json",json=df.to_dict(orient='index'))
    print(response)
    return df

if __name__=="__main__":
    load_data(sys.argv[1])
    