import socket
import random
import time

# ========== ERROR INJECTION METHODS ==========

"Bit Flip"
def bit_flip(data):
    if not data:
        return data
    pos = random.randint(0, len(data) - 1)
    char = data[pos]
    byte_val = ord(char)
    bit_pos = random.randint(0, 7)
    flipped = byte_val ^ (1 << bit_pos)
    return data[:pos] + chr(flipped) + data[pos+1:]

"Character Subs"
def char_substitution(data):
    if not data:
        return data
    
    pos = random.randint(0, len(data) - 1)
    new_char = chr(random.randint(65, 90)) #only Capital letters
    print(f"[CORRUPTION] Substituting '{data[pos]}' with '{new_char}' at position {pos}")
    return data[:pos] + new_char + data[pos+1:]

"Character Deletion"
def char_deletion(data):
    if len(data) <= 1:
        return data
    
    pos = random.randint(0, len(data) - 1)
    print(f"[CORRUPTION] Deleting '{data[pos]}' at position {pos}")
    return data[:pos] + data[pos+1:]

"Random Character Insertion"
def char_insertion(data):
    if not data:
        return data
    
    pos = random.randint(0, len(data))
    new_char = chr(random.randint(97, 122)) # only lowercase letters
    print(f"[CORRUPTION] Inserting '{new_char}' at position {pos}")
    return data[:pos] + new_char + data[pos:]

"Character Swapping"
def char_swapping(data):
    if len(data) < 2:
        return data
    
    pos = random.randint(0, len(data) - 2)
    print(f"[CORRUPTION] Swapping '{data[pos]}' and '{data[pos+1]}'")
    return data[:pos] + data[pos+1] + data[pos] + data[pos+2:]

"Multiple Bit Flips"
def multiple_bit_flips(data):
    if not data:
        return data
    
    num_flips = random.randint(2, 4)
    result = data
    for _ in range(num_flips):
        result = bit_flip(result)
    print(f"[CORRUPTION] Applied {num_flips} bit flips")
    return result

"Burst Error"
def burst_error(data):
    if len(data) < 3:
        return data
    
    burst_len = min(random.randint(3, 8), len(data))
    start = random.randint(0, len(data) - burst_len)
    
    corrupted = ''.join(chr(random.randint(33, 126)) for _ in range(burst_len)) # generates 5 random printable Characters
    print(f"[CORRUPTION] Burst error from position {start} to {start+burst_len-1}")
    return data[:start] + corrupted + data[start+burst_len:]

# ========== MAIN SERVER ==========

def apply_corruption(data):

    if random.random() < 0.3:
        print("[INFO] No corruption applied (testing correct data)")
        return data
    
    corruption_methods = [
        ('Bit Flip', bit_flip),
        ('Character Substitution', char_substitution),
        ('Character Deletion', char_deletion),
        ('Character Insertion', char_insertion),
        ('Character Swapping', char_swapping),
        ('Multiple Bit Flips', multiple_bit_flips),
        ('Burst Error', burst_error)
    ]
    
    method_name, method = random.choice(corruption_methods)
    print(f"[CORRUPTION] Applying: {method_name}")
    return method(data)

def main():
    print("=" * 50)
    print("SERVER - INTERMEDIATE & DATA CORRUPTOR")
    print("=" * 50)
    
    # Create server socket for Client 1
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('localhost', 8080))
    server_sock.listen(1)
    
    print("\n[INFO] Server listening on port 8080 (for Client 1)...")
    print("[INFO] Waiting for Client 1 to connect...\n")
    
    while True:
        try:
            # Accept connection from Client 1
            client1_sock, addr = server_sock.accept()
            print(f"[CONNECTION] Client 1 connected from {addr}")
            #Recieved Packet
            packet = client1_sock.recv(1024).decode()
            client1_sock.close()
            if not packet:
                continue
            print(f"[RECEIVED] {packet}")
            
            # Checks if The packet contains all the elements
            parts = packet.split('|')
            if len(parts) != 3:
                print("[ERROR] Invalid packet format!")
                continue
            
            data, method, control = parts
            print(f"[INFO] Original data: {data}")
            print(f"[INFO] Method: {method}")
            print(f"[INFO] Control info: {control}")
            
            # Apply corruption
            corrupted_data = apply_corruption(data)
            print(f"[INFO] Corrupted data: {corrupted_data}")
            
            # Create new packet with corrupted data
            corrupted_packet = f"{corrupted_data}|{method}|{control}"
            print(f"\n[SENDING] Forwarding to Client 2: {corrupted_packet}")
            
            time.sleep(0.5) #delay to wait for client 2
            
            client2_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client2_sock.connect(('localhost', 8081))
            client2_sock.send(corrupted_packet.encode())
            client2_sock.close()
            
            print("[SUCCESS] Data forwarded to Client 2!\n")
            print("-" * 50)
            print("Waiting for next transmission...\n")
            
        except KeyboardInterrupt:
            print("\n[INFO] Server shutting down...")
            break
        except Exception as e:
            print(f"[ERROR] {e}")
    
    server_sock.close()

if __name__ == "__main__":
    main()