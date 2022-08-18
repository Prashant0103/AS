from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from flask import jsonify,Flask,request,Response,Blueprint,json
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os 
from dotenv import load_dotenv
from flasgger import swag_from
import maskpass

load_dotenv()


username = os.environ.get("username")
passw = maskpass.askpass(prompt="Password:", mask="*")
database_name = os.environ.get("database_name")

api = SentinelAPI(username, passw)
read_f = geojson_to_wkt(read_geojson('data.geojson'))

app = Flask(__name__)
db = SQLAlchemy(app)
ma = Marshmallow(app)


app.config['SQLALCHEMY_DATABASE_URI'] = database_name
app.config['FLASK_ADMIN_SWATCH'] = 'cosmo'

admin = Admin(app, name='Its Admin', template_mode='bootstrap3')


class model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(500), unique=True)
    file_name = db.Column(db.String(500))
    cloud_cover_percentage = db.Column(db.Numeric)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)


class myappv(ma.Schema):
    class Meta:
        fields = ("id","product_id","end_date","file_name","cloud_cover_percentage","start_date")


my_data = myappv(many=True)
admin.add_view(ModelView(model, db.session))


# -------------------------------------------------------------------------

@app.errorhandler(Exception)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


@app.route("/id/<int:num>",methods=["POST","GET"])
def show_id(num):

    try:
        b = model.query.filter_by(id = num).all()
        print(len(b))
        if len(b) >= 1:
            res = my_data.dump(b)
            return jsonify(res)
        else:
            return jsonify(error="Id Does not exist"),404
    except Exception as e:
        return e


@app.route("/pro_id/<string:val>",methods=["POST","GET"])
def show_proid(val):
    try:
        b = model.query.filter_by(product_id = val).all()
        if len(b) >= 1:
            res = my_data.dump(b)
            return jsonify(res)    
        else:
            return jsonify(error="Product Id Does not exist"),404        
    except Exception as e:
        return e


@swag_from("hello_world.yml", methods=['GET'])
@app.route("/")
def show():
    try:
        data = model.query.all()
        res = my_data.dump(data)
        return jsonify(res)
    except Exception as e:
        return e

    
if __name__ == "__main__":
    app.secret_key = 'Rocky'
    db.create_all()
    app.run()
