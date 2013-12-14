import os,sys,nfqueue,socket,cherrypy,threading,commands
import subprocess,time
import redis

def runbridge_setup():
	fails, output = commands.getstatusoutput("brctl addbr pibridge")
	if fails:
		print "Error with brctl: " + str(output)
		sys.exit(1)
	fails, output = commands.getstatusoutput("brctl addif pibridge eth1")
	if fails:
		print "Error with brctl: " + str(output)
		sys.exit(1)
	fails, output = commands.getstatusoutput("brctl addif pibridge eth2")
	if fails:
		print "Error with brctl: " + str(output)
		sys.exit(1)

# these methods assume only one iptable rule exists in each chain
def add_filter_rule():
  print "add iprule called"
  if os.system("iptables -C FORWARD -i pibridge -j NFQUEUE --queue-num 0")!=0:
    os.system("iptables -A FORWARD -i pibridge -j NFQUEUE --queue-num 0")

def remove_filter_rule():
  print "remove iprule called"
  if os.system("iptables -C FORWARD -i pibridge -j NFQUEUE --queue-num 0")==0:
    os.system("iptables -D FORWARD 1")
  else:
    print "Warning attempted delete on filter ip rule but rule not found, logic error"

def add_server_rule():
  if os.system("iptables -C INPUT -p tcp --dport 80 -j ACCEPT") !=0:
    os.system("iptables -A INPUT -p tcp --dport 80 -j ACCEPT")


###########################################################################################
# Main Work
###########################################################################################

# System setup checks
print "Checking bridge..."
fails, output = commands.getstatusoutput("ifconfig | grep 'pibridge'")
if fails:
	runbridge_setup()

print "Adding Filter Rule..."
add_filter_rule()
print "Adding Webserver Rule..."
add_server_rule()

# r = redis.StrictRedis(host='localhost', port=6379, db=0)
r = redis.Redis(host='localhost', port=6379, db=0)
# r.flushdb() # flushes entire database

# set some default blocked pages for substance
r.hset("blocked", "www.reddit.com","blah")
r.hset("blocked", "www.woot.com","blah")

r.set("status",True) # true means the filter is running

if len(sys.argv) > 1:
	local_ip   = str(sys.argv[1]) # first arg taken is the local ip on eth0
else:
	local_ip   = '192.168.0.80' # default local ip and the ip the device often gets at home

# w = subprocess.Popen(["python webserver.py", local_ip])

# q = subprocess.Popen(["python queue.py"])

while True:
	time.sleep(1)
	sts = r.get("status")
	if not sts:
		remove_filter_rule()
	if sts:
		add_filter_rule()

















