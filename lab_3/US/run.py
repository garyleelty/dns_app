from socket import *
from flask import Flask,request,jsonify
import requests
import logging

app = Flask(__name__)
logging.getLogger().setLevel(logging.DEBUG)

@app.route('/fibonacci',methods=['Get'])
def fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = int(request.args.get('as_port'))
    logging.info("Revived:{},{},{},{},{}".format(hostname,fs_port,number,as_ip,as_port))
    if  hostname and fs_port and number and as_ip and as_port:
        sock = socket(AF_INET, SOCK_DGRAM)
        msg = "TYPE=A\nNAME={}".format(hostname)
        sock.sendto(msg.encode(),(as_ip,as_port))
        byte,address=sock.recvfrom(2048)
        sock.close()
        logging.info(byte.decode())
        b = byte.decode()
        bytes1 = b.split('\n')
        name = bytes1[1].spilt("=")[1]
        value = bytes1[2].spilt("=")[1]
        logging.info("Name:{}Value:{}".format(name,value))
        r = requests.get("http://{}:{}/fibonacci?number={}".format(value,fs_port,number))
        return jsonify(r.json()),200
   

    else:
        
        return jsonify("some any of the parameters are missing "), 404

app.run(host='0.0.0.0',
        port=8080,
        debug=True)