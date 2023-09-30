package database

import (
	"context"
	"encoding/json"
	"log"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func WatchCollection(ctx context.Context) ([][]byte, error) {
	log.Println("Attempting to connect to MongoDB...")

	client, err := mongo.Connect(ctx, options.Client().ApplyURI("mongodb://root:1234@mongodb1:27017,mongodb2:27018,mongodb3:27019/?replicaSet=rs0"))
	if err != nil {
		return nil, err
	}
	defer client.Disconnect(ctx)

	log.Println("Connected to MongoDB. Accessing 'AndroidLogMart' database and 'AndroidResourceMonitoring' collection.")
	database := client.Database("AndroidLogDataMart")
	collection := database.Collection("AndroidResourceMonitoring")

	log.Println("Setting up the Change Stream...")
	pipeline := mongo.Pipeline{}
	changeStream, err := collection.Watch(ctx, pipeline)
	if err != nil {
		return nil, err
	}
	defer changeStream.Close(ctx)
	log.Println(changeStream)
	log.Println("Listening to the Change Stream...")

	var changes [][]byte

	for changeStream.Next(ctx) {
		changeDoc := bson.M{}
		if err := changeStream.Decode(&changeDoc); err != nil {
			return nil, err
		}

		changeJSON, err := json.Marshal(changeDoc)
		if err != nil {
			return nil, err
		}

		changes = append(changes, changeJSON)
	}

	return changes, nil
}
