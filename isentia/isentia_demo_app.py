from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import datetime

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "guardian"
mongo = PyMongo(app)


@app.route('/', methods=['GET'])
def home_page():
    article_list = []
    for article in mongo.db.articles.find():
        article_list.append({'url': article['url'],
                             'headline': article['headline'],
                             'author': article['author'],
                             'published': article['published'],
                             'tags': article['tags']})
    return jsonify({'result': article_list})


@app.route('/tags', methods=['GET'])
def articles_with_specific_tags():
    article_list = []
    for article in mongo.db.articles.find({"tags": request.args.get('tag')}):
        article_list.append({'url': article['url'],
                             'headline': article['headline'],
                             'author': article['author'],
                             'published': article['published'],
                             'tags': article['tags']})
    return jsonify({'result': article_list})


@app.route('/date', methods=['GET'])
def articles_with_date_range():
    article_list = []
    for article in mongo.db.articles.find(
            {"published": {
                "$gte": datetime.datetime.strptime(request.args.get('start'), '%Y-%m-%d'),
                "$lte": datetime.datetime.strptime(request.args.get('end'), '%Y-%m-%d')}
            }
    ):
        article_list.append({'url': article['url'],
                             'headline': article['headline'],
                             'author': article['author'],
                             'published': article['published'],
                             'tags': article['tags']})
    return jsonify({'result': article_list})


if __name__ == '__main__':
    app.run(debug=True)
