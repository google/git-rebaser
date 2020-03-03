#!/bin/bash

# Add the binary to the commit
bazel build --build_python_zip :git_rebaser_main
cp -f bazel-bin/git_rebaser_main.zip ./
git add git_rebaser_main.zip
