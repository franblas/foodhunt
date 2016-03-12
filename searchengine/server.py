# -*- coding: utf-8 -*-

import rethinkdb as r
from database import Database
import flask
from flask import request
import itertools

PORT = 8001
app = flask.Flask(__name__, static_url_path='')

PRODUCTS_DATABASE = 'products'
PRODUCTS_TABLE = 'shopproducts'

db = Database(db=PRODUCTS_DATABASE)

'''
TODO: add french dictonary to catch french words
'''

def build_regex(query):
    print query
    q_split = query.split(' ')
    accents = {
        'a': "[aâäàA]",
        'e': "[eéèêëE]",
        'i': "[iîïI]",
        'o': "[oôöO]",
        'u': "[uûüùU]",
        'y': "[yÿY]"
    }
    short_words = ['de', 'des', 'le', 'la', 'les']

    def filter_short_words(word):
        return word not in short_words

    q_split = filter(filter_short_words, q_split)

    def word_builder(word):
        res = ""
        if word[-1] == 's': # if 's' at the end
            word = word[:-1]
        for k in accents.keys():
            word = word.replace(k, accents.get(k).decode('utf-8'))
        if word[0] == '[': # if voyelle at the begining
            res += "(" + word.lower() + "(s?)" + ")"
        else:
            res += "(" + "[" + word[0].upper() + word[0].lower() + "]" + word.lower()[1:] + "(s?)" + ")"
        return res

    reg = "([\s?\w\s?]+)?"
    for word in q_split:
        other_words = list(q_split)
        other_words.pop(other_words.index(word))
        reg += "("
        reg += word_builder(word)
        for other_word in other_words:
            reg += "|" + word_builder(other_word)
        reg += ")"
        reg += "([\s?\w\s?]+)?"

    reg = reg.encode('utf-8')
    return reg

'''
-- Routes
'''
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/ping')
def pong():
    return 'Pong from search engine'

@app.route('/shops', methods=['GET'])
def shops_list():
    """
    Search engine v0.1
    """
    cursor = db.run(r.table(PRODUCTS_TABLE).pluck('shop').distinct())
    data = [c for c in cursor]
    d = {'a': len(data),'data': data}
    return flask.jsonify(d)

@app.route('/search', methods=['GET'])
def search():
    """
    Search engine v0.1
     - arguments:
      - q: query to search (required)
      - shop: shop name (optional)
    """
    q = request.args.get('q', None)
    if not q:
        return flask.jsonify({'status': 'error', 'message': 'Missing query'}), 400

    shop = request.args.get('shop', None)
    if shop:
        reg = build_regex(q)
        print reg
        cursor = db.run(r.table(PRODUCTS_TABLE).filter(lambda doc:
            doc['name'].match(reg.decode('utf-8'))
        ).filter({
            'shop': shop
        }))
    else:
        reg = build_regex(q)
        cursor = db.run(r.table(PRODUCTS_TABLE).filter(lambda doc:
            doc['name'].match(reg.decode('utf-8'))
        ))

    data = [c for c in cursor]
    d = {'a': len(data),'data': data}
    return flask.jsonify({'status': 'ok', 'data': d}), 200

@app.route('/searchfront', methods=['GET'])
def search_front():
    """
    Search engine v0.1
     - arguments:
      - q: query to search (required)
    """
    q = request.args.get('q', None)
    if not q:
        return flask.jsonify({'status': 'error', 'message': 'Missing query'}), 400

    res = dict()
    cursor = db.run(r.table(PRODUCTS_TABLE).pluck('shop').distinct())
    shops = [c for c in cursor]
    reg = build_regex(q)
    cursor = db.run(r.table(PRODUCTS_TABLE).filter(lambda doc:
        doc['name'].match(reg.decode('utf-8'))
    ).order_by('price'))
    data = [c for c in cursor]

    d = {'shops': shops,'data': data}
    return flask.jsonify({'status': 'ok', 'data': d}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT) # Run flask app
