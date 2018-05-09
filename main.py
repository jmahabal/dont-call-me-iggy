import praw
import time
import string 
import random

SUBREDDIT_NAME = 'warriors'

import credentials

CLIENT_ID = credentials.reddit['CLIENT_ID']
CLIENT_SECRET = credentials.reddit['CLIENT_SECRET']
USERNAME = credentials.reddit['USERNAME']
PASSWORD = credentials.reddit['PASSWORD']
 
USER_AGENT = 'script: reply to comments that contain iggy in /r/warriors (by /u/dont-call-me-iggy)'
 
def authenticate():
    print("Authenticating...")
    return praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT,
        username=USERNAME,
        password=PASSWORD)
 
NBA_DESCRIPTIONS = set([
    'two-time NBA champion',
    'NBA Finals MVP',
    'NBA All-Star',
])

PERSONAL_DESCRIPTIONS = set([
    'bearer of the best-looking biceps in the NBA',
    'noted LeBron stopper',
])

def generate_response_description_pair():
    return 

def generate_response():
   return '''
Hi, you seem to have used "Iggy" to refer to Andre Iguodala, {} and {}. In [several](https://www.youtube.com/watch?v=-qSY3OVrS9E) [instances](https://twitter.com/andre/status/908090035697631232) Andre has said that he would rather be called by a different nickname.
&nbsp;  
&nbsp;

*****
^(If you have complaints or suggestions on how to improve this bot please message myself or the moderators!)
'''.format(random.sample(NBA_DESCRIPTIONS, 1)[0], random.sample(PERSONAL_DESCRIPTIONS, 1)[0])

def has_iggy(text):
    text = text.lower()
    if "azalea" in text:
        return False
    if "'iggy'" in text or '"iggy"' in text:
        return False

    # strip punctuation and split on spaces
    exclude = set(string.punctuation) - set("-") # for dont-call-me-iggy
    text = ''.join(ch if ch not in exclude else " " for ch in text).split()
    
    if "bot" in text:
        return False

    iggies = []
    for g in range(2, 5):
        for y in range(1, 8):
            iggies.append('i' + 'g'*g + 'y'*y)

    return any(iggy in text for iggy in iggies)

start_time = time.time()

# based on: https://github.com/acini/praw-antiabuse-functions
def is_summon_chain(post, reddit):
  if not post.is_root:
    parent_comment_id = post.parent().id
    parent_comment = reddit.comment(id=parent_comment_id)
    if parent_comment.author != None and str(parent_comment.author.name) == USERNAME:
      return True
    else:
      return False
  else:
    return False

def in_game_thread(post, reddit):
    submission_id = post.submission.id
    submission = reddit.submission(id=submission_id)
    if "game thread" in submission.title.lower():
        return True
    else:
        return False

def watch_stream():
    print('Starting comment stream...')
    reddit = authenticate()
    print("Authenticated as {}".format(reddit.user.me()))

    for comment in reddit.subreddit(SUBREDDIT_NAME).stream.comments():
        if comment.author == reddit.user.me():
            print ("comment #", comment.id, "not valid because from self")
            continue
        if comment.created_utc < start_time:
            print ("comment #", comment.id, "not valid because of age")
            continue
        if is_summon_chain(comment, reddit):
            print ("comment #", comment.id, "not valid because parent comment from bot")
            continue
        if in_game_thread(comment, reddit):
            print ("comment #", comment.id, "not valid because comment is in a game thread")
            continue
        if comment.saved:
            continue

        if has_iggy(comment.body):
            print ("processing comment #", comment.id)
            comment.save()
            reply = comment.reply(generate_response())
            print ("Posted to: https://www.reddit.com/r/" + SUBREDDIT_NAME + "/comments/" + comment.submission.id + "//" + reply.id + "")

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
    print (has_iggy("dont call him 'iggy'!"))
    print (has_iggy('dont call him "iggy"!'))
    print (has_iggy("iggy-dala"))
    print (has_iggy("iggy azalea"))
    print (has_iggy("paging /u/dont-call-me-iggy"))

    print ("Should return 10 different sample responses:")
    for i in range(1):
        print (generate_response())

if __name__ == '__main__':
    watch_stream()

    # if you want to run tests
    # run_tests()
    # pass
