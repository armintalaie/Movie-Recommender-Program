from django.shortcuts import render
from django.shortcuts import redirect
from django.template.backends import django
from django.views.decorators.csrf import csrf_exempt
from Rec import RecommendProgram
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_protect
import json

# Create your views here.

movie_to_add = None
moviesoo = []
reco = RecommendProgram("")


def intro(request):
    return render(request, "Intro.html")


@csrf_exempt
def external(request):
    print(request.POST['option'])
    passing = {}
    if request.POST['option'] == "show":
        movie = reco.show_movies_to_rate(True)
        global movie_to_add, moviesoo
        movie_to_add = movie
        passing = {"movie": movie['title']}
        pass
    elif request.POST['option'] == "result":
        rec1 = reco.recommend_movies()
        passing = {'result': rec1}
    else:
        movies = reco.search_movie(request.POST['option'])
        print(movies)
        passing = {"movies": movies}
        moviesoo = movies
    print("geee")

    return render(request, "Intro.html", passing)


@csrf_exempt
def add_movie(request):
    ss = json.loads(request.body)
    print(ss["movie"])
    print(ss['rate'])
    print("he")
    global movie_to_add, moviesoo
    # print(request.POST['but'])
    # reco.add_new_movie_rating(movie_to_add,request.POST['but'])
    for i, m in moviesoo.iterrows():
        if ss['movie'] == m['title']:
            movie_to_add = m
            break

    reco.add_new_movie_rating(movie_to_add, ss['rate'])
    aa = HttpRequest()
    aa.POST['option'] = "show"
    return external(aa)


@csrf_exempt
def add_movie_shown(request):
    print(request.POST['but'])
    reco.add_new_movie_rating(movie_to_add, request.POST['but'])
    aa = HttpRequest()
    aa.POST['option'] = "show"
    return external(aa)


@csrf_exempt
def give_results(request):
    global movie_to_add, moviesoo

    # rec1 = reco.recommend_movies()
    print("fffff")
    passing = {}

    aa = HttpRequest()
    # for i,moviess in rec1.iterrows():
    # print(moviess.title)
    aa.POST['option'] = "result"
    rec1 = "hhhh"
    passings = {'ola': 'pp'}
    return external(aa)


# coool vlue 1E96FC
# original yellow #ffed66;
#original blue 26547c;