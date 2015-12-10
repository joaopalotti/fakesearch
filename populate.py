import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

import django
django.setup()

from django.contrib.auth.models import User
from fakesearch.models import UserProfile, Query, Document, ResultList, Experiment, ListOrder, ExperimentSet, Vote, UserExperimentSet

def populate():

    user_john = add_user('john', 'password')
    user_james = add_user('james007', 'password')
    user_paul = add_user('paul21', 'password')

    query_1 = add_query("1", "Queryqwer 1 asdf")
    query_2 = add_query("2", "Query 2")
    query_3 = add_query("3", "This is query 3!")

    document_1 = add_document("1", "Document title 1", "This is the text of document 1", "http://example1.com")
    document_2 = add_document("2", "Document title 2", "This is the text of document 2", "http://example2.com")
    document_3 = add_document("3", "Document title 3", "This is the text of document 3", "http://example3.com")
    document_4 = add_document("4", "Document title 4", "This is the text of document 4", "http://example4.com")
    document_5 = add_document("5", "Document title 5", "This is the text of document 5", "http://example5.com")
    document_6 = add_document("6", "Document title 6", "This is the text of document 6", "http://example6.com")

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

    experiment_set_l1 = []
    experiment_set_l1.append( add_experiment(query_1, resultlist[0], resultlist[2], -1) )
    experiment_set_l1.append( add_experiment(query_1, resultlist[1], resultlist[0], -1) )
    experiment_set_l1.append( add_experiment(query_1, resultlist[2], resultlist[1], -1) )
    experiment_set_l1.append( add_experiment(query_1, resultlist[1], resultlist[1], -1) )
    # -----
    experiment_set_l2 = []
    experiment_set_l2.append( add_experiment(query_1, resultlist[0], resultlist[2], -1) )
    experiment_set_l2.append( add_experiment(query_1, resultlist[0], resultlist[4], -1) )
    experiment_set_l2.append( add_experiment(query_1, resultlist[1], resultlist[3], -1) )
    # -----
    experiment_set_l3 = []
    experiment_set_l3.append( add_experiment(query_2, resultlist[2], resultlist[5], -1) )
    experiment_set_l3.append( add_experiment(query_1, resultlist[2], resultlist[5], -1) )
    experiment_set_l3.append( add_experiment(query_3, resultlist[1], resultlist[3], -1) )

    experiment_set_1 = add_experiment_set("", experiment_set_l1)
    experiment_set_2 = add_experiment_set("", experiment_set_l2)
    experiment_set_3 = add_experiment_set("", experiment_set_l3)

    experiment_set_to_james = attributes_experiment_set(user_james, experiment_set_1)
    experiment_set_to_paul  = attributes_experiment_set(user_paul, experiment_set_1)
    experiment_set_to_john  = attributes_experiment_set(user_john, experiment_set_3)

    add_votes(user_james, experiment_set_to_james)
    add_votes(user_paul, experiment_set_to_paul)
    add_votes(user_john, experiment_set_to_john)

    print "DONE!"

def add_experiment_set(description, experiments):
    es = ExperimentSet.objects.create(description=description)
    es.save()
    for exp in experiments:
        es.experiments.add(exp)
    return es

def attributes_experiment_set(user, experiments):
    ues = UserExperimentSet.objects.create(user=user, experimentSet=experiments)
    ues.save()
    return ues

def add_votes(user, user_experiment_set):
    exp = UserExperimentSet.objects.get(pk=user_experiment_set.id).experimentSet.experiments.get_queryset()
    for e in exp:
        v, created = Vote.objects.get_or_create(user=user, experiment=e)
        v.preference = -1
        v.save()

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

def add_document(docname, title, snippet, url):
    d = Document.objects.get_or_create(docname=docname, title=title, url=url)[0]
    d.snippet = snippet
    d.save()
    return d

def add_resultlist(desc, doclists=[]):
    c = ResultList.objects.get_or_create(description=desc)[0]
    c.save()
    for l in doclists:
        c.doclist.add(l)
    return c

def add_experiment(query, listA, listB, preference):
    e = Experiment.objects.create(result_listA=listA, result_listB=listB, query=query)
    e.save()
    return e

# Start execution here!
if __name__ == '__main__':
    print "Starting Fakesearch population script..."
    populate()

