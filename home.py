from flask import Flask,request,jsonify,Response,current_app

from app import asr_bp
from users import user_bp
from preview import preview_bp

app = Flask(__name__)

app.register_blueprint(asr_bp, url_prefix='/asr')
app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(preview_bp, url_prefix='/preview')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)