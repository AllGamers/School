import getpass
import sys
import telnetlib
import fileinput
import time

def fa():
    TFTP_SERVER="192.168.100.10"
    HOSTS = ["192.168.4.1","192.168.4.2"]
    user = input("Enter your remote account: ")
    password = getpass.getpass()

    i=0
    for HOST in HOSTS:
        i+=1
        tn = telnetlib.Telnet(HOST)
        tn.read_until(b"Username: ")
        tn.write(user.encode('ascii') + b"\n")
        if password:
            tn.read_until(b"Password: ")
            tn.write(password.encode('ascii') + b"\n")
        tn.write(b"enable\n")
        tn.write(b"cisco\n")
        operacion_copia=f"copy run tftp://{TFTP_SERVER}/R{i}_backup\n".encode('UTF-8')
        tn.write(operacion_copia)
        tn.read_until (b"Address or name")
        tn.write(b"\n")
        tn.read_until (b"Destination filename")
        tn.write(b"\n")
        tn.write(b"exit\n")
    
    time.sleep(10)
    for x in range(2):
        with open(f"/tftp/R{x+1}_backup", "r") as f:
            lines = f.readlines()
        with open(f"/tftp/R{x+1}_backup", "w") as f:
            for line in lines:
                if "hostname" in line:
                    f.write(f"hostname Router{x+1}_backup\n")    
                else:
                    f.write(line)

    i=0
    for HOST in HOSTS:
        i+=1
        tn = telnetlib.Telnet(HOST)
        tn.read_until(b"Username: ")
        tn.write(user.encode('ascii') + b"\n")
        if password:
            tn.read_until(b"Password: ")
            tn.write(password.encode('ascii') + b"\n")
        tn.write(b"enable\n")
        tn.write(b"cisco\n")
        operacion_copia=f"copy tftp://{TFTP_SERVER}/R{i}_backup star\n".encode('UTF-8')
        tn.write(operacion_copia)
        tn.read_until (b"Destination filename")
        tn.write(b"\n")
        tn.write(b"exit\n")

    
fa() 