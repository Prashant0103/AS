from senti import api,read_f,model,db,app
# ------------------------------------------------------------------------
try:
    products = api.query(read_f,
                            date = ('20190625','20190627'),
                            platformname = 'Sentinel-2',
                            cloudcoverpercentage = (0, 30))
except:
    print("Internet Error...")


try:
    c = 0
    for (prod_id, j) in (products.items()):
                    ccp = j["cloudcoverpercentage"]
                    begin_pos = j["beginposition"]
                    fname = j["filename"]
                    end_pos = j["endposition"]

                    try:
                        database = model(product_id=prod_id,file_name=fname,cloud_cover_percentage=ccp,start_date=begin_pos,end_date=end_pos)
                        db.session.add(database)
                        db.session.commit()
                        c += 1
                        print(c, "Row Inserted")
                    except:
                        print("Product Id Already Exist In Table")
except:
    print("Somthing went Wrong...")


if __name__ == "__main__":
    app.secret_key = 'Rocky'
    db.create_all()
    app.run()

