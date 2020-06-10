from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import play_scraper

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class MyAppData(db.Model):
    app_id = db.Column(db.String(100), primary_key=True)
    category=db.Column(db.String(60), nullable=False)
    developer = db.Column(db.String(100))
    developer_address = db.Column(db.String(100))
    developer_email = db.Column(db.String(100))
    icon = db.Column(db.String(100))
    installs = db.Column(db.String(100))
    reviews = db.Column(db.String(100))
    score = db.Column(db.String(100))
    title = db.Column(db.String(100))
    url = db.Column(db.String(100))
    video = db.Column(db.String(100))
    
    def __repr__(self):
        return f"MyAppData('{self.app_id}', '{self.category}', '{self.developer}', '{self.developer_address}', '{self.developer_email}', '{self.icon}', '{self.installs}', '{self.reviews}', '{self.score}', '{self.title}', '{self.url}', '{self.video}')"
	

def app_fetcher():
  arr=play_scraper.search('top', page=1)
  length=min(10,len(arr))
  dict=[]
  for i in range(0,length):
    dict.append(arr[i]['app_id'])
  return dict




@app.route("/")
def home():
	top10app=app_fetcher()
	top10appshow=[]
	for myapp in top10app:
		pre=MyAppData.query.filter_by(app_id = myapp).all()
		dict=play_scraper.details(myapp)
		#topapp = {"app_id" = dict['app_id'] , "category" = dict['category'][0], "developer" = dict['developer'], "developer_address" = dict['developer_address'], "developer_email" = dict['developer_email'],	"icon" = dict['icon'], "installs" = dict['installs'], "reviews" = dict['reviews'], "score" = dict['score'], "title" = dict['title'], "url" = dict['url'], "video" = dict['video']}
		top10appshow.append(dict)
		if(len(pre)==0):
			new_app=MyAppData(app_id = dict['app_id'] , category = dict['category'][0], developer = dict['developer'], developer_address = dict['developer_address'], developer_email = dict['developer_email'],	icon = dict['icon'], installs = dict['installs'], reviews = dict['reviews'], score = dict['score'], title = dict['title'], url = dict['url'], video = dict['video'])
			db.session.add(new_app)
	db.session.commit()
	return render_template('startup_page.html', data=top10appshow)
	
  	
@app.route('/app_details/<app_id>')
def app_details(app_id):
	dict=play_scraper.details(app_id)
	return render_template('details_page.html', data=dict)
	

    


if __name__ == '__main__':
    app.run(debug=True)