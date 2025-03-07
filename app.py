from flask import Flask, request, send_file, render_template
from rembg import remove, new_session
from PIL import Image
import io
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

# Use the lighter "u2netp" model
session = new_session(model_name="u2netp")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    if "image" not in request.files:
        return {"error": "No file uploaded"}, 400
    
    file = request.files["image"]
    image = Image.open(file.stream)

    # Pass the session to prevent reloading the model
    output = remove(image, session=session)
    img_io = io.BytesIO()
    output.save(img_io, format="PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png", as_attachment=True, download_name="output.png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
