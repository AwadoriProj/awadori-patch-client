#!/usr/bin/env python3
"""
patch_client.py - patch in-place manifest dan .so (tanpa build, tanpa file baru).

Dijalankan dari folder yang berisi com.bilibili.sirius dan config.arm64_v8a
(atau beri path folder itu sebagai argumen).
"""
import os
import sys

root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")

MANIFEST = os.path.join(root, "com.bilibili.sirius", "AndroidManifest.xml")
SO_NAME = "libCysharp.Net.Http.YetAnotherHttpHandler.Native.so"
SO = os.path.join(root, "config.arm64_v8a", "lib", "arm64-v8a", SO_NAME)

NSC_ATTR = b'android:networkSecurityConfig="@xml/ugs_network_security_config"'
APP_TAG = b"<application "

SO_OFFSET = 0x13C458
SO_ORIG = bytes.fromhex("fd7bbfa9fd030091aad50094")
SO_PATCHED = bytes.fromhex("2800805208400f39aad50014")


def patch_manifest():
    if not os.path.isfile(MANIFEST):
        sys.exit(f"[!] Not found: {MANIFEST}")
    with open(MANIFEST, "r+b") as f:
        data = f.read()
        if NSC_ATTR in data:
            print("[=] Manifest already patched")
            return
        if data.count(APP_TAG) != 1:
            sys.exit("[!] Manifest: <application> tag not found exactly once")
        f.seek(0)
        f.write(data.replace(APP_TAG, APP_TAG + NSC_ATTR + b" ", 1))
        f.truncate()
    print("[+] Patched manifest")


def patch_so():
    if not os.path.isfile(SO):
        sys.exit(f"[!] Not found: {SO}")
    with open(SO, "r+b") as f:
        f.seek(SO_OFFSET)
        cur = f.read(len(SO_ORIG))
        if cur == SO_PATCHED:
            print(f"[=] {SO_NAME} already patched")
            return
        if cur != SO_ORIG:
            sys.exit(f"[!] {SO_NAME}: bytes at 0x{SO_OFFSET:x} don't match, aborted")
        f.seek(SO_OFFSET)
        f.write(SO_PATCHED)
    print(f"[+] Patched {SO_NAME}")


patch_manifest()
patch_so()