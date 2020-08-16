from django.shortcuts import render
from django.shortcuts import redirect
from django.template.backends import django
from django.views.decorators.csrf import csrf_exempt
from Rec import Recommender
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_protect
import json


# Create your views here.

movie_to_add = None
moviesoo = []
reco = Recommender()

def intro(request):

    return render(request, "Intro.html")


@csrf_exempt
def external(request):
    print(request.POST['option'])
    print("aaaaaa")
    passing = {}
    if request.POST['option'] == "show":
        movie = reco.show_movies_to_rate(True)
        global movie_to_add, moviesoo
        movie_to_add = movie
        passing = {"movie": movie['title']}
        pass
    elif request.POST['option'] == "result":
        pass
    else:
        movies = reco.search_movie(request.POST['option'])
        print(movies)
        passing = {"movies": movies}
        moviesoo = movies
    print("geee")

    return render(request, "Intro.html", passing)


@csrf_exempt
def add_movie(request):
    print("ss")
    ss = json.loads(request.body)
    print(ss["movie"])
    print(ss['rate'])
    print("he")
    global movie_to_add,moviesoo
    #print(request.POST['but'])
    #reco.add_new_movie_rating(movie_to_add,request.POST['but'])
    for i,m in moviesoo.iterrows():
        if ss['movie'] == m['title']:
            movie_to_add = m
            break

    reco.add_new_movie_rating(movie_to_add,ss['rate'] )
    aa = HttpRequest()
    aa.POST['option'] = "show"
    return external(aa)

