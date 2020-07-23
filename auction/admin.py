from django.contrib import admin
from auction.models import AuctionDate, AuctionSession, Category, SubCategory, Product
# Register your models here.


class AuctionSessionline(admin.StackedInline):
    model = AuctionSession
    extra = 1
    exclude = ['auction_end_time']


class AuctionDateAdmin(admin.ModelAdmin):
    inlines = [
        AuctionSessionline
    ]
    list_display = ['auction_date']
    search_fields = ('auction_date',)


admin.site.register(AuctionDate, AuctionDateAdmin)


class SubCategoryline(admin.StackedInline):
    model = SubCategory
    extra = 1


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('sub_category_name',)
    search_fields = ('sub_category_name',)
    list_filter = ('sub_category_name',)
    list_per_page = 20


admin.site.register(SubCategory, SubCategoryAdmin)


class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        SubCategoryline
    ]
    list_display = ['category_name']
    list_filter = ['category_name']
    search_fields = ('category_name',)


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('owner', 'title', 'category',
                    'sub_category', 'active', 'rejected', 'created')
    search_fields = ('owner__username', 'title', 'category', 'sub_category',)
    list_filter = ('owner__username', 'active',
                   'rejected', 'category', 'sub_category',)
    list_per_page = 20
    list_editable = ['active', 'rejected']
    autocomplete_fields = ['owner', 'category']


# Register your models here.
admin.site.register(Product, ProductAdmin)
