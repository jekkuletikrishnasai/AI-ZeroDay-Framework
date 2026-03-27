import socket
from shield import PreventionShield
from python_target import process_request # Your target code

shield = PreventionShield()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5000))
    server.listen(5)
    print("🌐 [CLOUD] Service Live on Port 5000.")

    while True:
        client, addr = server.accept()
        data = client.recv(4096) # Support larger payloads like your Overflow test
        if not data: break
        
        # --- THE PREVENTION GATEWAY ---
        if shield.is_safe(data):
            print(f"✅ [ALLOW] Safe request from {addr}")
            process_request(data) 
        else:
            print(f"🛑 [DROP] Attack from {addr} neutralized.")
        
        client.close()

if __name__ == "__main__":
    start_server()