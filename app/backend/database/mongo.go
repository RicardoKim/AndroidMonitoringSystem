package database

import (
	"context"
	"encoding/json"
	"log"
	"sync"

	"github.com/gorilla/websocket"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

var wsMutex sync.Mutex

func writeToSocket(conn *websocket.Conn, message []byte) {
	wsMutex.Lock()
	defer wsMutex.Unlock()

	err := conn.WriteMessage(websocket.TextMessage, message)
	if err != nil {
		log.Println("Error writing WebSocket message:", err)
	}
}

func WatchAndroidResourceMonitoringCollection(ctx context.Context, conn *websocket.Conn) {
	client, err := mongo.Connect(ctx, options.Client().ApplyURI("mongodb://root:1234@mongodb1:27017,mongodb2:27018,mongodb3:27019/?replicaSet=rs0"))
	if err != nil {
		log.Println(err)
		return
	}
	defer client.Disconnect(ctx)

	database := client.Database("AndroidLogDataMart")
	collection := database.Collection("AndroidResourceMonitoring")

	log.Println("Setting up the Change Stream...")
	pipeline := mongo.Pipeline{}
	changeStream, err := collection.Watch(ctx, pipeline)
	if err != nil {
		log.Println(err)
		return
	}
	defer changeStream.Close(ctx)
	log.Println(changeStream)
	log.Println("Listening to the Change Stream...")

	for changeStream.Next(ctx) {
		changeDoc := bson.M{}
		if err := changeStream.Decode(&changeDoc); err != nil {
			log.Println(err)
			return
		}
		wrappedDoc := map[string]interface{}{
			"process_info": changeDoc,
		}
		changeJSON, err := json.Marshal(wrappedDoc)
		if err != nil {
			log.Println(err)
			return
		}

		writeToSocket(conn, changeJSON)
	}
}

func WatchAndroidMemoryMonitoringCollection(ctx context.Context, conn *websocket.Conn) {
	client, err := mongo.Connect(ctx, options.Client().ApplyURI("mongodb://root:1234@mongodb1:27017,mongodb2:27018,mongodb3:27019/?replicaSet=rs0"))
	if err != nil {
		log.Println(err)
		return
	}
	defer client.Disconnect(ctx)

	database := client.Database("AndroidLogDataMart")
	collection := database.Collection("AndroidMemoryMonitoring")

	log.Println("Setting up the Change Stream...")
	pipeline := mongo.Pipeline{}
	changeStream, err := collection.Watch(ctx, pipeline)
	if err != nil {
		log.Println(err)
		return
	}
	defer changeStream.Close(ctx)
	log.Println(changeStream)
	log.Println("Listening to the Change Stream...")

	for changeStream.Next(ctx) {
		changeDoc := bson.M{}
		if err := changeStream.Decode(&changeDoc); err != nil {
			log.Println(err)
			return
		}
		wrappedDoc := map[string]interface{}{
			"memory_info": changeDoc,
		}
		changeJSON, err := json.Marshal(wrappedDoc)
		if err != nil {
			log.Println(err)
			return
		}

		writeToSocket(conn, changeJSON)
	}
}
