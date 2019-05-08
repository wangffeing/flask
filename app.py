from flask import Flask
from apps.front import bp as front_bp
from apps.pcenter import bp as pcenter_bp
from apps.ueditor import bp as uedit_bp
from apps.common import bp as common_bp
import config
from exts import db
from flask_wtf import CSRFProtect


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(front_bp)
    app.register_blueprint(pcenter_bp)
    app.register_blueprint(uedit_bp)
    app.register_blueprint(common_bp)
    db.init_app(app)
    CSRFProtect(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host='192.129.236.237',
        port=5000,
        debug=True
    )