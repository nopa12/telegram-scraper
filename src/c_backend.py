from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse

import db

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./db/sqlite.db'
# db = SQLAlchemy(app)
api = Api(app)

class TgMsgsRawResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('page', type=int, default=1, location='args')
        self.parser.add_argument('per_page', type=int, default=10, location='args')

    def get(self):
        args = self.parser.parse_args()
        page = args['page']
        per_page = args['per_page']
        offset = (page - 1) * per_page

        with db.transaction_context() as conn:
            existing_msg = conn.query(db.TgMsgsRaw).first()
            tg_msgs_raw = (
                conn.query(db.TgMsgsRaw)
                .order_by(db.TgMsgsRaw.tg_date.desc())
                .offset(offset)
                .limit(per_page)
                .all()
            )

            results = []
            for tg_msg_raw in tg_msgs_raw:
                tg_media = (
                    conn.query(db.TgMedia)
                    .filter_by(tg_msg_id=tg_msg_raw.id)
                    .first()
                )

                media_response = None

                if tg_media:
                    media_response = {
                        'id': str(tg_media.id),
                        'tg_file_path': tg_media.tg_file_path if tg_media else None,
                    }

                result = {
                    'id': str(tg_msg_raw.id),
                    'tg_id': tg_msg_raw.tg_id,
                    'tg_date': tg_msg_raw.tg_date.isoformat(),
                    'tg_chat': tg_msg_raw.tg_chat,
                    'tg_chat_id': tg_msg_raw.tg_chat_id,
                    'tg_msg': tg_msg_raw.tg_msg,
                    'tg_media': media_response,
                }
                results.append(result)

        return {'data': results}

api.add_resource(TgMsgsRawResource, '/tg_msgs_raw')

if __name__ == '__main__':
    app.run(debug=True, port=5030)
