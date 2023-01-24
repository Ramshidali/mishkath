from django.shortcuts import render

# Create your views here.


# @login_required
def index(request):
    context = {
        'page_name' : 'Dashboard'
    }
    return render(request,'base.html', context)

def create(request):
    return render(request,'create.html') 