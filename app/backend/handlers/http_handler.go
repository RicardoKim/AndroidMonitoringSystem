package handlers

import (
	"context"
	"fmt"
	"log"
	"net/http"
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

		ctx := context.Background()
		go watchCollection(ctx, conn)
		return
	}

	rw.Header().Set("Content-Type", "application/json")
	rw.Header().Set("Content-Length", fmt.Sprint(len(resp)))
	rw.Write(resp)
}
