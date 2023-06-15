import requests
import string
import sys
import pandas as pd
import load
# from importlib import reload  # Python 3.4+
# load = reload(load)

def search_car(keyword):
    
    #Cleaning the search keyword
    keyword = keyword.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
   
    #If keyword="honda accord" l=[carIDs having honda,carIDs having accord]
    l = []
    for search_token in keyword.split():
        try:
            l.extend(requests.get(f"https://durable-fact-274310-default-rtdb.firebaseio.com/index.json?orderBy=\"$key\"&equalTo=\"{search_token}\"").json()[search_token])
        except:
            continue
            
    if len(l)==0:
        print("No cars found for the given search")
    else:
        #indexmap maps car_ID to CarName 
        indexnamemap = load.get_df('cars.csv')['CarName'].to_dict()
        # z counts the frequency of times car_ID appeared in list l, if car_ID 41 appeared twice it means it has 2 tokens
        z = pd.DataFrame(pd.Series(l).value_counts())
        z.columns = ["count"]
        for i in z.index:
            z.loc[i,"carName"] = indexnamemap[i]        
        print("IDs of the car are:")
        
        #Sorting results first by the number of keywords, then breaking ties by sorting CarName lexicographically(Ascending Order)
        print(list(z.sort_values(by=['count','carName'],ascending=[False,True]).index))
        
if __name__=="__main__":
    search_car(sys.argv[1])