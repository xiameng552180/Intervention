'''
    The RESTful style api server
'''
from flask import render_template
from flask import Flask, request, redirect, jsonify, send_from_directory
from server import app
from functools import wraps
import hashlib
import random
import time
import datetime
import os
import json
import requests
import subprocess
from math import sqrt

#GLobal Parameters#
dataPath = 'server/data/zigzag.json'

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/loadData', methods= ['GET'])
# def loadData():
#     print("ok")
#     data = {}
#     with open(dataPath, 'r') as f:
#         print("ok")
#         data = json.load(f)
#         print(data)
#         return json.dumps(data)


