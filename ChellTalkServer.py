from bluetooth import *

connection = False
server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"


advertise_service( server_sock, "VoltMeterPiServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ] 
#                   protocols = [ OBEX_UUID ] 
                    )
while True:
    if(connection == False):
        print("Waiting for connection on RFCOMM channel %d" % port)
        client_sock, client_info = server_sock.accept()
        connection = True
        print("Accepted connection from ", client_info)
    try:
        data = client_sock.recv(1024)
        if (data == "disconnect"):
            print("Client wanted to disconnect")
            client_sock.close()
            connection = False
        elif (data == "voltage"):
            print(data)
        else:
            print("RECEIVED: %s" % data)
            client_sock.send("%s" % data)
            print("SENT: %s" % data) 
    except IOError:
        print("Connection disconnected!")
        client_sock.close()
        connection = False
        pass
    except BluetoothError:
        print("Something wrong with bluetooth")
    except KeyboardInterrupt:
        print("\nDisconnected")
        client_sock.close()
        server_sock.close()
        break
