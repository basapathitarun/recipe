from django.shortcuts import render,redirect,HttpResponse

from .models import *
# Create your views here.

def Getting_information():
    query = Receipe.objects.all()
    context = {'receipes': query}
    return context

def index(request):
    if request.method=='POST':
        data = request.POST
        receipe_name=data.get('receipe_name')
        receipe_description=data.get('receipe_description')
        receipe_image = request.FILES.get('receipe_image')
        print(receipe_name)
        Receipe.objects.create(
            receipe_name=receipe_name,
            receipe_description=receipe_description,
            receipe_image=receipe_image
        )
        return redirect('/')

    context = Getting_information()
    if request.GET.get('receipe_name'):
        querryset= context['receipes']
        query=querryset.filter(receipe_name__icontains = request.GET.get('receipe_name'))
        context = {'receipes': query}
    return render(request,'receipe.html',context)

def delete(request,id):
    obj =Receipe.objects.get(receipe_name=id)
    obj.delete()
    context = Getting_information()
    return render(request, 'receipe.html', context)

def update(request,id):
    query =Receipe.objects.get(receipe_name=id)

    if request.method  == 'POST':
        data = request.POST
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        receipe_image = request.FILES.get('receipe_image')

        query.receipe_name=receipe_name
        query.receipe_description=receipe_description

        if receipe_image:
            query.receipe_image = receipe_image

        query.save()
        return redirect('/')

    context = {'receipes':query}
    return render(request,'update.html',context)



