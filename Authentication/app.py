from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "your_secret_key_here"
users_storage = {}

def get_db_connection():
    return mysql.connector.connect(
        host="sql.freedb.tech",
        user="u_VwzE94",
        password="Ry93WCVFhmYz",
        database="freedb_aJWyqsEz"
    )


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
    user = None

    try:
        mydb = get_db_connection()
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute(
            "SELECT * FROM LoginDetails WHERE Email = %s",
            (email,)
        )
        user = mycursor.fetchone()
        mycursor.close()
        mydb.close()
    except Exception as e:
        session.clear()
        return redirect(url_for("login"))

    if not user:
        session.clear()
        return redirect(url_for("login"))

    return render_template(
        "welcome.html",
        name=user["Name"],
        email=user["Email"],
        msg="Logged in successfully."
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if "email" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            mydb = get_db_connection()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(
                "SELECT * FROM LoginDetails WHERE Email = %s AND Password = %s",
                (email, password)
            )
            user = mycursor.fetchone()
            mycursor.close()
            mydb.close()

            if user:
                session["email"] = email
                return redirect(url_for("dashboard"))
            else:
                return render_template(
                    "login.html",
                    error="Invalid email or password."
                )
        except Exception as e:
            print(f"Database connection error: {str(e)}")
            return render_template(
                "login.html",
                error=f"An error occurred: {str(e)}"
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

        if not full_name or not email or not password or not confirm_password:
            return render_template(
                "register.html",
                error="All fields are required."
            )

        if password != confirm_password:
            return render_template(
                "register.html",
                error="Passwords do not match."
            )

        try:
            mydb = get_db_connection()
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(
                "SELECT * FROM LoginDetails WHERE Email = %s",
                (email,)
            )
            existing_user = mycursor.fetchone()

            if existing_user:
                return render_template(
                    "register.html",
                    error="Email already exists."
                )

            mycursor.execute(
                "INSERT INTO LoginDetails (Name, Email, Password) VALUES (%s, %s, %s)",
                (full_name, email, password)
            )
            mydb.commit()
            mycursor.close()
            mydb.close()

            session["email"] = email
            return redirect(url_for("dashboard"))
        except Exception as e:
            print(f"Database connection error: {str(e)}")
            return render_template(
                "register.html",
                error=f"An error occurred: {str(e)}"
            )

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)