import socket

# ========== ERROR DETECTION METHODS==========

"Parity"
def calculate_parity(data):
    binary_str = ''.join(format(ord(c), '08b') for c in data)
    ones_count = binary_str.count('1')
    parity = '0' if ones_count % 2 == 0 else '1'
    return parity

"2D parity"
def calculate_2d_parity(data):
    size = len(data)
    matrix_size = int(size ** 0.5) + 1
    padded_data = data.ljust(matrix_size * matrix_size, '\0')
    
    matrix = [padded_data[i:i+matrix_size] for i in range(0, len(padded_data), matrix_size)]
    
    row_parities = []
    for row in matrix:
        binary = ''.join(format(ord(c), '08b') for c in row)
        row_parities.append('1' if binary.count('1') % 2 else '0')
    
    col_parities = []
    for col in range(matrix_size):
        binary = ''.join(format(ord(matrix[row][col]), '08b') for row in range(len(matrix)))
        col_parities.append('1' if binary.count('1') % 2 else '0')
    
    return ''.join(row_parities) + ''.join(col_parities)

"CRC-16"
def calculate_crc16(data):
    crc = 0xFFFF
    polynomial = 0x1021
    
    for byte in data.encode():
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ polynomial
            else:
                crc <<= 1
            crc &= 0xFFFF
    
    return format(crc, '04X')

"Hamming"
def calculate_hamming(data):
    result = []
    for char in data:
        bits = format(ord(char), '08b')
        d = [int(bits[i]) for i in range(4)]
        
        p1 = d[0] ^ d[1] ^ d[3]
        p2 = d[0] ^ d[2] ^ d[3]
        p3 = d[1] ^ d[2] ^ d[3]
        
        result.append(str(p1) + str(p2) + str(d[0]) + str(p3) + str(d[1]) + str(d[2]) + str(d[3]))
    
    return ''.join(result)

"Internet Checksum"
def calculate_checksum(data):
    byte_data = data.encode()
    
    if len(byte_data) % 2 != 0:
        byte_data += b'\x00'
    
    total = 0
    for i in range(0, len(byte_data), 2):
        word = (byte_data[i] << 8) + byte_data[i+1]
        total += word
        total = (total & 0xFFFF) + (total >> 16)
    
    checksum = ~total & 0xFFFF
    return format(checksum, '04X')

# ========== MAIN PROGRAM ==========

def main():
    print("=" * 50)
    print("CLIENT 2 - RECEIVER & ERROR CHECKER")
    print("=" * 50)
    
    # Create server socket to receive from Server
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('localhost', 8081))
    server_sock.listen(1)
    
    print("\n[INFO] Client 2 listening on port 8081...")
    print("[INFO] Waiting for data from server...\n")
    
    while True:
        try:
            # To accept connection from Server
            conn, addr = server_sock.accept()
            print(f"[CONNECTION] Received connection from server")
            
            # Receive packet
            packet = conn.recv(1024).decode()
            conn.close()
            
            if not packet:
                continue
            
            print(f"[RECEIVED] {packet}\n")
            
            # Checks if The packet contains all the elements
            parts = packet.split('|')
            if len(parts) != 3:
                print("[ERROR] Invalid packet format!\n")
                continue
            
            data, method, incoming_control = parts
            
            # Calculate control information based on method
            if method == "PARITY":
                computed_control = calculate_parity(data)
            elif method == "2D_PARITY":
                computed_control = calculate_2d_parity(data)
            elif method == "CRC16":
                computed_control = calculate_crc16(data)
            elif method == "HAMMING":
                computed_control = calculate_hamming(data)
            elif method == "CHECKSUM":
                computed_control = calculate_checksum(data)
            else:
                print(f"[ERROR] Unknown method: {method}\n")
                continue
            

            status = "DATA CORRECT ✓" if incoming_control == computed_control else "DATA CORRUPTED ✗"
            

            print("=" * 50)
            print("VERIFICATION RESULTS")
            print("=" * 50)
            print(f"Received Data        : {data}")
            print(f"Method               : {method}")
            print(f"Sent Check Bits      : {incoming_control}")
            print(f"Computed Check Bits  : {computed_control}")
            print(f"Status               : {status}")
            print("=" * 50)
            print()
            print("Waiting for next transmission...\n")
            
        except KeyboardInterrupt:
            print("\n[INFO] Client 2 shutting down...")
            break
        except Exception as e:
            print(f"[ERROR] {e}\n")
    
    server_sock.close()

if __name__ == "__main__":
    main()