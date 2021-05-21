from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import mysql.connector
from mysql.connector import errorcode
import time
import json



# replace mysql.server with "localhost" 
# if you are running via your own server!
# server       MySQL username	MySQL pass  Database name.

cnx = mysql.connector.connect(user='root', password='',
                              host='localhost',
                              database='users',
                              charset = 'utf8mb4')
cursor=cnx.cursor()

#consumer key, consumer secret,
#access token, access secret.
ckey =''
csecret =''
atoken =''
asecret =''


class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)

        # check to ensure there is text in
        # the json data
        if 'text' in all_data:
          tweet = all_data["text"]
          username = all_data["user"]["screen_name"]

          cursor.execute(
            "INSERT INTO tweetTable (time, username, tweet) VALUES (%s,%s,%s)",
            (time.time(), username, tweet))

          cnx.commit()

          print((username,tweet))

          return True
        else:
          return True

    def on_error(self, status):
        print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["covid"],languages = ["en"], stall_warnings = True)
