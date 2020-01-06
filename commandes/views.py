from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from .models import *
from .forms import *
from django.http import HttpResponse
from cart.models import *
from region.models import *
from django.core.mail import send_mail ,EmailMessage
from django.template.loader import render_to_string

# Create your views here.
class HomeCommande(TemplateView):
    def get(self,request):
         if request.user.is_authenticated:
            commande={
            'nom':request.user.first_name+' '+request.user.last_name,
            'adresse':request.user.userprofile.adresse,
            'wilaya':request.user.userprofile.wilaya,
            'commune':request.user.userprofile.commune,
            'livraison':request.user.userprofile.wilaya.prix,
            'email':request.user.email,
            'telephone':request.user.userprofile.telephone,
            }
            form=CommandeForm(instance=Commande(**commande))

         else:
            form=CommandeForm()

         context={'form':form}
         return render(request,'commandes/home.html',context)

    def post(self,request):
        try:
            items=CartItem.objects.filter(cart=Cart.objects.get(session_key = request.session.session_key))
        except:
            items=CartItem.objects.filter(cart=Cart.objects.get(user = request.user))

        if len(items)>0:
            form=CommandeForm(request.POST)
            if form.is_valid():
                commande=form.save(commit=False)
                if request.user.is_authenticated:
                    commande.user=request.user
                commande.save()    
                for item in items:
                    prix=item.produit.prix_promotionel if item.produit.prix_promotionel!=0 else item.produit.prix
                    if item.product_with_attribute:
                        prix=item.product_with_attribute.prix
                    kwargs={
                    'total':item.total,
                    'produit':item.produit.nom +' '+item.product_with_attribute.getValues() if item.product_with_attribute else item.produit.nom ,
                    'reference':item.produit.reference,
                    'prix':prix,
                    'user':item.produit.user.username,
                    'commission':item.produit.categorie.commission,
                    'qtt':item.qtt,
                    'Commande':commande,
                    }
                    CommandeItem(**kwargs).save()

                items.delete()
                msg_html = render_to_string('commandes/email.html', {'commande':commande,})
                recipient_list = [commande.email,]
                msg = EmailMessage(subject='Commande Dressme', body=msg_html, from_email='Dressme', bcc=recipient_list)
                msg.content_subtype = "html"  # Main content is now text/html
                msg.send()

                return render(request,'commandes/commande_completed.html')
            else:
                return render(request,'commandes/home.html',{'form':form})
        else:
            return redirect('shop')
