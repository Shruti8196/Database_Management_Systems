import requests
import sys

def search_price(p1:str,p2:str):
    '''Takes a range of price (in two arguments p1,p2) and outputs IDs of cars in the range (inclusive). 
       If no cars are in the specified price range, then returns ‘No cars found with the given range’.
    '''
    x = requests.get(f"https://durable-fact-274310-default-rtdb.firebaseio.com/cars.json?orderBy=\"price\"&startAt={p1}&endAt={p2}")
    if len(x.json())==0:
        print("No cars found with the given range")
    else:
        print("IDs for the car price range are:\n",sorted([int(i) for i in x.json().keys()]))
        
if __name__=="__main__":
    search_price(sys.argv[1],sys.argv[2])