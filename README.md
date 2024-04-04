# course-KG
> generating knowledge graphs from course material

## Installation
Install Docker engine. This should include `docker compose`.

### CUDA
To enable the use of GPU within Docker containers we will need NVIDIA Container Toolkit. 
See [NVIDIA docs](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installing-with-apt) for installation steps.

Run the following at the end to make sure everything is setup correctly:
```shell
docker run --rm --runtime=nvidia --gpus all ubuntu nvidia-smi
```

### Load Transcripts
Using `docker`'s volume mount feature we can provide containers access to folders containing course materials.
Suppose course materials are stored here: `/home/student/course-materials`

Modify the `docker-compose.yml` `x-airflow-common>volumes` as follows:
```yml
volumes:
    - ./airflow/dags:/opt/airflow/dags:rw
    - ...
    - /home/student/course-materials:/opt/course-materials
```

## Development
See `docs/system-design.excalidraw` for information regarding the various services.

```shell
docker compose build
docker compose up -d

# Navigate to http://localhost:3000/ for webclient
# Navigate to http://localhost:8080/ for airflow web interface

docker compose down
```

### kg-api
A FastAPI microservice is used to interface with MongoDB database to retrieve and modify knowledge graphs.
The API can be tested through the OpenAPI swagger docs: http://localhost:8000/docs

### MongoDB
MongoDB is used to store the nodes and edges comprising a knowledge graph.
```shell
docker compose exec -t mongodb mongosh -u root -p pw
> show dbs
...
```

### Ollama
Ollama is used to locally host LLMs such as `gemma` and `mistral`.
```shell
docker compose up -d
docker compose exec ollama bash
ollama pull <model-name>
# ex. ollama pull gemma:7b
```

### Airflow DAGS

To run text-to-KG pipelines we can use Airflow's DAG (Directed Acyclic Graphs) to define a sequence of operations to execute.

#### How to run a DAG
1. Create an Airflow DAG script and put it in the `airflow/dags` folder. See `airflow/dags/test-pipeline.py` for an example.
2. Use `docker compose up -d` to run Airflow-related services (scheduler, webserver, db, etc..)
    1. If there are errors for `airflow-webserver` related to permissions issues, check perms for `airflow/logs`
    2. Probably not the best approach but quick fix: `chmod -R 777 airflow/logs`
3. Wait. If it is the first time the process takes a while to initalize DB.
4. Navigate to [http://localhost:8080/] to access airflow web interface.
    1. Credentials `user:airflow pw:airflow`
5. Find the DAG you're interested in and click the play button to trigger it.
6. To check task logs:
    1. Click on the DAG name within the *DAGs* table.
    2. Click on the *Grid* view.
    3. Click on the square next to a specific task in the table.
    4. Go to *Logs* to see full logs.
    5. Go to *Xcom* to see the output produced from this task.


### text2kg Tests
Using `pytest` allows for the creation of unit tests. The following is an example:
```shell
python -m pytest --log-level=INFO -k summarize -rP
```