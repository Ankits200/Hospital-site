import secrets
from flask import Flask, jsonify, redirect, request, url_for
from flask import render_template

app = Flask(__name__)
secure_secret_key = secrets.token_hex(32)
app.secret_key = secure_secret_key
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact",methods =["POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")
        if name and email and subject and message:
            # Assuming form processing is successful
           return jsonify({'message': 'Message sent successfully!'}), 200
        else:
            return jsonify({'message': 'Failed to send message.'}), 400
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)