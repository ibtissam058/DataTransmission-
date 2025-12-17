import socket

# ========== Control Information ==========
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
    
    # Create matrix
    matrix = [padded_data[i:i+matrix_size] for i in range(0, len(padded_data), matrix_size)]
    
    # Row Parities
    row_parities = []
    for row in matrix:
        binary = ''.join(format(ord(c), '08b') for c in row)
        row_parities.append('1' if binary.count('1') % 2 else '0')
    
    # Column Parities
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
        
        # Calculate parity bits
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
    
    # Sum 16-bit words
    total = 0
    for i in range(0, len(byte_data), 2):
        word = (byte_data[i] << 8) + byte_data[i+1]
        total += word
        # Wrap around carry
        total = (total & 0xFFFF) + (total >> 16)
    
    # One's complement
    checksum = ~total & 0xFFFF
    return format(checksum, '04X')

# ========== MAIN PROGRAM ==========

def main():
    print("=" * 50)
    print("CLIENT 1 - DATA SENDER")
    print("=" * 50)

    data = input("\nEnter text to send: ").strip()
    
    if not data:
        print("Error: Empty input!")
        return
    
    # Methods
    print("\nChoose error detection method:")
    print("1. Parity Bit")
    print("2. 2D Parity")
    print("3. CRC-16")
    print("4. Hamming Code")
    print("5. Internet Checksum")
    
    choice = input("\nYour choice (1-5): ").strip()

    if choice == '1':
        method = "PARITY"
        control = calculate_parity(data)
    elif choice == '2':
        method = "2D_PARITY"
        control = calculate_2d_parity(data)
    elif choice == '3':
        method = "CRC16"
        control = calculate_crc16(data)
    elif choice == '4':
        method = "HAMMING"
        control = calculate_hamming(data)
    elif choice == '5':
        method = "CHECKSUM"
        control = calculate_checksum(data)
    else:
        print("Invalid choice!")
        return
    
    # Create packet
    packet = f"{data}|{method}|{control}"
    
    print(f"\n[INFO] Packet created: {packet}")
    print(f"[INFO] Connecting to server...")
    
    # Send to server
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 8080))
        sock.send(packet.encode())
        print(f"[SUCCESS] Data sent to server!")
        sock.close()
    except Exception as e:
        print(f"[ERROR] Failed to send: {e}")

if __name__ == "__main__":
    main()