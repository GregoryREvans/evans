Surmounting difficulties in installation on windows (especially from a distance)
==
1. the auto-generated `.abjad` folder which is supposed to be in the home directory fails to be written<br />
&nbsp;&nbsp;&nbsp;&nbsp;`windows` seems to dislike programs from unidentified developers to edit things in the home directory<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if we build it by hand, there is no problem (get a friend)<br />

2. PATH and PYTHONPATH concatenation<br />
&nbsp;&nbsp;&nbsp;&nbsp;because `windows` is not `Unix`, the shell is not `bash` and does not read `.bash_profile`<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`My Computer > Properties > Advanced System Settings > Environment Variables >`<br />
`https://stackoverflow.com/questions/3701646/how-to-add-to-the-pythonpath-in-windows-so-it-finds-my-modules-packages`<br />
May need to define the `PYTHONPATH` environment variable from scratch, but defaul `Path` setting works.<br />

3. *P.S.* don't forget to install `Python` and `Git`!
