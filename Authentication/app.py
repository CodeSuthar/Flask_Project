from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "your_secret_key_here"
users_storage = {}


@app.route("/")
def home():
    if "email" in session:
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():
    if "email" not in session:
        return redirect(url_for("login"))

    email = session["email"]
    user = users_storage.get(email)

    if not user:
        session.clear()
        return redirect(url_for("login"))

    return render_template(
        "welcome.html",
        name=user["name"],
        email=email,
        msg="Logged in successfully."
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if "email" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email in users_storage and users_storage[email]["password"] == password:
            session["email"] = email
            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Invalid email or password."
        )

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if "email" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        full_name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")

        if password != confirm_password:
            return render_template(
                "register.html",
                error="Passwords do not match."
            )

        if email in users_storage:
            return render_template(
                "register.html",
                error="Email already exists."
            )

        users_storage[email] = {
            "name": full_name,
            "password": password
        }

        session["email"] = email
        return redirect(url_for("dashboard"))

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)