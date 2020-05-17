import getopt
import sys
import xmlrpc.client


def main(argv):
    userid = ''
    userpass = ''
    serverip = ''

    try:
        opts, args = getopt.getopt(argv, "hu:p:s:", ["userid=", "userpass=", "serverip"])
    except getopt.GetoptError:
        print('addShl.py -u <inputfile> -p <outputfile>')
        sys.exit(2)
    if len(opts) == 0:
        print('addShl.py -u <inputfile> -p <outputfile>')
        sys.exit(2)
    else:
        for opt, arg in opts:
            if opt == '-h':
                print('addShl.py -u <inputfile> -p <outputfile>')
                sys.exit()
            elif opt in ("-u", "--userid"):
                userid = arg
            elif opt in ("-p", "--userpass"):
                userpass = arg
            elif opt in ("-s", "--serverip"):
                serverip = arg

        if not userpass:
            userpass = userid

        if not serverip:
            serverip = 'localhost'

        s = xmlrpc.client.ServerProxy('http://'+serverip+':8000')
        print(s.do_register(userid, userpass))


if __name__ == "__main__":
    main(sys.argv[1:])