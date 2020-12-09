from machine import Pin
from dht import *
from mqtt import MQTTClient
import network
from time import *
ssid="surya"
password="surya1827"

mqtt_server='broker.hivemq.com'
client_id="ESP32Surya01"
topic_pub='esp/dht/surya'
topic_sub='esp/dht/abhi'
dht=DHT11(Pin(23))

def connect_wifi():
  station=network.WLAN(network.STA_IF)
  station.active(True)
  station.connect(ssid,password)
  while station.isconnected()==False:
    pass
  print("WiFi Connected")
  
def readdht():
  dht.measure()
  t=dht.temperature()
  h=dht.humidity()
  return(t,h)
  
def connect_mqtt():
  client=MQTTClient(client_id,mqtt_server)
  client.set_callback(on_message)
  client.connect()
  client.subscribe(topic_sub)
  print("Connected to %s MQTT Broker"%(mqtt_server))
  return client
  
def on_message(topic,msg):
  print(topic.decode()+":"+msg.decode())

connect_wifi()
client=connect_mqtt()
while True:
  client.check_msg()
  t,h=readdht()
  #print(t,h)
  msg="Temperature:"+str(t)+",Humidity:"+str(h)
  print(msg)
  client.publish(topic_pub,msg)
  sleep(2)

