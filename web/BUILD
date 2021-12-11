load("@npm//@bazel/typescript:index.bzl", "ts_project")
load("@npm//@bazel/rollup:index.bzl", "rollup_bundle")
load("@io_bazel_rules_sass//:defs.bzl", "sass_binary", "sass_library")

rollup_bundle(
    name = "bundle",
    config_file = "rollup.config.js",
    entry_point = ":main.js",
    visibility = ["//:text-adventure"],
    deps = [
        ":main",
        "@npm//@babel/preset-env",
        "@npm//@rollup/plugin-babel",
        "@npm//@rollup/plugin-commonjs",
        "@npm//@rollup/plugin-node-resolve",
        "@npm//rollup-plugin-uglify",
    ],
)

filegroup(
    name = "static",
    srcs = [
        "index.html",
        ":bundle",
        ":styles",
    ],
    visibility = ["//:text-adventure"],
)

ts_project(
    name = "main",
    srcs = glob(["*.ts"]),
    incremental = True,
    source_map = True,
    tsconfig = "//:tsconfig.json",
    visibility = ["//:text-adventure"],
    deps = [
        "@npm//socket.io-client",
    ],
)

sass_binary(
    name = "styles",
    src = "styles.scss",
    deps = [":colors"],
)

sass_library(
    name = "colors",
    srcs = ["colors.scss"],
)
