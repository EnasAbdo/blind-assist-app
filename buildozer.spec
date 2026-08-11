[app]
title = مساعد المكفوفين
package.name = blindassist
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,onnx,txt
version = 0.1
requirements = python3==3.10.10,kivy==2.3.0,opencv,numpy,plyer
orientation = portrait
fullscreen = 0
android.permissions = CAMERA,RECORD_AUDIO
# تعديل السطور التالية داخل buildozer.spec:
android.api = 31
android.minapi = 24
android.ndk = 25b
android.ndk_api = 24

[buildozer]
log_level = 2
warn_on_root = 0
android.accept_sdk_license = True
