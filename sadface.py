__author__ = "Benjamin Keith (ben@benlk.com)"

import sys, os, random, re, time, ConfigParser, string
from twisted.words.protocols import irc
from twisted.internet import protocol
from twisted.internet import reactor
from collections import defaultdict
from time import localtime, strftime 

#
# Setting some settings
#

config_file = sys.argv[1]

requiredconfig = [('Connection', 'host'), ('Connection', 'port'), ('Bot', 'nickname'), ('Bot', 'erroneousNickFallback'), ('Bot', 'Channel'), ('Bot', 'realname'), ('Bot', 'username'), ('Bot', 'userinfo'), ('Brain', 'reply'), ('Brain', 'brain_file'), ('Brain', 'ignore_file'), ('Brain', 'STOP_WORD'), ('Brain', 'chain_length'), ('Brain', 'chattiness'), ('Brain', 'max_words')];
config = ConfigParser.ConfigParser()
config.read(config_file)
for setting in requiredconfig:
    if not config.has_option(setting[0], setting[1]):
        sys.exit('Error: Option "' + setting[1] + '" in section "' + setting[0] + '" is required! Take a look at your config.ini')

host = config.get('Connection', 'host')
port = int(config.get('Connection', 'port'))
password = config.get('Connection', 'password')

nickname = config.get('Bot', 'nickname')
erroneousNickFallback = config.get('Bot', 'erroneousNickFallback')
channel = config.get('Bot', 'channel')
chan = channel
realname = config.get('Bot', 'realname')
username = config.get('Bot', 'username')
userinfo = config.get('Bot', 'userinfo')
versionName = "sadface bot rev. 10"

reply = config.get('Brain', 'reply')
markov = defaultdict(list)
brain_file = config.get('Brain', 'brain_file')
STOP_WORD = config.get('Brain', 'STOP_WORD')
# punctuation = ['\n', '.', '?', '!', ',', '\r']
# Chain_length is the length of the message that sadface compares 
chain_length = int(config.get('Brain', 'chain_length'))
chattiness = float(config.get('Brain', 'chattiness'))
max_words = int(config.get('Brain', 'max_words'))
ignore_file = config.get('Brain', 'ignore_file')
ignore_nicks = []
for line in open(ignore_file, 'r'):
    ignore_nicks.append(line.strip())
#
# Begin actual code
#

def add_to_brain(msg, chain_length, write_to_file=False):
    if write_to_file:
        f = open(brain_file, 'a')
        f.write(msg + '\n')
        f.close()
    buf = [STOP_WORD] * chain_length
    for word in msg.split():
        markov[tuple(buf)].append(word)
        del buf[0]
        buf.append(word)
    markov[tuple(buf)].append(STOP_WORD)

# TODO
# Find the brain state, keep it saved on disk instead of in RAM.

def generate_sentence(msg, chain_length, max_words=1000): #max_words is defined elsewhere
    if msg[-1][-1] in string.punctuation: 
#        msg[-1] = msg[-1][:-1]
#        msg.replace([-1], '')
# converts string to list, drops the end character, converts back to string
        msg = list(msg)
        msg[-1] = msg[-1][:-1]
        msg[0] = msg[0].upper()
        msg = "".join(msg)
#    buf = msg.split()[-chain_length:] 
    buf = msg.split()[:chain_length]
   
# If message is longer than chain_length, shorten the message.
    if len(msg.split()) > chain_length: 
        message = buf[:]
    else:
        message = []
        for i in xrange(chain_length):
            message.append(random.choice(markov[random.choice(markov.keys())]))
    for i in xrange(max_words):
        try:
            next_word = random.choice(markov[tuple(buf)])
        except IndexError:
            continue
        if next_word == STOP_WORD:
            break
        message.append(next_word)
        del buf[0] # What happpens if this is moved down a line?
        buf.append(next_word)
    return ' '.join(message)

def ignore(user):
    if user in ignore_nicks:
        return True
    return False

class sadfaceBot(irc.IRCClient):
    realname = realname
    username = username
    userinfo = userinfo
    versionName = versionName
    erroneousNickFallback = erroneousNickFallback
    password = password

    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        self.join(self.factory.channel)
        print "signed on as %s." % (self.nickname,)

    def joined(self, channel):
        print "Joined %s." % (channel,)
        self.msg(self.factory.channel, "OP ME GO BUCKS!")

    def privmsg(self, user, channel, msg):
