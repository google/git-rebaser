# Rebaser For Git

This repository contains a rebaser tool for using git with gerrit. This tool
makes rebasing easier if anyone is following "one branch per commit" philosophy.
This tool will sit on top of normal "git" command, meaning you can do all "READ"
operation using git command, but some "WRITE" operation(commit, rebase) can be
helped from this tool.

# Mechanics

This tool parses local head to get the relationship between local branches.

# Examples

``` shell
GR="python git_rebaser_main.zip"
```
Initialize current repo for this tool. This will create a file to keep branches
in sync in current dir. This only needs to be done once for each repository.
``` shell
$GR init
```

List all the branches:
``` shell
$GR ll
```
You should see something like:
```
`- 0 [master] : (sync 8 weeks ago) a12345678
```

After added new file with "git add", then commit by:
``` shell
$GR ci
```
Then use "ll" to list branch will be something like:
```
`- 0 [master] : (sync 8 weeks ago) a12345678
   `- 1  : Commit test 1  <===============
```

The number 1 is the branch name automatically created by this tool. Followed by
the commit message. Followed by the arrow point which branch you are in right
now. This is for any branches other than master.

To switch the branch, use:
``` shell
$GR up 0
$GR ll
```
shows:
```
`- 0 [master] : (sync 8 weeks ago) a12345678  <===============
   `- 1  : Commit test 1
```

If you add another commit now, the tree will be:
```
`- 0 [master] : (sync 8 weeks ago) a12345678
   |- 1  : Commit test 1
   `- 2  : Commit test 2  <===============
```

Note: it will automatically switch to the last commited branch.

Now you can do rebase:
``` shell
$GR rebase -s 2 -d 1
$GR ll
```
```
`- 0 [master] : (sync 8 weeks ago) a12345678
   `- 1  : Commit test 1
      `- 2  : Commit test 2  <===============
```

If rebase failed due to the conflict, you can resolve the conflict by regular
git procedure, then do the same rebase command again to sync the branches.


For more detail supported operations:
``` shell
$GR -h
$GR rebase -h
```


# Develop

Checkout the repo. To build, follow the Bazel build instruction. 

Add test if necessary.

Remember to create executable for easier use:
``` shell
bazel build --build_python_zip :git_rebaser_main
cp -f bazel-bin/git_rebaser_main.zip ./
```

**This is not an officially supported Google product.**
