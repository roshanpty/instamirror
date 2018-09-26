# InstaMirror 1.1

## About:

Instamirror 1.1 is a workaround to enable cross posting between Facebook Pages and Instagram profiles. By default Facebook doesn't provide any feature or API to enable this and they have limited Instagram publish API access only to approved business partners. Follow the instructions in this README and your facebook page posts shall automatically be mirrored on to your instagram profile.

## Usage:
```
python instamirror.py
```
![Instamirror program](https://i.imgur.com/W37J00p.png)

## Environment Setup

Instamirror 1.1 has multiple software and API dependency. This section will detail on the steps which are to be followed to make the tool work seemlessly. 

### Step 1: Configuring the python environment
Neeedless to say you need to have Python installed. Python 2.7 to be precise. Instamirror was tested only on Windows 10 environment. Though you may be able to replicate the steps on Linux/MacOS, the results may vary and might encounter issues. This document shall only deal with the working of Instamirror on a Windows 10 environment.

Installing the dependencies
```
pip install update
pip install python-resize-image
pip install InstagramApi
```

Note: 
* For the above commands to work, path to pip need to be in the environment variable. Default location is `C:\Python27\Scripts`.
* Tons of thanks to @LevPasha for making life much easier with [InstagramApi](https://github.com/LevPasha/Instagram-API-python)


### Step 2: Configuring Facebook 
For the script to be running continuously, without any disruption, the API tokens must be 

1. Go to [Facebook for Developers](https://developers.facebook.com/)
2. From the 'My Apps' drop down on the top-right corner, click on 'Add new app'.
3. Give a display name and contact email to create an App ID which you would require for using this tool.
![App Creation](https://i.imgur.com/4DWDJfd.png)
4. Go to facebook [Graph API Explorer tool](https://developers.facebook.com/tools/explorer/) Instamirror was tested with Graph API version 3.1
5. On the Application drop down on Graph API explorer, select the right application.
![App Selection](https://i.imgur.com/8eUgBlO.png)
6. Click on the 'Get Token' dropdown and select 'Get Page Access Token'
![App Page Access Token](https://i.imgur.com/8ZgZ3HW.png)
7. Login with your facebook account in the prompt which follows and give permission for the app to manage your pages.
8. In the Graph API explorer, now you will be able to select the page for which you want to generate page access token. 
![Generating Page Access Token](https://i.imgur.com/U91Lu7Y.png)
9. Click on 'Access Token Info' and then select the 'Open in Access Token Tool' option.
![Open in PAT Tool](https://i.imgur.com/zqXYT46.png)
10. In the new window, it can be observed that the current token is a short living token.  To create a long living access token, click on the 'Extend Access Token' button.
![Short Token](https://i.imgur.com/ZfxvoxJ.png)
11. A new access token with approximately 2 months validity will be generated.
![Long Live Token](https://i.imgur.com/kIOSSkW.png)
![Long Live Token Debug](https://i.imgur.com/c3WyxZs.png)
12. To create the permanent page access token, a request has to be made with the following parameters to the AP1. The long living access token generated in the previous step must be used for this.
![Permanent Token](https://i.imgur.com/SdlHwoz.png)
13. This will generate a permanent page access token and it can be verified using the [Access Token Tool](https://developers.facebook.com/tools/debug/accesstoken/)
![Permanent Token Debug](https://i.imgur.com/ymBHCZG.png)

### Step 3: Configuring Instamirror

For instamirror to properly work, instaconfig.json file has to be configured correctly. Field names are self explanatory and the file is in json format.

```
{
	"_comment1":"This is the configuration file for instabot program",
	"_comment2":"All the basic configurations including credentials and API tokens need to be configured here",
	"_comment3":"This file contains sensitive information and must be stored securely.",
	"_comment4":"Instabot is now instamirror and it no longer support supplying parameters as arguments",
	"facebook" : {
		"GraphAPIURL":"https://graph.facebook.com/v3.1/",
		"PageID":"InternationalChaluUnion",
		"GraphAPINode": "/posts?fields=attachments%7Bdescription%2Cmedia%7D%2Ccreated_time&date_format=U&limit=1&access_token=",
		"PageToken":"<Your Permanent Page Access Token generated from previous step>",
		"RefreshInterval":<Time(in seconds) instamirror should wait to check whether there is a new post on page>,
		"PostExcludeSignature": ["<Posts_with_this_word_in_caption_will_be_excluded>","This_too"]
	},
	"instagram" : {
		"UserName":"<insta username>",
		"Password":"<insta password>"
	}
}
```


## Author:

Roshan Thomas
* [SecVibe](https://secvibe.com)
* [LinkedIn](https://www.linkedin.com/in/roshanpty/)
* [Twitter](https://twitter.com/roshanpty)

## Disclaimer:
- Use this tool at your own risk. 
- The author cannot be held liable for any loss caused by the use of this tool
- The application uses sensitive information including permanent API keys, usernames and passwords. Run it in a secure environment.
 ## Support:
 
 Error running the tool?
 Confusion in configuring the tool?
 
 Though I do not provide active support, I would try to help as much as possible. Raise it as an issue on the github project or tweet @roshanpty
