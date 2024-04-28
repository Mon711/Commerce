from django.contrib import admin

# Register your models here.
from .models import User,Listing,Bid,Comment

class ListingsAdmin(admin.ModelAdmin):
    list_display = ['id','title','owner','status']

class CommentsAdmin(admin.ModelAdmin):
    list_display = ['username','itemID','text']

# @admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','get_watchlist']

    def get_watchlist(self,obj):
        return [item for item in obj.watchlist.all()]


admin.site.register(User,UserAdmin)
admin.site.register(Listing,ListingsAdmin)
admin.site.register(Bid)
admin.site.register(Comment,CommentsAdmin)
