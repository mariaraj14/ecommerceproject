from django.contrib import admin
# Register your models herefrom .models import category,product
from .models import category,product
class categoryadmin(admin.ModelAdmin):
    list_display=['name','slug']
    prepopulated_fields={'slug':('name',)}
admin.site.register(category,categoryadmin)
class productadmin(admin.ModelAdmin):
    list_display=['name','price','stock','available','created','updated']
    list_editable=['price','stock','available']
    list_per_page= 20
    prepopulated_fields={'slug':('name',)}
admin.site.register(product,productadmin)