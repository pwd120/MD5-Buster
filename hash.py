import sys
import hashlib
import urllib2
import getopt
from os import path
from urllib import urlencode
from re import search, findall
from random import seed, randint
from base64 import decodestring, encodestring
from cookielib import LWPCookieJar
from httplib2 import Http
from libxml2 import parseDoc

########################################################################################################
### CONSTANTS
########################################################################################################

MD5 	= "md5"

USER_AGENTS = [
	"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Crazy Browser 1.0.5)",
	"curl/7.7.2 (powerpc-apple-darwin6.0) libcurl 7.7.2 (OpenSSL 0.9.6b)",
	"Mozilla/5.0 (X11; U; Linux amd64; en-US; rv:5.0) Gecko/20110619 Firefox/5.0",
	"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b8pre) Gecko/20101213 Firefox/4.0b8pre",
	"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
	"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)",
	"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0) chromeframe/10.0.648.205",
	"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727)",
	"Opera/9.80 (Windows NT 6.1; U; sv) Presto/2.7.62 Version/11.01",
	"Opera/9.80 (Windows NT 6.1; U; pl) Presto/2.7.62 Version/11.00",
	"Opera/9.80 (X11; Linux i686; U; pl) Presto/2.6.30 Version/10.61",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.861.0 Safari/535.2",
	"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.872.0 Safari/535.2",
	"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.812.0 Safari/535.1",
	"Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
	]
	


########################################################################################################
### CRACKERS DEFINITION
########################################################################################################


class MY_ADDR:
	
	name = 		"Alpha"
	url = 		""
	supported_algorithm = [MD5]

	def crack (self, hashvalue, alg):
		"""Try to crack the hash.
		@param hashvalue Hash to crack.
		@param alg Algorithm to crack."""
		
		# Build the URL
		url = "http://md5.my-addr.com/md5_decrypt-md5_cracker_online/md5_decoder_tool.php"
		
		# Build the parameters
		params = { "md5" : hashvalue,
			   "x" : 21,
			   "y" : 8 }
		
		# Make the request
		response = do_HTTP_request ( url, params )
		
		# Analyze the response
		html = None
		if response:
			html = response.read()
		else:
			return None
		
		match = search (r"<span class='middle_title'>Hashed string</span>: [^<]*</div>", html)
		
		if match:
			return match.group().split('span')[2][3:-6]
		else:
			return None


class MD5DECRYPTION:
	
	name = 		"Delta"
	url = 		""
	supported_algorithm = [MD5]
	
	def isSupported (self, alg):
		"""Return True if HASHCRACK can crack this type of algorithm and
		False if it cannot."""
		
		if alg in self.supported_algorithm:
			return True
		else:
			return False


	def crack (self, hashvalue, alg):
		"""Try to crack the hash.
		@param hashvalue Hash to crack.
		@param alg Algorithm to crack."""
		
		# Check if the cracker can crack this kind of algorithm
		if not self.isSupported (alg):
			return None
		
		# Build the URL
		url = self.url
		
		# Build the parameters
		params = { "hash" : hashvalue,
			   "submit" : "Decrypt It!" }
		
		# Make the request
		response = do_HTTP_request ( url, params )
		
		# Analyze the response
		html = None
		if response:
			html = response.read()
		else:
			return None
		
		match = search (r"Decrypted Text: </b>[^<]*</font>", html)
		
		if match:
			return match.group().split('b>')[1][:-7]
		else:
			return None



CRACKERS = [
		MY_ADDR,
		MD5DECRYPTION]



########################################################################################################
### GENERAL METHODS
########################################################################################################

def configureCookieProcessor (cookiefile='/tmp/searchmyhash.cookie'):
	'''Set a Cookie Handler to accept cookies from the different Web sites.
	
	@param cookiefile Path of the cookie store.'''
	
	cookieHandler = LWPCookieJar()
	if cookieHandler is not None:
		if path.isfile (cookiefile):
			cookieHandler.load (cookiefile)
			
		opener = urllib2.build_opener ( urllib2.HTTPCookieProcessor(cookieHandler) )
		urllib2.install_opener (opener)



