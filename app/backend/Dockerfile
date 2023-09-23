# app/server/Dockerfile

FROM golang:1.17

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN go build -o main .

EXPOSE 8000

CMD ["./main"]
