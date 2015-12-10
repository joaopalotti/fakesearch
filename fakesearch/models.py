from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

EXPERTISE_CHOICES = (
    (1, 'Layperson'),
    (2, 'Some Knowledge'),
    (3, 'Expert'),
)

LIST_PREFERENCE = (
    (1, 'Left List'),
    (2, 'None'),
    (3, 'Right List'),
)

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    expertise = models.IntegerField(default=-1)

    def __unicode__(self):
        return self.user.username

class Query(models.Model):
    qid = models.CharField(max_length=32)
    text = models.CharField(max_length=512)

    def __unicode__(self):
        return self.qid

class Document(models.Model):
    docname = models.CharField(max_length=32)
    title   = models.CharField(max_length=128)
    url     = models.URLField()
    snippet = models.CharField(max_length=512)

    def __unicode__(self):
        return self.docname

class ResultList(models.Model):
    description = models.CharField(max_length=128, default="-")
    doclist = models.ManyToManyField(Document, through='ListOrder')

    def __unicode__(self):
        return self.description

class ListOrder(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    resultlist = models.ForeignKey(ResultList, on_delete=models.CASCADE)
    rank = models.IntegerField()
    def __unicode__(self):
        return "%s, %s, %d" % (self.document.docname, self.resultlist.description, self.rank)

class Experiment(models.Model):
    # expid = models.CharField(max_length=128) # maybe a experiment description for human beings
    query = models.ForeignKey(Query)
    result_listA = models.ForeignKey(ResultList, null=True, related_name='listA')
    result_listB = models.ForeignKey(ResultList, null=True, related_name='listB')

    def __unicode__(self):
        return "%s,%s,%s" % (self.query.qid, self.result_listA, self.result_listB)

class ExperimentSet(models.Model):
    description = models.CharField(max_length=256)
    experiments = models.ManyToManyField(Experiment)

class UserExperimentSet(models.Model):
    user = models.ForeignKey(UserProfile)
    experimentSet = models.ForeignKey(ExperimentSet)

class Vote(models.Model):
    user = models.ForeignKey(UserProfile)
    experiment = models.ForeignKey(Experiment)
    preference = models.IntegerField(default=-1)

    def user_preference(self):
        return dict(LIST_PREFERENCE)[self.preference]

