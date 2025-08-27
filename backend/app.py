from flask import Flask, render_template, request
from search import search

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search_route():
    query = request.args.get("q", "")
    results = search(query) if query else []
    return render_template("results.html", query=query, results=results)

if __name__ == "__main__":
    app.run(debug=True)
