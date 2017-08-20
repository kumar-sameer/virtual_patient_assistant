#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases

install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import math

from flask import Flask
from flask import request
from flask import make_response
from flask import url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import sqlite3 as sql



import apiai

# Flask app should start in global layout
app = Flask(__name__)

apimedic_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImRobW9kaUBkZWxvaXR0ZS5jb20iLCJyb2xlIjoiVXNlciIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL3NpZCI6IjI5MSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvdmVyc2lvbiI6Ijk5IiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9saW1pdCI6Ijk5OTk5OTk5OSIsImh0dHA6Ly9leGFtcGxlLm9yZy9jbGFpbXMvbWVtYmVyc2hpcCI6IkJhc2ljIiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9sYW5ndWFnZSI6ImVuLWdiIiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9leHBpcmF0aW9uIjoiMjA5OS0xMi0zMSIsImh0dHA6Ly9leGFtcGxlLm9yZy9jbGFpbXMvbWVtYmVyc2hpcHN0YXJ0IjoiMjAwMC0wMS0wMSIsImlzcyI6Imh0dHBzOi8vYXV0aHNlcnZpY2UucHJpYWlkLmNoIiwiYXVkIjoiaHR0cHM6Ly9oZWFsdGhzZXJ2aWNlLnByaWFpZC5jaCIsImV4cCI6MTQ5OTk0NDkxMCwibmJmIjoxNDk5OTM3NzEwfQ.jywFlj5nSM6VQLj3i9F0N1holu3g8shXt9YwCLkSwNk"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

db = SQLAlchemy(app)
class embployee(db.Model):
    employee_id = db.Column('employee_id', db.String(100), primary_key = True)
    employee_name = db.Column(db.String(100))
    service_line = db.Column(db.String(50))
    country = db.Column(db.String(200))
    salary = db.Column(db.Integer)

    def __init__(self, employee_name, service_line, country,salary):
        self.employee_name = employee_name
        self.service_line = service_line
        self.country = country
        self.salary = salary

@app.route('/')
def index():
 return {}


