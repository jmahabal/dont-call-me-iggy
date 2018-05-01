![example of the bot responding](reddit.png)

(/u/dont-call-me-iggy)[https://www.reddit.com/u/dont-call-me-iggy] is a Reddit bot that reminds users that Andre Igoudala doesn't like to go by "Iggy".

Built using Praw and hosted on a DigitalOcean droplet running `forever`.

Changelog:

5/1/18:
* Now ignores comments whose _parent_ is /u/dont-call-me-iggy, not whose grandparent is (as was the intention)

4/30/18:
* Now ignores users who mention "bot" anywhere in the text, not just directly after "iggy"
* Ignores comments whose grandparent author is /u/dont-call-me-iggy

4/29/18:
* Fixed spelling of "Iguodala"

...

Exact date unknown, but the following improvements were added sometime after v0:
* Ignored users typing "bot"
* Ignored users typing "iggy azalea"
* Ignored users typing "iggy" in quotes
* Allowed for randomized copy via templates