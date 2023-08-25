import glob
import os
from flask import Flask, redirect, render_template, request, url_for
# imports
import ast  # for converting embeddings saved as strings back to arrays
import openai  # for calling the OpenAI API
import pandas as pd  # for storing text and embeddings data
import tiktoken  # for counting tokens
from scipy import spatial  # for calculating vector similarities for search
from pprint import pprint
import clickhouse_connect
import numpy as np
#from openai.embeddings_utils import cosine_similarity


app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
# models
EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_MODEL = "gpt-3.5-turbo"


client = clickhouse_connect.get_client(host= os.environ.get('CLICKHOUSE_HOST', 'localhost'),
                                       database= os.environ.get('CLICKHOUSE_DATABASE', 'openai'),
                                       username=os.environ.get('CLICKHOUSE_USERNAME', 'default'),
                                       password=os.environ.get('CLICKHOUSE_PASSWORD', ''),
                                       port=os.environ.get('CLICKHOUSE_PORT', 8123))

def get_embedding_for(text: str, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']

def save_adress_embedding_to_csv():
    file_list = glob.glob("data/z*.txt")
    data_list=[]
    if file_list:
        pprint("****** The list of files *********")
        pprint(file_list)
        for a_file_name in file_list:
            with open(a_file_name,'r') as f:
                # read first line that is address for embeding
                address = f.readline()
                # read rest of the lines that is description from zillow page
                description = f.read()
                pprint("address -----------> ")
                data_list.append({"address": address.strip(), "description": description.strip()})
        df = pd.DataFrame.from_records(data=data_list)
        df["adress_embedding"] = df.address.apply(lambda address: get_embedding_for(address))
        pprint(df.head(5))
        df.to_csv("address_embeddings_descriptions.csv")

def save_table_to_db():
    df = pd.read_csv("addess_embeddings_descriptions.csv.gz")
    df["address_embeddings"] = df.adress_embedding.apply(lambda string_embedings: np.asarray(ast.literal_eval(string_embedings), dtype='float32'))
    df= df.drop(["adress_embedding","Unnamed: 0"], axis=1)
    client.insert_df("qa_properties", df)
    pprint(df.head(2))
    return df


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        a_question = request.form["question"]
        pprint(a_question)
        #1. get embedings for question
        embedings_of_the_question = get_embedding_for(a_question)
        #pprint(embedings_of_the_question)
        #2. TODO search a DB key, embedings of which is closest
        parameters = {'question_embedings': embedings_of_the_question }
        df = client.query_df('SELECT min(cosineDistance(address_embeddings, {question_embedings:Array(Float32)})) as distance, description FROM qa_properties group by description order by 1 asc limit 1',parameters=parameters)
        dist= df.iloc[[0]][['distance']]
        desc=  df.iloc[[0]][['description']]
        #pprint(desc)
        query = f"""Use the below description of real estate property to answer the subsequent question. If the answer cannot be found, write "Not possible to answer"

Description of real estate property:
\"\"\"
{desc}
\"\"\"

Question: {a_question}?"""

        response = openai.ChatCompletion.create(
           messages=[
              {'role': 'system', 'content': 'You answer questions about real estate property.'},
              {'role': 'user', 'content': query},
           ],
           model=GPT_MODEL,
           temperature=0,
        )
        answer= response['choices'][0]['message']['content']
        pprint(answer)
        return redirect(url_for("index", result= answer))

    result = request.args.get("result")
    return render_template("index.html", result=result)

### Create the schema in clickhouse

###

#strings, relatednesses = strings_ranked_by_relatedness("curling gold medal", df, top_n=5)
#for string, relatedness in zip(strings, relatednesses):
#    print(f"{relatedness=:.3f}")
#    display(string)
# numbers=ast.literal_eval(v[0])
