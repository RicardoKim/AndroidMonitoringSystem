package handlers

import (
	"context"
	"log"
	"net/http"

	"github.com/RicardoKim/AndroidMonitoringSystem.com/AndroidMonitoringSystem/database"
	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

func watchCollection(ctx context.Context, conn *websocket.Conn) {
	changes, err := database.WatchCollection(ctx)
	if err != nil {
		log.Println("Error watching collection:", err)
		return
	}

	for _, change := range changes {
		err = conn.WriteMessage(websocket.TextMessage, change)
		if err != nil {
			log.Println("Error writing WebSocket message:", err)
			return
		}
		log.Println("Change document sent via WebSocket:", string(change))
	}
}
