#!/usr/bin/python

import sys, getopt
import xmlrpclib


def main(argv):
    userid = ''
    userpass = ''
    try:
        opts, args = getopt.getopt(argv, "hu:p:", ["userid=", "userpass="])
    except getopt.GetoptError:
        print 'addShl.py -u <inputfile> -p <outputfile>'
        sys.exit(2)
    if len(opts) == 0:
        print 'addShl.py -u <inputfile> -p <outputfile>'
        sys.exit(2)
    else:
        for opt, arg in opts:
            if opt == '-h':
                print 'addShl.py -u <inputfile> -p <outputfile>'
                sys.exit()
            elif opt in ("-u", "--userid"):
                userid = arg
            elif opt in ("-p", "--userpass"):
                userpass = arg
        if not userpass:
            userpass = userid

        server = xmlrpclib.ServerProxy('http://192.168.1.21:8000')
        multi = xmlrpclib.MultiCall(server)
        multi.doRegister(userid, userpass)
        for response in multi():
            print(response)


if __name__ == "__main__":
    main(sys.argv[1:])
