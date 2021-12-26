load("@rules_python//python:defs.bzl", "py_binary")
load("@io_bazel_rules_docker//python3:image.bzl", "py3_image")
load("@io_bazel_rules_docker//container:container.bzl", "container_image")
load("@pip//:requirements.bzl", "requirement")

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

py3_image(
    name = "latest",
    srcs = ["main.py"],
    base = ":base_image",
    data = [
        "//scenarios",
        "//web:static",
    ],
    main = "main.py",
    deps = [
        "//server",
    ],
)

container_image(
    name = "base_image",
    base = "@py3_image_base//image",
    creation_time = "{BUILD_TIMESTAMP}",
    # ports = [
    #     "8080:8080",
    # ],
)
