[app]
title = CortaMidia
package.name = cortamidia
package.domain = org.joao
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# Requisitos flexíveis para não dar conflito de compilação C
requirements = python3,kivy,kivymd,yt_dlp

orientation = portrait
fullscreen = 0

# Permissões do Android
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
