import socket
import mss
import mss.tools
import time
import io
from PIL import Image

# Set up the server address and port
server_ip = '127.0.0.1'  # Replace with the correct server IP address
server_port = 12345

# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((server_ip, server_port))

# Initialize MSS for capturing screenshots
with mss.mss() as sct:
    # Capture screenshots in a loop
    while True:
        # Capture the entire screen
        screenshot = sct.grab(sct.monitors[0])
        
        # Convert the screenshot to an Image object using PIL
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        
        # Save the image to a BytesIO object in PNG format
        img_buffer = io.BytesIO()
        img.save(img_buffer, format="PNG")
        img_data = img_buffer.getvalue()
        
        # Send the screenshot size first
        img_size = len(img_data)
        sock.sendall(img_size.to_bytes(4, 'big'))
        
        # Send the screenshot data
        sock.sendall(img_data)
        
        # Wait for a short period before capturing the next screenshot
        time.sleep(1)
