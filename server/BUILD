load("@rules_python//python:defs.bzl", "py_library")
load("@pip//:requirements.bzl", "requirement")

py_library(
    name = "server",
    srcs = ["main.py"],
    visibility = ["//:text-adventure"],
    deps = [
        ":enums",
        "//server/engine",
        requirement("flask"),
        requirement("flask_socketio"),
    ],
)

py_library(
    name = "enums",
    srcs = ["enums.py"],
    visibility = ["//:text-adventure"],
)
