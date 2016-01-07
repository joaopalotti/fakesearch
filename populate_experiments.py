import os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

import django
django.setup()

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from fakesearch.models import UserProfile, Query, Document, ResultList, Experiment, ListOrder, ExperimentSet, Vote, UserExperimentSet

def populate():

    user_john = add_user('john', 'password')

    resultlist = {}
    documents_in_list = {}

    # Query 1
    index = 0
    resultlist[index] = add_resultlist("Q1A P=3/5") #[0,X,X,0,X]
    documents_in_list[index] = ["attra0843_12_000536_1", "aldf.1864_12_000027_1", "arthr0949_12_000974_1", "stret4575_12_000461_1", "baby-2032_12_000032_1"]
    index += 1
    resultlist[index] = add_resultlist("Q1B P=2/5") #[X,0,0,X,0]
    documents_in_list[index] = ["baby-2032_12_000032_1", "nhslo3844_12_006773_1", "stret4575_12_000267_1", "lupus1314_12_000069_1", "cance0998_12_000001_1"]

    # Query 2
    index += 1
    resultlist[index] = add_resultlist("Q2A P=1/5") #[0,X,0,0,0]
    documents_in_list[index] = ["ent.a1154_12_000059_2","derma2523_12_001652_2","first1181_12_000241_2","famil2899_12_000687_2","mayoc3579_12_017993_2"]

    index += 1
    resultlist[index] = add_resultlist("Q2B P=2/5") #[0,X,0,0,X]
    documents_in_list[index] = ["mayoc3579_12_004376_2", "famil2899_12_000922_2", "patie3988_12_000152_2", "skinc4437_12_002348_2", "healt3097_12_001249_2"]

    # Query 3
    index += 1
    resultlist[index] = add_resultlist("Q3A P=4/5") #[X,X,0,X,X]
    documents_in_list[index] = ["altme0929_12_000038_3","altme0929_12_000038_3","every2870_12_006975_3","footh1185_12_000064_3","healt3099_12_000225_3"]

    index += 1
    resultlist[index] = add_resultlist("Q3B P=2/5") #[0,X,0,0,X]
    documents_in_list[index] = ["healt3115_12_001603_3","derma2524_12_000066_3","skinc4434_12_002431_3","vhl.o4897_12_000077_3","nhslo1393_12_007249_3"]

    # Query 4
    index += 1
    resultlist[index] = add_resultlist("Q4A P=2/5") #[0,X,X,0,0]
    documents_in_list[index] = ["mgh.o3697_12_002801_4","baby-2032_12_000232_4","skinc4437_12_001903_4","total4684_12_000354_4","webmd4945_12_000963_4"]

    index += 1
    resultlist[index] = add_resultlist("Q4B P=2/5") #[X,0,X,0,0]
    documents_in_list[index] = ["skinc4437_12_000932_4","mgh.o3697_12_002958_4","skinc4437_12_001903_4","yourh5013_12_449740_4","webmd4945_12_001409_4"]

    # Query 5
    index += 1
    resultlist[index] = add_resultlist("Q5A P=1/5") #[0,0,X,0,0]
    documents_in_list[index] = ["chkd.2351_12_001991_5","webmd4945_12_002459_5","webmd4945_12_002011_5","first1181_12_000326_5","healt3121_12_000386_5"]

    index += 1
    resultlist[index] = add_resultlist("Q5B P=2/5") #[0,0,0,X,X]
    documents_in_list[index] = ["chkd.2351_12_000299_5","healt3121_12_000462_5","babyc2037_12_000385_5","baby-2032_12_000007_5","webmd4945_12_002011_5"]

    # Query 6
    index += 1
    resultlist[index] = add_resultlist("Q6A P=2/5") #[0,X,X,0,0]
    documents_in_list[index] = ["bette2098_12_000923_6","mayoc3579_12_001922_6","nlm.n3868_12_001074_6","virtu4913_12_000775_6","nhslo3844_12_006822_6"]

    index += 1
    resultlist[index] = add_resultlist("Q6B P=2/5") #[X,X,0,0,0]
    documents_in_list[index] = ["virtu4909_12_001268_6","nlm.n3868_12_000812_6","mayoc3579_12_015759_6","nhslo1393_12_013211_6","bette2098_12_000710_6"]

    # Query 7
    index += 1
    resultlist[index] = add_resultlist("Q7A P=0/5") #[0,0,0,0,0]
    documents_in_list[index] = ["jfpon3369_12_000314_7","fromy1190_12_001796_7","blog.0976_12_000191_7","aids.0922_12_000376_7","clini0836_12_089944_7"]

    index += 1
    resultlist[index] = add_resultlist("Q7B P=2/5") #[0,X,0,X,0]
    documents_in_list[index] = ["jfpon3369_12_001111_7","blog.0976_12_000001_7","blog.0976_12_000191_7","fromy1190_12_002372_7","every2870_12_000559_7"]

    # Query 8
    index += 1
    resultlist[index] = add_resultlist("Q8A P=5/5") #[X,X,X,X,X]
    documents_in_list[index] = ["empow2815_12_000651_8","pedia4004_12_000091_8","allab1866_12_000011_8","nei.n3817_12_000510_8","nhslo3844_12_003301_8"]

    index += 1
    resultlist[index] = add_resultlist("Q8B P=2/5") #[0,X,0,X,0]
    documents_in_list[index] = ["allab1866_12_000205_8","eyere2883_12_000118_8","nei.n3817_12_000485_8","visio1658_12_000211_8","nlm.n3868_12_001975_8"]

    # Query 9
    index += 1
    resultlist[index] = add_resultlist("Q9A P=0/5") #[0,0,0,0,0]
    documents_in_list[index] = ["patie3988_12_000795_9","skinc4437_12_000521_9","visio1658_12_000265_9","cance0998_12_000001_9","visio1658_12_000442_9"]

    index += 1
    resultlist[index] = add_resultlist("Q9B P=2/5") #[0,X,0,0,X]
    documents_in_list[index] = ["healt3132_12_001486_9","bestb0834_12_000376_9","skinc4437_12_000714_9","daily0837_12_040697_9","visio1658_12_000039_9"]

    # Query 10
    index += 1
    resultlist[index] = add_resultlist("Q10A P=2/5") #[0,X,0,0,X]
    documents_in_list[index] = ["nhslo1393_12_014590_10","pathg3984_12_000284_10","uptod4830_12_045991_10","plast4085_12_000483_10","pathg3984_12_000497_10"]

    index += 1
    resultlist[index] = add_resultlist("Q10B P=2/5") #[0,X,0,X,0]
    documents_in_list[index] = ["plast4085_12_000022_10","patho3986_12_001019_10","nhslo1393_12_012258_10","pathg3984_12_000284_10","wikis0855_12_000080_10"]

    # -------------------------------

    # This code should be always run.
    for result_index, result_list in resultlist.iteritems():
        for i, docname in enumerate(documents_in_list[result_index]):
            try:
                d = Document.objects.get(docname=docname)
            except ObjectDoesNotExist:
                print "Not found document", docname
                sys.exit(1)
            list_order = ListOrder(document=d, resultlist = result_list, rank=i)
            list_order.save()
    # Ended compulsory code


    experiment_set_l1 = []
    experiment_set_l1.append( add_experiment("1", resultlist[0], resultlist[1]) )
    experiment_set_l1.append( add_experiment("2", resultlist[2], resultlist[3]) )
    experiment_set_l1.append( add_experiment("3", resultlist[4], resultlist[5]) )
    experiment_set_l1.append( add_experiment("4", resultlist[6], resultlist[7]) )
    experiment_set_l1.append( add_experiment("5", resultlist[8], resultlist[9]) )
    experiment_set_l1.append( add_experiment("6", resultlist[10], resultlist[11]) )
    experiment_set_l1.append( add_experiment("7", resultlist[12], resultlist[13]) )
    experiment_set_l1.append( add_experiment("8", resultlist[14], resultlist[15]) )
    experiment_set_l1.append( add_experiment("9", resultlist[16], resultlist[17]) )
    experiment_set_l1.append( add_experiment("10", resultlist[18], resultlist[19]) )

    # ----- Same as experiment set 1, but using the inverted order when showing query lists
    experiment_set_l2 = []
    experiment_set_l2.append( add_experiment("1", resultlist[1], resultlist[0]) )
    experiment_set_l2.append( add_experiment("2", resultlist[3], resultlist[2]) )
    experiment_set_l2.append( add_experiment("3", resultlist[5], resultlist[4]) )
    experiment_set_l2.append( add_experiment("4", resultlist[7], resultlist[7]) )
    experiment_set_l2.append( add_experiment("5", resultlist[9], resultlist[9]) )
    experiment_set_l2.append( add_experiment("6", resultlist[11], resultlist[10]) )
    experiment_set_l2.append( add_experiment("7", resultlist[13], resultlist[12]) )
    experiment_set_l2.append( add_experiment("8", resultlist[15], resultlist[14]) )
    experiment_set_l2.append( add_experiment("9", resultlist[17], resultlist[16]) )
    experiment_set_l2.append( add_experiment("10", resultlist[19], resultlist[18]) )

    experiment_set_1 = add_experiment_set("Compares only one single query yet", experiment_set_l1)
    experiment_set_2 = add_experiment_set("Inverted order of experiment set 1", experiment_set_l2)

    # The next two lines are not important actually. They are automatically done in the fakesearch code
    experiment_set_to_john = attributes_experiment_set(user_john, experiment_set_1)
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

def add_resultlist(desc, doclists=[]):
    c = ResultList.objects.get_or_create(description=desc)[0]
    c.save()
    for l in doclists:
        c.doclist.add(l)
    return c

def add_experiment(query, listA, listB):
    q = Query.objects.get(qid=query)
    e = Experiment.objects.create(result_listA=listA, result_listB=listB, query=q)
    e.save()
    return e

# Start execution here!
if __name__ == '__main__':
    print "Starting Fakesearch population script..."
    populate()

