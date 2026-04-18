import base64

# Paso 1: decode
encoded = "cVZaW1dDQllZTFdRW1xeUlBbX21CWFtHalRZXUJFRFhNX1ZcbllGQ15cUUNSRFpcVks="
decoded = base64.b64decode(encoded).decode()

# Paso 2: fibonacci rápido
def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

key = str(fib(150))

# Paso 3: XOR
result = ""
for i in range(len(decoded)):
    result += chr(ord(decoded[i]) ^ ord(key[i % len(key)]))

print(result)