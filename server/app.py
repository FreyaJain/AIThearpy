from api.app import app
from flask import make_response, jsonify
from api.blueprints import blueprint
from flask_graphql import GraphQLView
from api.schema import schema

app.register_blueprint(blueprint, url_prefix="/api")
class AppConfig:
    PORT = 3001
    DEBUG = True
    
@app.route('/', methods=["GET"])
def meta():
    meta = {
        "programmed by": "@ByteSystem",
        "main": "AI Therapy",
        "description": "AI chatbot API that will behave and chat with human like a therapist.",
        "language": "python",
        "libraries": ["pytorch", "torchtext", "spacy"],
    }
    return make_response(jsonify(meta)), 200

app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True,
))

if __name__ == "__main__":
    app.run(debug=AppConfig().DEBUG, port=AppConfig().PORT, )