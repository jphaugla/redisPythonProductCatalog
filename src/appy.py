#!/bin/python

# Dependencies:
# pip install flask
# pip install redis

from flask import Flask, jsonify
from flask import request
import redis
import time
import json
from flask import Response, stream_with_context

app = Flask(__name__)
app.debug = True
db = redis.Redis('localhost')  # connect to server

ttl = 31104000  # one year


def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


@app.route('/', defaults={'path': ''}, methods=['PUT', 'GET', ])
@app.route('/<path:path>', methods=['PUT', 'GET', 'DELETE'])
def home(path):
    print("the request method is " + request.method + " path is " + path)
    if request.method == 'PUT':
        # if prod_idx is set it is a replace
        # if proc_idx is not set, is insert
        print('in PUT')
        event = request.json
        print('event is %s ' % event)
        if path == 'NEW':
            prod_idx = str(db.incr("prod_highest_idx"))
            path = "prod:" + str(prod_idx)
            print("insert-new index is " + path)
        else:
            print("prod_idx exists so is a replace")
        event['updated'] = int(time.time())
        event['ttl'] = ttl
        db.delete(path)  # remove old keys
        db.hmset(path, event)
        db.expire(path, ttl)
        return jsonify(event, 201)

    if request.method == 'DELETE':
        return_status = db.delete(path)
        print("delete with path = " + path + " and status of " + str(return_status))
        return jsonify(str(return_status), 201)

    if request.method == 'GET':
        if path == 'search':
            search_str = request.args.get("search_string")
            print("search string is ", search_str)
            min_str = '[' + search_str
            max_str = min_str + "-"
            print("min is " + min_str + " max is " + max_str)
            results = db.zrangebylex("zProdModelName", min_str, max_str)
            return jsonify(results, 200)

        if not db.exists(path):
            return "Error: thing doesn't exist"

        event = db.hgetall(path)
        print("got event back" + str(event))
        event["ttl"] = db.ttl(path)
        # put path in as product index
        event["prod_idx"] = path
        # cast integers accordingly, nested arrays, dicts not supported for now  :(
        dict_with_ints = dict((k,int(v) if isInt(v) else v) for k, v in event.items())
        # return json.dumps(dict_with_ints), 200
        return jsonify(dict_with_ints, 200)


if __name__ == "__main__":
    app.run()
