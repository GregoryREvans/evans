YAML:
	kind of like a shell session
	pre install: name shell variables to makes things easier to reference
	install necessary packages
	install package to be tested
	run test

pytest:
	install pytest-helper to run pytest on abjad
	use: python -m pytest <wrapper directory>

	Exit code 0:	All tests were collected and passed successfully
	Exit code 1:	Tests were collected and run but some of the tests failed
	Exit code 2:	Test execution was interrupted by the user
	Exit code 3:	Internal error happened while executing tests
	Exit code 4:	pytest command line usage error
	Exit code 5:	No tests were collected

writing tests:
	needs to be relevant to current project
	there are many kinds of testing
	regression testing
	testing scores:
		push repo with rendered segments
		test should take old `.ly` file and copy it with a new name `.old.ly`
		the segment should be rerendered
		use diff to compare the two files to ensure that they are identical
		1. the test will fail if the file cannot be run
		2. the test will fail if the `.ly` files do not match
