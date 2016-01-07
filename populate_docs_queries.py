import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','myproject.settings')

import django
django.setup()

from django.contrib.auth.models import User
from fakesearch.models import Document, Query

quick_snippet_fix = True

def populate_queries():

    add_query("1", "many red marks on legs after traveling from US")
    add_query("2", "lump with blood spots on nose")
    add_query("3", "dry red and scaly feet in children")
    add_query("4", "itchy lumps skin")
    add_query("5", "whistling noise and cough during sleeping children")
    add_query("6", "child make hissing sound when breathing")
    add_query("7", "rosacea symptoms")
    add_query("8", "cloudy cornea and vision problem")
    add_query("9", "red itchy eyes")
    add_query("10", "crater type bite mark")

def populate_documents():
    snippets_file = "./snippets.txt"

    f = open(snippets_file)
    lines = f.readlines()

    for i in range(0,len(lines),3):
        fields = lines[i].strip().split()
        topic, docid = fields[0], fields[2]
        url_title = lines[i+1].strip().rsplit("\t",1)

        if len(url_title) == 2:
            title = url_title[1]
        else:
            title = ""
        url = url_title[0]

        # Preprocessing of snippet: removed all the text till the first <strong> is found.
        # This should be enough to remove the url and date from snippets.
        snippet = lines[i+2].strip()
        if quick_snippet_fix:
            snippet = snippet[snippet.find("<strong>"):]
        add_document(docid + "_" + topic, title, snippet, url)
        #print "\nDocument: ", docid + "_" + topic,"\n", "Title:", title, "\nSnippet:", snippet, "\nurl:", url

def add_document(docname, title, snippet, url, comments=""):
    d = Document.objects.get_or_create(docname=docname, title=title, url=url)[0]
    d.snippet = snippet
    d.save()
    return d

def add_query(qid, text):
    q = Query.objects.get_or_create(qid=qid)[0]
    q.text = text
    q.save()
    return q

# Start execution here!
if __name__ == '__main__':
    print "Populating queries..."
    populate_queries()
    print "Populating documents..."
    populate_documents()



