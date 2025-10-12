# Personal Knowledge Management System

### Current version: 1.0.0

## About
*A Personal Knowledge Management,also commonly known as PKM is a system of recording,storing and retrieving crucial information essential in user's learning process.*


## A comprehensive guide to terms used 
- ***Notebook*** is a collection of notes of particular kinds in a structured manner. It can be better understood as a vault which stores certain kinds of objects/things or notes(in this case). For instance, a user can create a notebook named "Journals" where only journaling notes are stored and managed.
- ***Note*** can be thought of as an actual information to be stored or recorded from which an individual can derive an invalauble insight after analysis of content within it.
- ***Tags*** are extra labels attached to a particular note which simply provide what a reader can expect from the contents written inside that note. Usually, tags tend to let readers get an idea about the  core themes of the information stored within or the state of the note under consideration.


## Features
- Notebook CRUD operation
- Notes CRUD operation
- Filtering notes via ***tags***
- Listing notes in a particular notebook
- Well structured database management
- Proper storing of notes in  *.md* file format for easy export and compatibility across suitable services

### Available features
- [x] Filtering notes via tags
- [x] Listing notes feature
- [x] Notebook creation
- [x] Note creation,reading, editing and deletion 
- [x] Notes stored in respective table with same name as that of their category in database.
- [x] Storing notes in *.md* format
- [x] Searching notes via keyword (only available within a specific notebook)

### Structure of the project
- Database/             ---> storing notebook and notes
- Notebooks/            ---> Actual home for all notes and their respective notebook
- Object_database/      ---> Home to note_object.db and notebook_object.db
- note_object.db        ---> storing note as an object
- notebook_object.db    ---> stroing notebook as an object
- PKM.py                ---> Actual code
- requirements.txt      ---> Necessary dependencies and libraries
- READMe.md             ---> Friendly overview of the project

### Main code (PKM.py)
This version of code achieves the above mentioned features mainly via the implementation of both user-defined and pre-defined functions.Though minimal, the program has also been approached with an object oriented paradigm. Furthermore, the use of library modules also complement the functionality of the code.

#### Third Party Modules used
- tabulate
- rich
- prompt_toolkit
