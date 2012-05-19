import sys, os, random, re, time, ConfigParser
from twisted.words.protocols import irc
from twisted.internet import protocol
from twisted.internet import reactor
from collections import defaultdict

config_file = sys.argv[1]

requiredconfig = [('Connection', 'host'), ('Connection', 'port'), ('Bot', 'nickname'), ('Bot', 'erroneousNickFallback'), ('Bot', 'Channel'), ('Bot', 'realname'), ('Bot', 'username'), ('Bot', 'userinfo'), ('Bot', 'versionName'), ('Brain', 'reply'), ('Brain', 'brain_file'), ('Brain', 'STOP_WORD'), ('Brain', 'chain_length'), ('Brain', 'chattiness'), ('Brain', 'max_words')];
config = ConfigParser.ConfigParser()
config.read(config_file)
for setting in requiredconfig:
    if not config.has_option(setting[0], setting[1]):
        sys.exit('Error: Option "' + setting[1] + '" in section "' + setting[0] + '" is required! Take a look at your config.ini')
#

# default settings
#
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
versionName = config.get('Bot', 'versionName')

reply = config.get('Brain', 'reply')
markov = defaultdict(list)
brain_file = config.get('Brain', 'brain_file')
STOP_WORD = config.get('Brain', 'STOP_WORD')
chain_length = int(config.get('Brain', 'chain_length'))
chattiness = float(config.get('Brain', 'chattiness'))
max_words = int(config.get('Brain', 'max_words'))

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

def generate_sentence(msg, chain_length, max_words=10000):
	buf = msg.split()[:chain_length]
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
		del buf[0]
		buf.append(next_word)
	return ' '.join(message)

class sadfaceBot(irc.IRCClient):

	irc.IRCClient.realname = realname
	irc.IRCClient.username = username
	irc.IRCClient.userinfo = userinfo
	irc.IRCClient.versionName = versionName
	irc.IRCClient.erroneousNickFallback = erroneousNickFallback
	irc.IRCClient.password = password

	def _get_nickname(self):
		return self.factory.nickname
	nickname = property(_get_nickname)

	def signedOn(self):
		self.join(self.factory.channel)
		print "signed on as %s." % (self.nickname,)

	def joined(self, channel):
		print "Joined %s." % (channel,)

	def privmsg(self, user, channel, msg):
		print msg
		if not user:
			return
		if reply == 'True':
			if self.nickname in msg:
				time.sleep(0.2) #to prevent flooding
				msg = re.compile(self.nickname + "[:,]* ?", re.I).sub('', msg)
				prefix = "%s: " % (user.split('!', 1)[0], )
			else:
				prefix = '' 

			add_to_brain(msg, self.factory.chain_length, write_to_file=True)
			if prefix or random.random() <= self.factory.chattiness:
				sentence = generate_sentence(msg, self.factory.chain_length,
					self.factory.max_words)
				if sentence:
					self.msg(self.factory.channel, prefix + sentence)
		else: 	#for when you don't want it talking back
			prefix = '' 

			add_to_brain(msg, self.factory.chain_length, write_to_file=True)
			if prefix or random.random() <= self.factory.chattiness:
				sentence = generate_sentence(msg, self.factory.chain_length,
					self.factory.max_words)


	
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
#
#	We begin!
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
	reactor.connectTCP(host, port, sadfaceBotFactory('#' + channel, nickname, chain_length, chattiness, max_words))
	reactor.run()

