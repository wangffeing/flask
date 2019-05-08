import os

DB_URI = "mysql+pymysql://root:1qaz!QAZ@127.0.0.1:3306/zxbbs2?charset=utf8"

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS =False

SECRET_KEY = os.urandom(24)

USER_ID = 'FFFF'

UEDITOR_UPLOAD_PATH=os.path.join(os.path.dirname(__file__),'app/static/images')
UPLOADED_AVATER_PATH = os.path.join(os.path.dirname(__file__),'app/static/avatar/')

PER_PAGE = 10
MANAGE_PER_PAGE = 15