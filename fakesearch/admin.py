from django.contrib import admin
from fakesearch.models import UserProfile, Query, Document, ResultList, Experiment, ListOrder

admin.site.register(UserProfile)
admin.site.register(Query)
admin.site.register(Document)
admin.site.register(ResultList)
admin.site.register(Experiment)
admin.site.register(ListOrder)
