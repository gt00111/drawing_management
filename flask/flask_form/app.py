from flask import Flask, render_template, url_for, redirect, session, flash,request
from flask_wtf import FlaskForm
from wtforms import ValidationError, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_login import LoginManager, UserMixin,login_user
from werkzeug.security import check_password_hash
#　後から追加_______________________________________________________
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from pytz import timezone
#_______________________________________________________________

app = Flask(__name__)

app.config["SECRET_KEY"] = "mysecretkey"
#　後から追加_______________________________________________________
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from sqlalchemy.engine import Engine
from sqlalchemy import event

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    
class User(db.Model, UserMixin):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    administrator = db.Column(db.String(1))
    post = db.relationship("BlogPost", backref="author", lazy="dynamic")
    
    def __init__(self, email, username, password_hash, administrator):
        self.email = email
        self.username = username
        self.password_hash = password_hash
        self.administrator = administrator
        
    def __repr__(self):
        return f"UserName: {self.username}"
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class BlogPost(db.Model):
    __tablename__ = "blog_post"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    date = db.Column(db.DateTime, default=datetime.now(timezone("Asia/Tokyo")))
    title = db.Column(db.String(140))
    text = db.Column(db.Text)
    summary = db.Column(db.String(140))
    featured_img = db.Column(db.String(140))
    
    def __init__ (self, title, text, featured_img, user_id, summary):
        self.title = title
        self.text = text
        self.featured_img = featured_img
        self.user_id = user_id
        self.summary = summary
        
    def __repr__(self):
        return f"PostID: {self.id}, Title: {self.title}, Author: {self.author} \n"
#_______________________________________________________________
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(message="正しいメースアドレスを入力して下さい")])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("ログイン")


class RegistrationForm(FlaskForm):
    email = StringField("メールアドレス", validators=[DataRequired(), Email(message="正しいメールアドレスを入力して下さい")])
    username = StringField("ユーザー名", validators=[DataRequired()])
    password = PasswordField("パスワード", validators=[DataRequired(), EqualTo("pass_confirm", message="パスワードが一致していません")])
    pass_confirm = PasswordField("パスワード（確認）", validators=[DataRequired()])
    submit = SubmitField("登録")
    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("入力されたユーザー名はすでに使用されています。")
            
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("入力されたメールアドレスはすでに登録されています。")
        
class UpdateUserForm(FlaskForm):
    email = StringField("メールアドレス", validators=[DataRequired(), Email(message="正しいメールアドレスを入力して下さい")])
    username = StringField("ユーザー名", validators=[DataRequired()])
    password = PasswordField("パスワード", validators=[EqualTo("pass_confirm", message="パスワードが一致していません")])
    pass_confirm = PasswordField("パスワード(確認)")
    submit = SubmitField("更新")
    
    def __init__(self, user_id, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.id = user_id
        
    def validate_email(self, field):
        if User.query.filter(User.id != self.id).filter_by(email=field.data).first():
           raise ValidationError("入力されたメールアドレスはすでに登録されています。")
       
    def validate_username(self, field):
        if User.query.filter(User.id != self.id).filter_by(username=field.data).first():
            raise ValidationError("入力されたユーザー名はすでに使われています。")
 
@app.route("/login", methods=["GET", "POST"])        
def Login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            if user.check_password(form.password.data):
                login_user(user)
                next = request.args.get("next")
                if next == None or not next[0] == "/":
                    next = url_for("user_maintenance")
                return redirect(next)
            else:
                flash("パスワードが一致しません")
        else:
            flash("入力されたユーザーは存在しません")
    
    return render_template("login.html", form=form)
            
@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # session["email"] = form.email.data
        # session["username"] = form.username.data
        # session["password"] = form.password.data
        user = User(email=form.email.data, username=form.username.data, password_hash=form.password.data, administrator="0")
        db.session.add(user)
        db.session.commit()
        flash("ユーザーが登録されました")
        return redirect(url_for("user_maintenance"))
    return render_template("register.html", form=form)

@app.route("/user_maintenance")
def user_maintenance():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.id).paginate(page=page, per_page=10)
    return render_template("user_maintenance.html", users=users)

@app.route("/<int:user_id>/account", methods=["GET", "POST"])
def account(user_id):
    user = User.query.get_or_404(user_id)
    form = UpdateUserForm(user_id)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        if form.password.data:
            user.password_hash = form.password.data
        db.session.commit()
        flash("ユーザーアカウントが更新されました")
        return redirect(url_for("user_maintenance"))
    elif request.method == "GET":
        form.username.data = user.username
        form.email.data = user.email 
    return render_template("account.html", form=form)

@app.route("/<int:user_id>/delete", methods=["GET", "POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("ユーザーアカウントが削除されました")
    return redirect(url_for('user_maintenance'))

if __name__ == "__main__":
    app.run(debug=True)
 