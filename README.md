# LFI Suite

![alt tag](https://github.com/D35m0nd142/LFISuite/blob/master/screenshot.png)

<h3> What is LFI Suite? </h3>

LFI Suite is a totally <b>automatic</b> tool able to scan and exploit Local File Inclusion vulnerabilities using many different methods of attack, listed in the section `Features`.

<h3> Features </h3>

* Works with Windows, Linux and OS X
* It provides 8 different Local File Inclusion attack modalities:
  - /proc/self/environ
  - php://filter
  - php://input
  - /proc/self/fd
  - access log
  - phpinfo
  - data://
  - expect://

* It provides a ninth modality called <b>Auto-Hack</b>, which scans and exploits the target automatically by trying all the attacks one after the other without you having to do anything (except for providing, at the beginning, a list of paths to scan, which if you don't have you can find in this project directory in two versions, small and huge). 
* Tor proxy support
* Reverse Shell for Windows, Linux and OS X


<h3> Dependencies </h3>

* Python <b>2.7</b>.x
* Python modules to install: termcolor, requests
* socks.py available in this Github project directory

<h3> Disclaimer </h3>

I am not responsible for any kind of illegal acts you cause. This is meant to be used for ethical purposes by penetration testers. If you plan to copy, redistribute please give credits to the original author.

Video: Be patient..it will be available in a few days
Follow me: https://twitter.com/d35m0nd142
