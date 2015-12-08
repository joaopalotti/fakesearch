import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

import django
django.setup()

from django.contrib.auth.models import User
from fakesearch.models import UserProfile, Query, Document, ResultList, Experiment, ListOrder

def populate():

    user_john = add_user('john', 'password')
    user_james = add_user('james007', 'password')
    user_paul = add_user('paul21', 'password')

    query_1 = add_query("1", "Query 1")
    query_2 = add_query("2", "Query 2")

    document_1 = add_document("1", "This is the text of document 1")
    document_2 = add_document("2", "This is the text of document 2")
    document_3 = add_document("3", "This is the text of document 3")
    document_4 = add_document("4", "This is the text of document 4")
    document_5 = add_document("5", "This is the text of document 5")
    document_6 = add_document("6", "This is the text of document 6")

    resultlist = {}
    documents_in_list = {}

    resultlist[0] = add_resultlist("q1_rl1")
    documents_in_list[0] = [document_6, document_2, document_1]

    resultlist[1] = add_resultlist("q1_rl2")
    documents_in_list[1] = [document_2, document_4, document_1]

    resultlist[2] = add_resultlist("q1_rl3")
    documents_in_list[2] = [document_3, document_2, document_5]

    resultlist[3] = add_resultlist("q2_rl1")
    documents_in_list[3] = [document_4, document_4, document_5]

    resultlist[4] = add_resultlist("q2_rl2")
    documents_in_list[4] = [document_5, document_4, document_1]

    resultlist[5] = add_resultlist("q2_rl3")
    documents_in_list[5] = [document_6, document_1, document_2]

    for result_index, result_list in resultlist.iteritems():
        for i, document in enumerate(documents_in_list[result_index]):
            list_order = ListOrder(document=document, resultlist = result_list, rank=i)
            list_order.save()

    experiment_john_1 = add_experiment(user_john, query_1, resultlist[0], resultlist[1], -1)
    experiment_john_2 = add_experiment(user_john, query_1, resultlist[1], resultlist[0], -1)
    experiment_john_3 = add_experiment(user_john, query_2, resultlist[2], resultlist[0], -1)
    experiment_john_4 = add_experiment(user_john, query_2, resultlist[0], resultlist[4], -1)
    # -----
    experiment_james_1 = add_experiment(user_james, query_1, resultlist[0], resultlist[2], 1)
    experiment_james_2 = add_experiment(user_james, query_1, resultlist[0], resultlist[4], 2)
    experiment_james_3 = add_experiment(user_james, query_1, resultlist[1], resultlist[3], -1)
    experiment_james_4 = add_experiment(user_james, query_2, resultlist[2], resultlist[1], -1)
    # -----
    experiment_paul_1 = add_experiment(user_paul, query_2, resultlist[2], resultlist[5], 20)

    # Print out what we have added to the user.
    #for c in Category.objects.all():
    #    for p in Page.objects.filter(category=c):
    #        print "- {0} - {1}".format(str(c), str(p))

    print "DONE!"

def add_user(username, password='password'):
    u = User.objects.get_or_create(username=username)[0]
    u.set_password(password)
    u.save()
    profile = UserProfile.objects.get_or_create(user=u)[0]
    profile.save()
    return profile

def add_query(qid, text):
    q = Query.objects.get_or_create(qid=qid)[0]
    q.text = text
    q.save()
    return q

def add_document(docname, snippet):
    d = Document.objects.get_or_create(docname=docname)[0]
    d.snippet = snippet
    d.save()
    return d

def add_resultlist(desc, doclists=[]):
    c = ResultList.objects.get_or_create(description=desc)[0]
    c.save()
    for l in doclists:
        c.doclist.add(l)
    return c

def add_experiment(user, query, listA, listB, preference):
    e, created = Experiment.objects.get_or_create(user=user, result_listA=listA, result_listB=listB, query=query, preference=preference)
    if created:
        print "Created new Experiment"
    else:
        print "Just loaded experiment: user %s" % (user)
    e.save()
    #for l in lists:
    #    e.result_lists.add(l)

# Start execution here!
if __name__ == '__main__':
    print "Starting Fakesearch population script..."
    populate()

