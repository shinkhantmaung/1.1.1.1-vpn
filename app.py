import urllib.request
import json
import datetime
import random
import string
import time
import sys
import os
from flask import Flask,render_template,redirect,url_for,request
app = Flask(__name__)

@app.route("/")
def index():
  return render_template('index.html')

@app.route("/script_run", methods = ['POST', 'GET'])
def script_run():
  if request.method == 'POST':
    userid = str(request.form['userid'])
    no_of_gb = int(request.form['gb'] )
    referrer  = userid
    if referrer == '':
      return render_template('index.html')
    def genString(stringLength):
      try:
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for i in range(stringLength))
      except Exception as error:
        print(error)

    def digitString(stringLength):
      try:
        digit = string.digits
        return ''.join((random.choice(digit) for i in range(stringLength)))    
      except Exception as error:
        print(error)	

    url = f'https://api.cloudflareclient.com/v0a{digitString(3)}/reg'

    def run():
      try:
        install_id = genString(22)
        body = {"key": "{}=".format(genString(43)),
            "install_id": install_id,
            "fcm_token": "{}:APA91b{}".format(install_id, genString(134)),
            "referrer": referrer,
            "warp_enabled": False,
            "tos": datetime.datetime.now().isoformat()[:-3] + "+02:00",
            "type": "Android",
            "locale": "es_ES"}
        data = json.dumps(body).encode('utf8')
        headers = {'Content-Type': 'application/json; charset=UTF-8',
              'Host': 'api.cloudflareclient.com',
              'Connection': 'Keep-Alive',
              'Accept-Encoding': 'gzip',
              'User-Agent': 'okhttp/3.12.1'
              }
        req         = urllib.request.Request(url, data, headers)
        response    = urllib.request.urlopen(req)
        status_code = response.getcode()	
        return status_code
      except Exception as error:
        print("")
        print(error)

    g = 0
    b = 0
    while True:
      os.system('cls' if os.name == 'nt' else 'clear')
      sys.stdout.write("\r[+] Sending request...   [□□□□□□□□□□] 0%")
      sys.stdout.flush()
      result = run()
      if result == 200 and g != no_of_gb:
        g += 1
        print(f"[#] Total: {g} Good {b} Bad")
        for i in range(18,0,-1):
          sys.stdout.write(f"\r[*] After {i} seconds, a new request will be sent.")
          sys.stdout.flush()
          time.sleep(1)
      elif g == no_of_gb:
        break
      else:
        b += 1
        print(f"[#] Total: {g} Good {b} Bad")
        for i in range(10,0,-1):
          sys.stdout.write(f"\r[*] Retrying in {i}s...")
          sys.stdout.flush()
          time.sleep(1)
    return render_template('result.html',gb = g , userid = referrer , no_of_gb = no_of_gb , status = "success")

  else:
    return index()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('404.html'), 500

@app.errorhandler(503)
def service_unavailable(e):
    return render_template('404.html'), 503

@app.errorhandler(403)
def page_forbidden(e):
    return render_template('404.html'), 403

@app.errorhandler(410)
def page_forbidden(e):
    return render_template('404.html'), 410

if __name__ == "__main__":
  app.run(debug = True)