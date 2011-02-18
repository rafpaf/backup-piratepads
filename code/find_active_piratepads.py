import config
import sqlite3
import os
import time
import re

pad_domain = "piratepad.net"

# make a copy of the firefox history database, since if firefox is
# open, the original will be exclusively locked.
history_db_copy = "/tmp/copy_of_firefox_history_for_piratepad_backups_%d" % time.time()
os.system('cp %s %s' % (config.firefox_history_db, history_db_copy))

conn = sqlite3.connect(history_db_copy)
c = conn.cursor()
c.execute("""
SELECT DISTINCT url FROM `moz_places`
WHERE   url LIKE 'http://%s/%%'
OR      url LIKE 'https://%s/%%'"""
% (pad_domain, pad_domain))

is_a_pad_slug = lambda x: (not (
        x.startswith('ep/')
        or x.startswith('ep/')
        or x.startswith('front-page')))

fn = os.path.join(os.path.dirname(__file__), 'pad_slugs')
f = open(fn, 'r+')

known_slugs = f.readlines()

for x in c.fetchall():
    url = x[0]
    # get the id string or "slug" out of the url
    slug = re.split(r'https?://piratepad.net/+', url)[1]
    # remove multiple trailing slashes if necessary
    slug = re.findall(r'(.*?)/*$', slug)[0]
    slug_br = '%s\n' % slug # best to add the linebreak here
    if slug_br not in known_slugs:
        if is_a_pad_slug(slug):
            f.write(slug_br)

f.close()

# vim: set columns=80:
