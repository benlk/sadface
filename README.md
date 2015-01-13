# sadface

an IRC Markov Chain chatbot

## Intro

Markov bots make for amusing text generators. They don’t make much sense, 
usually. When they do make sense, it’s pure chance.

sadface draws its vocabulary and concepts from a flat text file, where 
each line is considered a sentence. The bot chains words together to create 
sentences, which it passes to the IRC channel it is in.

Right now, sadface only supports one channel, but you can have multiple 
instances of sadface running with different configuration files. The 
configuration file is specified at runtime as an argument: 
`python sadface.py config-file.ini`

Included in this repo are sadface.py and default.ini. If you want to change 
default.ini, I encourage you to copy default.ini and change the variables, 
so you can have an untouched default.ini.

You can start sadface with a blank brain_file.txt, but its replies won’t 
make much sense at all until it’s heard a lot of conversation. I recommend 
putting several books into the file. Project Gutenberg 
(http://www.gutenberg.org/browse/scores/top) is a good place to start. 
Separate sentences by newlines. Replies look best if there are no quotes 
or tabs in brain_file.txt. You can specify different brain files with your 
config.ini.

## Included files

`sadface.py`

Usage: `python sadface.py /path/to/config.ini`

sadface also requires brain_file.txt, which is a flat txt file of newline-
separated sentences. brain_file.txt is specified in config.ini

`default.ini`

The example configuration

`sed_cleaning.sh`

Usage: `sed_cleaning.sh old_brain.txt temporaryfile clean_brain.txt`

A sed script that cleans up brain_file.txt by writing it to a new brain_file. 
Add whatever you need to to clean up the files you feed sadface.

## Prerequisites

- `brain_file.txt`: A flat text file of newline-separated sentences. sadface draws from `brain_file.txt` to create its replies, and adds things said in-channel 
to the brain file. This can have a different name, set in the `.ini` file

- Python 2.7.3  

- [python-twisted](http://twistedmatrix.com/trac/wiki/Downloads

## Credits

- Eric Florenzano
	- sadface derives heavily from his MomBot Markov bot code
	- http://eflorenzano.com/blog/2008/11/16/writing-markov-chain-irc-bot-twisted-and-python/
	- http://wayback.archive.org/web/20130106092748/http://eflorenzano.com/blog/2008/11/16/writing-markov-chain-irc-bot-twisted-and-python/

- hhokanson
	- sadface's configuration methods derive from her AnonBot IRC anonymizer bot
	- https://bitbucket.org/hhokanson/anonbot/src

