from main import db

class resData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    searchengine = db.Column(db.String(1))
    subdomain = db.Column(db.String(50))
    # tags = db.Column(db)
    # res_title = 
    # res_url =
    # res_content =
    # update_time = 