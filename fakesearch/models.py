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
    expertise = models.IntegerField(default=1)

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

# TODO: maybe lind result list and query with a throgh relation.

class ResultList(models.Model):
    description = models.CharField(max_length=128, default="-")
    doclist = models.ManyToManyField(Document, through='ListOrder') # TODO: It creates a set (NOT A LIST) of Documents

    def __unicode__(self):
        return self.description
        #return "%s, First doc: %s " % (self.query.text, self.doclist.all()[0].docname)
        #return self.rlid

class ListOrder(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    resultlist = models.ForeignKey(ResultList, on_delete=models.CASCADE)
    rank = models.IntegerField()
    def __unicode__(self):
        return "%s, %s, %d" % (self.document.docname, self.resultlist.description, self.rank)

class Experiment(models.Model):
    # expid = models.CharField(max_length=128) # maybe a experiment description
    user = models.ForeignKey(UserProfile)
    query = models.ForeignKey(Query)
    result_listA = models.ForeignKey(ResultList, null=True, related_name='listA')
    result_listB = models.ForeignKey(ResultList, null=True, related_name='listB')
    preference = models.IntegerField(default=-1)

    def user_preference(self):
        return dict(LIST_PREFERENCE)[self.preference]

    def __unicode__(self):
        return "%s,%s,%s,%d" % (self.user.user.username, self.result_listA, self.result_listB, self.preference)
        # return str(self.expid)

##### ------------------------------------------------------------------------------- #####

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField() #unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __unicode__(self):      #For Python 2, use __str__ on Python 3
        return self.title
