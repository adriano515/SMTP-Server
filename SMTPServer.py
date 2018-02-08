from multiprocessing import pool

import socket
import sys
import time
import os
import threading
import re

class SMTPServer:

    ok = "250 Ok".encode()
    msg = ""

    def __init__(self, port = 2407):
        self.host = '0.0.0.0'
        self.port = port

    def activate_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print ("Launching SMTP server on ", self.host, ":", self.port)
            self.socket.bind((self.host,self.port))

        except Exception as e:
            print("Error: Could not launch server")
            self.shutdown()
            sys.exit(1)

        print("Server successfully started the socket")
        self._wait_for_connections()

    def shutdown(self):
        try:
            print("Shutting down server")
            socket.socket.shutdown(socket.SHUT_RDWR)

        except Exception as e:
            print("Could not shutdown server, error : ", e)

    def match_helo(self, string):
        string = bytes.decode(string)
        if re.search('HELO \w+', string):
            return True
        return False

    def match_mail_from(self,string):
        string = bytes.decode(string)
        if re.search('(MAIL FROM: <)\w+(@)\w+(.)\w+(>)',string):
            return True
        return False

    def match_rcpt(self, string):
        string = bytes.decode(string)
        if re.search('(RCPT TO: <)\w+(@)\w+(.)\w+(>)', string):
            return True
        return False

    def match_subject(self, string):
        string = bytes.decode(string)
        if re.search('Subject: \w*', string):
            return True
        return False

    def match_from(self, string):
        string = bytes.decode(string)
        if re.search('From: \w+@\w+.\w+', string):
            return True
        return False

    def match_to(self, string):
        string = bytes.decode(string)
        if re.search('To: \w+@\w+.\w+', string):
            return True
        return False

    def match_empty(self, string):
        string = bytes.decode(string)
        if string == "":
            return True
        return False

    def catch_msg(self, string, client_socket):
        string = bytes.decode(string)
        while string != ".\n":

            msg = "{}{}{}".format(msg, string, "\n")
            string = client_socket.recv(1024)
            string = bytes.decode(string)
            print(string)
        return msg

    def send_mail(self, domain, mail_from, rcpt_to, msg):
        dns = socket.gethostbyname(domain)

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect(dns, 2407)

        response = server_socket.recv(1024)
        if("220" not in bytes.decode(response)):
            print ("Server with domain " + domain + "responded with error")
            return
        server_socket.send("HELO uvg.domain.com")
        response = server_socket.recv(1024)
        if ("250" not in bytes.decode(response)):
            print("Server with domain " + domain + "responded with error")
            return
        server_socket.send("MAIL FROM: <" + mail_from + ">")
        response = server_socket.recv(1024)
        if ("250" not in bytes.decode(response)):
            print("Server with domain " + domain + "responded with error")
            return
        server_socket.send("RCPT TO: <" + rcpt_to + ">")
        response = server_socket.recv(1024)
        if ("250" not in bytes.decode(response)):
            print("Server with domain " + domain + "responded with error")
            return
        server_socket.send("DATA")
        response = server_socket.recv(1024)
        if ("250" not in bytes.decode(response)):
            print("Server with domain " + domain + "responded with error")
            return

        msgArray = msg.split("\n")
        for i in msgArray:
            server_socket.send(msgArray[i])
        server_socket.send(".\n")
        response = server_socket.recv(1024)
        if ("250" not in bytes.decode(response)):
            print("Server with domain " + domain + "responded with error")
            return
        server_socket.send("quit")
        response = server_socket.recv(1024)
        server_socket.close()



    def client_func(self, client_socket, client_address):

        to_list = []

        print("Client ", client_address, " connected")

        #220 Servidor FreddieSMTP
        client_socket.send("220 Servidor FreddieSMTP\n".encode())
        client_response = client_socket.recv(1024)
        hello = self.match_helo(client_response)
        # HELO something
        while not hello:
            client_socket.send("502 Unrecognized command\n".encode())
            client_response = client_socket.recv(1024)
            hello = self.match_helo(client_response)
        #250 Yo! pleased to meet ya
        client_socket.send("250 Yo! pleased to meet ya\n".encode())

        client_response = client_socket.recv(1024)
        mail_from = self.match_mail_from(client_response)
        #MAIL FROM: <SOMETHING@SOMETHING.SOMETHING>
        while not mail_from:
            client_socket.send("502 Unrecognized command\n".encode())
            client_response = client_socket.recv(1024)
            mail_from = self.match_mail_from(client_response)
        #250 OK
        client_socket.send("250 OK\n".encode())
        client_response = client_socket.recv(1024)
        recpt_to = self.match_rcpt(client_response)
        to_list.append(recpt_to)
        #RCPT TO: <SOMETHING@SOMETHING.SOMETHING>
        while not recpt_to:
            client_socket.send("502 Unrecognized command\n".encode())
            client_response = client_socket.recv(1024)
            recpt_to = self.match_rcpt(client_response)
        #250 OK
        client_socket.send("250 OK\n".encode())
        client_response = bytes.decode(client_socket.recv(1024))
        #DATA
        while recpt_to:
            client_socket.send("250 OK\n".encode())
            client_response = client_socket.recv(1024)
            recpt_to = self.match_rcpt(client_response)
            to_list.append(recpt_to)

        while client_response != 'DATA\n':
            client_socket.send("502 Unrecognized command\n".encode())
            client_response = bytes.decode(client_socket.recv(1024))

        client_socket.send("354 End data with <CR><LF>.<CR><LF>\n".encode())
        

        #if ( != ):
        # has to validate the to twice

        client_response = client_socket.recv(1024)  
        msg = self.catch_msg(client_response, client_socket)

        client_socket.send("250 Ok\n".encode())
        client_response = client_socket.recv(1024)
        client_socket.send("221 Bye\n".encode())

        print("Closing connection with client: ", client_address)
        client_socket.close()

        for x in to_list:
            domain = to_list[x].split('@')[1]

            self.send_mail(domain,mail_from,to_list[x], msg)


    def _wait_for_connections(self):

        #needs thread pool

        while 1:

            print("Waiting for clients")
            self.socket.listen(5)
            client_socket, client_address = self.socket.accept()

            try:
                thread = threading.Thread(target=self.client_func, args=(client_socket,client_address))
                thread.start()
            except Exception as e:
                print("Unable to create new thread for client ", client_address)



print("Starting server")

server = SMTPServer(2407)
server.activate_server()
