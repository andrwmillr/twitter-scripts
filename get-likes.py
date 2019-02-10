### Authenticate with Twitter

import tweepy
import requests
from secrets import sender_password, twitter_auth, screen_names

auth = tweepy.OAuthHandler(twitter_auth["consumer_key"],
                           twitter_auth["consumer_secret"])
auth.set_access_token(twitter_auth["access_token"],
                      twitter_auth["access_secret"])

api = tweepy.API(auth)


### Get tweets

likes = []

for name in screen_names:
	content = tweepy.Cursor(
		api.favorites, screen_name = name).items(10)
	likes.append({'name': name, 'likes': content})


### Generate message body

header = """
		<head>
		  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		  <title>html title</title>
		  <style>
		    blockquote.twitter-tweet {
			  display: inline-block;
			  font-family: "Helvetica Neue", Roboto, "Segoe UI", Calibri, sans-serif;
			  font-size: 12px;
			  font-weight: bold;
			  line-height: 16px;
			  border-color: #eee #ddd #bbb;
			  border-radius: 5px;
			  border-style: solid;
			  border-width: 1px;
			  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.15);
			  margin: 10px 5px;
			  padding: 0 16px 16px 16px;
			  max-width: 468px;
			}

			blockquote.twitter-tweet p {
			  font-size: 16px;
			  font-weight: normal;
			  line-height: 20px;
			}

			blockquote.twitter-tweet a {
			  color: inherit;
			  font-weight: normal;
			  text-decoration: none;
			  outline: 0 none;
			}

			blockquote.twitter-tweet a:hover,
			blockquote a:focus {
			  text-decoration: underline;
			}
		  </style>
		</head>
		"""

send_string = ""

for like_list in likes:
	send_string += "<h2>" + like_list['name'] + "</h2>"
	for like in like_list['likes']:
		html = requests.get(
			'https://publish.twitter.com/oembed', 
			params = {'url': 'https://twitter.com/twitter/status/' + str(like.id)}
			).json()['html']

		send_string += html

body = header + send_string


### Send email

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender = 'my.twitter.scripts@gmail.com'
password = sender_password

recipient = 'admiller9@gmail.com'
subject = 'Your recently liked Tweets'

msg = MIMEMultipart('alternative')
msg.attach(MIMEText(body, 'plain')) # plain-text
msg.attach(MIMEText(body, 'html'))

msg['Subject'] = subject
msg['From'] = sender
msg['To'] = recipient

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()
server.login(sender, password)
server.sendmail(sender, [recipient], msg.as_string())
server.close()

print('Email sent!')
