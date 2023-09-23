import pymongo

# Connection string for the replica set
connection_string = "mongodb://root:1234@localhost:27017,localhost:27018,localhost:27019/?replicaSet=rs0"

# Create a MongoDB client
client = pymongo.MongoClient(connection_string)

# Test the connection
try:
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
    print("Connected to the MongoDB replica set!")
except pymongo.errors.ConnectionFailure as e:
    print("Could not connect to the MongoDB replica set: %s" % e)
