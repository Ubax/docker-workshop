## Commands

- `pipenv run python main.py` - Start the server

## Environment variables

- `PORT` - The port the server will listen on. Default is `5000`.
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB` - Connection details for the PostgreSQL database. All are required
- `SERVICE_BASE_URL` - The base URL of the report service

## API

### `GET /report`

Get a list of reports. This endpoint fetches data from the service and returns it as JSON.

### `GET /item`

Get a list of items. This endpoint fetches data from the database and returns it as JSON.

### `POST /item`

Create a new item. This endpoint accepts a JSON object in the request body and saves it to the database.

```json
{
  "name": "Item name",
}
```

### `DELETE /item/<name>`

Delete an item by name. This endpoint removes the item from the database.