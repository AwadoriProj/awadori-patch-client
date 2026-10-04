Decompile:
```console
apktool d com.bilibili.sirius.apk
apktool d config.arm64_v8a.apk
```
Patch:
```console
python patch_client.py
```
Build:
```console
apktool b com.bilibili.sirius
apktool b config.arm64_v8a
```
