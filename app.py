from flask import Flask, render_template, request, redirect, url_for
import os, uuid

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
jobs = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/book", methods=["GET", "POST"])
def book():
    if request.method == "GET":
        return render_template("booking.html")
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
        "notes": notes,
        "media": []
    }
    return redirect(url_for("job_view", token=token))

@app.route("/job/<token>")
def job_view(token):
    job = jobs.get(token)
    if not job:
        return "Job not found", 404
    return render_template("job_view.html", job=job, token=token)

@app.route("/admin")
def admin():
    return render_template("admin.html", jobs=jobs)

@app.route("/upload/<token>", methods=["POST"])
def upload(token):
    job = jobs.get(token)
    if not job:
        return "Invalid job", 404
    files = request.files.getlist("media")
    for file in files:
        filename = f"{uuid.uuid4()}_{file.filename}"
        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(path)
        job["media"].append(filename)
    return redirect(url_for("admin"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
