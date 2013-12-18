import os,sys,nfqueue,socket,copy,redis
from scapy.all import *

conf.verbose  = 0
conf.L3socket = L3RawSocket

# redis connection
r = redis.Redis(unix_socket_path='/tmp/redis.sock')

blocked_list = r.hgetall("blocked")

def filter_pkt(payload):
	global blocked_list
	if r.get("change") == "yes": # change detected, reload dict
		blocked_list = r.hgetall("blocked")
		r.set("change","no")
	data = payload.get_data()
	pkt = IP(data)

	if pkt.getlayer(DNS) and pkt[DNS].qd and not pkt[DNS].an:
		print "blocked list"
		print blocked_list
		print "requested dns"
		print pkt[DNS].qd.qname
		if pkt[DNS].qd.qname in blocked_list:
			print "domain found in block list"
			# self.redirect(data)
			payload.set_verdict(nfqueue.NF_DROP)

	payload.set_verdict(nfqueue.NF_ACCEPT)

q = nfqueue.queue()
q.open()
q.bind(socket.AF_INET)
q.set_callback(filter_pkt)
q.create_queue(0)
q.try_run()