Dependencies
============

Front-end
---------

typeahead.js: https://twitter.github.io/typeahead.js/
handlebars.js: http://handlebarsjs.com/



apt-get install uwsgi-plugin-python3


$ cat /etc/init/uwsgi.conf 
description "uWSGI"
start on runlevel [2345]
stop on runlevel [06]
respawn

env UWSGI=/usr/local/bin/uwsgi
# /home/apps/gdb_venv/bin/uwsgi
env LOGTO=/var/log/uwsgi/emperor.log

# exec $UWSGI --master --emperor /etc/uwsgi/vassals --die-on-term --uid apps --gid apps --logto $LOGTO
exec $UWSGI --master --emperor /etc/uwsgi/apps-enabled --die-on-term --uid apps --gid apps --logto $LOGTO

$ sudo mkdir -p /var/log/uwsgi
$ sudo mkdir -p /etc/uwsgi/apps-available
$ sudo mkdir -p /etc/uwsgi/apps-enabled

$ sudo service uwsgi start


$ cat /etc/uwsgi/apps-available/wordbook.ini


[uwsgi]
# Variables
base=/home/apps/apps/wordbook
app = app
# Generic Config
plugins = http,python
home = /home/apps/venv_wordbook
pythonpath = %(base)
socket = /var/www/run/%n.sock
module = %(app)
logto = /var/log/uwsgi/%n.log

$ ln -s /etc/uwsgi/apps-available/wordbook.ini /etc/uwsgi/apps-enabled/wordbook.ini

cat /etc/nginx/sites-available/words.lizardschool.pl 
server {
    #if ($host !~ ^(words.lizardschool.pl)$ ) {
            # return 418;
                    #}
                    
                        listen 80;
                            server_name words.lizardschool.pl;
                                charset utf-8;
                                    client_max_body_size 2M;
                                            root /home/apps/apps/wordbook;
                                                access_log /var/log/nginx/words.lizardschool.pl-access.log;
                                                    error_log /var/log/nginx/words.lizardschool.pl-error.log;
                                                    
                                                        auth_basic "Restricted";
                                                            # htpasswd -c /etc/nginx/.htpasswd-words.lizardschool.pl matee
                                                                auth_basic_user_file /etc/nginx/.htpasswd-words.lizardschool.pl;
                                                                
                                                                    location ^ /static/  {
                                                                            alias /home/apps/apps/wordbook/wordbook/flaskapp/static/;
                                                                                    include /etc/nginx/gzip.conf;
                                                                                            expires 7d;
                                                                                                }
                                                                                                
                                                                                                    location / {
                                                                                                                include uwsgi_params;
                                                                                                                            uwsgi_pass unix:/var/www/run/wordbook.sock;
                                                                                                                                    }
                                                                                                                                    }




nginx -t

service nginx restart