@app.route('/speech')
def speech():
    return redirect(url_for('static', filename='speech.html'))


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    # if req.get("result").get("action") == "weather":
    #     baseurl = "https://query.yahooapis.com/v1/public/yql?"
    #     yql_query = makeYqlQuery(req)
    #     if yql_query is None:
    #         return {}
    #     yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    #     result = urlopen(yql_url).read()
    #     data = json.loads(result)
    #     res = makeWebhookWeatherResult(data)
    #     return res
    #
    # elif req.get("result").get("action") == "weather.temperature":
    #     baseurl = "https://query.yahooapis.com/v1/public/yql?"
    #     yql_query = makeYqlQuery(req)
    #     if yql_query is None:
    #         return {}
    #     yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    #     result = urlopen(yql_url).read()
    #     data = json.loads(result)
    #     res = makeWebhookTemperatureResult(data)
    #     return res

    if req.get("result").get("action") == "IdentifyDisease.info":
        baseurl = "https://healthservice.priaid.ch/issues/"
        addQuery = "/info?token=" + apimedic_key + "&language=en-gb&&format=json"
        result = req.get("result")
        context = result.get("contexts")
        parameter = context[0].get('parameters')
        try:
            issue = parameter.get('issueid')
            print("Issue Id: " + issue)
            if issue is None:
                return {}
            issueid = issue.split('.')[0]
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")
        except Exception:
            print("Exception occurred...")
        yql_url = baseurl + issueid + addQuery
        print(yql_url)
        result = urlopen(yql_url).read()
        #print(json.dumps(result))
        data = json.loads(result)
        res = makeWebhookInfoResult(data)
        return res

    elif req.get("result").get("action") == "identify.symptoms":
        baseurl = "https://healthservice.priaid.ch/issues/"
        addQuery = "/info?token=" + apimedic_key + "&language=en-gb&&format=json"
        result = req.get("result")
        context = result.get("contexts")
        parameter = context[0].get('parameters')
        try:
            issue = parameter.get('issueid')
            print("Issue Id: " + issue)
            if issue is None:
                return {}
            issueid = issue.split('.')[0]
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")
        except Exception:
            print("Exception occurred...")
        yql_url = baseurl + issueid + addQuery
        print(yql_url)
        result = urlopen(yql_url).read()
        #print(json.dumps(result))
        data = json.loads(result)
        res = makeWebhookDiseaseResult(data)
        return res

    elif (req.get("result").get("action") == "identify.disease"):
        baseurl = "https://healthservice.priaid.ch/diagnosis?token=" + apimedic_key + "&gender=male&language=en-gb&year_of_birth=1988&"
        yql_query = makeSymptomsQuery(req)
        #print(yql_query)
        if yql_query is None:
            return {}
        yql_url = baseurl + yql_query + "&format=json"
        print(yql_url)
        result = urlopen(yql_url).read()
        #print(json.dumps(result))
        data = json.loads(result)
        res = makeWebhookDiagnosisResult(data)
        return res

    elif req.get("result").get("action") == "identify.doctor":
        baseurl = "https://api.betterdoctor.com/2016-03-01/doctors?skip=0&limit=1&user_key=8230d2719f3a549ea70e918951350c93&"
        result = req.get("result")
        parameters = result.get("parameters")
        city = parameters.get("geo-city")
        symptoms = parameters.get("symptoms2")
        #print(json.dumps(symptoms))
        context = result.get("contexts")
        #print(json.dumps(context[1]))
        cName = context[1].get("name")
        print(json.dumps(cName))
        if (cName is "identifydisease-followup") or (cName == "identifydisease-followup"):
            symptoms = context[1]['parameters']['symptoms.original']

        print(json.dumps(symptoms))
        print(json.dumps(city))
        if (city is None) or (not city):
            if (symptoms is None) or (not symptoms):
                return {
                    "speech": "Please provide either symptom or location for the search",
                    "displayText": "Please provide either symptom or location for the search",
                    # "data": data,
                    # "contextOut": [],
                    "source": "apiai-weather-webhook-sample"
                }
            yql_url = baseurl + urlencode({'query': json.dumps(symptoms)})
            print(yql_url)
            result = urlopen(yql_url).read()
            print(json.dumps(result))
            data = json.loads(result)
            res = makeWebhookDoctorResult(data)
            return  res
        elif req.get("result").get("action") == "employee.information":
            con = sql.connect("employee.db")
            con.row_factory = sql.Row

            result = req.get("result")
            parameters = result.get("parameters")
            table = parameters.get("tables")
            attribute = parameters.get("attibute")
            operation = parameters.get("operation")
            if ((attribute[0] is not None) and (attribute[0] == "count")):
                cur = con.cursor()
                cur.execute("select count(*) from " + table[0])
                rows = cur.fetchall()
                outText = "There are " + rows[0] + " number of " + table[0] + "/s"
                return {
                    "speech": outText,
                    "displayText": outText,
                    # "data": data,
                    # "contextOut": [],
                    "source": "Dhaval"
                }
        else:
            googleurl = "https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyCQiBWiGy-aaNrthZCShG8sOs3G_ynJkEI&"
            q = urlencode({'address': city})
            yql_url = googleurl + q
            print(yql_url)
            result = urlopen(yql_url).read()
            print(json.dumps(result))
            data = json.loads(result)
            response2 = data.get('results')
            if response2 is None:
                return {
                    "speech": "Please re-try with different query",
                    "displayText": "Please re-try with different query",
                    # "data": data,
                    # "contextOut": [],
                    "source": "apiai-weather-webhook-sample"
                }
            print(json.dumps(response2))
            latitude = response2[0]['geometry']['location']['lat']
            longitude = response2[0]['geometry']['location']['lng']
            if (latitude is None) or (longitude is None):
                return {
                    "speech": "Please re-try with different query",
                    "displayText": "Please re-try with different query",
                    # "data": data,
                    # "contextOut": [],
                    "source": "apiai-weather-webhook-sample"
                }
            print(json.dumps(latitude))
            print(json.dumps(longitude))
            if (symptoms is None) or (not symptoms):
                yql_url = baseurl + urlencode({'location': json.dumps(latitude) + ',' + json.dumps(longitude) + ',1'})
            else:
                yql_url = baseurl + urlencode({'query': json.dumps(symptoms), 'location': json.dumps(latitude) + ',' + json.dumps(longitude) + ',100'})
            print(yql_url)
            result = urlopen(yql_url).read()
            print(json.dumps(result))
            data = json.loads(result)
            res = makeWebhookDoctorResult(data)
            return res


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    address = parameters.get("address")
    if address is None:
        return None
    city = address.get("city")
    # city = parameters.get("city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"

def makeSymptomsQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    symptoms = parameters.get("symptoms")
    #print(json.dumps(parameters))
    #print(json.dumps(symptoms))
    if symptoms is None:
        return None
    list = ",".join(symptoms)
    print (list)
    return "symptoms=[" + list + "]"

def makeDoctorQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    symptoms = parameters.get("symptoms2")
    print(json.dumps(symptoms))
    if symptoms is None:
        return None
    print(json.dumps(city))
    if city is None:
        return urlencode({'query': json.dumps(symptoms)})
    else:
        baseurl = "https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyCQiBWiGy-aaNrthZCShG8sOs3G_ynJkEI&"
        q = urlencode({'address': city})
        yql_url = baseurl + q
        print(yql_url)
        result = urlopen(yql_url).read()
        print(json.dumps(result))
        data = json.loads(result)
        response2 = data.get('results')
        if response2 is None:
            return None
        print(json.dumps(response2))
        latitude = response2[0]['geometry']['location']['lat']
        longitude = response2[0]['geometry']['location']['lng']
        if (latitude is None) or (longitude is None):
            return None
        print(json.dumps(latitude))
        print(json.dumps(longitude))
        return urlencode({'query': json.dumps(symptoms), 'location': latitude + "," + longitude})



def makeWebhookWeatherResult(data):
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}

    # print(json.dumps(item, indent=4))

    speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
             "the temperature is " + condition.get('temp') + " " + units.get('temperature')

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "virtual-patient-assistant"
    }

def makeWebhookTemperatureResult(data):
    print(json.dumps(data))
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}

    # print(json.dumps(item, indent=4))

    speech = "Today in " + location.get('city') + ": " \
             ", the temperature is " + condition.get('temp') + " " + units.get('temperature')

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "virtual-patient-assistant"
    }

def makeWebhookDiagnosisResult(data):
    result = data[0]
    if result is None:
        return {}

    issue = result['Issue']
    if issue is None:
        return {}
    print(issue)
    name = result['Issue']['Name']
    id = result['Issue']['ID']
    if name is None:
        return {}

    diagnosis = result['Issue']['IcdName']
    if diagnosis is None:
        return {}

    # print(json.dumps(item, indent=4))

    speech = "You might be experiencing " + name + ". These are signs of " + diagnosis

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        "contextOut": [{"name":"identifydisease-followup", "lifespan":5, "parameters":{"issue":id}}],
        "source": "virtual-patient-assistant"
    }

def makeWebhookInfoResult(data):
    description = data['Description']
    if description is None:
        return {}
    #print(description)
    #name = result['Issue']['Name']
    #id = result['Issue']['ID']
    #if name is None:
    # return {}

    #diagnosis = result['Issue']['IcdName']
    #if diagnosis is None:
    #    return {}

    # print(json.dumps(item, indent=4))

    #speech = "You might be experiencing " + name + ". These are signs of " + diagnosis

    #print("Response:")
    #print(description)

    return {
        "speech": description,
        "displayText": description,
        # "data": data,
        #"contextOut": [{"name":"identifydisease-followup", "lifespan":5, "parameters":{"issue":id}}],
        "source": "virtual-patient-assistant"
    }

def makeWebhookDiseaseResult(data):
    description = data['PossibleSymptoms']
    if description is None:
        return {}
    #print(description)
    #name = result['Issue']['Name']
    #id = result['Issue']['ID']
    #if name is None:
    # return {}

    #diagnosis = result['Issue']['IcdName']
    #if diagnosis is None:
    #    return {}

    # print(json.dumps(item, indent=4))

    speech = "Probable symptoms are " + description

    #print("Response:")
    #print(description)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        #"contextOut": [{"name":"identifydisease-followup", "lifespan":5, "parameters":{"issue":id}}],
        "source": "virtual-patient-assistant"
    }


def makeWebhookDoctorResult(data):
    result = data.get('data')
    if result is None:
        return {}
    #print(json.dumps(result, indent=4))

    docList = result[0]
    if docList is None:
        return {}

    #print(json.dumps(docList, indent=4))
    practices = docList['practices'][0]
    if practices is None:
        return {}
    #print(json.dumps(practices, indent=4))

    name = practices['name']
  #  print(json.dumps(name, indent=4))

    visit_address = practices['visit_address']['city']
   # print(json.dumps(visit_address, indent=4))

    phones = practices['phones'][0]['number']

   # print(json.dumps(phones, indent=4))

    speech = "Please visit Dr. " + name + ". The clinic is located in " + visit_address + ". For further details, contact him at " + phones + ". Do you want to schedule an appointment?"

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        "contextOut": [{"name":"identifydoctor-followup", "lifespan":5, "parameters":{"doctor":name}}],
        "source": "virtual-patient-assistant"
    }

if __name__ == '__main__':
    db.create_all()
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
