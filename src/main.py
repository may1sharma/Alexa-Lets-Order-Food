from flask import Flask, render_template, request
from process import Data
import sys

app = Flask(__name__)
data = Data()

@app.route("/", methods=['GET','POST'])
def welcome():
    popular = data.whatsTrending(20)
    return render_template('index.html', popular=popular)
    # return render_template('index.html')


@app.route("/recommend", methods=['GET','POST'])
def main():
    username = request.form['username']
    username = data.getUserName(username)
    reco = data.getRecoForUser([username], 10)
    return render_template('recommendations.html', user=username, reco=reco)

@app.route("/item_<item>", methods=['GET','POST'])
def item(item):
    name = data.queryAmazon([item])[0].encode('UTF8')
    img_url = data.queryAmazon([item], 'Images')[0].encode('UTF8')
    rating = data.getAverageRating(item)
    similar = data.getSimilarItems(item, 10)
    helpful = data.helpfulReviews(item, 5)
    return render_template('item.html', id=item, name=name, url=img_url, rating=rating, similar=similar, helpful=helpful)

if __name__ == '__main__':
    if len(sys.argv)==2 and sys.argv[1] == 'create':
        data.createModels()
    elif len(sys.argv)==2 and sys.argv[1] == 'debug':
        app.debug = True
        app.run(threaded=True)
    else:
        app.run(threaded=True)