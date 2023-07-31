from .api import setUSR,subs,inputs,nxt
import sys
import time
from socket import gethostbyname,gaierror

def timeform(t):return time.strftime("%a, %d %b %Y %H:%M", time.localtime(t))

def ip4():
    try:
        return "Host: rpiz3 @ IPv4: "+gethostbyname("rpiz3.local")+"\n"
    except gaierror:
        return "Host: rpiz3 not responding\n"

def state():
    lines=[]
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
    return '\n'.join(lines)+"\n"
