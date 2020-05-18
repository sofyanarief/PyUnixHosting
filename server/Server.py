import socket
import subprocess
import mysql
from mysql.connector import errorcode
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
            self.mysqlHost = 'localhost'
            self.mysqlUser = 'api'
            self.mysqlPass = '0joMlebu!'
            pass

        def do_register(self, userid, userpass):
            ret = ''
            self.userId = userid
            self.userPass = userpass
            if self.add_unix_user() == 'done':
                if self.add_mysql_database() == 'done':
                    if self.add_mysql_user() == 'done':
                        if self.add_mysql_privileges() == 'done':
                            ret = 'done'
                        else:
                            flag = 'err'
                            while flag == 'err':
                                flag = self.del_mysql_user()
                            flag = 'err'
                            while flag == 'err':
                                flag = self.del_mysql_database()
                            flag = 'err'
                            while flag == 'err':
                                flag = self.del_unix_user()
                            ret = 'err_add_mysql_privileges'
                    else:
                        flag = 'err'
                        while flag == 'err':
                            flag = self.del_mysql_database()
                        flag = 'err'
                        while flag == 'err':
                            flag = self.del_unix_user()
                        ret = 'err_add_mysql_user'
                else:
                    flag = 'err'
                    while flag == 'err':
                        flag = self.del_unix_user()
                    ret = 'err_add_mysql_database'
            else:
                ret = 'err_add_unix_user'
            return ret

        def do_unregister(self, userid, userpass):
            ret = ''
            self.userId = userid
            self.userPass = userpass
            if self.del_unix_user() == 'done':
                if self.del_mysql_privileges() == 'done':
                    if self.del_mysql_user() == 'done':
                        if self.del_mysql_database() == 'done':
                            ret = 'done'
                        else:
                            flag = 'err'
                            while flag == 'err':
                                self.add_mysql_user()
                            flag = 'err'
                            while flag == 'err':
                                self.add_mysql_privileges()
                            flag = 'err'
                            while flag == 'err':
                                self.add_unix_user()
                            ret = 'err_del_mysql_database'
                    else:
                        flag = 'err'
                        while flag == 'err':
                            self.add_mysql_privileges()
                        flag = 'err'
                        while flag == 'err':
                            self.add_unix_user()
                        ret = 'err_del_mysql_user'
                else:
                    flag = 'err'
                    while flag == 'err':
                        self.add_unix_user()
                    ret = 'err_del_mysql_privileges'
            else:
                ret = 'err_del_unix_user'
            return ret

        def add_unix_user(self):
            try:
                subprocess.check_call(
                    'useradd -p $(openssl passwd -1 '+self.userPass+') -m -U -s /bin/bash '+self.userId,
                    shell=True)
            except subprocess.CalledProcessError:
                return 'err'
            else:
                return 'done'

        def del_unix_user(self):
            try:
                subprocess.check_call(
                    'deluser '+self.userId+' && rm -Rf /home/'+self.userId,
                    shell=True)
            except subprocess.CalledProcessError:
                return 'err'
            else:
                return 'done'

        def check_mysql_conn(self):
            try:
                conn = mysql.connector.connect(
                    host=self.mysqlHost,
                    user=self.mysqlUser,
                    passwd=self.mysqlPass,
                )
            except mysql.connector.Error as err:
                return ['done', conn]
            else:
                conn.close()
                return ['err', '']

        def add_mysql_database(self):
            conn = self.check_mysql_conn()
            if conn[0] == 'done':
                conn = conn[1]
                cursor = conn.cursor()
                try:
                    cursor.execute(
                        'USE DATABASE ' + self.userId + ';'
                    )
                except mysql.connector.Error as err:
                    try:
                        cursor.execute(
                            'CREATE DATABASE ' + self.userId + ';'
                        )
                    except mysql.connector.Error as err:
                        conn.close()
                        return 'err'
                    else:
                        conn.close()
                        return 'done'
                else:
                    conn.close()
                    return 'done'
            else:
                return 'err'

        def del_mysql_database(self):
            conn = self.check_mysql_conn()
            if conn[0] == 'done':
                conn = conn[1]
                cursor = conn.cursor()
                try:
                    cursor.execute(
                        'USE DATABASE ' + self.userId + ';'
                    )
                except mysql.connector.Error as err:
                    conn.close()
                    return 'done'
                else:
                    try:
                        cursor.execute(
                            'DROP DATABASE ' + self.userId + ';'
                        )
                    except mysql.connector.Error as err:
                        conn.close()
                        return 'err'
                    else:
                        conn.close()
                        return 'done'
            else:
                return 'err'


        def add_mysql_user(self):
            conn = self.check_mysql_conn()
            if conn[0] == 'done':
                conn = conn[1]
                cursor = conn.cursor()
                try:
                    cursor.execute(
                        'CREATE USER \''+ self.userId +'\'@\'localhost\' IDENTIFIED BY \''+self.userPass+'\';'
                    )
                except mysql.connector.Error as err:
                    conn.close()
                    return 'err'
                else:
                    conn.close()
                    return 'done'
            else:
                conn.close()
                return 'err'

        def del_mysql_user(self):
            conn = self.check_mysql_conn()
            if conn[0] == 'done':
                conn = conn[1]
                cursor = conn.cursor()
                try:
                    cursor.execute(
                        'DROP USER \'' + self.userId + '\'@\'localhost\';'
                    )
                except mysql.connector.Error as err:
                    conn.close()
                    return 'err'
                else:
                    conn.close()
                    return 'done'
            else:
                return 'err'

        def add_mysql_privileges(self):
            conn = self.check_mysql_conn()
            if conn[0] == 'done':
                conn = conn[1]
                cursor = conn.cursor()
                try:
                    cursor.execute(
                        'GRANT ALL PRIVILEGES ON '+ self.userId +' . * TO \''+ self.userId +'\'@\'localhost\';'
                    )
                except mysql.connector.Error as err:
                    conn.close()
                    return 'err'
                else:
                    try:
                        cursor.execute(
                            'FLUSH PRIVILEGES;'
                        )
                    except mysql.connector.Error as err:
                        conn.close()
                        return 'err'
                    else:
                        conn.close()
                        return 'done'
            else:
                return 'err'

        def del_mysql_privileges(self):
            conn = self.check_mysql_conn()
            if conn[0] == 'done':
                conn = conn[1]
                cursor = conn.cursor()
                try:
                    cursor.execute(
                        'REVOKE ALL PRIVILEGES ON '+ self.userId +' . * FROM \''+ self.userId +'\'@\'localhost\';'
                    )
                except mysql.connector.Error as err:
                    conn.close()
                    return 'err'
                else:
                    try:
                        cursor.execute(
                            'FLUSH PRIVILEGES;'
                        )
                    except mysql.connector.Error as err:
                        conn.close()
                        return 'err'
                    else:
                        conn.close()
                        return 'done'
            else:
                return 'err'

    server.register_instance(Server())

    # Run the server's main loop
    try:
        print('Use Control-C to exit')
        print('Your Computer IP Address is:' + IpAddress)
        server.serve_forever()
    except KeyboardInterrupt:
        print('Exiting')
