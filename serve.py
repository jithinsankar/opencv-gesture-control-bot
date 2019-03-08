 # -*- coding: utf-8 -*- 
from flask import Flask
import json
app = Flask(__name__)
@app.route('/node')
def helloHandler():
	f = open("text.txt",'r')
	Q=f.read(1)
	return Q
app.run(host='0.0.0.0', port= 8090)

#http://192.168.43.112:8090/helloesp
