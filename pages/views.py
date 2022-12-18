from django.http import HttpResponse
from django.shortcuts import render

from params.forms import ParamsForm
from params.models import Params

from utils.genPoem import genPoem

# Create your views here.
def home_view(request, *args, **kwargs):
    #Intiliazie form to load into context
    #Form is based on the params modal
    form = ParamsForm(request.POST or None)

    if form.is_valid():
        form.save()
        form = ParamsForm()

    context = {
        "form":form,
    }

    return render(request, "home.html", context)

def poem_view(request, *args, **kwargs):
    #Get the parameters of the poem from the form
    genre = request.POST.get("genre")
    syls = request.POST.get("syls")

    #Genreate a poem based on those paramaters
    poem = genPoem(genre, syls)

    #Pass the generated poem into the context
    context = {
        "poem": poem

    }

    return render(request, "poem.html", context)
