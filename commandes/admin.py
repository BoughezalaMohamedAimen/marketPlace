from django.contrib import admin
from .models import *
# Register your models here.


class ModelAInline(admin.StackedInline):
  model = CommandeItem




class CommandeAdmin(admin.ModelAdmin):
    list_display = ('created_at','etat','wilaya','email','telephone','get_total')
    list_filter = ('created_at','etat','wilaya','email','telephone')
    # fields = ('created_at','etat','wilaya','email','telephone',)
    inlines = [ModelAInline]
    # readonly_fields = ['recu','destination','telephone', 'email','dateAller','dateRetour','nom','prenom','ville','nbrAdulte','nbrEnfant','nbrChambre']
        # if 'is_submitted' in readonly_fields:
        #     readonly_fields.remove('is_submitted')
        # return readonly_fields
    def get_total(self, obj):
            return obj.getTotal()
    get_total.short_description = 'Total'
    # get_total.admin_order_field = 'book__author'

admin.site.register(Commande,CommandeAdmin)
admin.site.register(CommandeItem)

admin.site.register(Etat)
