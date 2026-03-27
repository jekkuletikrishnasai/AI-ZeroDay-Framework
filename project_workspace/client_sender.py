import socket

def send(msg):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 5000))
    s.send(msg)
    s.close()

print("1. Test Safe User")
print("2. Test Attacker (Zero-Day)")
choice = input("Select: ")

if choice == "1":
    send(b"List_Files") # Normal request
elif choice == "2":
    # Use a signature you know is in your log (e.g., the Admin Backdoor)
    send(b"ADMIN_ACCESS_REVEAL_SECRET")