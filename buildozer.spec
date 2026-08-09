[app]
title = مساعد المكفوفين
package.name = blindassist
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,onnx,txt

version = 0.1

requirements = python3,kivy==2.3.0,opencv-python,numpy,plyer,android
orientation = portrait
fullscreen = 0

# صلاحيات ضرورية: الكاميرا للكشف الحي
android.permissions = CAMERA,RECORD_AUDIO

android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 0
android.accept_sdk_license = True