def do_HTTP_request (url, params={}, httpheaders={}):
	'''
	Send a GET or POST HTTP Request.
	@return: HTTP Response
	'''

	data = {}
	request = None
	
	# If there is parameters, they are been encoded
	if params:
		data = urlencode(params)

		request = urllib2.Request ( url, data, headers=httpheaders )
	else:
		request = urllib2.Request ( url, headers=httpheaders )
		
	# Send the request
	try:
		response = urllib2.urlopen (request)
	except:
		return ""
	
	return response


def printSyntax ():
	print """\033[1;94m       _  _ ___   ___   ___  _  _ ____ ___ ____ ____ 
       |\/| |  \ |___   |__] |  | [__   |  |___ |__/ 
       |  | |__/  __/   |__] |__| ___]  |  |___ |  \\ v0.3\033[1;m"""
	print "\t\033[1;32m    Servers Loaded: Alpha, Delta, Gamma\033[1;m"
	hashvalue = raw_input('\033[1;91mEnter your MD5 hash: \033[1;m')
	return crackHash(MD5, hashvalue=hashvalue, hashfile=None)



def crackHash (algorithm, hashvalue=None, hashfile=None):
	"""Crack a hash or all the hashes of a file.
	
	@param alg Algorithm of the hash (MD5, SHA1...).
	@param hashvalue Hash value to be cracked.
	@param hashfile Path of the hash file.
	@return If the hash has been cracked or not."""
	
	global CRACKERS
	
	# Cracked hashes will be stored here
	crackedhashes = []
	
	# Is the hash cracked?
	cracked = False
	
	# hashestocrack depends on the input value
	hashestocrack = None
	if hashvalue:
		hashestocrack = [ hashvalue ]
	else:
		try:
			hashestocrack = open (hashfile, "r")
		except:
			print "\nIt is not possible to read input file (%s)\n" % (hashfile)
			return cracked
	
	
	# Try to crack all the hashes...
	for activehash in hashestocrack:
		hashresults = []
		
		# Standarize the hash
		activehash = activehash.strip()
		if algorithm not in [MD5]:
			activehash = activehash.lower()

		# Each loop starts for a different start point to try to avoid IP filtered
		begin = randint(0, len(CRACKERS)-1)
		
		for i in range(len(CRACKERS)):
			
			# Select the cracker
			cr = CRACKERS[ (i+begin)%len(CRACKERS) ]()
			
			# Analyze the hash
			print "Cracking using %s %s" % (cr.name, cr.url)
			
			# Crack the hash
			result = None
			try:
				result = cr.crack ( activehash, algorithm )
			# If it was some trouble, exit
			except:
				print "\nSomething was wrong. Please, contact with us to report the bug:\n\nbloglaxmarcaellugar@gmail.com\n"
				if hashfile:
					try:
						hashestocrack.close()
					except:
						pass
				return False
			
			# If there is any result...
			cracked = 0
			if result:
				
				# If it is a hashlib supported algorithm...
				if algorithm in [MD5]:
					# Hash value is calculated to compare with cracker result
					h = hashlib.new (algorithm)
					h.update (result)
					
					# If the calculated hash is the same to cracker result, the result is correct (finish!)
					if h.hexdigest() == activehash:
						hashresults.append (result)
						cracked = 2
				
				# If it is a half-supported hashlib algorithm
				elif algorithm in [MD5]:
					alg = algorithm.split('_')[1]
					ahash =  decodestring ( activehash.split('}')[1] )
					
					# Hash value is calculated to compare with cracker result
					h = hashlib.new (alg)
					h.update (result)
					
					# If the calculated hash is the same to cracker result, the result is correct (finish!)
					if h.digest() == ahash:
						hashresults.append (result)
						cracked = 2
				
				# If it is another algorithm, we search in all the crackers
				else:
					hashresults.append (result)
					cracked = 1
			
			# Had the hash cracked?
			if cracked:
				print "\033[1;32mHash Cracked!\033[1;m"
				# If result was verified, break
				if cracked == 2:
					break
			else:
				print "....."
		
		
		# Store the result/s for later...
		if hashresults:
			
			# With some hash types, it is possible to have more than one result,
			# Repited results are deleted and a single string is constructed.
			resultlist = []
			for r in hashresults:
				#if r.split()[-1] not in resultlist:
					#resultlist.append (r.split()[-1])
				if r not in resultlist:
					resultlist.append (r)
					
			finalresult = ""
			if len(resultlist) > 1:
				finalresult = ', '.join (resultlist)
			else:
				finalresult = resultlist[0]
			
			# Valid results are stored
			crackedhashes.append ( (activehash, finalresult) )
	
	
	# Loop is finished. File can need to be closed
	if hashfile:
		try:
			hashestocrack.close ()
		except:
			pass
		
	# Show a resume of all the cracked hashes
	print "\nResult\n----------------------------------\n"
	print crackedhashes and "\n".join ("%s -> %s" % (hashvalue, result.strip()) for hashvalue, result in crackedhashes) or "NO HASH WAS CRACKED."
	print
	
	return cracked




