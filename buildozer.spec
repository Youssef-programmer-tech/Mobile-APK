[app]
# Title of your application
title = Return Of The Artifact

# Package name
package.name = returnartifact

# Package domain (should be unique)
package.domain = org.returnartifact

# Source directory where main.py is located
source.dir = .

# Source to include in APK (add all your file extensions)
source.include_exts = py,png,jpg,jpeg,html,js,css,json,txt,xml,csv,md

# Main entry point
main = main.py

# Version
version = 1.0

# Requirements
requirements = python3,flask,werkzeug,jinja2

# Android specific
osx.android.api = 28
osx.android.minapi = 21

# Orientation
orientation = portrait

# Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# Presplash screen (optional)
# presplash.filename = %(source.dir)s/presplash.png
# icon.filename = %(source.dir)s/icon.png

# Build mode
build_type = debug

# Log level
log_level = 2

[buildozer]
# Buildozer version
log_level = 2
