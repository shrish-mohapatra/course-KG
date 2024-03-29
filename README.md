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

### CUDA
To enable the use of GPU within Docker containers we will need NVIDIA Container Toolkit. 
See [NVIDIA docs](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installing-with-apt) for installation steps.

Run the following at the end to make sure everything works:
```shell
docker run --rm --runtime=nvidia --gpus all ubuntu nvidia-smi
```