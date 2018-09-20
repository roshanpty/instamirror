#!/usr/bin/env python 
from InstagramAPI import InstagramAPI
from PIL import Image
from resizeimage import resizeimage
import time
import urllib
import urllib2
import json
import os

# Loading config file with Facebook API details
# The page token need to be a 'Page Access Token'

with open('instabotconfig.json', 'r') as f:
    config = json.load(f)
print "Configuration file loaded."
print "Changes in credentials must be made to the configuration file only after quitting the instamirror program."

tstp = 1 # Timestamp placeholder
lAspRatio = 1.11 # Aspect Ratio float holder
minAsp = 0.8
maxAsp = 1.9
GraphAPI = config["facebook"]["GraphAPIURL"]
pageID = config["facebook"]["PageID"]
GAPIMethod = config["facebook"]["GraphAPINode"]
PageToken = config["facebook"]["PageToken"]
rTime = config["facebook"]["RefreshInterval"]
InstaUser = config["instagram"]["UserName"]
InstaPass = config["instagram"]["Password"]

# Constructing the URL to query for last post on page.

qURL = GraphAPI+pageID+GAPIMethod+PageToken

# Instagram Login
InstagramAPI = InstagramAPI(InstaUser,InstaPass)
InstagramAPI.login()  # login

# Loop to regularly query page feed for new posts
while True:
	fbFeed = urllib2.urlopen(qURL)
	lPost = json.load(fbFeed) 
	print "Loading the page feed..."

	# Separating data from the feed json response.
	lCaption = lPost["data"][0]["attachments"]["data"][0]["description"]
	lPhotoSrc = lPost["data"][0]["attachments"]["data"][0]["media"]["image"]["src"]
	lHeight = lPost["data"][0]["attachments"]["data"][0]["media"]["image"]["height"]
	lWidth = lPost["data"][0]["attachments"]["data"][0]["media"]["image"]["width"]
	lAspRatio = lWidth/lHeight
	lTimstamp = lPost["data"][0]["created_time"]

	# whether any new post was uploaded on page 
	if lTimstamp > tstp:
		print "There is a new post on page..."
		tstp = lTimstamp # update placeholder value

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
			nWidth = 0.9*nHeight
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
#			fd_img = open(originalFile, 'r')
#			img = Image.open(fd_img)
			img = Image.open(originalFile)
			img = resizeimage.resize_contain(img, [int(nWidth), int(nHeight)])
			img.save(resizeFile, img.format)
#			img.close()
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
			nHeight = nWidth/1.8
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
#			fd_img = open(originalFile, 'r')
#			img = Image.open(fd_img)
			img = Image.open(originalFile)
			img = resizeimage.resize_contain(img, [int(nWidth), int(nHeight)])
			img.save(resizeFile, img.format)
#			fd_img.close()
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
