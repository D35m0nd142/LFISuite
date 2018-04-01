![Version 1.13](https://img.shields.io/badge/Version-1.13-green.svg)
![Python 2.7.x](https://img.shields.io/badge/Python-2.7.x-yellow.svg)
[![GPLv3 License](https://img.shields.io/badge/License-GPLv3-red.svg)](https://github.com/D35m0nd142/LFISuite/blob/master/COPYING.GPL)
[![Twitter](https://img.shields.io/badge/Twitter-%40d35m0nd142-blue.svg)](https://www.twitter.com/d35m0nd142)

# LFI Suite

![alt tag](https://github.com/D35m0nd142/LFISuite/blob/master/screen.png)

<h3> What is LFI Suite? </h3>

LFI Suite is a totally <b>automatic</b> tool able to scan and exploit Local File Inclusion vulnerabilities using many different methods of attack, listed in the section `Features`.

* * * 

<h3> Features </h3>

* Works with Windows, Linux and OS X
* Automatic Configuration 
* Automatic Update
* Provides 8 different Local File Inclusion attack modalities:
  - /proc/self/environ
  - php://filter
  - php://input
  - /proc/self/fd
  - access log
  - phpinfo
  - data://
  - expect://

* Provides a ninth modality, called <b>Auto-Hack</b>, which scans and exploits the target automatically by trying all the attacks one after the other without you having to do anything (except for providing, at the beginning, a list of paths to scan, which if you don't have you can find in this project directory in two versions, small and huge). 
* Tor proxy support
* Reverse Shell for Windows, Linux and OS X


<h3> How to use it? </h3>

Usage is extremely simple and LFI Suite has an easy-to-use user interface; just run it and let it lead you.
##### Reverse Shell
When you got a LFI shell by using one of the available attacks, you can easily obtain a reverse shell by entering the command <b>"reverseshell"</b> (obviously you must put your system listening for the reverse connection, for instance using <b>"nc -lvp port"</b>).

<h3> Dependencies </h3>

* Python <b>2.7</b>.x
* Python extra modules: termcolor, requests
* socks.py 

> When you run the script, in case you are missing some modules, it will check if you have <b>pip</b> installed and, in case you don't, it will install it <b>automatically</b>, then using pip it will install also the missing modules and download the necessary file <b>socks.py</b>.<br>I tried it on different operating systems (Debian,Ubuntu,Fedora,Windows 10,OS X) and it worked great, but if something strange happens to you and the automatic installation of pip and other modules fails, please install missing modules manually and re-run the script.
<br>![#f03c15](https://placehold.it/15/f03c15/000000?text=+) <b>IMPORTANT: In order to allow the script to install missing modules (and in case pip) automatically, you MUST run the script as root (or, at least, with sufficient permissions) the first time.</b>

<h3> Collaboration </h3>

LFI Suite already contains a lot of features but, as you probably know, there are plenty of other possible attacks still to implement.
If you are a Python programmer/Penetration tester and you want to join this project in order to improve it and extend it, please contact me at <<b>d35m0nd142@gmail.com</b>> or directly here.

<h3> Disclaimer </h3>

I am not responsible for any kind of illegal acts you cause. This is meant to be used for ethical purposes by penetration testers. If you plan to copy, redistribute please give credits to the original author.

Video: https://www.youtube.com/watch?v=6sY1Skx8MBc <br>
Follow me: <b>https://twitter.com/d35m0nd142</b>
