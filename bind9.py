import requests
import os
lista='https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling-porn-social/hosts'
r = requests.get(lista, allow_redirects=True)
hosts=r.content.decode()
hosts=hosts.split("\n")
hostlist=[]
for host in hosts:
    if "0.0.0.0 " in host and "#" not in host:
        host=host.replace("0.0.0.0 ", "")
        hostlist.append(host)


def bindhost(host):
    zone='{ type master; notify no; file "null.zone.file"; };'
    host="zone \" IN"+host+"\" "
    return host+zone

def squidhost(host):
    host=host.replace(".","\.")
    host="(^|\.)"+host+"$"
    return host
    
bindhostlist=[]
squidhostlist=[]
hostlist.remove(hostlist[0])
for host in hostlist:
    bindhostlist.append(bindhost(host))
    squidhostlist.append(squidhost(host))

with open("/etc/named/blackhole.zones", 'w') as f:
    for host in bindhostlist:
        f.write(host+"\n")
    f.close
with open('/etc/squid/squid_blackhole.conf', 'w') as f:
    for host in squidhostlist:
        f.write(host+"\n")
    f.close
os.system('rndc reload')
os.system('squid -k reconfigure')
