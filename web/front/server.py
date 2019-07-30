from flask import Flask, jsonify, render_template, request

from nltkpass.nltkpass import NltkPass

app = Flask(__name__, static_folder="../../public", template_folder="../../public", static_url_path="/")
np = NltkPass()
np.add_source("brown")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/sentence", methods=["POST"])
def get_sentence():
    return jsonify({
        "sentence": np.generate_sentence(specificity=2)
    })


@app.route("/api/password", methods=["POST"])
def get_password():
    r = request.form
    s = r.get("sentence")

    if s is None:
        s = np.generate_sentence(specificity=2)

    return jsonify({
        "sentence": s,
        "password": np.generate_password(s).password
    })
