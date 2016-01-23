import requests
import requests.auth
import json
import sys
import shutil
import os
import random
from time import gmtime, strftime
from PIL import Image
import subprocess

CLIENT_ID='X'
SECRET='X'
USERNAME="X"
PASSWORD="X"
USER_AGENT_HEADER = " courtesy of X"
DIR = "X"
WRITE_DIR = DIR + "images/"
LOG_FILE = DIR + "log.txt"
SUBREDDITS = ["earthporn"]

def get_access_token():
	client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET)
	post_data = {"grant_type": "password", "username": USERNAME, "password": PASSWORD}
	headers = {"User-Agent": USER_AGENT_HEADER}
	response = requests.post("https://ssl.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
	json = response.json()
	return json["access_token"]

def get_imgur_url(access_token, subreddit):
	# auth headers
	auth_header = "bearer " + access_token
	headers = {"Authorization": auth_header, "User-Agent": USER_AGENT_HEADER}
	time_periods = ["year", "day", "month", "week"]
	random.shuffle(time_periods)
	time_period = time_periods[0]
	url = "https://oauth.reddit.com/r/" + subreddit + "/top/.json?limit=20&sort=top&t=day"
	response = requests.get(url, headers=headers)
	json = response.json()
	# parse the json response
	data = json["data"]
	children = data["children"]
	if len(children) < 1:
		print "Got bad json back from reddit: " + json
	else:
		# else we should refactor this iceberg of code below
		# get a random imgur post from the list of posts
		random.shuffle(children)
		log_file.write("Got this many links: " + str(len(children)) + "\n")
		for post in children:
			data = post["data"]
			img_url = data["url"]
			if "i.imgur" in img_url:
				log_file.write("Getting image from url " + img_url + "\n")

				img_response = requests.get(img_url, stream=True)

				# delete existing images in the images directory
				for the_file in os.listdir(WRITE_DIR):
				    file_path = os.path.join(WRITE_DIR, the_file)
				    try:
				        if os.path.isfile(file_path):
				            os.unlink(file_path)
				    except Exception, e:
				        print e

				# construct the file name to save to
				# the image file name should be in the url after the final '/' if the post is from imgur
				img_url_tokens = img_url.split('/')
				img_file_name = img_url_tokens[len(img_url_tokens) - 1]
				image_location = WRITE_DIR + img_file_name
				f = open(image_location, 'wb')
				img_response.raw.decode_content = True
				shutil.copyfileobj(img_response.raw, f)
				image_file = Image.open(image_location)
				width, height = image_file.size
				if width > 1600:
					log_file.write("image file size " + str(image_file.size) + " from subreddit " + subreddit + " exiting\n")
					# set background with the image
					#SCRIPT = """/usr/bin/osascript<<END
					#tell application "Finder"
					#set desktop picture to POSIX file "%s"
					#end tell
					#END"""

					#subprocess.Popen(SCRIPT%image_location, shell=True)
					sys.exit(0)
		log_file.write("Got a page of posts without any imgur links. Wierd " + subreddit + ". Exiting \n")
		# TODO: get a new page
		sys.exit(1)

# select a random subreddit from our list
random.shuffle(SUBREDDITS)
subreddit = SUBREDDITS[0]

log_file = open(LOG_FILE, 'a')
log_file.write("\n")
curr_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
#log_file.write("Running for subreddit " + subreddit + " time: " + curr_time + "\n")

# get an access token from reddit so we can use oauth
access_token = get_access_token()
get_imgur_url(access_token, subreddit)
