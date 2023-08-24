# QA with Embeding

This is an attemt to build simple Question Answer Systems for data about real estate property. 


## Setup (After cloning this repo)

Build the docker image with dependencies:

`docker build . -t openai`

Start docker compose with `openia` and `clickhouse` containers:

`U_ID=$UID docker-compose up --remove-orphans`

Observe the succesful start and open another termianal. 
To make sure containers are up execute the `docker ps` in the another terminal:

```
io@io-MacBook:~/projects/openai-qa-python$ docker ps
CONTAINER ID   IMAGE                          COMMAND            CREATED       STATUS         PORTS                                                                                            NAMES
21254e03dc9c   openai                         "bash"             2 hours ago   Up 2 minutes   0.0.0.0:5000->5000/tcp, :::5000->5000/tcp                                                        openai
c20a49fa2f36   clickhouse/clickhouse-server   "/entrypoint.sh"   3 hours ago   Up 2 minutes   0.0.0.0:8123->8123/tcp, :::8123->8123/tcp, 0.0.0.0:9000->9000/tcp, :::9000->9000/tcp, 9009/tcp   clickhouse

```

### Create clickhouse schema and load the data

The file `addess_embeddings_descriptions.csv.gz` contains sample data with `embedings` vectors precomputed for an `address` field.
The sample data must be loaded into clickhouse. The docker compose uses persistent volume to store clickhouse data and data survive the restarts of docker compose.

#### create the schema in clickhouse

Make sure `clickhouse-client` is installed https://clickhouse.com/docs/en/integrations/sql-clients/cli. 
Connect to clickhouse:

`clickhouse-client -u lupi --password lupi -d openai`

If there is no errors this is what should be on the screen:

```
$ clickhouse-client -u lupi --password lupi -d openai 
ClickHouse client version 23.7.4.5 (official build).
Connecting to database openai at localhost:9000 as user lupi.
Connected to ClickHouse server version 23.7.4 revision 54465.

clickhouse :) 
```

Paste the following to create a table:

```sql
CREATE TABLE qa_properties
(
	`address` String,
    `description` String,
    `address_embeddings` Array(Float32)
)
ENGINE = MergeTree
ORDER BY (`address_embeddings`,`address`)
```

Verify the table is created:

```
clickhouse :) show tables

SHOW TABLES

Query id: 9bfd7044-c774-486a-81c4-ce470081080c

┌─name──────────┐
│ qa_properties │
└───────────────┘

1 row in set. Elapsed: 0.006 sec. 

clickhouse :) desc qa_properties

DESCRIBE TABLE qa_properties

Query id: 6db0efd8-9760-4fd4-a562-5b92ef46ad3d

┌─name───────────────┬─type───────────┬─default_type─┬─default_expression─┬─comment─┬─codec_expression─┬─ttl_expression─┐
│ address            │ String         │              │                    │         │                  │                │
│ description        │ String         │              │                    │         │                  │                │
│ address_embeddings │ Array(Float32) │              │                    │         │                  │                │
└────────────────────┴────────────────┴──────────────┴────────────────────┴─────────┴──────────────────┴────────────────┘

3 rows in set. Elapsed: 0.004 sec. 

```


It uses the [Flask](https://flask.palletsprojects.com/en/2.0.x/) web framework.

1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/).

2. Clone this repository.

3. Navigate into the project directory:

   ```bash
   $ cd openai-qa-python
   ```

4. Create a new virtual environment:

   ```bash
   $ python -m venv venv
   $ . venv/bin/activate
   ```

5. Install the requirements:

   ```bash
   $ pip install -r requirements.txt
   ```

6. Make a copy of the example environment variables file:

   ```bash
   $ cp .env.example .env
   ```

7. Add your [API key](https://beta.openai.com/account/api-keys) to the newly created `.env` file.

8. Run the app:

   ```bash
   $ flask run
   ```

You should now be able to access the app at [http://localhost:5000](http://localhost:5000)! For the full context behind this example app, check out the [tutorial](https://beta.openai.com/docs/quickstart).

https://github.com/ClickHouse/laion/blob/main/search.py

