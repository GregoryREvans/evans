- unix: <br />

\ <br />
&nbsp;&nbsp;&nbsp;&nbsp;line continuation character <br />
&nbsp;&nbsp;&nbsp;&nbsp;must be eol <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;end of line <br />

man man <br />
&nbsp;&nbsp;&nbsp;&nbsp;manual for the manual <br />

man name <br />
&nbsp;&nbsp;&nbsp;&nbsp;doc about name command <br />
&nbsp;&nbsp;&nbsp;&nbsp;[space] = page down <br />
&nbsp;&nbsp;&nbsp;&nbsp;[q] = exit manual <br />

rm [file] <br />
&nbsp;&nbsp;&nbsp;&nbsp;remove file <br />

rm -rf [directory] <br />
&nbsp;&nbsp;&nbsp;&nbsp;remove directory <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;can also use blobs <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[a-z]* <br />

(files and directories are basically the same, just sockets) <br />

ls -l <br />
&nbsp;&nbsp;&nbsp;&nbsp;list contents of directory in “long form” <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;includes permissions/owner/last modified timestamp/etc <br />

ls -1 <br />
&nbsp;&nbsp;&nbsp;&nbsp;lists contents of directory in single column <br />

touch [file] <br />
&nbsp;&nbsp;&nbsp;&nbsp;create empty file if file doesn’t exist <br />
&nbsp;&nbsp;&nbsp;&nbsp;change file access and modification times <br />
&nbsp;&nbsp;&nbsp;&nbsp;updates “last modified” timestamp preexisting <br />
&nbsp;&nbsp;&nbsp;&nbsp;makes empty files <br />
&nbsp;&nbsp;&nbsp;&nbsp;(don’t confuse with mkdir) <br />

mkdir -p [path] <br />
&nbsp;&nbsp;&nbsp;&nbsp;makes directories with intermediate directories <br />

Makefiles <br />
&nbsp;&nbsp;&nbsp;&nbsp;.PHONY <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;means that target has no dependencies and is always “out of date” <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;this lets us `make [target]` on everything in `Scores` always <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;c/cpp files have lots of dependencies for compilation of a package <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;object files are a result <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;since we don’t have these with out scores we want to force the clone/pull <br />

ctrl + a <br />
&nbsp;&nbsp;&nbsp;&nbsp;shell beginning of line <br />

ctrl + e <br />
&nbsp;&nbsp;&nbsp;&nbsp;shell end of line <br />
&nbsp;&nbsp;&nbsp;&nbsp;don’t forget z is kill process <br />

modifications is a synonym for permissions <br />
chmod <br />
&nbsp;&nbsp;&nbsp;&nbsp;change modifications <br />
&nbsp;&nbsp;&nbsp;&nbsp;use 755 to read and execute but not write <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;equivalent to -rwxr-xr-x <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;this gives permission to execute the script <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+x is the semantic version (executability) <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;order = `chmod`+`modifications`+`path` <br />

git checkout . <br />
&nbsp;&nbsp;&nbsp;&nbsp;discards local changes <br />


\`\` opens subshell in unix and returns the result <br />
	i.e. `which py.test` - rf <br />
		may be redundant <br />

updating python? <br />

always use git diff (in the largest vertical window) <br />

isort <br />
	- check status of repo <br />
	- run `isort-check` in wrapper directory of package <br />
	- run `isort-reformat` in wrapper directory <br />
	- git diff <br />
	- rerender segments <br />
	- git diff . in specific segment directory  to check that lily file is unchanged <br />

update os by friday <br />

do this process for all scores <br />

`git mv` but *not* `git rm` <br />

`symlinks` <br />
&nbsp;&nbsp;&nbsp;&nbsp;made with `ln -s [remotepath] [localname]` <br />
&nbsp;&nbsp;&nbsp;&nbsp;unlinked with `rm -rf [localname]` <br />
&nbsp;&nbsp;&nbsp;&nbsp;`unlink` synonym for `rm` <br />
* always view symlink (atom etc) to ensure paths are written correctly.
* we can link to non-existent files which error silently.

get black and isort to agree <br />
&nbsp;&nbsp;&nbsp;&nbsp;Done by setting both to 90 characters? <br />

find ways to run scores over all scores or 1 score <br />
&nbsp;&nbsp;&nbsp;&nbsp;controllability <br />
&nbsp;&nbsp;&nbsp;&nbsp;temporary local scripts <br />

git checkout [file]
	reverts to last pushed version

***git checkout . reverts the entire repository not pwd***
