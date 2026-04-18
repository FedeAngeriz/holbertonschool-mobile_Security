# Android Cryptography Challenge – Intercepting and Decrypting Data

## Overview

In this challenge, the objective was to analyze an Android application that performs encrypted operations and retrieve a hidden flag. The app simulates a heavy computation process and does not expose the result directly in the UI.

---

## Step 1 – Static Analysis

The APK was decompiled using JADX. During the analysis, the main logic was found inside:

* `MainActivityKt`

The following function was identified as the core of the decryption:

```java
public static final String performslowDecryption() {
    byte[] bArrDecode = Base64.getDecoder().decode("cVZaW1dDQllZTFdRW1xeUlBbX21CWFtHalRZXUJFRFhNX1ZcbllGQ15cUUNSRFpcVks=");
    return xorDecrypt(new String(bArrDecode), String.valueOf(slowRecursive(150)));
}
```

---

## Step 2 – Understanding the Logic

The application performs three main steps:

1. **Base64 decoding**
2. **Key generation using Fibonacci**
3. **XOR decryption**

### Key Observation

The function:

```java
slowRecursive(150)
```

implements a naive recursive Fibonacci algorithm:

```java
public static final long slowRecursive(int i) {
    return i <= 1 ? i : slowRecursive(i - 1) + slowRecursive(i - 2);
}
```

This has exponential complexity:

```
O(2^n)
```

This makes the computation extremely slow and impractical to execute directly.

---

## Step 3 – Identifying the Weakness

The vulnerability lies in:

* Use of **predictable key generation**
* Use of **XOR encryption (weak)**
* Use of an **inefficient algorithm intentionally slowing execution**

Instead of executing the app, we can replicate the logic efficiently.

---

## Step 4 – Reimplementing the Decryption

A Python script was used to:

* Decode the Base64 string
* Compute Fibonacci efficiently (iterative approach)
* Apply XOR decryption

```python
import base64

encoded = "cVZaW1dDQllZTFdRW1xeUlBbX21CWFtHalRZXUJFRFhNX1ZcbllGQ15cUUNSRFpcVks="
decoded = base64.b64decode(encoded).decode()

def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

key = str(fib(150))

result = ""
for i in range(len(decoded)):
    result += chr(ord(decoded[i]) ^ ord(key[i % len(key)]))

print(result)
```

---

## Step 5 – Extracted Flag

```
Holberton{fibonacci_slow_computation_optimization}
```

---

## Conclusion

This challenge demonstrates:

* How weak cryptographic implementations (XOR + predictable keys) can be broken
* The importance of algorithm efficiency in security
* That not all challenges require dynamic analysis tools (Frida, Burp, etc.)

Sometimes, **understanding the code is enough to break the system**.

---

## Key Takeaways

* Avoid using XOR for encryption in production
* Never rely on predictable keys (like Fibonacci sequences)
* Inefficient algorithms can hide logic but not protect it
* Static analysis is often more powerful than dynamic analysis in such cases
