import os
import json
from flask import Flask, render_template, url_for, redirect, session, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "drawings.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
Migrate(app, db)


class Drawing(db.Model):
    __tablename__ = "drawings"
    id = db.Column(db.Integer, primary_key=True)
    clientname = db.Column(db.String(64), index=True)
    modelname = db.Column(db.String(64), index=True)
    drawingnumber = db.Column(db.String(64), index=True)
    version = db.Column(db.String(64), index=True)
    pagenumber = db.Column(db.String(64), index=True)

    def __init__(self, clientname, modelname, drawingnumber, version, pagenumber):
        self.clientname = clientname
        self.modelname = modelname
        self.drawingnumber = drawingnumber
        self.version = version
        self.pagenumber = pagenumber

    def __repr__(self):
        return f"clientname: {self.clientname}, modelname: {self.modelname}, drawingnumber: {self.drawingnumber}, version: {self.version}, pagenumber: {self.pagenumber}" 



# JSON ファイルから顧客リストをロードする関数
def load_clients():
    try:
        with open("clients.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        return [(clients["id"], clients["name"]) for clients in data]
    except (FileNotFoundError, json.JSONDecodeError):
            return []  # ファイルがない、またはJSONが壊れていた場合は空リストを返す

class RegistrationForm(FlaskForm):
    clientname = SelectField("顧客名", choices=load_clients(), validators=[DataRequired(message="顧客名を選択してください")]) # JSONからデータを取得
    modelname = StringField("機種名", validators=[DataRequired(message="機種名を入力してください")])
    drawingnumber = StringField("図面番号", validators=[DataRequired(message="図面番号を入力してください")])
    version = StringField("バージョン", validators=[DataRequired(message="バージョンを入力してください")])
    pagenumber = SelectField("ページ", choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")], validators=[DataRequired(message="ぺージをジ選択してください")])
    submit = SubmitField("登録")

    # クラスの初期化時にロード
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clientname.choices = load_clients()

# 検索フォームのクラス
class SearchForm(FlaskForm):
    searchtext = StringField("検索", validators=[DataRequired()])
    submit = SubmitField("検索")




@app.route("/drawing_management", methods=["GET", "POST"])
def drawing_management():
    form = RegistrationForm()

    # ページの取得
    page = request.args.get("page", 1, type=int)
    
    # データベースをidで全て取得ページネーションで1ページ10行表示
    drawings = Drawing.query.order_by(Drawing.id).paginate(page=page, per_page=10)
    if form.validate_on_submit():
        # データベースに保存する処理
        # すべての項目が一致するレコードがすでにあるかチェック
        existing_drawing = Drawing.query.filter_by(clientname=form.clientname.data, modelname=form.modelname.data, drawingnumber=form.drawingnumber.data, version=form.version.data, pagenumber=form.pagenumber.data).first()# 一致するデータが1つでもあれば取得
        if existing_drawing:
            flash("すでに登録されています。")
        else:
            drawing = Drawing(clientname=form.clientname.data, modelname=form.modelname.data, drawingnumber=form.drawingnumber.data, version=form.version.data, pagenumber=form.pagenumber.data)
            db.session.add(drawing)
            db.session.commit()
            flash("図面の登録が完了しました。")
            return redirect(url_for("drawing_management"))
    return render_template("drawing_management.html", form=form, searchtext=None, drawings=drawings, pagination=drawings, search_mode=False)

@app.route("/<int:drawing_id>/delete", methods=["POST"])
def delete_drawing(drawing_id):
    drawing = Drawing.query.get_or_404(drawing_id)
    db.session.delete(drawing)
    db.session.commit()
    flash("登録図面が削除されました。")
    return redirect(url_for("drawing_management"))

@app.route("/comparsion")
def comparsion():
    return render_template("comparsion.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    searchtext = request.args.get("searchtext", "")
    
    # 検索ワードに基づいてクエリを実行
    if searchtext:
        drawings_pagination = Drawing.query.filter(Drawing.drawingnumber.like(f"%{searchtext}%")).all()
    else:
         # 検索しない場合は全データを表示（リダイレクト）
        return redirect(url_for("drawing_management"))

    return render_template(
        "drawing_management.html",
        searchtext=searchtext,
        drawings=drawings_pagination,  # 検索結果をそのままリストで渡す
        form=RegistrationForm(),
        search_mode=True  # 検索中であることを示すフラグ
    )

if __name__ == "__main__":
    app.run(debug=True)