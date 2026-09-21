[app]
title = TrustLens V8
package.name = trustlensv8
package.domain = com.eldoret.trustlensv8
source.dir =.
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
p4a.accept_sdk_license_agreements = True
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.build_tools_version = 33.0.2
android.ant_path = /usr/bin/ant
