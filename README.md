# QA with Embeding

This is a simple attemt to build Question Answer Systems for data about real estate property. 
It uses the [Flask](https://flask.palletsprojects.com/en/2.0.x/) web framework. Check out the tutorial or follow the instructions below to get set up.

## Setup

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

### Clickhouse schema

'''sql

CREATE TABLE qa_proerties
(
	`adress` String,
	`_embedding` Array(Float32),
	`image_embedding` Array(Float32),
	`orientation` String DEFAULT exif['Image Orientation'],
	`software` String DEFAULT exif['Image Software'],
	`copyright` String DEFAULT exif['Image Copyright'],
	`image_make` String DEFAULT exif['Image Make'],
	`image_model` String DEFAULT exif['Image Model']
)
ENGINE = MergeTree
ORDER BY (height, width, similarity)
'''
