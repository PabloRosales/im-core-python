#!/usr/bin/env python

import sys, os, time, atexit
import logging
from signal import SIGTERM 
from im.core.config import conf

logger = logging.getLogger('im.core.utils.daemon')

class Daemon(object):
    """
    A generic daemon class.
    
    Usage: subclass the Daemon class and override the run() method
    Original: http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
    """
    def __init__(self, name, interval=5, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null', piddir='/tmp/daemons/'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.name = name
        self.pidfile = name + ".pid"
        self.interval = interval
        self.piddir = piddir
    
    def daemonize(self):
        """
        UNIX double-fork magic
        
        Original: "Advanced Programming in the UNIX Environment"  (ISBN 0201563177)
        """
        try: 
            pid = os.fork() 
            if pid > 0:
                sys.exit(0) 
        except OSError, e: 
            logger.error("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
    
        os.chdir("/") 
        os.setsid() 
        os.umask(0) 
    
        try: 
            pid = os.fork() 
            if pid > 0:
                sys.exit(0) 
        except OSError, e: 
            logger.error("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1) 
    
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
    
        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.piddir + self.pidfile,'w+').write("%s\n" % pid)

    
    def delpid(self):
        os.remove(self.piddir + self.pidfile)

    def getpid(self):
        try:
            if not os.path.exists(self.piddir):
                os.makedirs(self.piddir)
                
            pf = file(self.piddir + self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        return pid

    def start(self):
        """
        Start the daemon
        """
        logger.debug("Starting %s..." % self.name)
        
        self.before_start()

        pid = self.getpid()
    
        if pid:
            message = "Could not start %s, pid file %s already exist. Daemon already running?\n"
            logger.error(message % (self.name, self.pidfile))
            sys.exit(1)
        
        # Start the daemon
        self.daemonize()
        
        logger.info("%s daemon started" % self.name)
        self.run()

    def stop(self, restart=False):
        """
        Stop the daemon
        """
        logger.debug("Stopping %s..." % self.name)

        self.before_stop()

        # Get the pid from the pidfile
        pid = self.getpid()
    
        if not pid:
            if not restart:
                message = "Could not stop %s, pid file %s does not exist. Daemon not running?\n"
                logger.error(message % (self.name, self.pidfile))
            return

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, SIGTERM)
                logger.warn("killing %s " % pid)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                logger.info("%s daemon stopped" % self.name)
                if os.path.exists(self.piddir + self.pidfile):
                    os.remove(self.piddir + self.pidfile)
            else:
                print str(err)
                sys.exit(1)

    def stat(self):
        """
        Stat the daemon
        """

        # Get the pid from the pidfile
        pid = self.getpid()
    
        if not pid:
            message = "%s not running"
            logger.info(message % self.name)
            return False
        else:
            message = "%s running in pid %s"
            logger.info(message % (self.name, pid))
            return True

    def restart(self):
        """
            Restart the daemon
        """
        self.stop(True)
        self.start()

    def run(self):
        """
            Main loop
        """ 
        while True:
            self.task()
            time.sleep(self.interval)
        
    def task(self):
        """
            Override this method
        """ 
        logger.warn("Task not implemented")

    def parse_args(self):
        if len(sys.argv) == 2:
            if 'start' == sys.argv[1]:
                self.start()
            elif 'stop' == sys.argv[1]:
                self.stop()
            elif 'restart' == sys.argv[1]:
                self.restart()
            elif 'stat' == sys.argv[1]:
                self.stat()
            else:
                print "Unknown command"
                sys.exit(2)
            sys.exit(0)
        else:
            print "usage: %s start|stop|restart|start" % sys.argv[0]
            sys.exit(2)

    def before_start(self):
        pass

    def before_stop(self):
        pass