def searchHash (hashvalue):
	'''Google the hash value looking for any result which could give some clue...
	
	@param hashvalue The hash is been looking for.'''
	
	start = 0
	finished = False
	results = []
	
	sys.stdout.write("\nThe hash wasn't found in any database. Maybe Google has any idea...\nLooking for results...")
	sys.stdout.flush()
	
	while not finished:
		
		sys.stdout.write('.')
		sys.stdout.flush()
	
		# Build the URL
		url = "http://www.google.com/search?hl=en&q=%s&filter=0" % (hashvalue)
		if start:
			url += "&start=%d" % (start)
			
		# Build the Headers with a random User-Agent
		headers = { "User-Agent" : USER_AGENTS[randint(0, len(USER_AGENTS))-1] }
		
		# Send the request
		response = do_HTTP_request ( url, httpheaders=headers )
		
		# Extract the results ...
		html = None
		if response:
			html = response.read()
		else:
			continue
			
		resultlist = findall (r'<a href="[^"]*?" class=l', html)
		
		# ... saving only new ones
		new = False
		for r in resultlist:
			url_r = r.split('"')[1]
			
			if not url_r in results:
				results.append (url_r)
				new = True
		
		start += len(resultlist)
		
		# If there is no a new result, finish
		if not new:
			finished = True
		
	
	# Show the results
	if results:
		print "\n\nGoogle has some results. Maybe you would like to check them manually:\n"
		
		results.sort()
		for r in results:
			print "  *> %s" % (r)
		print
	
	else:
		print "\n\nGoogle doesn't have any result. Sorry!\n"


########################################################################################################
### MAIN CODE
########################################################################################################

def main():
	"""Main method."""


	###################################################
	# Syntax check
	if len (sys.argv) < 4:
		printSyntax()
		sys.exit(1)
	
	else:
		try:
			opts, args = getopt.getopt (sys.argv[2:], "gh:f:")
		except:
			printSyntax()
			sys.exit(1)
	
	
	###################################################
	# Load input parameters
	algorithm = sys.argv[1].lower()
	hashvalue = None
	hashfile  = None
	googlesearch = False
	
	for opt, arg in opts:
		if opt == '-h':
			hashvalue = arg
		elif opt == '-f':
			hashfile = arg
		else:
			googlesearch = True
	
	
	###################################################
	# Configure the Cookie Handler
	configureCookieProcessor()
	
	# Initialize PRNG seed
	seed()
	
	cracked = 0
	
	
	###################################################
	# Crack the hash/es
	cracked = crackHash (algorithm, hashvalue, hashfile)
	
	
	###################################################
	# Look for the hash in Google if it was not cracked
	if not cracked and googlesearch and not hashfile:
		searchHash (hashvalue)
	
	
	
	# App is finished
	sys.exit()



if __name__ == "__main__":
    main()
