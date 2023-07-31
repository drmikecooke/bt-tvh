from bluedot.btcomm import BluetoothServer
from signal import pause
from subprocess import run
from .tvh import ip4,state
from .api import setUSR,subs,inputs,nxt
from os import environ

stop=["sudo","shutdown","now"]
restart=["sudo","shutdown","-r","now"]

def connection():
	print("Connection")
	s.send(ip4(h))
	if not "TVH" in environ:
		s.send("user?\n")
	else:
		s.send("How can I help?\n")

def disconnection():
	print("Disconnection")
	
def data_received(data):
	if not "TVH" in environ:
		environ["TVH"]=data
		s.send("pwd?\n")
		return
	if not ":" in environ["TVH"]:
		environ["TVH"]+=":"+data
		environ["TVH"]=environ["TVH"].replace("\r\n","")
		setUSR(h)
		stt=state()
		s.send(stt+"How can I help?\n")
		return
	if "stop" in data:
		s.send("Stopping . . .\n")
		run(stop)
	elif "restart" in data:
		s.send("Restarting . . .\n")
		run(restart)
	elif "state" in data:
		s.send("State report:\n"+state())
		print("Sending state")
	elif "reset" in data:
		s.send("Resetting user details\nuser?\n")
		print("Resetting user details")
		del environ["TVH"]
	else:
		s.send("Not sure what you want:\n")
		s.send(data)

def server(host):
	global s,h
	h=host
	s = BluetoothServer(
		data_received,
		when_client_connects=connection,
		when_client_disconnects=disconnection
	)
	pause()
