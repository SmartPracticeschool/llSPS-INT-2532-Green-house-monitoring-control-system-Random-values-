import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import requests
#Provide your IBM Watson Device Credentials
organization ="12lv8e"
deviceType = "raspberrypi"
deviceId = "123456"
authMethod = "token"
authToken = "0123456789"
#fast2sms credentials
url = "https://www.fast2sms.com/dev/bulk"

querystring = {"authorization":"PWNukjFiJdXO1Q9rBhbelKRDvLS0s26IVzpZC7n45m8xytMAEcP4ZWKJrSmwkXxfVBIF35ycNpj1REvd","sender_id":"FSTSMS","message":"Temperature , Humidity and soil moisture values are beyond the threshold values. Please check it thoroughly.","language":"english","route":"p","numbers":"9515989478"}

headers = {
   'cache-control': "no-cache"
}

def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data['command'])


        if cmd.data['command']=='sprinkleron':
                print("sprinkleon command IS RECEIVED")
                
                
        elif cmd.data['command']=='sprinkleroff':
        
                print("sprinkle OFF command IS RECEIVED")

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)

except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()



# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        
        hum=random.randint(0,100)
        #print(hum)
        temp =random.randint(0,100)

        moisture =random.randint(0,100)
        
        #Send Temperature & Humidity &soil moisture to IBM Watson
        data = { 'Temperature' : temp, 'Humidity': hum ,'Soil_Moisture': moisture}

        #print (data)
        def myOnPublishCallback():
            print ("Published Temperature = %s C" % temp, "Humidity = %s %%" % hum,"Soil_Moisture = %s %%" %moisture,"to IBM Watson")
        success = deviceCli.publishEvent("Green house monitoring", "json", data, qos=0, on_publish=myOnPublishCallback)

        if not success:
            print("Not connected to IoTF")
        
        if((temp<20 or temp>45)or (hum<30 and hum>80) or (moisture<40 and moisture>90)):
           response = requests.request("GET", url, headers=headers, params=querystring)
           print(response.text)
        time.sleep(30)
        deviceCli.commandCallback = myCommandCallback
        

# Disconnect the device and application from the cloud
deviceCli.disconnect()
