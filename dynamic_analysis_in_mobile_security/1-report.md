# 🔍 Android Native Hooking with Frida – Task Report

## 📌 Objective

The goal of this challenge was to perform **dynamic analysis** on an Android application that uses native code (JNI), and extract a hidden flag by hooking a native function using Frida.

---

## 🧪 Environment

* Android Emulator (x86_64)
* Frida 17.9.1
* ADB (Android Debug Bridge)
* Target APK: `task2_d.apk`

---

## 🔎 Step 1 – Identify Native Library

The APK was inspected and a native library was found:

```
libnative-lib.so
```

---

## 🔎 Step 2 – Analyze Native Code

After extracting the `.so` file and inspecting it, the following JNI function was identified:

```
Java_com_holberton_task2_1d_MainActivity_getSecretMessage
```

> ⚠️ Note: Even though the app package is `task2_d`, the native function still references `task2_1d`.

---

## ⚙️ Step 3 – Setup Frida

1. Start the emulator
2. Push `frida-server` to the device
3. Run it as root:

```bash
adb root
adb shell
cd /data/local/tmp
./frida-server
```

4. Verify connection:

```bash
frida-ps -U
```

---

## 🧠 Step 4 – Enumerate Native Functions

Using Frida:

```javascript
Process.getModuleByName("libnative-lib.so").enumerateExports()
```

This revealed the target function.

---

## 🎯 Step 5 – Hook the Native Function

The function was hooked dynamically using Frida:

```javascript
var addr = Process.getModuleByName("libnative-lib.so")
    .enumerateExports()
    .find(e => e.name.includes("getSecretMessage")).address;

Interceptor.attach(ptr(addr), {
    onLeave: function (retval) {
        try {
            var env = Java.vm.getEnv();
            var result = env.getStringUtfChars(retval, null).readCString();
            console.log("[FLAG] => " + result);
        } catch (e) {
            console.log("Error:", e);
        }
    }
});
```

---

## ⚠️ Important Finding

The return value was not a standard C string (`char *`), but a JNI `jstring`.

Attempting:

```javascript
retval.readCString()
```

resulted in an access violation.

✔ Correct approach:

```javascript
Java.vm.getEnv().getStringUtfChars(...)
```

---

## 🚩 Step 6 – Extract the Flag

After triggering the function from the app UI, the flag was captured:

```
Holberton{native_hooking_is_no_different_at_all}
```

---

## 🧾 Conclusion

* The flag was not visible statically (not present in strings)
* It was generated or handled in native code at runtime
* Frida allowed interception without modifying the APK
* JNI return types must be handled correctly (`jstring` vs `char *`)

---

## 🧠 Key Takeaways

* Native code can hide sensitive logic effectively
* Dynamic analysis is essential to bypass such protections
* Understanding JNI types is crucial when working with Android reversing

---
