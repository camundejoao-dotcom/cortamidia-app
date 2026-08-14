[app]
title = CortaMidia
package.name = cortamidia
package.domain = org.joao
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html,js,css
version = 1.0

# Requisitos do app (pyjnius é essencial para abrir arquivos no Android)
requirements = python3,kivy==2.2.1,pyjnius

orientation = portrait
fullscreen = 0

# Permissões de armazenamento e mídia
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, READ_MEDIA_VIDEO
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
