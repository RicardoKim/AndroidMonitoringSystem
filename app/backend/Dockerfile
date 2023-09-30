# Build stage
FROM golang:1.17 AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN go build -o main .

# Run stage
FROM debian:buster-slim

WORKDIR /app

COPY --from=builder /app/main /app/main

EXPOSE 8000

CMD ["./main"]