from chalice import Chalice
import os
import sys
import pymongo
import ast
import json
from bson.json_util import dumps, loads
from bson.objectid import ObjectId

app = Chalice(app_name='dbmodChalice')

#Get Amazon DocumentDB ceredentials from environment variables
username = "sysadmin"
password = "Rosler28"
clusterendpoint = "docdb-2022-02-24-03-13-24.cluster-cajctnqyrb1s.ap-southeast-1.docdb.amazonaws.com"

@app.route('/dummy', methods=['GET'])
def index():
    client = pymongo.MongoClient(clusterendpoint, username=username, password=password, tls='true', tlsCAFile='rds-combined-ca-bundle.pem',retryWrites='false')
    db = client.sample_database
    questions = db['questions']
    #query = {'_id': '621e5e474965549da7004044'}

    questions = db['questions']
    cursor = questions.find( {"_id": ObjectId("621f74b50cfe53954c0dc899")}, {"questionnaire": 1} )
    list_cur = list(cursor)
    thisDict = list_cur[0]
    myNewList = thisDict["questionnaire"]
    json_data = dumps(myNewList)
    print(json_data)

    return json_data

@app.route('/connect', methods=['POST'])
def conn():
    data = app.current_request.raw_body.decode()
#def conn(event, context):
    client = pymongo.MongoClient(clusterendpoint, username=username, password=password, tls='true', tlsCAFile='rds-combined-ca-bundle.pem',retryWrites='false')
    db = client.sample_database
    NEW_DATA=ast.literal_eval(data)
    profiles = db['contacts']
    #Insert data
    profiles.insert_one(NEW_DATA)
    print("Successfully inserted data")
    return data

@app.route('/answer', methods=['POST'])
def conn():
    data = app.current_request.raw_body.decode()
#def conn(event, context):
    client = pymongo.MongoClient(clusterendpoint, username=username, password=password, tls='true', tlsCAFile='rds-combined-ca-bundle.pem',retryWrites='false')
    db = client.sample_database
    NEW_DATA=ast.literal_eval(data)
    profiles = db['answers']
    #Insert data
    profiles.insert_one(NEW_DATA)
    print("Successfully inserted data")
    return data

@app.route('/create', methods=['POST'])
def create():
    data = app.current_request.raw_body.decode()

    client = pymongo.MongoClient(clusterendpoint, username=username, password=password, tls='true', tlsCAFile='rds-combined-ca-bundle.pem',retryWrites='false')
    db = client.sample_database

    NEW_DATA=ast.literal_eval(data)

    new_questionnaire = db['questions']

    #Insert data
    new_questionnaire.insert_one(NEW_DATA)

    myquery = { "questionnaire": "" }
    
    f = open('data.json')
    questions = json.load(f)
    print(questions)
    newvalues = { "$set": { "questionnaire": questions } }
    new_questionnaire.update_one(myquery, newvalues)

    print("Successfully inserted data")
    return data

@app.route('/sendAnswers', methods=['POST'])
def sendAnswers():
    data = app.current_request.raw_body.decode()

    client = pymongo.MongoClient(clusterendpoint, username=username, password=password, tls='true', tlsCAFile='rds-combined-ca-bundle.pem',retryWrites='false')
    db = client.sample_database

    print('data received: ')
    print(data)
    NEW_DATA=ast.literal_eval(data)
    print(NEW_DATA)

    new_answers = db['questions']
    
    counter = 0
    
    text_ = "questionnaire.0.answer"
    for i in NEW_DATA:
        print(i)
        _text = "questionnaire." + str(counter) + ".answer"
        _ans = i
        print(_text)
        print(i)
        new_answers.update_one({"_id": ObjectId("621f74b50cfe53954c0dc899")}, { '$set': {_text : _ans} });
        # new_answers.update_one({"_id": ObjectId("621f74b50cfe53954c0dc899")}, { '$set': {"questionnaire.2.answer" : '2222'} });
        counter += 1;
 
    print("Successfully updated answers")
    return NEW_DATA

@app.route('/calcRes', methods=['GET'])
def calcRes():

    # data = app.current_request.raw_body.decode()

    client = pymongo.MongoClient(clusterendpoint, username=username, password=password, tls='true', tlsCAFile='rds-combined-ca-bundle.pem',retryWrites='false')
    db = client.sample_database
    questions = db['questions']
    #query = {'_id': '621e5e474965549da7004044'}

    questions = db['questions']
    cursor = questions.find_one( {"_id": ObjectId("621fa5541b70a83bb6dc391d")}, {"questionnaire.weights": 1, "_id": 0} )
    print(cursor)
    print(type(cursor))
    list_cur = list(cursor)
    #myNewList = thisDict["questionnaire"]
    #json_data = dumps(list_cur)
    print(cursor["questionnaire"])

    #return json_data
    return cursor["questionnaire"]
