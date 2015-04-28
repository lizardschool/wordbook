arbiter = "egg:gunicorn"   # The arbiter to use for worker management
backlog = 512              # The listen queue size for the server socket
bind = "unix:/home/apps/var/run/wordbook.sock"     # Or "unix:/tmp/gunicorn.sock"
daemon = False            # Whether work in the background
debug = True              # Some extra logging
keepalive = 5             # Time we wait for next connection (in seconds)
logfile = '/home/apps/var/log/wordbook-gunicorn.log'               # Name of the log file
loglevel = "info"         # The level at which to log
pidfile = '/home/apps/var/run/wordbook-gunicorn.pid'              # Path to a PID file
workers = 2               # Number of workers to initialize
umask = 0                 # Umask to set when daemonizing
user = 'apps'                 # Change process owner to user
group = 'apps'              # Change process group to group
proc_name = 'wordbook_gunicorn'            # Change the process name
tmp_upload_dir = 'tmp'       # Set path used to store temporary uploads
worker_connections = 100     # Maximum number of simultaneous connections
timeout = 30                #

after_fork = lambda server, worker: server.log.info("Worker spawned (pid: {pid})".format(pid=worker.pid))
before_fork = lambda server, worker: server.log.info("Forking (pid: {pid})".format(pid=worker.pid))
before_exec = lambda server: server.log.info("Forked child, reexecuting")
