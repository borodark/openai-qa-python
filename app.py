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

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
# models
EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_MODEL = "gpt-3.5-turbo"

# search function
def strings_ranked_by_relatedness(
    query: str,
    df: pd.DataFrame,
    relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y),
    top_n: int = 1
) -> tuple[list[str], list[float]]:
    """Returns a list of strings and relatednesses, sorted from most related to least."""
    query_embedding_response = openai.Embedding.create(
        model=EMBEDDING_MODEL,
        input=query,
    )
    query_embedding = query_embedding_response["data"][0]["embedding"]
    strings_and_relatednesses = [
        (row["text"], relatedness_fn(query_embedding, row["embedding"]))
        for i, row in df.iterrows()
    ]
    strings_and_relatednesses.sort(key=lambda x: x[1], reverse=True)
    strings, relatednesses = zip(*strings_and_relatednesses)
    return strings[:top_n], relatednesses[:top_n]

def get_embedings_of_the_question(a_question: str):
    return {}

def read_local(files_list):
    df1 = (pd.read_json(f) for f in files_list)
    df = pd.concat(df1, ignore_index=True)
    return df

def load_db_():
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
                data_list.append({"address": address, "description": description})
    pprint(data_list)


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        a_question = request.form["question"]
        pprint(a_question)
        #1. get embedings for question
        embedings_of_the_question = get_embedings_of_the_question(a_question) #{} # TODO
        #2. TODO search a DB key, embedings of which is closest
        db_key_with_closest_embedings = {} # TODO
        # response = { choices: [ { text: "it's Fake!"} ] } # TODO
        query = 'Which athletes won the gold medal in curling at the 2022 Winter Olympics?'
        response = openai.ChatCompletion.create(messages=[
            {'role': 'system', 'content': 'You answer questions about the 2022 Winter Olympics.'},
            {'role': 'user', 'content': query},],
                    model=GPT_MODEL,
                                                temperature=1,
            )
        pprint(response)
        return redirect(url_for("index",
                                result=response))

    result = request.args.get("result")
    return render_template("index.html", result=result)

###

#strings, relatednesses = strings_ranked_by_relatedness("curling gold medal", df, top_n=5)
#for string, relatedness in zip(strings, relatednesses):
#    print(f"{relatedness=:.3f}")
#    display(string)
