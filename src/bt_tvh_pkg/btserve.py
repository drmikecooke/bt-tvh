from bluedot.btcomm import BluetoothServer
from signal import pause,SIGKILL
from subprocess import run
from .tvh import ip4,state
from .api import setUSR,subs,inputs,nxt
from os import environ,kill,getpid

stop=["sudo","shutdown"]
restart=["sudo","shutdown","-r"]

def connection():
	print("Connection")
	s.send(ip4(h))
	if not "TVH" in environ:
		s.send("user?\n")
	else:
		setUSR(h)
		stt=state()
		s.send(stt+"How can I help?\n")

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
		kill(getpid(),SIGKILL)
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

def server():
	global s,h
	h="localhost"
	print("Server starting . . .")
	s = BluetoothServer(
		data_received,
		when_client_connects=connection,
		when_client_disconnects=disconnection
	)
	pause()
