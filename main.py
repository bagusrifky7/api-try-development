# import package
from fastapi import FastAPI, HTTPException, Header
import pandas as pd

password = 'secret123'

# Create app for fastapi
app = FastAPI()

# create endpoint

@app.get('/')
def getHome():
    return {
        'message' : 'This is home section'
    }

@app.get('/data')
def getData():
    # load data to pandas
    df = pd.read_csv('data.csv')

    # change from csv to json
    return df.to_dict(orient='records')

@app.get('/data/{name}')
def getDataByName(name: str):
    # load data to pandas
    df = pd.read_csv('data.csv')

    # store to variable
    result = df[df['name'] == name]
    
    if len(result) > 0:
        # change from csv to json
        return result.to_dict(orient = 'records')
    else:
        raise HTTPException(status_code = 404, detail = 'data ' + name + ' not found')
    
@app.delete('/data/{name}')
def deleteDataByName(name: str, api_key: str = Header(None)):
    #check authetication
    if api_key != None and api_key == password:
        # load data to pandas
        df = pd.read_csv('data.csv')

        # store in variable result
        result = df[~(df['name'] == name)]

        # replace current csv
        result.to_csv('data.csv', index = False)

        # change from csv to json
        return result.to_dict(orient = 'records')
    else:
        raise HTTPException(status_code = 403, detail = 'Invalid password')


