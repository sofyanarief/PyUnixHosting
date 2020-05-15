#!/usr/bin/python

import socket
import subprocess
from SimpleXMLRPCServer import SimpleXMLRPCServer


class Server:

    def doRegister(self,userid, userpass):
        ret = 'err'
        ret = self.addUnixUser(userpass,userpass)
        return ret

    def doUnregister(self):
        ret = 'err'
        return ret

    def addUnixUser(self, userid, userpass):
        print userpass
        # shl = subprocess.Popen("sudo mkdir /" + userid, shell=True, stdout=subprocess.PIPE,)
        # stdout = shl.communicate()
        try:
            subprocess.check_call('sudo mkdir /' + userid, shell=True)
        except subprocess.CalledProcessError:
            return 'err'
        else:
            return 'done'
        # There was an error - command exited with non-zero code
        # if stdout[1] != 'None':
        #     return 'err'
        # else:
        #     return 'done'


hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

server = SimpleXMLRPCServer((IPAddr, 8000), logRequests=True, allow_none=True);
server.register_multicall_functions()
server.register_instance(Server())

try:
    print('Use Control-C to exit')
    print('Your Computer IP Address is:' + IPAddr)
    server.serve_forever()
except KeyboardInterrupt:
    print('Exiting')
