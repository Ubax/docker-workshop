FROM golang:1.23 AS build-stage
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY *.go ./
RUN CGO_ENABLED=0 GOOS=linux go build -o server

FROM scratch
WORKDIR /
COPY --from=build-stage /app/server /server
ENV MONGODB_URI mongodb://localhost:27017
EXPOSE 5001
ENTRYPOINT ["/server"]