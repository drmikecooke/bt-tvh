from .api import subs,inputs,nxt
import sys
import time
from socket import gethostbyname,gaierror,gethostname

def timeform(t):return time.strftime("%a, %d %b %Y %H:%M", time.localtime(t))

def ip4(host):
    try:
        ip=gethostbyname(host)
        if ip[:3]=="127":
            noWifi="NOT a wifi connection. Down?\n"
            return f"Host: {host} @ IPv4: {ip}\n"+noWifi                
        return f"Host: {host} @ IPv4: "+ip+"\n"
    except gaierror:
        return f"Host {host} not responding\n"

def state():
    lines=[]
    try:
        for item in subs():
            lines+=[' '*12+item]
        errs=inputs()
        lines+=[' '*12+errs["input"]]
        del errs["input"]
        nzerrs={key:errs[key] for key in errs if errs[key]>0}
        if nzerrs:
            lines+=[' '*12+str(nzerrs)]
        start,stop=nxt()
        if not start:
            lines+[' '*12+'No recordings scheduled']
            sys.exit(0)
        if start<time.time():
            lines+=[' '*12+f'first stop at {timeform(stop)}']
        else:
            lines+=[' '*12+f'next start at {timeform(start)}']
            if start-time.time()>1800:
                alarm=timeform(start-1800) # half hour prep
                lines+=[' '*12+f'ALARM for {alarm}']
    except:
        print("Error: user details?")
        lines=["Error: user details?"]
    return '\n'.join(lines)+"\n"
