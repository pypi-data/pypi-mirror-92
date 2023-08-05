import setuptools, os, platform, sys, re
from base64 import b64encode

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="besocurl",
    version="0.0.3",
    author="Omri Baso",
    author_email="omribaso6@gmail.com",
    description="A library wrapper for PyCurl combained with WinAPI calls to support automatic proxy detection with a 'requests'-like infterface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OmriBaso/besocurl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)

def make_powershell(strr):
    return b64encode(strr.encode('UTF-16LE')).decode('UTF-8')

if sys.argv[1].lower() == "install":
    if platform.system() == "Linux":
        os.system("apt install libcurl4-openssl-dev libssl-dev -y")
        os.system("apt install python-dev python3-dev build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev -y")
        py_ver = platform.python_version()
        os.system("%s -m pip install setuptools wheel pycurl -y" % sys.executable)
        os.system("%s -m pip install setuptools wheel pycurl -y" % sys.executable)
    elif platform.system() == "Windows":
        py_ver = re.search(r"(\d.\d)",platform.python_version().strip()).group(1)
        import struct
        py_bit_rate = "win-amd64" if 8 * struct.calcsize("P") == 64 else "win32"
        search_string = "%s-py%s.exe" % (py_bit_rate, py_ver)
        check_py_curl_version = os.popen("powershell -enc %s" % make_powershell('(New-Object Net.WebClient).downloadString("https://dl.bintray.com/pycurl/pycurl/") ; exit')).read()
        check_py_curl_version = re.search("(pycurl.*{}?)\"".format(search_string), check_py_curl_version).group(1)
        print("[+] Downloading %s" % check_py_curl_version)
        download_file = 'powershell (New-Object Net.WebClient).DownloadFile("https://dl.bintray.com/pycurl/pycurl/%s", "$env:TEMP\pycurl-install.exe") ; exit'.strip("\n") % check_py_curl_version
        os.popen("powershell -enc %s" % make_powershell(download_file))
        print("[+] Installing PyCurl")
        os.popen("powershell -enc %s" % make_powershell('cmd /c "$env:TEMP\pycurl-install.exe"'))

