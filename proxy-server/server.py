from flask import Flask, json
import requests_unixsocket
import socket
import netifaces as ni
import urllib

IF_NAME = "eth0"
ELASTIC_DATA_DIR = "/mnt/data/elastic/"

def get_ip_address(ifname):
    return ni.ifaddresses(ifname)[ni.AF_INET][0]['addr']

def url_encode(string):
    return urllib.parse.quote_plus(string)

def get_data(endpoint):
  session = requests_unixsocket.Session()
  uri = ELASTIC_DATA_DIR + get_ip_address(IF_NAME) + "/services/proxyv2/data/proxy_admin.sock"
  r = session.get('http+unix://' + url_encode(uri) + '/api/v0/' + endpoint)
  detail = r.json()
  return {'metricset': endpoint, 'detail': detail}


api = Flask(__name__)

@api.route('/health', methods=['GET'])
def get_health():
  return json.dumps(get_data('health'))

@api.route('/maintenance', methods=['GET'])
def get_maintenance():
  return json.dumps(get_data('maintenance'))

@api.route('/stats', methods=['GET'])
def get_stats():
  return json.dumps(get_data('stats'))

@api.route('/connections', methods=['GET'])
def get_connections():
  return json.dumps(get_data('connections'))

if __name__ == '__main__':
    api.run(port="9990")