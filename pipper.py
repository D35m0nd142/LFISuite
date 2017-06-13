import os
import sys
import urllib
import subprocess

def download(file_url,local_filename):
	web_file = urllib.urlopen(file_url)
	local_file = open(local_filename, 'w')
	local_file.write(web_file.read())
	web_file.close()
	local_file.close()

def get_windows_pip_path():
	python_dir = sys.executable
	split = python_dir.split("\\")
	pip_path = ""
	for i in range(0,len(split)-1):
		pip_path = "%s/%s" %(pip_path,split[i])
	pip_path = "%s/Scripts/pip" %pip_path[1:]

	return pip_path

def pip_install_module(module_name):
	pip_path = "pip"
	DEVNULL = open(os.devnull,'wb')
	new_installation = True

	try:
		subprocess.call(["pip"], stdout=DEVNULL) # verify if pip is already installed
	except OSError as e:
		if(sys.platform[:3] == "win"):
			pip_path = get_windows_pip_path()
			try:
				subprocess.call([pip_path],stdout=DEVNULL)
				new_installation = False
				print "[+] Found Windows pip executable at '%s'" %pip_path
			except:
				pass

		if(new_installation):
			print "[!] pip is not currently installed."

			if(os.path.isfile("get-pip.py") is False):
				print "[*] Downloading get-pip.py.."
				download("https://bootstrap.pypa.io/get-pip.py","get-pip.py")
			else:
				print "[+] get-pip-py found in the current directory."

	    	os.system("python get-pip.py")

	    	try:
	    		subprocess.call(["pip"],stdout=DEVNULL)
	    	except:
	    		if(sys.platform[:3] == "win"):
		    		python_dir = sys.executable # "C:\\Python27\\python.exe"
		    		split = python_dir.split("\\")
		    		pip_path = ""
		    		for i in range(0,len(split)-1): # let's avoid python.exe
		    			pip_path = "%s/%s" %(pip_path,split[i])

		    		pip_path = "%s/Scripts/pip" %pip_path[1:]

	if(new_installation):
		try:
			os.remove("get-pip.py")
		except:
			pass

	os.system("%s install --upgrade pip" %pip_path)
	print "\n[*] Installing module '%s'" %module_name
	os.system("%s install %s" %(pip_path,module_name))

