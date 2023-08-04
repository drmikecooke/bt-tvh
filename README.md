# bt-tvh
Use bluetooth comm api supplied in bluedot python package to get tvheadend (tvh) info and allow machine to stop or restart from android phone serial bluetooth terminal.

Much of this was cribbed from my other project [bluedot-mpd](https://github.com/drmikecooke/bluedot-mpd), where more explanation is available.

## Motivation

It may be because I live in a society that is breaking down, or perhaps I am just a cheapskate, but the wifi connection to my ISP-supplied router gets lost fairly often. It is not restricted to a particular machine. It can be the desktop-router link or the TVH server-router link that breaks. Also this continues to be a problem, irrespective of the ISP (I have tried a number over the years). This package is my latest attempt to provide a cleaner shutdown or restart process rather than just pulling out the plug. The service also gives a summary report to say if the tvh server is recording or when the next program is due to record. I also like to start the machine half an hour beforehand to allow the system to settle and provide time to check that the bits are working correctly, so there is a suggestion for setting an alarm.

## pipx

```
cd bt-tvh
pipx install .
```

gives a command

```
btTVH
```

that launches a server that can be accessed via a Bluetooth terminal. Such are available in Android from Google store. 

## systemd

To get a service running in the background:

1. Edit systemd/btTVH.service lines:

```
ExecStart=/home/mike/.local/bin/btTVH
Environment=PYTHONUNBUFFERED=1
Environment="TVH=user:pwd"
```

You will need to find where pipx has installed your btTVH server command. This probably just a matter of changing "mike" to your user name.

The TVH environment variable also needs to be changed or deleted if you want to be asked for your TVH password every time you want to interact with the TVH server over bluetooth.

Copy to systemd folder:

```
sudo cp systemd/btTVH.service /etc/systemd/system
```

Status can be checked via:

```
systemctl status btTVH
```

We need sudo to start and enable (start at boot time)

```
sudo systemctl start btTVH
sudo systemctl enable btTVH
```
