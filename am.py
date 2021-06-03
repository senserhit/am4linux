import socket
import re
import uuid

PORT = 5001
SERVER = "192.168.103.249"
ADDRESS = (SERVER, PORT)
FORMAT = "gbk"

class AM:
    def __init__(self, user, passwd, user_id):
        self.user = user
        self.passwd = passwd
        self.user_id = user_id
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(ADDRESS)
        except socket.error as err:
            print(err)
            raise
        else:
            self.my_ip =  self.client.getsockname()[0]
            self.my_mac = "08:00:27:AF:9A:FE"

    def login(self):
        try:
            msg = "LGI 1 {name} {id} \nmacaddr: {mac}\napptype: AM\nlocalip: {ip}\n\n".format(name=self.user,id=self.user_id,
            mac=self.my_mac, ip=self.my_ip)
            self.client.sendall(msg.encode(FORMAT))
            data = self.client.recv(1024) #LGI 1\n\n
            msg = "USR 2 NON I {name} {id}  1\nsurentytask: 7\nuseramversion: 64502\nmacaddr: {mac}\napptype: AM\nlocalip: {ip}\n\n".format(name=self.user, id=self.user_id, mac=self.my_mac, ip=self.my_ip)
            self.client.sendall(msg.encode(FORMAT))
            data = self.client.recv(1024) #
            uid = data.decode(FORMAT).split()[4]
            msg = "USR 3 NON S c516f13f01 {uid} 1\n\n".format(uid=uid)
            self.client.sendall(msg.encode(FORMAT))
            data = self.client.recv(1024)
            uid = data.decode(FORMAT).split()[6]
            data = self.client.recv(1024)
            msg = "USR 9 NON V {name} {uid}\n\n".format(name=self.user, uid=uid)
            print(msg)
            self.client.sendall(msg.encode(FORMAT))
            msg = "USR 10 NON V {name} {uid}\n\n".format(name=self.user, uid=uid)
            self.client.sendall(msg.encode(FORMAT))
            msg = "USR 11 NON V {name} {uid}\n\n".format(name=self.user, uid=uid)
            self.client.sendall(msg.encode(FORMAT))
            msg = "USR 12 NON V {name} {uid}\n\n".format(name=self.user, uid=uid)
            self.client.sendall(msg.encode(FORMAT))
            recv_str = ""
            while True:
                data = self.client.recv(1024)
                recv_str += data.decode(FORMAT)
                if re.search(r'USR 12', recv_str):
                    break
            msg = "LSV 4 SV\n\n"
            self.client.sendall(msg.encode(FORMAT))
            msg = "LSV 5 CV\n\n"
            self.client.sendall(msg.encode(FORMAT))
            msg = "VER 8 64502\n\nCHG 6 NLN\n\n"
            self.client.sendall(msg.encode(FORMAT))
            recv_str = ""
            while True:
                data = self.client.recv(1024)
                recv_str += data.decode(FORMAT)
                if re.search(r'CHG 6', recv_str):
                    break
        except socket.error as err:
            print(err)
            raise
    def send_msg(self, user, msg):
        print(user, msg)
        data1 = r'{\rtf1\ansi\ansicpg936\deff0\deflang1033\deflangfe2052{\fonttbl{\f0\fmodern\fprq6\fcharset134 \'cb\'ce\'cc\'e5;}}'+"\r\n"+r'{\colortbl ;\red0\green0\blue0;}'+"\r\n"+r'{\*\generator Msftedit 5.41.15.1515;}\viewkind4\uc1\pard\cf1\lang2052\f0\fs20 '+msg+r'\par'+"\r\n}\r\n"
        print(data1)
        data1_len = len(data1.encode(FORMAT))
        data2 = "MSG 14 {} 0 {}\n".format(user,"{"+str(uuid.uuid1())+"}")+"content-length: {}\nsubject: {}\n".format(data1_len,msg)+"msgtype: 0\n"+"msgflag: 16384\n"+"content-type: Text/Plain\n\n"
        self.client.sendall(data2.encode(FORMAT))
        self.client.sendall(data1.encode(FORMAT))

    def recv_msg(self):
        data = self.client.recv(1024)
        return data.decode('gbk')


if __name__ == "__main__":
    am = AM('zhangqingrong', 'c516f13f01', '3336')
    am.login()
    am.send_msg('duanyunfeng', '1234')
    am.recv_msg()