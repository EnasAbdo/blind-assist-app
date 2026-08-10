[app]
title = مساعد المكفوفين
package.name = blindassist
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,onnx,txt
version = 0.1

# 1. تم تعديل opencv-python إلى opencv ليعمل التجميع مع أندرويد بشكل صحيح
requirements = python3==3.11.9,hostpython3==3.11.9,kivy==2.3.0,opencv,numpy,plyer,android

orientation = portrait
fullscreen = 0

# صلاحيات ضرورية: الكاميرا للكشف الحي
android.permissions = CAMERA,RECORD_AUDIO
android.api = 33
android.minapi = 24

# 2. تحديد إصدار NDK بشكل صريح ليطابق التعديل
android.ndk = 25b
android.ndk_api = 24

# 3. بناء معمارية arm64-v8a فقط يسرّع البناء ويقلل الأخطاء والتضارب
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 0
android.accept_sdk_license = True
