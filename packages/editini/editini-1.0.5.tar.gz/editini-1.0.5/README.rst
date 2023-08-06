=====================
edit ini Ver1.0.0
=====================

This was created because the author found it difficult to use "configparser".
"edit ini" is partially compatible with "configparser".
You can create, edit and delete "[section]" and "option = value" for files with ".ini" extension.
`日本語版はこちらです <http://penguin0093.html.xdomain.jp/page/project/python/editini.html>`_


License
^^^^^^^^^
Copyright (c) 2020 Penguin0093
Released under the MIT license
https://opensource.org/licenses/mit-license.php




How to use it.
===============

The basic style is::

	iniio.iopen("File name","Open mode","section","option","value")

| First argument: File Name
| Second argument: mode (Write : w ,Read : r ,Delete : d)
| Third argument: section name ([] in)
| Fourth argument: option name (left of "=")
| Fifth argument: value (to the right of "=")


1.Import
^^^^^^^^^^^
::

	from editini Import iniio


2.Writing
^^^^^^^^^^
Code
::

	iniio.iopen("config.ini","w","section","option","value")

Result config.ini
::

	[section]
	option = value

If the "value" is empty, "" (empty character) is substituted


3.Reading
^^^^^^^^^^
::

	iniio.iopen(" .ini","r","section","option")

| The return value is the read result.

config.ini
::

	[section]
	option = value


Code
::

	print(iniio.iopen("config.ini","r","section","option")+"\n")
	print(iniio.iopen("config.ini","r","section")+"\n")
	print(iniio.iopen("config.ini","r")+"\n")

Result
::

	value

	option = value

	[section]
	option = value


4.Delete
^^^^^^^^^^
::

	iniio.iopen(" .ini","d","section","option")

config.ini
::

	[section]
	option = value



Code #1
::

	iniio.iopen("config.ini","d","section","option")


Result #1 config.ini
::

	[section]



Code #2
::

	iniio.iopen("config.ini","d","section")

Result #2 config.ini
::

	(Empty)


`Click here for details (Japanese) <http://penguin0093.html.xdomain.jp/page/project/python/editini.html>`_