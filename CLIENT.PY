import socket
import mss
import pickle
import struct

# Set up server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 9999))  # Listen on all available interfaces
server_socket.listen(5)

print("Server is listening...")

# Wait for a connection from a client
client_socket, addr = server_socket.accept()
print(f"Connection from {addr} has been established!")

with mss.mss() as sct:
    # Define the monitor to capture (you can customize the region)
    monitor = sct.monitors[1]

    while True:
        # Capture the screen
        img = sct.grab(monitor)

        # Convert the image to bytes
        img_bytes = img.rgb

        # Serialize the image data
        data = pickle.dumps(img_bytes)

        # Send the size of the serialized data first
        message_size = struct.pack("Q", len(data))
        client_socket.sendall(message_size + data)

# Close the connection
client_socket.close()
server_socket.close()
