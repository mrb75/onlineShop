from django.contrib import admin
from .models import Category, Product, Property, Value, Color, Comment, ProductMedia


class PropertyInline(admin.TabularInline):
    model = Product.properties.through


class ColorInline(admin.TabularInline):
    model = Product.colors.through


class PropertyCategoryInline(admin.TabularInline):
    model = Property
    fk_name = "category"


class ChildInline(admin.TabularInline):
    model = Category
    fk_name = "parent"


class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        PropertyCategoryInline,
        ChildInline,
    ]
    list_display = ('name', 'create_date_time', 'modify_date_time')


class ProductAdmin(admin.ModelAdmin):
    inlines = [PropertyInline, ColorInline]
    list_display = ('name', 'price', 'discount', 'description',
                    'create_date_time', 'modify_date_time', 'seller', 'category')

    # def get_object(self, request, object_id, st):
    #     # Hook obj for use in formfield_for_manytomany
    #     self.obj = super(ProductAdmin, self).get_object(request, object_id)
    #     print("Got object:", self.obj)
    #     return self.obj

    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     if db_field.name == "properties":
    #         if not (self.obj):
    #             kwargs["queryset"] = Value.objects.filter(
    #                 prop__category=self.obj.category)
    #         else:
    #             kwargs["queryset"] = Value.objects.all()
    #     return super().formfield_for_manytomany(db_field, request, **kwargs)


class PropertyAdmin(admin.ModelAdmin):
    pass


class ValueAdmin(admin.ModelAdmin):
    pass


class ColorAdmin(admin.ModelAdmin):
    pass


class CommentAdmin(admin.ModelAdmin):
    pass


class ProductMediaAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Value, ValueAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ProductMedia, ProductMediaAdmin)
