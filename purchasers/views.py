from django.shortcuts import render, HttpResponse, redirect
from purchasers.forms import NewPurchaserForm
from django.contrib.auth.decorators import login_required
from directconnect.settings import LOGIN_URL
from purchasers.models import Purchaser
# Create your views here.


@login_required(login_url=LOGIN_URL)
def new_purchaser(request):
    if request.method == "POST":
        purchaser = NewPurchaserForm(request.POST).save(commit=False)
        purchaser.user = request.user
        purchaser.save()
        return redirect('/')
    if len(request.user.purchaser_set.all()):
        return redirect('/')
    return render(request, 'purchasers/purchaser_form.html', {'form': NewPurchaserForm(), 'url': request.path,
                                                           'action_url': '/purchasers/new'})


@login_required(login_url=LOGIN_URL)
def edit_purchaser(request, purchaser_id):
    purchaser = Purchaser.objects.get(id=purchaser_id)
    form = NewPurchaserForm(instance=purchaser)
    if request.method == "POST":
        NewPurchaserForm(request.POST, instance=purchaser).save()
        return redirect("/auth/details")
    return render(request, 'purchasers/purchaser_form.html', {'form': form,
                                                            'action_url': '/purchasers/edit/{0}'.format(purchaser_id)})
