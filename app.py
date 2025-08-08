from flask import Flask, render_template, request, redirect, url_for, flash
import os, uuid

app = Flask(__name__)
app.secret_key = "change_this_later"

# In-memory store (for testing, will reset on app restart)
jobs = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/book", methods=["POST"])
def book():
    name = request.form["name"]
    address = request.form["address"]
    service = request.form["service"]
    urgency = request.form["urgency"]
    notes = request.form["notes"]
    token = str(uuid.uuid4())
    jobs[token] = {
        "name": name,
        "address": address,
        "service": service,
        "urgency": urgency,
        "notes": notes
    }
    return redirect(url_for("job_view", token=token))

@app.route("/job/<token>")
def job_view(token):
    job = jobs.get(token)
    if not job:
        return "Job not found", 404
    return render_template("job_view.html", job=job, token=token)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
