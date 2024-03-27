# course-KG
generating knowledge graphs from course material

## Development
See `docs/system-design.excalidraw`

```shell
docker compose build
docker compose up -d

# Navigate to http://localhost:3000/ for webclient

docker compose down
```

### MongoDB
```shell
docker compose exec -t mongodb mongosh -u root -p pw
> show dbs
...
```