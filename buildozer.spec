[app]
title = blindassist
package.name = blindassist
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,onnx,txt
version = 0.1
requirements = python3,kivy==2.3.0,numpy==1.26.4,opencv,plyer,android
#requirements = python3,kivy==2.3.0,opencv,numpy,plyer,android

orientation = portrait
fullscreen = 0
android.permissions = CAMERA,RECORD_AUDIO

android.api = 31
android.minapi = 24
android.sdk_build_tools_version = 31.0.0
android.ndk = 25b
android.ndk_api = 24
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 0
android.accept_sdk_license = True
