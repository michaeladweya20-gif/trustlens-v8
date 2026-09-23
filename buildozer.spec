[app]
title = TrustLens V8
package.name = trustlensv8
package.domain = com.trustlens.app
source.dir =.
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.2.0
orientation = portrait

[buildozer]
log_level = 2

[app:android]
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license_agreements = True
p4a.accept_sdk_license_agreements = True
