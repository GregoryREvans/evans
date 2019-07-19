YAML:<br/>
	kind of like a shell session<br/>
	pre install: name shell variables to makes things easier to reference<br/>
	install necessary packages<br/>
	install package to be tested<br/>
	run test<br/>
<br/>
pytest:<br/>
	install pytest-helper to run pytest on abjad<br/>
	use: python -m pytest <wrapper directory><br/>
<br/>
```	Exit code 0:	All tests were collected and passed successfully
	Exit code 1:	Tests were collected and run but some of the tests failed
	Exit code 2:	Test execution was interrupted by the user
	Exit code 3:	Internal error happened while executing tests
	Exit code 4:	pytest command line usage error
	Exit code 5:	No tests were collected```<br/>
<br/>
writing tests:<br/>
	needs to be relevant to current project<br/>
	there are many kinds of testing<br/>
	regression testing<br/>
	testing scores:<br/>
		push repo with rendered segments<br/>
		test should take old `.ly` file and copy it with a new name `.old.ly`<br/>
		the segment should be rerendered<br/>
		use diff to compare the two files to ensure that they are identical<br/>
		1. the test will fail if the file cannot be run<br/>
		2. the test will fail if the `.ly` files do not match<br/>
