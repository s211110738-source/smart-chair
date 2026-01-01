[app]
title = Smart Chair
package.name = chairmonitor
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,paho-mqtt
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.arch = arm64-v8a
p4a.branch = master
[buildozer]
log_level = 2
warn_on_root = 1
