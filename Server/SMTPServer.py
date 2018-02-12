from multiprocessing import pool

import socket
import sys
import re
import pymongo
from queue import Queue
from threading import Thread


class Worker(Thread):
    """ Thread executing tasks from a given tasks queue """
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                # An exception happened in this thread
                print(e)
            finally:
                # Mark this task as done, whether an exception happened or not
                self.tasks.task_done()


class ThreadPool:
    """ Pool of threads consuming tasks from a queue """
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """ Add a task to the queue """
        self.tasks.put((func, args, kargs))

    def map(self, func, args_list):
        """ Add a list of tasks to the queue """
        for args in args_list:
            self.add_task(func, args)

    def wait_completion(self):
        """ Wait for completion of all the tasks in the queue """
        self.tasks.join()

class SMTPServer:
    ok = "250 Ok".encode()
    local_domain = "grupo2.com"
    pool = ThreadPool(5)

    def __init__(self, port=2407, ):
        self.host = (socket.gethostbyname(socket.gethostname()))
        self.port = port

    def activate_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print("Launching SMTP server on ", self.host, ":", self.port)
            self.socket.bind((self.host, self.port))
            print("Initializing DB")

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

    def match_mail_from(self, string):
        string = bytes.decode(string)
        if re.search('(MAIL FROM: <)\w+(@)\w+(.)\w+(>)', string):
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
        msg = ""
        while not re.search('.', string):
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

        if ("220" not in bytes.decode(response)):
            print("Server with domain " + domain + "responded with error")
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

        # 220 Servidor FreddieSMTP
        client_socket.send("220 Servidor FreddieSMTP\n".encode())
        print("Sent 220")
        client_response = client_socket.recv(1024)

        print(client_response)
        hello = self.match_helo(client_response)
        # HELO something
        while not hello:
            client_socket.send("502 Unrecognized command\n".encode())
            print("Sent 502 on HELO")
            client_response = client_socket.recv(1024)
            print(client_response)
            hello = self.match_helo(client_response)
        # 250 Yo! pleased to meet ya
        client_socket.send("250 Yo! pleased to meet ya\n".encode())
        print("Sent 250 on meeting")
        client_response = client_socket.recv(1024)

        mail_from = self.match_mail_from(client_response)

        # MAIL FROM: <SOMETHING@SOMETHING.SOMETHING>
        while not mail_from:
            client_socket.send("502 Unrecognized command\n".encode())
            print("Sent 502 on MAIL")
            client_response = client_socket.recv(1024)
            print(client_response)
            mail_from = self.match_mail_from(client_response)
        # 250 OK
        print(client_response)
        client_socket.send("250 OK\n".encode())
        print("Sent 250 after mail")
        client_response = client_socket.recv(1024)
        print(client_response)
        recpt_to = self.match_rcpt(client_response)

        # RCPT TO: <SOMETHING@SOMETHING.SOMETHING>
        while not recpt_to:
            client_socket.send("502 Unrecognized command\n".encode())
            print("Sent 502 on RCPT")
            client_response = client_socket.recv(1024)
            print(client_response)
            recpt_to = self.match_rcpt(client_response)
        # 250 OK
        to_list.append(bytes.decode(client_response))
        client_socket.send("250 OK\n".encode())
        print("Sent 250 after rcpt")
        client_response = bytes.decode(client_socket.recv(1024))
        print(client_response)

        while self.match_rcpt(client_response.encode()):
            client_socket.send("250 OK\n".encode())
            print("Sent 250 on recpt data")
            client_response = client_socket.recv(1024)
            print(client_response)
            recpt_to = self.match_rcpt(client_response)
            to_list.append(bytes.decode(client_response))
        # DATA
        while client_response != "DATA":
            print("Sent 502 on data")
            client_socket.send("502 Unrecognized command\n".encode())
            client_response = bytes.decode(client_socket.recv(1024))
            print(client_response)

        client_socket.send("354 End data with <CR><LF>.<CR><LF>\n".encode())
        print("Sent 354")

        # if ( != ):
        # has to validate the to twice

        client_response = client_socket.recv(1024)
        print(client_response)
        msg = self.catch_msg(client_response, client_socket)
        print("Finished data")
        client_socket.send("250 Ok\n".encode())
        client_response = client_socket.recv(1024)
        print(client_response)
        client_socket.send("221 Bye\n".encode())

        print("Closing connection with client: ", client_address)
        client_socket.close()

        for i in range(len(to_list)):
            domain = to_list[i].split("@")[1]
            domain = domain.replace(">", "")
            print("domain is " + domain)
            if(domain != self.local_domain):
                self.send_mail(domain, mail_from, to_list[i], msg)
            #else:


    def _wait_for_connections(self):

        while 1:

            print("Waiting for clients")
            self.socket.listen()
            client_socket, client_address = self.socket.accept()

            try:
                pool.add_task(self.client_func, args=(client_socket, client_address))
            except Exception as e:
                print("Unable to create new thread for client ", client_address)


print("Starting server")

server = SMTPServer(2407)
server.activate_server()
