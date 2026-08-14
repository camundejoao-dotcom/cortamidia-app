[app]
title = CortaMidia
package.name = cortamidia
package.domain = org.joao
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# Dependencias essenciais incluindo ffmpeg nativo para android
requirements = python3,kivy==2.2.1,kivymd==1.1.1,yt_dlp,ffmpegandroid

orientation = portrait
fullscreen = 0

# Permissoes do Android
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
