## Commands

- `go mod download` - Download dependencies
- `go run main.go` - Start the server

## Environment variables

- `PORT` - The port the service will listen on. Default is `5001`.
- `MONGODB_URI`
- `DB_NAME`

## API

### `GET /report`

Get a list of reports. This endpoint fetches data from the mongo database and returns it as JSON.