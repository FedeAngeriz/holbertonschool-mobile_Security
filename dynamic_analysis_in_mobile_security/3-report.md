# Android Security Challenge – Revealing Hidden Functions

## Overview

This challenge focused on identifying and invoking hidden functions داخل an Android application. The goal was to retrieve a secret flag stored in a function that is never executed during normal app usage.

Unlike previous challenges, the flag was not exposed through UI interaction or standard execution flow, requiring dynamic analysis to locate and trigger the hidden logic.

---

## Step 1 – Static Analysis

The APK was decompiled using JADX. The main logic was located in:

* `MainActivityKt`

While analyzing the code, the following suspicious function was identified:

```java
private static final void aBcDeFgHiJkLmNoPqRsTuVwXyZ123456(Function1<? super String, Unit> function1)
```

### Observations:

* The function name is heavily obfuscated
* It is **never called** anywhere in the code
* It receives a `Function1` callback instead of returning a value

---

## Step 2 – Understanding the Hidden Logic

Inside the function:

1. A Base64-encoded string is decoded
2. Each byte is transformed using:

   * XOR operation
   * Bitwise shifts
   * Arithmetic manipulation
3. The result is reconstructed into a string (`flag`)
4. The flag is passed to a callback:

```java
function1.invoke(flag);
```

### Key Insight

The function does not return the flag — it **delivers it through a callback**, making it harder to retrieve using simple hooks.

---

## Step 3 – Dynamic Analysis with Frida

To retrieve the flag, Frida was used to:

* Hook into the running application
* Create a custom implementation of `kotlin.jvm.functions.Function1`
* Invoke the hidden function manually

---

## Step 4 – Frida Script

```javascript
Java.perform(function () {
    console.log("[+] Starting hidden function attack");

    var clazz = Java.use("com.holberton.task4_d.MainActivityKt");

    // Create custom callback
    var callback = Java.registerClass({
        name: "com.example.MyCallback",
        implements: [Java.use("kotlin.jvm.functions.Function1")],
        methods: {
            invoke: function (arg) {
                console.log("[🔥 FLAG] => " + arg);
                return null;
            }
        }
    });

    var cbInstance = callback.$new();

    // Invoke hidden function
    setTimeout(function () {
        console.log("[+] Invoking hidden function...");
        clazz.aBcDeFgHiJkLmNoPqRsTuVwXyZ123456(cbInstance);
    }, 1000);
});
```

---

## Step 5 – Execution

The application was launched, and the script was attached using:

```bash
frida -U -n com.holberton.task4_d -l script.js
```

After execution, the hidden function was successfully invoked.

---

## Step 6 – Extracted Flag

```
Holberton{calling_uncalled_functions_is_now_known!}
```

---

## Conclusion

This challenge highlights several important security concepts:

* Hidden functions do not guarantee security if they remain accessible at runtime
* Obfuscation alone is insufficient to protect sensitive logic
* Callback-based designs can obscure data flow but are still exploitable
* Dynamic analysis tools like Frida allow direct interaction with application internals

---

## Key Takeaways

* Always assume that any code shipped in an application can be accessed
* Sensitive operations should not rely on obscurity
* Proper access control and secure architecture are essential
* Reverse engineering combined with dynamic instrumentation is a powerful attack vector

---
