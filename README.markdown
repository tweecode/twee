README : tweecode/twee
======

To run twee, you will need a copy of this code, a local Python installation, and a .tw file.  You can get this fork from github using, for example, the ZIP button.  Python should come pre-installed on a Mac; a Windows installer is available at [python.org](http://www.python.org/getit/).

Once you have all those, open the Terminal or a command prompt, change to the twee directory, and type something like:

    ./twee my-input-file.tw > my-output-file.html

To compile to Sugarcane instead of Jonah, use the -t flag:

    ./twee -t sugarcane my-input-file.tw > my-other-output-file.html

To export the story data to JSON (which could be used by third-party programs like [Twine for AS3](https://github.com/emmett9001/twine-as3)), simply use

    ./twee -t json my-input-file.tw > my-story-output.json
