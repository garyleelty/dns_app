from flask import Flask,request,jsonify
from socket import *
import logging

app = Flask(__name__)
logging.getLogger().setLevel(logging.DEBUG)

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        return fib(n-1)+fib(n-2)

@app.route('/fibonacci',methods=['GET'])
def fibonacci():
    number = request.args.get('number')
    if not number :
        return jsonify('Bad format'), 400
    logging.info("F={}".format(number))
    return jsonify(fib(int(number))), 200


@app.route('/register',methods=['PUT'])
def register():
    data = request.get_json()
    hostname = data.get('hostname')
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = int(data.get('as_port' ))
    hostname = "fib.com"
    ip ='127.0.0.1'
    as_ip = '127.0.0.1'
    as_port =53533
    logging.info('register:{},{},{},{},{}'.format(hostname,ip,as_ip,as_port))
    res = False
    if hostname and ip and as_ip and as_port:
        sock = socket(AF_INET, SOCK_STREAM)
        msg = "TYPE=A\n"+"NAME={}\nVALUE={}TTL=10".format(hostname,ip)
        
        sock.sendto(msg.encode(),(as_ip,as_port))
        md, sd = sock.recvfrom(2048)
        logging.info(md.decode())
        sock.close()
        
        if md.decode() == "Success":
            return jsonify("Successful"), 201
        else:
            return jsonify("fail"), 500
    elif res is False:
        sock = socket(AF_INET, SOCK_DGRAM)
        msg = "TYPE=A\n"+"NAME={}\nVALUE={}TTL=10".format(hostname,ip)
        sock.sendto(msg.encode(),(as_ip,as_port))
        md, sd = sock.recvfrom(2048)
        logging.info(md.decode())
        sock.close()
        if md.decode() == "Success":
            return jsonify("Successful"), 201
        else:
            return jsonify("fail"), 500
    else:
        return jsonify("fail"), 400
        
app.run(host='0.0.0.0',
        port=9090,
        debug=True)