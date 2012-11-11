class UploadImage():
    """
    Upload images to imgur
    """
 
    # Not very verbose at the moment in terms of errors - will build on that later
    def __init__(self,image,upload_method="anon"):
        import pycurl
        from xml.dom import minidom
        import cStringIO
 
        # setup some initial items we will need
        self.c = pycurl.Curl()
        self.response = cStringIO.StringIO()
        self.minidom = minidom
        self.image = image
        self.imageURL = ""
        self.error = ""
 
        # provide some various methods for uploading
        # by default - at least for now in testing - we will use anonymous upload method
        if upload_method == "anon":
            self.anon_upload()
        # later or on-demand we can switch to oauth based uploads
        elif upload_method == "oauth":
            self.auth_upload()
 
    # anonymous upload method
    def anon_upload(self):
        "Upload anonymously to imgur"
 	lines = [line.strip() for line in open('config.txt')] #open a config file
        # setup the basic parameters
        params = [
                ("key", lines[4]),
                ("image", (self.c.FORM_FILE, self.image))
            ]
 
        # setup the url and pipe in our key and image
        self.c.setopt(self.c.URL, "http://api.imgur.com/2/upload.xml")
        self.c.setopt(self.c.HTTPPOST, params)
 
        # we want to capture the output so lets set the write output to go to our cStringIO so we can parse it
        self.c.setopt(self.c.WRITEFUNCTION, self.response.write)
 
        # run it
        self.c.perform()
        self.c.close()
 
        try:
            # parse the XML return string and get the URL of our image
            xml = self.minidom.parseString(self.response.getvalue())
            self.imageURL = xml.getElementsByTagName("original")[0].firstChild.data
 
        except:
            self.error = "Problem uploading anonymously."
 
        return self.imageURL,self.error
 
    # oauth-based upload method
    def oauth_upload(self):
        "Upload using oauth to imgur"
 
        ### Not coded yet but we will use python-oauth2
        pass