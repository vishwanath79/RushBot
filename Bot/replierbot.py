from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API


#from nltk.chat import zen
import Bot.chatter as zen
import json
from Bot.config import ACCESS_SECRET, ACCESS_TOKEN, CONSUMER_KEY, CONSUMER_SECRET, account_screen_name, account_user_id


consumer_key = CONSUMER_KEY
consumer_secret = CONSUMER_SECRET
access_token = ACCESS_TOKEN
access_token_secret = ACCESS_SECRET
#stream_rule = config.get('app', 'rule')

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitterApi = API(auth)

chatbot = zen.Chat(zen.responses)


class ReplyToTweet(StreamListener):
    def on_data(self, data):
        print(data)
        tweet = json.loads(data.strip())


        retweeted = tweet.get('retweeted')
        from_self = tweet.get('user', {}).get('id_str', '') == account_user_id

        #if retweeted is not None and not retweeted and not from_self:
        if retweeted is not None and not from_self:

            tweetId = tweet.get('id_str')
            screenName = tweet.get('user', {}).get('screen_name')
            #screenName = "rushlyricbot"
            tweetText = tweet.get('text')

            chatResponse = chatbot.respond(tweetText)
            #chatResponse = " My counterpart, my foolish heart"

            replyText = '@' + screenName + ' ' + str(chatResponse)

            # check if repsonse is over 140 char
            if len(replyText) > 140:
                replyText = replyText[0:139] + '…'

            print('Tweet ID: ' + tweetId)
            print('From: ' + screenName)
            print('Tweet Text: ' + tweetText)
            print('Reply Text: ' + replyText)

            # If rate limited, the status posts should be queued up and sent on an interval
            twitterApi.update_status(status=replyText, in_reply_to_status_id=tweetId)

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    print(zen.responses)
    streamListener = ReplyToTweet()
    twitterStream = Stream(auth, streamListener)
    twitterStream.userstream(_with='user')



# fix multiple replies issue
# ffind how to set eliza pairs


