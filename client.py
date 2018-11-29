#Client
import socket as mysoc
import pickle
import sys

""" as_host = sys.argv[1]
file_name = sys.argv[2] """

def client():
    #[ as socket]
    try:
        ctoas=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)

    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))

    #[tlds1 socket]
    try:
        ctots1=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)

    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    #[tlds2 socket]
    try:
        ctots2=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)

    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    #load file with hostname information to be resolved
    try:
        #fname = input("Enter file to read (Ex: foo.txt): ")
        file_name = "PROJ3-HNS.txt"
        fr = open(file_name, "r")
    except IOError as err:
        print('{} \n'.format("File Open Error ",err))
        print("Please ensure table file exists in source folder")
        exit()

    #[determine hostname of Authentication server and port ]
    # print(rs_host)
    host=mysoc.gethostname()
    sa_sameas_myaddr = mysoc.gethostbyname(host)
    # Define the port on which you want to connect to the server
    portAS = 50008
    portTLDS1 = 5679
    portTLDS2 = 5676
    #[bind ctors socket to RS address, RS port]
    try:
        server_binding=(sa_sameas_myaddr,portAS)
        ctoas.connect(server_binding)
    except mysoc.error as err:
        print('{} \n'.format("connect error "), err)
        exit()
    
    #check as-server.py for information on how data
    #is being transferred and stored
    #write all resolved IP information to RESOLVED.txt
    first1 = True
    if first1:
        first1=False
        try:
            server_binding=(sa_sameas_myaddr,portTLDS1)
            ctots1.connect(server_binding)
        except mysoc.error as err:
            print('{} \n'.format("connect error "), err)
            exit()
    first2 = True
    if first2:
        first2=False
        try:
            server_binding=(sa_sameas_myaddr,portTLDS2)
            ctots2.connect(server_binding)
        except mysoc.error as err:
            print('{} \n'.format("connect error "), err)
            exit()
    with open("RESOLVED.txt", "w") as fw:
        for hostname in fr:
            digest = hostname.split()
            ctoas.send(pickle.dumps(digest))
            dataFromAS=pickle.loads(ctoas.recv(100))
            if "TLDS1" in dataFromAS:
                ctots1.send(pickle.dumps(digest[2]))
                data=pickle.loads(ctots1.recv(100))
                fw.write(data+'\n')
            elif "TLDS2" in dataFromAS:
                ctots2.send(pickle.dumps(digest[2]))
                data=pickle.loads(ctots2.recv(100))
                fw.write(data+'\n')
            else:
                fw.write(digest[2]+" - No servers matching key\n")
    # close everything
    fr.close()
    fw.close()
    ctots1.close()
    ctots2.close()
    ctoas.close()
    exit()

client()