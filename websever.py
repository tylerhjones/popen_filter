import os,sys,socket,cherrypy,redis

from multiprocessing import Process
from mako.template import Template
from mako.lookup import TemplateLookup

if len(sys.argv) > 1:
	local_ip   = str(sys.argv[1]) # first arg taken is the local ip on eth0
else:
	local_ip   = '192.168.0.80' # default local ip and the ip the device often gets at home

cherrypy.config.update({'server.socket_host': local_ip, 
                         'server.socket_port': 80, 
                        }) 

# mako template directory
lookup = TemplateLookup(directories=['views'])

class FilterServ(object):
  @cherrypy.expose
  def index(self):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    blocked_list = r.hgetall("blocked")
    filter_status = r.get("status")

    # default index page
    tmpl = lookup.get_template("index.html")
    return tmpl.render(block_list=blocked_list, status=filter_status)


  def add_block(self, url=None):
    print "ADDing URL ... "
    filt.add_url_to_list(url)
    filt.restart()
    tmpl = lookup.get_template("index.html")
    return tmpl.render(block_list=filt.blocked_list, status=filter_status)
  add_block.exposed = True

  def toggle(self):
    print "toggle function"
    toggler()
    tmpl = lookup.get_template("index.html")
    return tmpl.render(block_list=filt.blocked_list, status=filter_status)  
  toggle.exposed = True   

  def remove(self, url=None, key=None):
    filt.remove_url(key)
    filt.restart()
    tmpl = lookup.get_template("index.html")
    return tmpl.render(block_list=filt.blocked_list, status=filter_status) 
  remove.exposed = True  

print "Starting cherrypy server..."

try:
	cherrypy.quickstart(FilterServ())
except KeyboardInterrupt:
	print "Exiting..."
	fq.terminate()
	sys.exit(1)