[app]
title = TrustLens V8
package.name = trustlensv8
package.domain = com.trustlens.v8

source.dir =.
source.include_exts = py,png,jpg,kv,atlas
version = 8.0
requirements = python3,kivy==2.2.0
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2

[app:build]
# no extra

[app:android]
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license_agreement = True
android.permissions = INTERNET,CAMERA
