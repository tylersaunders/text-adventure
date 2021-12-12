load("@rules_python//python:defs.bzl", "py_binary")

exports_files(["tsconfig.json"])

package_group(
    name = "text-adventure",
    packages = [
        "//...",
        "//scenarios/...",
        "//server/...",
        "//web/...",
    ],
)

py_binary(
    name = "main",
    srcs = ["main.py"],
    data = [
        "//scenarios",
        "//web:static",
    ],
    deps = [
        "//server",
    ],
)
