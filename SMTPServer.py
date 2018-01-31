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
        if re.search('/HELO \w+/', string):
            return True
        return False

    def match_mail_from(self,string):
        string = bytes.decode(string)
        if re.search('/(MAIL FROM: <)\w+(@)\w+(.)\w+(>)/',string):
            return True
        return False

    def match_rcpt(self, string):
        string = bytes.decode(string)
        if re.search('/(RCPT TO: <)\w+(@)\w+(.)\w+(>)/', string):
            return True
        return False

    def match_subject(self, string):
        string = bytes.decode(string)
        if re.search('/Subject: \w*/', string):
            return True
        return False

    def match_from(self, string):
        string = bytes.decode(string)
        if re.search('/From: \w+@\w+.\w+/', string):
            return True
        return False

    def match_to(self, string):
        string = bytes.decode(string)
        if re.search('/To: \w+@\w+.\w+/', string):
            return True
        return False

    def match_empty(self, string):
        string = bytes.decode(string)
        if string == "":
            return True
        return False

    def catch_msg(self, string, client_socket):
        string = bytes.decode(string)
        while string != ".":
            msg = "{}{}".format(msg, string)
            string = client_socket.recv(1024)
            string = bytes.decode(string)
        return

    def client_func(self, client_socket, client_address):

        print("Client ", client_address, " connected")

        #220 Servidor FreddieSMTP
        client_socket.send("220 Servidor FreddieSMTP".encode())
        client_response = client_socket.recv(1024)
        hello = self.match_helo(client_response)
        # HELO something
        while not hello:
            client_socket.send("502 Unrecognized command".encode())
            client_response = client_socket.recv(1024)
            hello = self.match_helo(client_response)
        #250 Yo! pleased to meet ya
        client_socket.send("250 Yo! pleased to meet ya".encode())

        client_response = client_socket.recv(1024)
        mail_from = self.match_mail_from(client_response)
        #MAIL FROM: <SOMETHING@SOMETHING.SOMETHING>
        while not mail_from:
            client_socket.send("502 Unrecognized command".encode())
            client_response = client_socket.recv(1024)
            mail_from = self.match_mail_from(client_response)
        #250 OK
        client_socket.send("250 OK".encode())
        client_response = client_socket.recv(1024)
        recpt_to = self.match_rcpt(client_response)
        #RECPT TO: <SOMETHING@SOMETHING.SOMETHING>
        while not recpt_to:
            client_socket.send("502 Unrecognized command".encode())
            client_response = client_socket.recv(1024)
            recpt_to = self.match_rcpt(client_response)
        #250 OK
        client_socket.send("250 OK".encode())
        client_response = bytes.decode(client_socket.recv(1024))
        #DATA
        while client_response != "DATA":
            client_socket.send("502 Unrecognized command".encode())
            client_response = bytes.decode(client_socket.recv(1024))

        client_socket.send("354 End data with <CR><LF>.<CR><LF>".encode())
        client_response = client_socket.recv(1024)
        mail_subject = self.match_subject(client_response)

        while not mail_subject:
            client_socket.send("502 Unrecognized command".encode())
            client_response = client_socket.recv(1024)
            mail_subject = self.match_subject(client_response)

        client_response = client_socket.recv(1024)
        mail_from = self.match_from(client_response)

        while not mail_from:
            client_socket.send("502 Unrecognized command".encode())
            client_response = client_socket.recv(1024)
            mail_from = self.match_from(client_response)

        client_response = client_socket.recv(1024)
        mail_to = self.match_to(client_response)

        while not mail_to:
            client_socket.send("502 Unrecognized command".encode())
            client_response = client_socket.recv(1024)
            mail_to = self.match_to(client_response)

        #if ( != ):
        # has to validate the to twice

        client_response = client_socket.recv(1024)
        empty = self.match_empty(client_response)

        while not empty:
            client_socket.send("502 Unrecognized command".encode())
            client_response = client_socket.recv(1024)
            empty = self.match_empty(client_response)

        client_response = client_socket.recv(1024)
        self.catch_msg(client_response, client_socket)

        client_socket.send("250 Ok".encode())
        client_response = client_socket.recv(1024)
        client_socket.send("221 Bye".encode())

        print("Closing connection with client: ", client_address)
        client_socket.close()


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