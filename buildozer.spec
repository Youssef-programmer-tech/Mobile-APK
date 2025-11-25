[app]
title = Return Of The Artifact
package.name = returnartifact
package.domain = org.returnartifact
source.dir = .
source.include_exts = py,png,jpg,jpeg,html,js,css,json,txt,xml,csv,md

# Main entry point
main = main.py

version = 1.0

# Requirements - add all necessary dependencies
requirements = python3,flask,werkzeug,jinja2,itsdangerous,click

osx.android.api = 28
osx.android.minapi = 21

orientation = portrait

# Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# Build mode
build_type = debug

# Log level
log_level = 2

[buildozer]
log_level = 2
