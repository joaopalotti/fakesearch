from django.contrib import admin
from fakesearch.models import UserProfile, Query, Document, ResultList, Experiment, ListOrder, ExperimentSet, Vote, UserExperimentSet

admin.site.register(UserProfile)
admin.site.register(Query)
admin.site.register(Document)
admin.site.register(ResultList)
admin.site.register(Experiment)
admin.site.register(UserExperimentSet)
admin.site.register(ExperimentSet)
admin.site.register(ListOrder)
admin.site.register(Vote)
