from flask import Flask
import redis
from flask_cors import CORS

# pool = redis.ConnectionPool(host='bigwin777-redis.tajvik.clustercfg.memorydb.sa-east-1.amazonaws.com', port='6379', db=0, decode_responses=True)
pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db=0, decode_responses=True)
redis = redis.Redis(connection_pool=pool)


def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    cors = CORS(app, resources={r"/static/*": {"origins": "*"}})

    # 后台配置
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)
    # 数据报表
    from .data_report import data_report as data_report_blueprint
    app.register_blueprint(data_report_blueprint)
    # 游戏配置
    from .game import game as game_blueprint
    app.register_blueprint(game_blueprint)
    # 用户数据
    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint)
    # 活动配置
    from .activity import activity as activity_blueprint
    app.register_blueprint(activity_blueprint)
    return app