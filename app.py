import os

import openai
from flask import Flask, redirect, render_template, request, url_for
# imports
import ast  # for converting embeddings saved as strings back to arrays
import openai  # for calling the OpenAI API
import pandas as pd  # for storing text and embeddings data
import tiktoken  # for counting tokens
from scipy import spatial  # for calculating vector similarities for search

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# search function
def strings_ranked_by_relatedness(
    query: str,
    df: pd.DataFrame,
    relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y),
    top_n: int = 100
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

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        question = request.form["question"]
        #1. get embedings for question
        embedings_of_the_question = {} # TODO
        #2. TODO search a DB key, embedings of which is closest
        db_key_with_closest_embedings = {} # TODO
        # response = { choices: [ { text: "it's Fake!"} ] } # TODO
        return redirect(url_for("index",
                                result="it's Fake!" # TODO result=response.choices[0].text
                                ))

    result = request.args.get("result")
    return render_template("index.html", result=result)

###

#strings, relatednesses = strings_ranked_by_relatedness("curling gold medal", df, top_n=5)
#for string, relatedness in zip(strings, relatednesses):
#    print(f"{relatedness=:.3f}")
#    display(string)
