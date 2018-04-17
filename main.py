import praw
import string 

SUBREDDIT_NAME = 'warriors'
RESPONSE = 'Hi! I think you might have used "Iggy" to refer to Andre Igoudala, our supreme leader. In [several](https://www.youtube.com/watch?v=-qSY3OVrS9E) [instances](https://twitter.com/andre/status/908090035697631232) he\'s said that he\'d appreciate being called by another name. Let\'s try to respect his wishes.'

import credentials

CLIENT_ID = credentials.reddit['CLIENT_ID']
CLIENT_SECRET = credentials.reddit['CLIENT_SECRET']

print (CLIENT_ID)
 
USER_AGENT = 'script: reply to comments that contain iggy in /r/warriors (by /u/dont-call-me-iggy)'
 
def authenticate():
    print("Authenticating...")
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT)
    print("Authenticaed as {}".format(reddit.user.me()))
 
def has_iggy(comment):
    # strip punctuation and split on spaces
    exclude = set(string.punctuation) - set("-")
    text = ''.join(ch if ch not in exclude else " " for ch in comment.lower()).split()
    
    iggies = []
    for g in range(2, 5):
        for y in range(1, 8):
            iggies.append('i' + 'g'*g + 'y'*y)

    return any(iggy in text for iggy in iggies)

def watch_stream():
    print('Starting comment stream...')
    for comment in reddit.subreddit(SUBREDDIT_NAME).stream.comments():
        if comment.saved:
            continue

        not_self = comment.author != reddit.user.me()
        if has_iggy(comment.body) and not_self:
            comment.save()
            reply = comment.reply(RESPONSE)
            print('http://reddit.com{}'.format(reply.permalink()))

def run_tests():
    print ("Should all be true:")
    print (has_iggy("blah blah blah iggy"))
    print (has_iggy("iggy!!!!"))
    print (has_iggy("That reaction after the Iggy 3 was all time"))
    print (has_iggy("KLAY WITH 31. IGGY 4 FOR 5 FROM THREE. KD WITH 32. My lord."))
    print (has_iggy("iggy!!three!!!"))
    print (has_iggy("Talk about flipping the switch! Iggy's playing smart and intense."))
    print (has_iggy("Iggy, Dwest and JaVale all stepped up big time. Huge win!"))
    print (has_iggy("DONT CALL HIM IGGYYYYYY!!!!"))
    print (has_iggy("IGGGYYYY"))
    print ()

    print ("Should all be false:")
    print (has_iggy("andre igoudala"))
    print (has_iggy("getting jiggy with it"))
    print (has_iggy("iggy-dala"))
    print (has_iggy("paging /u/dont-call-me-iggy"))

if __name__ == '__main__':
    # reddit = authenticate()
    # watch_stream()

    # if you want to run tests
    # run_tests()
    pass
