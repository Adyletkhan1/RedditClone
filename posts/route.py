import praw
from flask import *
import requests
import json
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

# Create flask instance and flask_restful instance


app = Flask(__name__, template_folder='../templates')
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
base_url = 'https://www.reddit.com/'
reddit_username = 'Adiletkhan1'
reddit_password = 'adanadamratygon1'
app_id = 'RtkQ4pDvk_KY0A'
app_secret = 'obKQIUCBMJaqk1nHMLgXJcIRwJ4'
data = {'grant_type': 'password', 'username': reddit_username,
                                    'password': reddit_password}

client_auth = requests.auth.HTTPBasicAuth(app_id, app_secret)
response = requests.post(base_url + 'api/v1/access_token',
                         data=data,
                         headers={'user-agent': 'puppy-parser by alpscode'},
                         auth=client_auth)
print(response.status_code)
values = response.json()

token = 'bearer {}'.format(values['access_token'])
print(token)
api_url = 'https://oauth.reddit.com'
url = 'https://oauth.reddit.com/r/all/'
headers = {'Authorization': token, 'User-Agent': 'puppy-parser by alpscode'}
response = requests.get(api_url + '/api/v1/me', headers=headers)

posts = []



class search_sub_form(FlaskForm):
    search = StringField('Search for subreddit', validators=[DataRequired()])
    submit = SubmitField('Search')


@app.route("/")
@app.route('/home')
def home():
    ##payload = {'limit': 10, 'sort': 'relevance'}
    response = requests.get(url, headers=headers)##, params=payload)
    print(response.status_code)
    posts = response.json()
    print(posts)
    return render_template('home.html', posts=posts['data']['children'])


@app.route("/search/subreddit", methods=['GET', 'POST'])
def search():
    form = search_for_subreddit()
    if form.validate_on_submit():
            return redirect(url_for('searchforsubreddit', string = form.search.data))
    else:
        return render_template('search.html', form=form)


def searchforsubreddit(string):
    payload = {'q':string, 'sort': 'relevance'}
    response = requests.get(api_url+'/subreddits/search/',
                            headers=headers,
                            params=payload)
    subreddits=response.json()
    return render_template('home.html', posts=subreddits['data']['children'])


@app.route("/history")
def history():
    payload = {'limit': 10, 'sort': 'relevance'}
    response = requests.get('https://oauth.reddit.com/u/Adiletkhan1/',
                            headers=headers,
                            params=payload)

    posts = response.json()
    return render_template("user.html", posts=posts['data']['children'])


@app.route("/collections")
def collections():
    payload = {'limit': 10, 'sort': 'relevance'}
    response = requests.get('https://oauth.reddit.com/user/Adiletkhan1/saved.json',
                            headers=headers,
                            params=payload)

    posts = response.json()
    # print(posts)
    return render_template("home.html", posts=posts['data']['children'])





if __name__ == '__main__':
    app.run()
