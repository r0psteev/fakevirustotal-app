FROM golang:alpine as builder
WORKDIR /app
COPY . .
RUN go mod tidy
RUN go build -o server  ./cmd/server/main.go

FROM alpine
EXPOSE 8080
WORKDIR /app
COPY --from=builder  /app/server .
CMD ["./server"]