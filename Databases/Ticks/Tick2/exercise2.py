#!/usr/bin/python3.5

import sys
import os.path
import pickle
import pprint

data_dir = sys.argv[1]
name1 = sys.argv[2]
name2 = sys.argv[3]

movies_path = os.path.join(data_dir, 'movies.pickled')
people_path = os.path.join(data_dir, 'people.pickled')

with open(movies_path, mode= "rb") as moviesFile:
    movies = pickle.load(moviesFile)

with open(people_path, mode= "rb") as peopleFile:
    people = pickle.load(peopleFile)

for movie_id in movies:
    movie = movies[movie_id]
    if "actors" in movie:
        found1 = False
        found2 = False
        for actor in movie["actors"]:
            name = actor["name"]
            if name == name1:
                found1 = True
            if name == name2:
                found2 = True
            
            if found1 and found2:
                break
        if found1 and found2:
            title = movie["title"]
            print ("%s and %s are coactors in %s" % (name1, name2, title))
    