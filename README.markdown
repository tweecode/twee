README : mcdemarco/twee
======

This is a working fork of tweecode/twee, the command-line python script to compile twee files into HTML.  It includes the 1.2 patch to Sugarcane for the &lt;&lt;back>> macro, but no support yet in Jonah for &lt;&lt;back>>.

This fork has been tested with Python 2.6.1 and 2.7.2 on Mac OS 10.6.8.

***

To run twee, you will need a copy of this fork, a local Python installation, and a .tw file.  You can get this fork from github using, for example, the ZIP button.  Python should come pre-installed on a Mac; a Windows installer is available at [python.org](http://www.python.org/getit/).  You can find some sample twee files at [gimcrackd.com](http://gimcrackd.com/).

Once you have all those, open the Terminal or a command prompt, change to the twee directory, and type something like:

    ./twee my-input-file.tw > my-output-file.html

To compile to Sugarcane instead of Jonah, use the -t flag:

    ./twee -t sugarcane my-input-file.tw > my-other-output-file.html

The other targets are not recommended.  

***

See the [twee documentation](http://gimcrackd.com/etc/doc/) for more information about twee.  