from csv import reader
from pymongo import MongoClient

filename = "C:\\Users\\Greg\\Desktop\\Flask Tutorial\\twitterApp\\twitterSampleData.csv"
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
