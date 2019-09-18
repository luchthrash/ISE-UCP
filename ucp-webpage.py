from flask import Flask, render_template, flash, redirect
from forms import ChangePasswordForm
from config import Config

import http.client
import base64
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import sys
from tacacs_plus import client



appContext = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

app=Flask(__name__)
app.config.from_object(Config)



def getUserFromISE(user, password):

#replace "IP" with the hostname/IP of your PAN server 
   conn = http.client.HTTPSConnection("IP:9060", context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2))

   creds = str.encode(':'.join((user, password)))
   encodedAuth = bytes.decode(base64.b64encode(creds))

   headers = {
    'accept': "application/json",
    'authorization': " ".join(("Basic",encodedAuth)),
    'cache-control': "no-cache",
    }

   conn.request("GET", "/ers/config/internaluser/", headers=headers)

   res = conn.getresponse()
   
   if (res.status == 200):
      data = res.read()
      resultList=[
      ("Header:\n{}".format(res.headers)),
      ("Body:\n{}".format(data.decode("utf-8")))]
      resultArrayString=''.join(resultList)
      return resultArrayString
   else:
      return str(res.status)


def getUserID (name):
   #replace "IP" with the hostname/IP of your PAN server 
   conn = http.client.HTTPSConnection("IP:9060", context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2))
   #replace "Username" with your API admin username and "Password" with your password
   creds = str.encode(':'.join(("Username", "Password")))
   encodedAuth = bytes.decode(base64.b64encode(creds))

   headers = {
	'accept': "application/vnd.com.cisco.ise.identity.internaluser.1.2+xml",
    'content-type': "application/json",
    'authorization': " ".join(("Basic",encodedAuth)),
    'cache-control': "no-cache",
    }

   conn.request("GET", "/ers/config/internaluser?filter=name.EQ.{}".format(name), headers=headers)

   res = conn.getresponse()

  
   if (res.status == 200):
      data = res.read()
     
      listResult=str(data).split(" ")
      for i in listResult:
	     #replace "IP" with the hostname/IP of your PAN server 
         if ("href=\"https://IP:9060/ers/config/internaluser/" in i):
            userIDUrl=i.split("=")[1]
            userID=userIDUrl.split("/")[-1][0:-1]
            return userID

   else:
      return str(res.status)


def changePassword (userID, user, newPwd):
   #replace "IP" with the hostname/IP of your PAN server 
   conn = http.client.HTTPSConnection("IP:9060", context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2))
   #replace "Username" with your API admin username and "Password" with your password
   creds = str.encode(':'.join(("Username", "Password")))
   encodedAuth = bytes.decode(base64.b64encode(creds))

   req_body_json = """ {{
       "InternalUser" : {{
           "id" : "{}",
		   "name" : "{}",
           "password" : "{}"
       }}
   }} """.format(userID,user,newPwd)

   headers = {
	'accept': "application/vnd.com.cisco.ise.identity.internaluser.1.2+xml",
    'content-type': "application/json",
    'authorization': " ".join(("Basic",encodedAuth)),
    'cache-control': "no-cache",
    }

   conn.request("PUT", "/ers/config/internaluser/{}".format(userID), headers=headers, body=req_body_json)

   res = conn.getresponse()
  
   if (res.status == 200):
      return "OK"
   else:
      print(res.headers)
      data=res.read().decode("utf-8")
      print(data)
      errorMessage=str(data).split("<title>")[1].split("</title>")[0]
      return errorMessage


def authenticateTACACS(user, password):
    #replace "IP" with your PSN hostname/IP and "Secret" with your TACACS secret
	return client.TACACSClient('IP', 49, 'Secret',timeout=10).authenticate(
user, password, client.TAC_PLUS_AUTHEN_TYPE_ASCII
    )


@app.route('/', methods=['GET','POST'])
def home():
   form = ChangePasswordForm()
   if form.validate_on_submit():
      authResult=authenticateTACACS(form.username.data, form.password.data)
      if "status: FAIL" in str(authResult):
         form.errors.update({'generalErrors' : ["Wrong username/password"]})
      else:
         if (form.newPassword.data != form.confirmNewPassword.data):
           form.errors.update({'generalErrors' : ["New password fields don't match"]})
         else:			
            userID=getUserID(form.username.data)
            result=changePassword(userID, form.username.data, form.newPassword.data)
            if result != "OK":
               form.errors.update({'generalErrors' : [result]})
            else:
               form.errors.update({'messages': ["Password has been successsfully updated"]})
      
   else:
       print(form.errors)
   return render_template("template.html", form=form)

	
if __name__=="__main__":
   app.run(debug=True, host='0.0.0.0', port='443', ssl_context=appContext)