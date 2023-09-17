from flask import Flask, redirect, render_template, request, url_for

from auth.auth import Auth 

AUTH = Auth()

app = Flask(__name__)

global signed_up
signed_up = False

@app.route("/")
def index():
    session_id = request.cookies.get("session_id", None)
    if session_id is not None:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return f"<h1>Welcome {user.email}</h1>"
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["user"]
        password = request.form["password"]
        if AUTH.is_valid_login(user, password):
            session_id = AUTH.create_session(user)
            response = redirect("/")
            response.set_cookie("session_id", session_id)
            return response
        else:
            return render_template("login.html", error=True, user=user, msg="password, username or email incorrect"), 403    
    else:
        global signed_up
        response = render_template("login.html", success=signed_up, msg="log-up was successful log-in to begin")
        signed_up = False
        return response

    
@app.route("/logup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        password = request.form["password"]
        re_password = request.form["password_verification"]
        email = request.form["user"]
        msg = None
        if password == re_password:
            try:
                user = AUTH.register_user(email, password)
                global signed_up
                signed_up = True
                return redirect("/login")
            except ValueError as error:
                msg = str(error)
        else:
            msg="something is not right"
        return render_template("/signup.html", error=True, usr=email, msg=msg)
    else:
        return render_template("signup.html")
