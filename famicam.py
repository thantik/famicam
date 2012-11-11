import sys
import urllib
import time
import os
from PIL import Image, ImageStat
from StringIO import StringIO
import math
import twitter
from imgur import UploadImage as U

# Settings
camera_ip = "localhost:8080"
twitter_user = ""
twitter_pass = ""
imgur_api_key = ""
views = ["9ff,4ff,24","6ff,4ff,24","3ff,4ff,24", "ff,2ff,24"]

stamp = time.strftime("%y%d%m%H%M%S",time.localtime())
imglist = [] #Temp list to hold all of our images while we manage them.


def brightness(im_file):
   stat = ImageStat.Stat(im_file)
   r,g,b = stat.mean
   return math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2))


# Loop over the views
for v in views:
    # Pan the camera to the view
    params = urllib.urlencode({'AbsolutePanTilt': v})
    f = urllib.urlopen("http://"+camera_ip+"/command/ptzf.cgi", params)
    f.read()
    
    source = os.path.join('./', stamp + '.jpg') 
    data = Image.open(StringIO(urllib.urlopen("http://"+camera_ip+"/oneshotimage.jpg").read()))

    imglist.append(data)

if len(imglist) > 0:    #If we've got pictures to handle...
    height = imglist[0].size[1]
    width = imglist[0].size[0]
    canvas_width = width*len(imglist) #Total width of all pictures
    
    canvas_image = Image.new("RGB", (canvas_width,height)) #Create a new canvas wide enough to put all of our pictures.
    bright_values = []

    for index, img in enumerate(imglist):               #Put together whole image, store some brightness values.
        bright_values.append(brightness(img))
        canvas_image.paste(img, (width*index,0))
    bright_values.append(brightness(canvas_image))       #Bright values can be used later for additional logic.
                                                        #bright_values[-1] is all images.

    print bright_values #19-22 when lights are off at night.
    
    #canvas_image.show()
    canvas_image.save("lastimage.jpg")

    imgur_upload = U("lastimage.jpg") #Upload the image, assign return data to variable.

    lines = [line.strip() for line in open('config.txt')] #open a config file, so we can stuff secrets into them without them being accidentally sent to github

    #TWITTER
    app_key = lines[0]
    app_secret = lines[1]
    oauth_token = lines[2]
    oauth_token_secret = lines[3]

famitwitter = twitter.Api(consumer_key=app_key,
                  consumer_secret=app_secret,
                  access_token_key=oauth_token,
                  access_token_secret=oauth_token_secret)

famitwitter.PostUpdate(imgur_upload.imageURL) #Post the Oooarelll...