# TODO
# make the privmsg class run:
#    check for user
#    check for reply
#        check for self.

        user_nick = user.split('!', 1)[0]
        # Prints the message to stdout
        print channel + " <" + user_nick + "> " + msg 
        if not user:
            print "NON-USER:" + msg 
            return
        # Ignores the message if the person is in the ignore list
        elif ignore(user_nick):
            print "\t" + "Ignored message from <" + user_nick + "> at: " + strftime("%a, %d %b %Y %H:%M:%S %Z", localtime()) 
            # Time method from http://stackoverflow.com/a/415527
        # Replies to messages containing the bot's name
        elif reply == '1':
            if self.nickname in msg:
                time.sleep(0.2) #to prevent flooding
                msg = re.compile(self.nickname + "[:,]* ?", re.I).sub('', msg)
                prefix = "%s: " % (user_nick, )
            elif msg.lower().translate(string.maketrans("",""), string.punctuation).startswith(("hello", "hi", "sup", "howdy", "hola", "salutation", "yo", "greeting", "what up")):
		time.sleep(0.2) #to prevent flooding
                msg = re.compile(self.nickname + "[:,]* ?", re.I).sub('', msg) + " to you"
                prefix = "%s: " % (user_nick, )
            else:
                prefix = '' 

            add_to_brain(msg, self.factory.chain_length, write_to_file=True)
            print "\t" + msg #prints to stdout what sadface added to brain
            if prefix or random.random() <= self.factory.chattiness:
                sentence = generate_sentence(msg, self.factory.chain_length,
                    self.factory.max_words)
                if sentence:
                    self.msg(self.factory.channel, prefix + sentence)
                    print ">" + "\t" + sentence #prints to stdout what sadface said
        # Replies to messages starting with the bot's name.
        elif reply == '2':
            if msg.startswith(self.nickname): #matches nickname, mecause of Noxz
                time.sleep(0.2) #to prevent flooding
                msg = re.compile(self.nickname + "[:,]* ?", re.I).sub('', msg)
                prefix = "%s: " % (user_nick, )
            else:
                msg = re.compile(self.nickname + "[:,]* ?", re.I).sub('', msg)
                prefix = '' 

            add_to_brain(msg, self.factory.chain_length, write_to_file=True)
            print "\t" + msg #prints to stdout what sadface added to brain
            if prefix or random.random() <= self.factory.chattiness:
                sentence = generate_sentence(msg, self.factory.chain_length,
                    self.factory.max_words)
                if sentence:
                    self.msg(self.factory.channel, prefix + sentence)
                    print ">" + "\t" + sentence #prints to stdout what sadface said


        else:     #for when you don't want it talking back
            print msg
            prefix = '' 

            add_to_brain(msg, self.factory.chain_length, write_to_file=True)
            if prefix or random.random() <= self.factory.chattiness:
#                sentence = generate_sentence(msg, self.factory.chain_length,
#                    self.factory.max_words)
                pass
#
# Idea for later implementation
# To limit who gets to talk to the bot, the talker's nickname is self.nickname
# if user in allowed_people:
#    Check that user is okayed with nickserv
#    pass
# else:
#    fail
#    

class sadfaceBotFactory(protocol.ClientFactory):
    protocol = sadfaceBot

    def __init__(self, channel, nickname, chain_length, chattiness, max_words):
        self.channel = channel
        self.nickname = nickname
        self.chain_length = chain_length
        self.chattiness = chattiness
        self.max_words = max_words

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)
        quit()
#
#    We begin!
#

if __name__ == "__main__":
    config_file = sys.argv[1]
    if config_file == False:
        print "Please specify a valid config file in the arguments." 
        print "Example:"
        print "python sadface_configgable.py default.ini"
    if os.path.exists(brain_file):
        f = open(brain_file, 'r')
        for line in f:
            add_to_brain(line, chain_length)
        print 'Brain reloaded'
        f.close()
    else:
        print "Hoi! I need me some brains! Whaddya think I am, the Tin Man?"
    reactor.connectTCP(host, port, sadfaceBotFactory('#' + channel, nickname, chain_length, chattiness, max_words))
    reactor.run()

