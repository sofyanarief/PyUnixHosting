import getopt
import sys
import xmlrpc.client


def main(argv):
    userid = ''
    userpass = ''
    serverip = ''
    mode = ''

    try:
        opts, args = getopt.getopt(argv, "hu:p:s:m:", ["userid=", "userpass=", "serverip", "mode"])
    except getopt.GetoptError:
        print('Client.py -u <inputfile> -p <outputfile> -s <serverip> -m <mode>')
        sys.exit(2)
    if len(opts) == 0:
        print('Client.py -u <inputfile> -p <outputfile> -s <serverip> -m <mode>')
        sys.exit(2)
    else:
        for opt, arg in opts:
            if opt == '-h':
                print('Client.py -u <inputfile> -p <outputfile> -s <serverip> -m <mode>')
                sys.exit()
            elif opt in ("-u", "--userid"):
                userid = arg
            elif opt in ("-p", "--userpass"):
                userpass = arg
            elif opt in ("-s", "--serverip"):
                serverip = arg
            elif opt in ("-m", "--mode"):
                mode = arg

        if not mode:
            print('You must specify mode with -m option')
            sys.exit(2)

        if not serverip:
            print('You must specify server\'s ip with -s option')
            sys.exit(2)

        if not userpass:
            userpass = userid

        s = xmlrpc.client.ServerProxy('http://' + serverip + ':8000')
        if mode is 'reg':
            print(s.do_register(userid, userpass))
        elif mode is 'unreg':
            print(s.do_unregister(userid, userpass))
        else:
            print('You must enter valid mode [reg|unreg] in -m option')
            sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
