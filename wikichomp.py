import cgi

import re
import sys
import random
import urllib2

form = cgi.FieldStorage()
if not form.has_key("input"):
	print """Content-Type: text/html

<html>
<head>
  <title>[[Wikipedia|Wikichomp]] Acronymizer</title>
</head>
<body>
  <form action="/" method="get">
    <div><input type="text" name="input" size="60"/></div>
    <div><input type="submit" value="Acronymize Word or Phrase w/ Its Wikipedia Article!"/></div>
  </form>
</body>
</html>
"""
	sys.exit()

print 'Content-Type: text/plain'
print ''

term = form.getvalue("input")
req = urllib2.Request("http://en.wikipedia.org/wiki/%s" % term.replace(' ', '_'), \
                      headers={'User-Agent': 'Mozilla/5.0 (F-Minus Loser Anti-Art; Me; emdash)'})
this = urllib2.urlopen(req).read().lower()
fing = re.compile('<a href=".*?" title=".*?">.*?</a>')
that = re.findall(fing,this)

#construct vocabulary
vocabulary = []
for each in that:
	vocabulary.append(re.sub(".*>","",each[:-4])) 
	
for bang in range(0,vocabulary.count('')):
	vocabulary.remove('')
	
vocab = sorted(vocabulary, key=str.lower)
term = term.lower()
acronym_dict = []
for element in term:
	if element == '_' or element == ' ':
		acronym_dict.append('')
		continue
	acronym_equiv = []
	for each in vocab:
		if each[0] == element:
			acronym_equiv.append(each)
	acronym_dict.append(acronym_equiv)
print term + " acronymized:\n"
for each in acronym_dict:
	if each == '':
		print
	else:
		print random.choice(each)

print "\n" + term + " acronymized!\n"

