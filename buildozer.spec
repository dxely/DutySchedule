[app]

title = 我的值班表
package.name = dutyschedule
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

requirements = python3,kivy
orientation = portrait

osx.python_version = 3
osx.kivy_version = 2.2.0

fullscreen = 0

android.permissions = INTERNET,ACCESS_NETWORK_STATE

android.api = 31
android.minapi = 21
android.sdk = 24
android.ndk = 25b

android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1
