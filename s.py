import socket               # Import socket module

soc = socket.socket()         # Create a socket object
host = "0.0.0.0" # Get local machine name
port = 2004                # Reserve a port for your service.
soc.bind((host, port))       # Bind to the port
soc.listen(5)                 # Now wait for client connection.
while True:
    conn, addr = soc.accept()     # Establish connection with client.
    print ("Got connection from",addr)
    msg = conn.recv(1024)
    print (msg)
   
