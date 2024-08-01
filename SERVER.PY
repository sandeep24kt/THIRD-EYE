import socket
import pickle
import struct
import cv2
import numpy as np

# Set up client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('SERVER_IP', 9999))  # Replace 'SERVER_IP' with the server's IP address

data = b""
payload_size = struct.calcsize("Q")

while True:
    # Retrieve message size
    while len(data) < payload_size:
        packet = client_socket.recv(4 * 1024)
        if not packet:
            break
        data += packet

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    # Retrieve the image data
    while len(data) < msg_size:
        data += client_socket.recv(4 * 1024)

    img_data = data[:msg_size]
    data = data[msg_size:]

    # Deserialize the image data
    img_bytes = pickle.loads(img_data)

    # Convert bytes to numpy array and reshape it to the image dimensions
    img_np = np.frombuffer(img_bytes, dtype=np.uint8)
    img_np = img_np.reshape((1080, 1920, 3))  # Adjust dimensions to match the server's captured screen

    # Display the image
    cv2.imshow("Live Feed", img_np)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close the connection
client_socket.close()
cv2.destroyAllWindows()
