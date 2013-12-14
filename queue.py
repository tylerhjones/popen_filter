import os,sys,nfqueue,socket,copy
from scapy.all import *
import redis

conf.verbose  = 0
conf.L3socket = L3RawSocket

# redis connection
r = redis.StrictRedis(host='localhost', port=6379, db=0)

def filter_pkt(self, payload):
	blocked_list = r.hgetall("blocked") # gets the blocked list from the db returned as a dictionary
	data = payload.get_data()
	pkt = IP(data)

	if pkt.getlayer(DNS) and pkt[DNS].qd and not pkt[DNS].an:
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