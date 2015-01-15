from csv import reader
from pymongo import MongoClient

filename = "twitterSampleData.csv" # change filepath if necessary
reader = reader(open(filename, 'r'))

data = []
titleRow = reader.next()

for row in reader:
    dataDict = {}
    
    for key, value in zip(titleRow, row):
        dataDict[key] = value

    data.append(dataDict)

client = MongoClient()
db = client['twitterData']

posts = db.posts
posts.insert(data)

client.close()
