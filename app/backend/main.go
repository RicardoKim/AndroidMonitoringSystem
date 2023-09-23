package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/gorilla/websocket"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

func watchCollection(ctx context.Context, conn *websocket.Conn) {
	log.Println("Attempting to connect to MongoDB...")

	client, err := mongo.Connect(ctx, options.Client().ApplyURI("mongodb://root:1234@mongodb1:27017,mongodb2:27018,mongodb3:27019/?replicaSet=rs0"))
	if err != nil {
		log.Fatal("Failed to connect to MongoDB:", err)
	}
	defer client.Disconnect(ctx)

	log.Println("Connected to MongoDB. Accessing 'AndroidLogMart' database and 'AndroidResourceMonitoring' collection.")
	database := client.Database("AndroidLogDataMart")
	collection := database.Collection("AndroidResourceMonitoring")

	log.Println("Setting up the Change Stream...")
	pipeline := mongo.Pipeline{}
	changeStream, err := collection.Watch(ctx, pipeline)
	if err != nil {
		log.Fatal("Error setting up Change Stream:", err)
	}
	defer changeStream.Close(ctx)
	log.Println(changeStream)
	log.Println("Listening to the Change Stream...")
	for changeStream.Next(ctx) {
		log.Println(ctx)
		changeDoc := bson.M{}
		if err := changeStream.Decode(&changeDoc); err != nil {
			log.Fatal("Error decoding change stream:", err)
		}

		changeJSON, err := json.Marshal(changeDoc)
		if err != nil {
			log.Fatal("Error marshalling change document to JSON:", err)
		}

		err = conn.WriteMessage(websocket.TextMessage, changeJSON)
		if err != nil {
			log.Println("Error writing WebSocket message:", err)
			return
		}
		log.Println("Change document sent via WebSocket:", string(changeJSON))
	}
}

func main() {
	handler := http.HandlerFunc(func(rw http.ResponseWriter, req *http.Request) {
		var resp []byte
		if req.URL.Path == "/handler-initial-data" {
			log.Println("Received request for /handler-initial-data")
			resp = []byte(`{"text": "helloWorld"}`)
		} else if req.URL.Path == "/handler" {
			log.Println("Received request for /handler. Upgrading to WebSocket...")
			conn, err := upgrader.Upgrade(rw, req, nil)
			if err != nil {
				log.Println("Error with WebSocket upgrade:", err)
				return
			}

			ctx := context.Background()
			go watchCollection(ctx, conn)
			return
		}

		rw.Header().Set("Content-Type", "application/json")
		rw.Header().Set("Content-Length", fmt.Sprint(len(resp)))
		rw.Write(resp)
	})

	log.Println("Server is starting at http://localhost:8000")
	log.Fatal(http.ListenAndServe(":8000", handler))
}
