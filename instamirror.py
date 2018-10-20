#!/usr/bin/env python 
from InstagramAPI import InstagramAPI
from PIL import Image
from resizeimage import resizeimage
import time
import urllib
import urllib2
import json
import os
import argparse

class config:
	def loadConfig(self,confile):
		with open(confile, 'r') as f:
			configuredata = json.load(f)
    		return configuredata

	def fbURL(self,datastream):
		GraphAPI = datastream["facebook"]["GraphAPIURL"]
		pageID = datastream["facebook"]["PageID"]
		GAPIMethod = datastream["facebook"]["GraphAPINode"]
		PageToken = datastream["facebook"]["PageToken"]
		qURL = GraphAPI+pageID+GAPIMethod+PageToken
		return qURL
	def fbConf(self,datastream):
		rTime = datastream["facebook"]["RefreshInterval"]
		eString = datastream["facebook"]["PostExcludeSignature"]
		fbVal = [rTime,eString]
		return fbVal

	def instaLogon(self,datastream):
		InstaUser = datastream["instagram"]["UserName"]
		InstaPass = datastream["instagram"]["Password"]
		global InstagramAPI
		# Instagram Login
		InstagramAPI = InstagramAPI(InstaUser,InstaPass)
		InstagramAPI.login()  # login
		


	

parser = argparse.ArgumentParser()
parser.add_argument("-c","--configfile", help="Path to json configuration input file.", default = "instamirror_beta.config")
args = parser.parse_args()
if not os.path.isfile(args.configfile):
	print "The provided configfile is not a valid path."
	parser.print_help()
	exit()

cinstance = config() # instantiating config class
cnf = cinstance.loadConfig(args.configfile) # loading value
qURL = cinstance.fbURL(cnf) # generating fb api link
rTime = cinstance.fbConf(cnf)[0]
eString = cinstance.fbConf(cnf)[1]
cinstance.instaLogon(cnf)

tstp = 1 # Timestamp placeholder	
minAsp = 0.9
maxAsp = 1.8
eFlag = 0

# Loop to regularly query page feed for new posts
while True:
	eFlag = 0
	mFlag = 0
	try :
		fbFeed = urllib2.urlopen(qURL)
	except:
		print "Couldnt load feed from FB"
		time.sleep(300)
		continue
	lPost = json.load(fbFeed) 
	print "Loading the page feed..."

	try:
		# Separating data from the feed json response.
		lCaption = lPost["data"][0]["attachments"]["data"][0]["description"]
		lPhotoSrc = lPost["data"][0]["attachments"]["data"][0]["media"]["image"]["src"]
		lHeight = float(lPost["data"][0]["attachments"]["data"][0]["media"]["image"]["height"])
		lWidth = float(lPost["data"][0]["attachments"]["data"][0]["media"]["image"]["width"])
		lAspRatio = lWidth/lHeight
		lTimstamp = lPost["data"][0]["created_time"]

	except:
		print "Error loading structured facebook feed. \n Potentially due to a post without caption or feed unreachable."
		continue
	datafile = file('log.txt')
	for line in datafile:
		if str(lTimstamp) in line:
			mFlag = 1
			break
	# Set the flag if the caption contains any unsupported string
	for s in eString:
		if s in lCaption:
			eFlag = 1


	# whether any new post was uploaded on page 
	if lTimstamp > tstp:
		print "There is a new post on page..."
		print "Adding the timestamp to log"
		tstplog = str(lTimstamp)+"\n"
		with open("log.txt", "a") as myfile:
			myfile.write(tstplog)
		tstp = lTimstamp # update placeholder value
		print "Aspect ratio of the new image: ",lHeight,"/",lWidth,"=",lAspRatio,"\n"
		
		if eFlag == 1 or mFlag == 1:
			print "This post contains an exclude string configured via the config file or was already posted."
			print "This will not be posted."
		else:
			print "Post does not include any exclude strings and wasn't posted earlier"
			print "Proceeding further..."

			# Check whether the photo has a valid aspect ratio.
			if (lAspRatio >= minAsp) and (lAspRatio <= maxAsp) :
				print "The new post is of instagram supported aspect ratio"
				print "Downloading the image"

				# Download the file and store it with the name timestamp.jpg
				filename = str(lTimstamp)+".jpg"
				urllib.urlretrieve(lPhotoSrc, filename)
				print "Image saved successfully as ",filename
				
				# Instagram Photo Upload
				print "Posting the image to instagram"
				InstagramAPI.uploadPhoto(filename, caption=lCaption)

				# Cleanup to save file space
				os.remove(filename)
				print "Clean Up: ", filename, " was deleted"

			elif lAspRatio < minAsp:
				# Defining the instagram supported aspect ratio for new image.
				nHeight = lHeight
				nWidth = minAsp*nHeight
				print "The aspect ratio of attached image is unsupported by instagram."
				print "Reason: Image height is too large"
			
				# Downloading the original file.
				print "Downloading the image"
				originalFile = str(lTimstamp)+".jpeg" # Naming
				urllib.urlretrieve(lPhotoSrc, originalFile)
				print "Image saved successfully as ",originalFile

				# Resizing the original incompatible file
				print "Resizing image to an instagram compatible aspect ratio"
				resizeFile = "resized_"+originalFile # Naming resized image
				img = Image.open(originalFile)
				img = resizeimage.resize_contain(img, [int(nWidth), int(nHeight)])
				img.save(resizeFile, img.format)
				print "Imgae resized successfully as ",resizeFile

				#Posting the new resized image to instagram.
				print "Posting the image to instagram"
				InstagramAPI.uploadPhoto(resizeFile, caption=lCaption)

				# Cleanup to save file space
				os.remove(originalFile)
				os.remove(resizeFile)
				print "Clean Up: "+ originalFile +" & "+ resizeFile + " was deleted"

			elif lAspRatio > maxAsp:
				# Defining the instagram supported aspect ratio for new image.
				nWidth = lWidth
				nHeight = nWidth/maxAsp
				print "The aspect ratio of attached image is unsupported by instagram."
				print "Reason: Image is too wide"
	
				# Downloading the original file.
				print "Downloading the image"
				originalFile = str(lTimstamp)+".jpeg" # Naming
				urllib.urlretrieve(lPhotoSrc, originalFile)
				print "Image saved successfully as ",originalFile

				# Resizing the original incompatible file
				print "Resizing image to an instagram compatible aspect ratio"
				resizeFile = "resized_"+originalFile # Naming resized image
				img = Image.open(originalFile)
				img = resizeimage.resize_contain(img, [int(nWidth), int(nHeight)])
				img.save(resizeFile, img.format)
				print "Imgae resized successfully as ",resizeFile

				#Posting the new resized image to instagram.
				print "Posting the image to instagram"
				InstagramAPI.uploadPhoto(resizeFile, caption=lCaption)

				# Cleanup to save file space
				os.remove(originalFile)
				os.remove(resizeFile)
				print "Clean Up: "+ originalFile +" & "+ resizeFile + " was deleted"

			else:
				# This could have been the previous elif. But for troubleshooting.
				print "Invalid aspect ratio"

	else:
		print "No new post"

	time.sleep (rTime)
