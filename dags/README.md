# Airflow DAGS

To run text-to-KG pipelines we can use Airflow's DAG (Directed Acyclic Graphs) to define a sequence of operations to execute.

## Usage
1. Create an Airflow DAG script and put it in the `/dags` folder. See `/dags/test-pipeline.py` for an example.
2. Use `docker compose up -d` to run Airflow-related services (scheduler, webserver, db, etc..)
    1. If there are errors for `airflow-webserver` related to permissions issues, check perms for `/logs`
    2. Probably not the best approach but quick fix: `chmod -R 777 ./logs`
3. Wait. If it is the first time the process takes a while to initalize DB.
4. Navigate to [http://localhost:8080/] to access airflow web interface.
    1. Credentials `user:airflow pw:airflow`
5. Find the DAG you're interested in and click the play button to trigger it.
6. To check task logs:
    1. Click on task within the *Recent Tasks*
    2. Click on task instance *Task Id*
    3. Go to *XCom* to see output from task.
    4. Go to *Log* to see full logs.