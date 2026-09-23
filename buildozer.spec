[app]
title = TrustLens V8
package.name = trustlensv8
package.domain = com.trustlens.v8

source.dir =.
source.include_exts = py,png,jpg,kv,atlas,json

version = 0.8
requirements = python3,kivy
orientation = portrait

[buildozer]
log_level = 2

[app:android]
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.build_tools_version = 34.0.0
android.accept_sdk_license_agreements = True
android.archs = arm64-v8a, armeabi-v7a
p4a.branch = master
android.permissions = INTERNET,CAMERA

# If you have main.py in a folder, change this:
# source.dir =./your_app_folder
