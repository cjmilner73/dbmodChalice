from chalice import Chalice
import os
import sys
import pymongo
import ast

app = Chalice(app_name='dbmodChalice')
print(pymongo.__version__)

#Insert sample data
SEED_DATA = [
{ "_id" : 1, "name" : "Tim", "status": "active", "level": 12, "score":202},
{ "_id" : 2, "name" : "Justin", "status": "inactive", "level": 2, "score":9},
{ "_id" : 3, "name" : "Beth", "status": "active", "level": 7, "score":87},
{ "_id" : 4, "name" : "Jesse", "status": "active", "level": 3, "score":27}
]

#Get Amazon DocumentDB ceredentials from environment variables
username = "sysadmin"
password = "Rosler28"
clusterendpoint = "docdb-2022-02-24-03-13-24.cluster-cajctnqyrb1s.ap-southeast-1.docdb.amazonaws.com"

@app.route('/dummy', methods=['GET'])
def index():
    #data = app.current_request.json_body
    client = pymongo.MongoClient(clusterendpoint, username=username, password=password, tls='true', tlsCAFile='rds-combined-ca-bundle.pem',retryWrites='false')
    db = client.sample_database
    profiles = db['profiles']
    query = {'name': 'Jesse'}
    print("Printing query results")
    print(profiles.find_one(query))
    return query

@app.route('/connect', methods=['POST'])
def conn():
    print("Running post code")
    data = app.current_request.raw_body.decode()
#def conn(event, context):
    client = pymongo.MongoClient(clusterendpoint, username=username, password=password, tls='true', tlsCAFile='rds-combined-ca-bundle.pem',retryWrites='false')
    db = client.sample_database
    NEW_DATA=ast.literal_eval(data)
    profiles = db['profiles']
    print("Pring data:")
    print(NEW_DATA)
    print("Pring data type:")
    print(type(NEW_DATA))    
    #Insert data
    profiles.insert_many(SEED_DATA)
    #profiles.insert_one(SEED_DATA)
    print("Successfully inserted data")
    return data
