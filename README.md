# Personal Knowledge Management System

### Current version: 0.0.1

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
- [x] Note creation,reading and deletion (Editing feature is yet to be added)
- [x] Notes stored in respective table with same name as that of their category in database.
- [x] Storing notes in *.md* format
- [x] Searching notes via keyword (only available within a specific notebook)

### Structure of source code
- This rudimentary version of the program tends to apply OOP complemented with heavy function-based programming.Note and Notebook are the only two classes definied within a program with their own respective methods implementing function within.