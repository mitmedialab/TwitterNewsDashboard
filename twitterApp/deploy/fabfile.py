# Import Fabric's API module
from fabric.api import *


env.hosts = [
    '127.0.0.1:2222',
  # 'ip.add.rr.ess
  # 'server2.domain.tld',
]
# Set the username
env.user   = "vagrant"

# Set the password [NOT RECOMMENDED]
env.password = "vagrant"

project_dir = "/path/to/project"

#def create_project_dir():
#  run("mkdir {0}".format(project_dir))

def share_credentials_with_host():
  put("<<PATH>>/TwitterNewsDashboard/twitterApp/twitterConfig.json", "/home/vagrant/TwitterNewsDashboard/twitterApp/")

def checkout_from_github():
  run("git clone https://github.com/c4fcm/TwitterNewsDashboard.git")
  
def install_software():
  checkout_from_github()
#  share_credentials_with_host()
  

def launch_software():
  with cd("/home/vagrant/TwitterNewsDashboard/twitterApp/"):
    run("gunicorn -w 15 -b 0.0.0.0:8000 twitterUpdate:app")

def stop_software():
  pass # DO SOMETHING HERE, some gunicorn command to take it down

def reload_software():
  stop_software()
  launch_software()
