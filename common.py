# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Common utils """
import os, sys, shutil, fnmatch
import subprocess

DEBUG_ = False


def sys_raise(cmd, retry=0):
  error = sys(cmd, retry)
  if error:
    raise RuntimeError("Command %s fails with error code: %s", cmd, error)


def sys(cmd, retry=0):
  if DEBUG_:
    print(">>>>>>>>> cmd >>>>>>>>>\n", cmd)
  while True:
    error = os.system(cmd)
    if error == 0:
      return error
    retry -= 1
    if retry < 0:
      return error


def sys_output(cmd):
  if DEBUG_:
    print(">>>>>>>>> cmd >>>>>>>>>\n", cmd)
  result = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
  return result
