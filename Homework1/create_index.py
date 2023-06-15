import pandas as pd
import requests 
import sys
import string 

def create_index(cars:str):
    '''Creates a keyword index for keywords appearing in car name. 
       The keywords in a car name are a list of words resulting from tokenizing the car name by punctuation characters and white spaces. 
       For each unique keyword in the car names, the index stores a list of IDs of cars whose name contains the keyword. 
    '''
    df = pd.read_csv(cars,index_col="car_ID")
    df.sort_values(by="CarName",inplace=True)
    
    #token set keeps track of unique token
    #Each unique token is a key in index whose value is a list of carIDs in which it appears.
    tokens,index = set(),{}
    for carid,name in zip(df.index,df['CarName']):
        
        #Creating tokens out of car name
        translator = str.maketrans(string.punctuation,' '*len(string.punctuation))
        name = name.translate(translator).lower().split()
        tokens.update(name)
        for token in name:
            if token not in index:
                index[token] = []    
            index[token].append(carid)   
    
    url = "https://durable-fact-274310-default-rtdb.firebaseio.com/"
    # Putting the index on Firebase
    response = requests.put(url+"index.json",json=index)

if __name__=="__main__":
    create_index(sys.argv[1])