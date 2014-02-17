README : tweecode/twee
======

To run twee, you will need a copy of this code, a local Python installation, and a .tw file.  You can get this fork from github using, for example, the ZIP button.  Python should come pre-installed on a Mac; a Windows installer is available at [python.org](http://www.python.org/getit/).  You can find some sample twee files at [gimcrackd.com](http://gimcrackd.com/).

Once you have all those, open the Terminal or a command prompt, change to the twee directory, and type something like:

    ./twee my-input-file.tw > my-output-file.html

To compile to Sugarcane instead of Jonah, use the -t flag:

    ./twee -t sugarcane my-input-file.tw > my-other-output-file.html

Fork by @emmett9001
-------------------

This fork of twee adds the ability to export to the JSON interchange format. This feature is most useful when exporting twine story data for use in other media settings, such as embedding in another python program, or in an actionscript applet via [twine for actionscript](https://github.com/emmett9001/twine-as3) by Emmett Butler.

To export with JSON, simply use

    ./twee -t json my-input-file.tw > my-story-output.json

***

See the [twee documentation](http://gimcrackd.com/etc/doc/) for more information about twee.  
