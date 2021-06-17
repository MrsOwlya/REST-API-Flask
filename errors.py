from flask import jsonify
from app import app, db, logger


@app.errorhandler(422)
def error_handler(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request'])
    if headers:
        logger.warning(f'Marshmallow error: {Exception}')
        return jsonify({'message': messages}), 422, headers
    else:
        logger.warning(f'Marshmallow error: {Exception}')
        return jsonify({'message': messages}), 422


# @app.errorhandler(500)
# def iternal_error(err):
#     headers = err.data.get('headers', None)
#     messages = err.data.get('messages', ['500 error'])
#     if headers:
#         db.session.rollback()
#         logger.warning(f'Iternal error: {Exception}')
#         return jsonify({'message': messages}), 500, headers
#     else:
#         db.session.rollback()
#         logger.warning(f'Iternal error: {Exception}')
#         return jsonify({'message': messages}), 500
