YAML:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;kind of like a shell session<br/>
&nbsp;&nbsp;&nbsp;&nbsp;pre install: name shell variables to makes things easier to reference<br/>
&nbsp;&nbsp;&nbsp;&nbsp;install necessary packages<br/>
&nbsp;&nbsp;&nbsp;&nbsp;install package to be tested<br/>
&nbsp;&nbsp;&nbsp;&nbsp;run test<br/>
<br/>
pytest:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;install pytest-helper to run pytest on abjad<br/>
&nbsp;&nbsp;&nbsp;&nbsp;use: python -m pytest <wrapper directory><br/>
<br/>
```
	Exit code 0:	All tests were collected and passed successfully
	Exit code 1:	Tests were collected and run but some of the tests failed
	Exit code 2:	Test execution was interrupted by the user
	Exit code 3:	Internal error happened while executing tests
	Exit code 4:	pytest command line usage error
	Exit code 5:	No tests were collected
```
<br/>
<br/>
writing tests:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;needs to be relevant to current project<br/>
&nbsp;&nbsp;&nbsp;&nbsp;there are many kinds of testing<br/>
&nbsp;&nbsp;&nbsp;&nbsp;regression testing<br/>
&nbsp;&nbsp;&nbsp;&nbsp;testing scores:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;push repo with rendered segments<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;test should take old `.ly` file and copy it with a new name `.old.ly`<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;the segment should be rerendered<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;use diff to compare the two files to ensure that they are identical<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. the test will fail if the file cannot be run<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. the test will fail if the `.ly` files do not match<br/>
