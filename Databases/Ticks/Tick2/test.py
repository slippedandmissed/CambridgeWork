#!/usr/bin/python3.8

import sys
import os.path
import pickle
import pprint

data_dir = sys.argv[1]

movies_path = os.path.join(data_dir, 'movies.pickled')
people_path = os.path.join(data_dir, 'people.pickled')

with open(movies_path, mode= "rb") as moviesFile:
    movies = pickle.load(moviesFile)

with open(people_path, mode= "rb") as peopleFile:
    people = pickle.load(peopleFile)

print(people[list(people.keys())[1100]])