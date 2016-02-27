from flask import Flask, render_template, request, redirect
from rank.db.storage import Storage

app = Flask(__name__)


@app.route("/")
def index():
    with open("../data/comments.bin", "rb") as f:
        comments = Storage.load(f)
    return render_template("comment_list.html", comments=comments)


@app.route("/update", methods=["POST"])
def update():
    import re
    with open("../data/comments.bin", "rb") as f:
        comments = Storage.load(f)

    store = Storage()
    for key, val in request.form.items():
        if "rating" in key:
            id = re.match(r"rating\[(?P<id>(\d+))\]", key).group("id")
            store.add_comment(comments[int(id)-1].text, val)

    with open("../data/comments.bin", "wb") as f:
        import pickle
        pickle.dump(store.comments, f)

    return redirect("/")


@app.route("/delete/<id>")
def delete(id):
    with open("../data/comments.bin", "rb") as f:
        comments = Storage.load(f)

    comments.pop(int(id) - 1)
    with open("../data/comments.bin", "wb") as f:
        import pickle
        pickle.dump(comments, f)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
