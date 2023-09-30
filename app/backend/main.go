package main

import (
	"log"
	"net/http"

	"github.com/RicardoKim/AndroidMonitoringSystem.com/AndroidMonitoringSystem/handlers"
)

func main() {
	handler := http.HandlerFunc(handlers.MainHandler)

	log.Println("Server is starting at http://localhost:8000")
	log.Fatal(http.ListenAndServe(":8000", handler))
}
