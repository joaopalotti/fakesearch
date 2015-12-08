from django.contrib import admin
from fakesearch.models import Category, Page, UserProfile, Query, Document, ResultList, Experiment, ListOrder

# Add in this class to customized the Admin Interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page)

admin.site.register(UserProfile)
admin.site.register(Query)
admin.site.register(Document)
admin.site.register(ResultList)
admin.site.register(Experiment)
admin.site.register(ListOrder)
