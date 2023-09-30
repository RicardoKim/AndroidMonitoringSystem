package handlers

import (
	"context"
	"fmt"
	"log"
	"net/http"

	"github.com/RicardoKim/AndroidMonitoringSystem.com/AndroidMonitoringSystem/database"
)

func MainHandler(rw http.ResponseWriter, req *http.Request) {
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

		resource_ctx := context.Background()
		go database.WatchAndroidResourceMonitoringCollection(resource_ctx, conn)
		memory_ctx := context.Background()
		go database.WatchAndroidMemoryMonitoringCollection(memory_ctx, conn)
		return
	}

	rw.Header().Set("Content-Type", "application/json")
	rw.Header().Set("Content-Length", fmt.Sprint(len(resp)))
	rw.Write(resp)
}
