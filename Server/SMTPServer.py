import pprint
from multiprocessing import pool

import socket
import sys
import re
from pymongo import MongoClient
from queue import Queue
from threading import Thread
from bson.json_util import dumps


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
    pool = ThreadPool(5)   #threadsafe?
    client = MongoClient()
    client2 = MongoClient()
    server_db = client.domainEmails
    client_db = client2.users


    def __init__(self, port=2407, ):
        self.host = (socket.gethostbyname(socket.gethostname()))
        self.port_smtp = 2407
        self.port_pop3 = 2000

    def activate_server(self):
        self.socket_smtp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_pop3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print("Launching SMTP server on ", self.host, ":", self.port_smtp)
            self.socket_smtp.bind((self.host, self.port_smtp))

        except Exception as e:
            print("Error: Could not launch smtp server")
            self.shutdown(self.socket_smtp)
            #sys.exit(1)

        try:
            print("Launching Pop3 server on ", self.host, ":", self.port_pop3)
            self.socket_pop3.bind((self.host, self.port_pop3))

        except Exception as e:
            print("Error: Could not launch pop3 server", e)
            self.shutdown(self.socket_pop3)
          #  sys.exit(1)


        smtp_thread = Thread(target = self._wait_for_connections, args = (self.socket_smtp, "smtp"))
        smtp_thread.start()
        self._wait_for_connections(self.socket_pop3, "pop3")

    def shutdown(self, socket_prot):
        try:
            print("Shutting down server")
            socket_prot.shutdown(socket.SHUT_RDWR)

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

    def match_parameter(self, str_to_match, str_to_test):
        string = bytes.decode(str_to_test)
        if re.search(str_to_match, string):
            return True
        return False

    def catch_msg(self, string, client_socket):
        #isnt saving spaces
        string = bytes.decode(string)
        msg = ""
        while not re.search('^\.$', string):
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

        print("Client ", client_address, " connected to smtp server")

        # 220 Servidor FreddieSMTP
        client_socket.send("220 Servidor SMTP\n".encode())
        print("Sent 220")
        client_response = client_socket.recv(1024)

        print(bytes.decode(client_response))
        hello = self.match_helo(client_response)
        # HELO something
        while not hello:
            client_socket.send("502 Unrecognized command\n".encode())
            print("Sent 502 on HELO")
            client_response = client_socket.recv(1024)
            print(bytes.decode(client_response))
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
            print(bytes.decode(client_response))
            mail_from = self.match_mail_from(client_response)
        # 250 OK
        mail_from = bytes.decode(client_response).strip().split("<")[1].replace(">","")
        print(bytes.decode(client_response))
        client_socket.send("250 OK\n".encode())
        print("Sent 250 after mail")
        client_response = client_socket.recv(1024)
        print(bytes.decode(client_response))
        recpt_to = self.match_rcpt(client_response)

        # RCPT TO: <SOMETHING@SOMETHING.SOMETHING>
        while not recpt_to:
            client_socket.send("502 Unrecognized command\n".encode())
            print("Sent 502 on RCPT")
            client_response = client_socket.recv(1024)
            print(bytes.decode(client_response))
            recpt_to = self.match_rcpt(client_response)
        # 250 OK
        to_list.append(bytes.decode(client_response).strip().split("<")[1].replace(">",""))
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
            to_list.append(bytes.decode(client_response).strip().split("<")[1].replace(">",""))
        # DATA
        while not re.search('^DATA$', client_response):
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
            domain = domain.strip()
            print("domain is " + domain)
            if(domain != self.local_domain):
                print("not local domain, trying to send msg to domain ", domain)
                self.send_mail(domain, mail_from, to_list[i], msg)
            else:
                print("self domain, storing message")

                collection = self.server_db[to_list[i]]
                if (collection.count() != 0):

                    post = dict(
                            From = mail_from,
                            To = to_list[i],
                            Subject = "test",
                            Date = "date",
                            Data = msg,
                    )

                    post_id = collection.insert_one(post).inserted_id
                #else:
                ##################################
                #send message to email : from saying email : to_list[i] doesnt exist.


    def transaction_0(self, user, number):
        #list
        collection = self.server_db[user]
        if (collection.count() != 0):
            docs = collection.find({},{'_id':False})
            for x in docs:
                dump = dumps(x)
                byte_size = len(dump)
        print(user, " petition: list")
        return True
    def transaction_1(self, user, number):
        #retr
        print(user ," petition: retr ", number)
        return True
    def transaction_2(self, user, number):
        #dele
        print(user, " petition: retr ", number)
        return True
    def transaction_3(self, user, number):
        #quit
        print(user, " petition: quit")
        return False

    def match_transaction(self, string, user):
        number = 0
        string = bytes.decode(string)
        action = re.findall('(list)|(retr \d)|(dele \d)|(quit)', string)

        for x in range(len(action[0])):
            if (len(action[0][x]) > 1):
                method_name = 'transaction_' + str(x)
                method = getattr(self, method_name, lambda: "nothing")

                if (x == 1 or x == 2):
                    numbers = [int(s) for s in string.split() if s.isdigit()]
                    number = numbers[0]
                return method(user,number)
        return




    def check_usr(self, user, password):
        collection = self.client_db[user]
        if (collection.count() != 0):
            if collection.find_one({ "pwd":password}):
                return True
            return False
        else:
            return False

    def register_usr(self,user, password):
        collection = self.client_db[user]
        print(user)
        print(collection.count())
        if (collection.count() == 0):
            post = dict(
                user=user,
                pwd=password
            )

            post_id = collection.insert_one(post).inserted_id


    def pop3_server(self, client_socket, client_address):

        self.register_usr("test@grupo2.com", "test")

        print("Client ", client_address, " connected to pop3 server")

        client_socket.send("+OK POP3 server ready\n".encode())
        print("Sent +OK server ready")
        client_response = client_socket.recv(1024)
        print(bytes.decode(client_response))

        while not(self.match_parameter('user \w+', client_response)):
            print("Error on user")
            client_socket.send("-ERR user\n".encode())
            client_response = client_socket.recv(1024)
            print(bytes.decode(client_response))

        user = bytes.decode(client_response).split(" ")[1].strip()
        client_socket.send("+OK\n".encode())
        print("Sent +OK user")
        client_response = client_socket.recv(1024)
        print(bytes.decode(client_response))

        while not(self.match_parameter('pass \w+', client_response)):
            print("Error on pass")
            client_socket.send("-ERR pass\n".encode())
            client_response = client_socket.recv(1024)
            print(bytes.decode(client_response))

        password = bytes.decode(client_response).split(" ")[1].strip()

        if not (self.check_usr(user, password)):
            print("Error on authentication")
            client_socket.send("-ERR authenticating\n".encode())
            # -----------------------------------------------------------
            # should we close connection here? should the server restart?, currently only closing connection
            # -----------------------------------------------------------
            print(bytes.decode(client_response))
            return

        client_socket.send("+OK user successfully logged on\n".encode())
        print("Sent +OK authenticated")


        #---------Transaction Phase-------------
        on = True
        while on:
            client_response = client_socket.recv(1024)
            print("got from user ",client_response ," ", bytes.decode(client_response))
            on = self.match_transaction(client_response, user)
        print("client: ", client_address, " closed connection on pop3")



    def _wait_for_connections(self,socket_prot, string):
        print("Waiting for clients on socket " , string)
        while 1:

            socket_prot.listen(5)
            client_socket, client_address = socket_prot.accept()

            try:
                if("smtp" in string):
                    self.pool.add_task(self.client_func, client_socket, client_address)
                elif ("pop3" in string):
                    self.pool.add_task(self.pop3_server, client_socket, client_address)
            except Exception as e:
                print("Unable to create new thread for client ", client_address, e)
            print("Waiting for clients")

print("Starting server")

server = SMTPServer(2407)
server.activate_server()
