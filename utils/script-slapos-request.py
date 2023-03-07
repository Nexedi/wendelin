selenium_SR_url = "~/srv/project/slapos/software/seleniumserver/software.cfg"

# request instance(s) (they should be 2 or more)
instance = request(selenium_SR_url, "seleniumserver")

instance.getState()
# 'started'

# get a specific parameter info
instance.getConnectionParameter('url')
# 'https://selenium:jvT0SRR9Mtad@[2001:67c:1254:5f:d58a::5933]:9443/wd/hub'

instance.getConnectionParameter('connection-parameters')
# ?? ERROR, not found

# outside python, using slapos client:

slapos service list
#{
#  "seleniumserver": "~/srv/project/slapos/software/seleniumserver/software.cfg"
#}

slapos service info seleniumserver
# dict with all info

