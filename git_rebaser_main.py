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

import argparse

import git_rebaser

_ARG_ALIASES = {
    'xl': ['ll', 'l'],
    'update': ['up'],
    'commit': ['ci'],
    'prune': ['d', 'delete']
}


def _get_arg_with_aliases(arg):
  return {'name': arg, 'aliases': _ARG_ALIASES.get(arg, [])}


def main():

  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers(dest='subparser_name')

  sub_arg = subparsers.add_parser(
      **_get_arg_with_aliases('amend'), help='Amend current branch')

  sub_arg = subparsers.add_parser(
      **_get_arg_with_aliases('xl'),
      help='show revision history of entire repository')

  sub_arg = subparsers.add_parser(
      **_get_arg_with_aliases('change_branch_name'),
      help='change current branch name')
  sub_arg.add_argument(
      '--branch_name',
      default=None,
      help='branch name. If not specified, it will use next available positive number'
  )

  sub_arg = subparsers.add_parser(
      **_get_arg_with_aliases('set_as_master_branch'),
      help='Set current branch as master branch, it will be associated with another'
      ' branch name 0 so it is easier to refer to')

  sub_arg = subparsers.add_parser(
      **_get_arg_with_aliases('diff'), help='diff file with parent branch')

  sub_arg = subparsers.add_parser(
      **_get_arg_with_aliases('difftool'),
      help='diff file with parent branch using git difftool')

  sub_arg = subparsers.add_parser(
      **_get_arg_with_aliases('commit'),
      help='commit the specified files or all outstanding changes')
  sub_arg.add_argument('--branch_name', default=None)

  sub_arg = subparsers.add_parser(
      **_get_arg_with_aliases('init'),
      help='Initialize git_rebaser on current directory')

  sub_arg = subparsers.add_parser(
      **_get_arg_with_aliases('prune'),
      help='delete a branch, but keeping sub branches if there is any')
  sub_arg.add_argument('branch_name')

  sub_arg = subparsers.add_parser(
      **_get_arg_with_aliases('rebase'),
      help='rebase a branch with its sub-branches(the whole chain) on top of a branch'
  )
  sub_arg.add_argument('-s', '--source', help='source branch name')
  sub_arg.add_argument('-d', '--dest', help='destination branch name')

  sub_arg = subparsers.add_parser(
      **_get_arg_with_aliases('sync'), help='sync git from remote')

  sub_arg = subparsers.add_parser(
      **_get_arg_with_aliases('update'),
      help='update working directory (or switch revisions)')
  sub_arg.add_argument('branch_name')

  args = parser.parse_args()
  sub_arg_name = args.subparser_name
  for key, value in _ARG_ALIASES.items():
    if sub_arg_name in value:
      sub_arg_name = key
  if sub_arg_name is None:
    parser.print_help()
    exit(1)

  # pass the sub argument to corresponding method call.
  rebaser = git_rebaser.GitRebaser()
  getattr(rebaser, sub_arg_name)(args)


if __name__ == '__main__':
  main()
