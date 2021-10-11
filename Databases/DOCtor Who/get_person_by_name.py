# This will be the common prelude to all of our queries. 

import sys     # talk to the operating system 
import os.path # manipulate paths to files, directories 
import pickle  # read/write pickled python dictionaries 
import pprint  # pretty print JSON

data_dir = sys.argv[1] # first command-line argument -- the directory of data 

# use os.path.join so that path works on both Windows and Unix 
movies_path = os.path.join(data_dir, 'movies.pickled')
people_path = os.path.join(data_dir, 'people.pickled')

# open data dictionary files and un-pickle them 
moviesFile = open(movies_path, mode= "rb")
movies     = pickle.load(moviesFile)

peopleFile = open(people_path, mode= "rb")
people     = pickle.load(peopleFile)

#####################################
# write your query code here ...

def get_person_by_name (str): 
    # initialise output 
    the_person = {} 
    # iterate through all the keys of the people dictionary 
    # looking for one with the right name 
    for person_id in people.keys():
        if people[person_id]['name'] == str: 
            the_person = people[person_id]
    return the_person 

name    = sys.argv[2] 

pprint.pprint (get_person_by_name(name))
