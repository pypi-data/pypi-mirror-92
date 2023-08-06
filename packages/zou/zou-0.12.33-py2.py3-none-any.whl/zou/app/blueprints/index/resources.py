import redis
import requests

from datetime import datetime

from flask import Response, abort
from flask_restful import Resource
from zou import __version__

from zou.app import app, config
from zou.app.utils import permissions
from zou.app.services import projects_service, stats_service

from flask_jwt_extended import jwt_required


class IndexResource(Resource):
    def get(self):
        return {"api": app.config["APP_NAME"], "version": __version__}


class BaseStatusResource(Resource):
    def get_status(self):
        is_db_up = True
        try:
            projects_service.get_open_status()
        except:
            is_db_up = False

        is_kv_up = True
        try:
            store = redis.StrictRedis(
                host=config.KEY_VALUE_STORE["host"],
                port=config.KEY_VALUE_STORE["port"],
                db=config.AUTH_TOKEN_BLACKLIST_KV_INDEX,
                decode_responses=True,
            )
            store.get("test")
        except redis.ConnectionError:
            is_kv_up = False

        is_es_up = True
        try:
            requests.get(
                "http://{host}:{port}".format(
                    host=config.EVENT_STREAM_HOST, port=config.EVENT_STREAM_PORT
                )
            )
        except Exception:
            is_es_up = False

        version = __version__

        api_name = app.config["APP_NAME"]

        return (api_name, version, is_db_up, is_kv_up, is_es_up)


class StatusResource(BaseStatusResource):
    def get(self):
        (api_name, version, is_db_up, is_kv_up, is_es_up) = self.get_status()

        return {
            "name": api_name,
            "version": version,
            "database-up": is_db_up,
            "key-value-store-up": is_kv_up,
            "event-stream-up": is_es_up,
        }


class TxtStatusResource(BaseStatusResource):
    def get(self):
        (api_name, version, is_db_up, is_kv_up, is_es_up) = self.get_status()

        text = """name: %s
version: %s
database-up: %s
event-stream-up: %s
key-value-store-up: %s
""" % (
            api_name,
            version,
            "up" if is_db_up else "down",
            "up" if is_kv_up else "down",
            "up" if is_es_up else "down",
        )
        return Response(text, mimetype="text")


class InfluxStatusResource(BaseStatusResource):
    def get(self):
        (api_name, version, is_db_up, is_kv_up, is_es_up) = self.get_status()

        return {
            "database-up": int(is_db_up),
            "key-value-store-up": int(is_kv_up),
            "event-stream-up": int(is_es_up),
            "time": datetime.timestamp(datetime.now()),
        }


class StatsResource(Resource):

    @jwt_required
    def get(self):
        if not permissions.has_admin_permissions():
            abort(403)
        return stats_service.get_main_stats()


class ConfigResource(Resource):
    def get(self):
        return {
            "crisp_token": app.config["CRISP_TOKEN"]
        }
