#!/usr/bin/env python
from urllib import *
from re import search, findall
print((56 * '\033[31m-\033[1;m'))
print """\033[1;97m   _  _ ___   ___   ___  _  _ ____ ___ ____ ____ 
   |\/| |  \ |___   |__] |  | [__   |  |___ |__/      
   |  | |__/  __/   |__] |__| ___]  |  |___ |  \\ v0.3\033[1;m"""
print "\t\033[1;32m  Servers Loaded: Alpha, Delta, Gamma\033[1;m"
print((56 * '\033[31m-\033[1;m'))
hashvalue = raw_input('\033[97mEnter your MD5 hash: \033[1;m')
try:
    data = urlencode({"hash":hashvalue,"submit":"Decrypt It!"})
    html = urlopen("http://md5decryption.com", data)
    find = html.read()
    match = search(r"Decrypted Text: </b>[^<]*</font>", find)
    if len(hashvalue) != 0:
    	print "\033[1;31m[Error] Invalid MD5 hash\033[1;m"
    	exit()
    if match:
    	print "\n\033[1;32mHash cracked by Alpha:\033[1;m", match.group().split('b>')[1][:-7]
    else:
    	data = urlencode({"md5":hashvalue,"x":"21","y":"8"})
        html = urlopen("http://md5.my-addr.com/md5_decrypt-md5_cracker_online/md5_decoder_tool.php", data)
        find = html.read()
        match = search (r"<span class='middle_title'>Hashed string</span>: [^<]*</div>", find)    
        if match:
            print "\n\033[1;32mHash cracked by Beta:\033[1;m", match.group().split('span')[2][3:-6]
        else:
            url = "http://www.nitrxgen.net/md5db/" + hashvalue
            purl = urlopen(url).read()
            if len(purl) > 0:
                print "\n\033[1;32mHash cracked by Gamma:\033[1;m", purl
            else:
            	print "\033[1;31mSorry this hash is not present in our database.\033[1;m"
except len(hashvalue) == 0:
	print "Empty Input"
