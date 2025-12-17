# Error Detection Simulation (Client–Server Model)

This project simulates **data transmission with error detection techniques** using a **Client–Server–Client architecture** implemented in Python sockets. It demonstrates how different error detection methods behave when data is intentionally corrupted during transmission.

---

## 📌 Project Overview

The system consists of **three programs**:

* **Client 1 (Sender)**: Sends data along with error-detection control bits.
* **Server (Intermediate)**: Randomly introduces transmission errors.
* **Client 2 (Receiver)**: Recomputes control bits and checks data integrity.

This setup helps visualize how well different error detection techniques detect corrupted data.

---

## 🗂 Project Structure

```
.
├── client1.py   # Data sender & control-bit generator
├── server.py    # Intermediate server & error injector
├── client2.py   # Data receiver & error verifier
└── README.md
```

---

## 🧠 Supported Error Detection Methods

Client 1 can choose one of the following methods:

1. **Parity Bit** – Single-bit parity check
2. **2D Parity** – Row and column parity bits
3. **CRC-16** – Polynomial-based cyclic redundancy check
4. **Hamming Code** – Error detection with parity bits
5. **Internet Checksum** – One’s complement checksum

Client 2 recalculates the same method and compares results.

---

## ⚠️ Error Injection (Server Side)

The server randomly applies **one of the following corruption techniques** (or none):

* Bit Flip
* Character Substitution
* Character Deletion
* Character Insertion
* Character Swapping
* Multiple Bit Flips
* Burst Error

There is a **30% chance that no corruption is applied**, allowing correct transmissions for comparison.

---

## 🚀 How to Run the Project

### 1️⃣ Start Client 2 (Receiver)

```bash
python client2.py
```

Client 2 listens on port **8081**.

---

### 2️⃣ Start the Server

```bash
python server.py
```

The server listens on port **8080** and forwards data to Client 2.

---

### 3️⃣ Start Client 1 (Sender)

```bash
python client1.py
```

* Enter text to send
* Choose an error detection method (1–5)

---

## 🔄 Data Flow

```
Client 1  →  Server (corruption)  →  Client 2
```

Each transmitted packet has the format:

```
DATA | METHOD | CONTROL_BITS
```

---

## 📊 Output Example (Client 2)

```
Received Data        : HELLO
Method               : CRC16
Sent Check Bits      : 1D0F
Computed Check Bits  : A42C
Status               : DATA CORRUPTED ✗
```

If the data is unchanged:

```
Status : DATA CORRECT ✓
```

---

## 🛠 Requirements

* Python 3.x
* No external libraries required (uses standard `socket`, `random`, `time`)

---

## 🎯 Educational Purpose

This project is ideal for:

* Computer Networks labs
* Error detection & data integrity demonstrations
* Understanding real-world transmission errors

---

## ✍️ Author

Developed for educational purposes to demonstrate **error detection techniques in data communication**.

---

## 📜 License

This project is free to use for **learning and academic purposes**.
