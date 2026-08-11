[app]
title = blindassist
package.name = blindassist
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,onnx,txt
version = 0.1
#requirements = python3,kivy==2.3.0,numpy==1.26.4,opencv,plyer,android
#requirements = python3,kivy==2.3.0,opencv,numpy,plyer,android
# 1. إزالة أي تحديثات أرقام إصدارات يدويًا لـ numpy و opencv
# 1. التعديل الأول: سطر المتطلبات (استخدام النسخة المخصصة لـ Android)
#requirements = python3,kivy==2.3.0,numpy,opencv,plyer,android
requirements = python3,kivy==2.3.0,plyer,android,opencv
# 2. التعديل الثاني: تثبيت إصدار NDK و API محدد يمنع تضارب C++

# 3. منع التجميع المعقد وإجبار p4a على تسريع الربط
p4a.branch = master
#requirements = python3,kivy==2.3.0,numpy,opencv-python,plyer,android
# 1. التعديل الأول: سطر المتطلبات (Requirements)
#requirements = python3,kivy==2.3.0,opencv-python,plyer,android
# 2. تحديد المعمارية الصريحة للضغط والربط (تمنع تضارب الـ C++ libraries)

# 3. استخدام NDK مستقر ومتوافق مع ووصفة numpy الخاصة بأندرويد
#android.ndk = 25b

orientation = portrait
fullscreen = 0
android.permissions = CAMERA,RECORD_AUDIO

android.api = 31
android.minapi = 24
android.sdk_build_tools_version = 31.0.0
android.ndk = 25b
android.ndk_api = 21
#android.ndk_api = 24
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 0
android.accept_sdk_license = True
