var addr = Process.getModuleByName("libnative-lib.so")
    .enumerateExports()
    .find(e => e.name.includes("getSecretMessage")).address;

Interceptor.attach(ptr(addr), {
    onLeave: function (retval) {
        try {
            var env = Java.vm.getEnv();
            var result = env.getStringUtfChars(retval, null).readCString();
            console.log("[🔥 FLAG] => " + result);
        } catch (e) {
            console.log("Error:", e);
        }
    }
});

este hook convierte el jstring a string real