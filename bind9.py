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
    zone='IN { type master; notify no; file "/etc/named/null.zone.file"; };'
    host="zone \""+host+"\" "
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
        f.write(host.replace("_","-")+"\n")
    f.close
with open('/etc/squid/squid_blackhole.conf', 'w') as f:
    for host in squidhostlist:
        f.write(host+"\n")
    f.close
with open('/etc/named/null.zone.file', 'w') as f:
    f.write("""; BIND db file for ad servers - point all addresses to an invalid IP
$TTL	864000	; ten days

@       IN      SOA     ns0.example.net.      hostmaster.example.net. (
                        2008032800       ; serial number YYMMDDNN
                        288000   ; refresh  80 hours
                        72000    ; retry    20 hours
                        8640000  ; expire  100 days
                        864000 ) ; min ttl  10 day
                NS      ns0.example.net.

		A	0.0.0.0

*		IN      A       0.0.0.0


""")
    f.close

os.system('rndc reload')
os.system('squid -k reconfigure')
