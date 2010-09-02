import cgi

import re
import sys
import random
import urllib2
import string
import xml.dom.minidom

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
agent = {'User-Agent': 'Mozilla/5.0 (F-Minus Loser Anti-Art; Me; emdash)'}

#grab the page and chomp relevant terms
req = urllib2.Request("http://en.wikipedia.org/wiki/%s" % term.replace(' ', '_'), \
                      headers=agent)
dom = xml.dom.minidom.parseString(urllib2.urlopen(req).read())
edit = [l.getAttribute('href') \
	for l in dom.getElementsByTagName('link') \
		if l.getAttribute('rel') == 'edit']
if not edit:
	edit = [l.firstChild.getAttribute('href') \
		for l in dom.getElementsByTagName('li') \
			if l.getAttribute('id') == 'ca-viewsource']
req = urllib2.Request("http://en.wikipedia.org" + edit[0], headers=agent)
wiki_dump = urllib2.urlopen(req).read().lower()
relevance = re.compile(r'\[\[([\w\':,.()# -]+)(?:\|([\w\':,.()# -]+))?\]\]')
relephants = re.findall(relevance, wiki_dump)

#construct vocabulary
vocabulary = []
for each in relephants:
	vocabulary.append(re.sub('^[^\w]', '', each[0]))
	if each[1]: vocabulary.append(re.sub('^[^\w]', '', each[1]))
vocab = sorted(set(vocabulary) - set(['']))

#form a dictionary from vocabulary
acro_term = term.lower().translate(string.maketrans("",""), string.punctuation) #got from http://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
acronym_dict = []
for element in acro_term:
	if element == '_' or element == ' ':
		acronym_dict.append('')
		continue
	acronym_equiv = []
	for each in vocab:
		if each[0] == element:
			acronym_equiv.append(each)
	acronym_dict.append(acronym_equiv)
for tick in range(len(acronym_dict)):
	if acronym_dict[tick] == []:
		acronym_dict[tick].append(acro_term[tick])

# now generate a random acronym from the dictionary
print acro_term + " acronymized:\n"
for each in acronym_dict:
	if each == '':
		print
	else:
		print random.choice(each).capitalize()
print "\n" + acro_term + " acronymized!\n"
