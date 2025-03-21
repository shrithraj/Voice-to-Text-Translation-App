import http.server
import socketserver
import socket
import pyqrcode
import os
import webbrowser

# Configuration
PORT = 8010

def get_local_ip():
    """Get the local IP address of the machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"  # Fallback to localhost
    finally:
        s.close()
    return ip

# Get desktop path
if os.name == "nt":
    desktop = os.path.join(os.environ["USERPROFILE"],"OneDrive", "Desktop")
else:
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")

os.chdir(desktop)  # Serve files from Desktop

# Get local IP and generate QR code
IP = f"http://{get_local_ip()}:{PORT}"
qr = pyqrcode.create(IP)
qr.svg("myqr.svg", scale=8)
webbrowser.open("myqr.svg")

# Start HTTP server
class Handler(http.server.SimpleHTTPRequestHandler):
    pass

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    print(f"Type this in your Browser: {IP} or scan the QR code.")
    httpd.serve_forever()
