#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") == "action.balance":
        result = req.get("result")
        parameters = result.get("parameters")
        accountType = parameters.get("account-type")
        balance = {'Checking':4500, 'Savings':200, 'Business Checking':15000, 'Business Savings':1500}
        speech = "The balance on your " + accountType + " Account is " + str(balance[accountType]) + " dollars. Is there anything else I can help you with?"
        print("Response:")
        print(speech)
        return {
            "speech": speech,
            "displayText": speech,
            "source": "banking-genie"
        }
    elif req.get("result").get("action") == "action.transfer":
        result = req.get("result")
        parameters = result.get("parameters")
        person = parameters.get("person")
        #contexts = result.get("contexts")
        amount = result.get("contexts")["parameters"].get("unit-currency.original")
        print(amount)
        speech = "Sure, I have successfully transferred " + amount + " to your " + person + " from your Checking account. Would you like to perform any other transaction?"
        print("Response:")
        print(speech)
        return {
            "speech": speech,
            "displayText": speech,
            "source": "banking-genie"
        }
    else:
        return {}
	
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))  

    app.run(debug=True, port=port, host='0.0.0.0')
