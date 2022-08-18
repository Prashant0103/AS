from senti import app,db
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flask import jsonify,Flask,request


app.json_encoder = LazyJSONEncoder
swagger_template = dict(
info = {
    'title': LazyString(lambda: 'Its Sentinel Api'),
    'version': LazyString(lambda: '0.1'),
    'description': LazyString(lambda: 'This Page shows the sentinelsat fetch data'),
    },
    host = LazyString(lambda: request.host)
)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'hello_world',
            "route": '/api',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/"
}


swagger = Swagger(app, template=swagger_template,             
                  config=swagger_config)


if __name__ == "__main__":
    app.secret_key = 'Rocky'
    db.create_all()
    app.run()
