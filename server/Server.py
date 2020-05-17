import socket
import subprocess
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

hostname = socket.gethostname()
IpAddress = socket.gethostbyname(hostname)


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


# Create server
with SimpleXMLRPCServer((IpAddress, 8000),
                        requestHandler=RequestHandler) as server:
    server.register_introspection_functions()


    class Server:
        def __init__(self):
            self.userId = ''
            self.userPass = ''
            self.stepDone = []
            # self.mydb = mydb = mysql.connector.connect(
            #     host="localhost",
            #     user="yourusername",
            #     passwd="yourpassword"
            # )
            pass

        def do_register(self, userid, userpass):
            ret = ''
            self.userId = userid
            self.userPass = userpass
            # if self.add_unix_user() == 'done':
            #     self.stepDone.append('Step1')
            # else:
            #     ret = 'err_add_unix_user'
            return self.add_unix_user()

        def do_unregister(self, mode):
            ret = ''
            if mode is 'rollback':
                print('rollback')
            else:
                print('normal')
            return ret

        def add_unix_user(self):
            try:
                # subprocess.check_call(
                #     'useradd -p $(openssl passwd -1 '+self.userPass+') -m -U -s /bin/bash '+self.userId,
                #     shell=True)
                subprocess.check_call(
                    'mkdir /' + self.userId,
                    shell=True
                )
            except subprocess.CalledProcessError:
                return 'err'
            else:
                return 'done'

        def add_mysql_database(self):
            try:
                subprocess.check_call(
                    'echo "CREATE DATABASE ' + self.userId + ';" | mysql -u root', shell=True)
            except subprocess.CalledProcessError:
                return 'err'
            else:
                return 'done'

        def add_mysql_user(self):
            try:
                subprocess.check_call(
                    'sudo useradd -p $(openssl passwd -1 ' + self.userPass + ') -m -U -s /bin/bash ' + self.userId,
                    shell=True)
            except subprocess.CalledProcessError:
                return 'err'
            else:
                return 'done'


    server.register_instance(Server())

    # Run the server's main loop
    try:
        print('Use Control-C to exit')
        print('Your Computer IP Address is:' + IpAddress)
        server.serve_forever()
    except KeyboardInterrupt:
        print('Exiting')
