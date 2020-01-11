from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class ProduitAdmin(admin.ModelAdmin):
    list_display = ('id', 'valid','motif','nom', 'categorie','user','prix')
    list_filter=('valid','categorie',)
    search_fields = ('user__username', 'user__email','nom')
    readonly_fields = ["image_image1","image_image2","image_image3","image_image4"]
    def image_image1(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.image.url,
            width=200,
            height=200,
            )
    )
    def image_image2(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.image2.url,
            width=200,
            height=200,
            )
    )
    def image_image3(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.image3.url,
            width=200,
            height=200,
            )
    )
    def image_image4(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.image4.url,
            width=200,
            height=200,
            )
    )
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom')
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'attribute','value')
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'produit','get_values','stock','prix')
    list_filter = ('attributevalues',)
    def get_values(self, obj):
            return obj.getValues()
    get_values.short_description = 'attributs'


class MotifAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')



# Register your models here.
admin.site.register(Produit,ProduitAdmin)
admin.site.register(Attribute,AttributeAdmin)
admin.site.register(AttributeValue,AttributeValueAdmin)
admin.site.register(ProductAttribute,ProductAttributeAdmin)
admin.site.register(Motif,MotifAdmin)
# admin.site.register(Attribut)
