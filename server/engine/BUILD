load("@rules_python//python:defs.bzl", "py_library")
load("@pip//:requirements.bzl", "requirement")

py_library(
    name = "engine",
    srcs = [
        "action_result.py",
        "actions.py",
        "adventure_engine.py",
        "ending.py",
        "location.py",
        "object.py",
        "scenario.py",
        "scenario_parser.py",
    ],
    visibility = ["//:text-adventure"],
    deps = [
        "//server:enums",
        requirement("pyyaml"),
    ],
)
