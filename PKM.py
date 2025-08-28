
import os
from datetime import date
import sqlite3

class note:
    def __init__(self,title,author,date,tag,content):
        self.title=title
        self.author=author
        self.date= date
        self.tag=tag
        self.content=content
    def editnote(self):
        print("comming soon")
    def deletenote(self):
        print("comming soon")

def add_note(notebook_name):
    title=input("Title: ").strip()
    author=input("Author: ").strip()
    date=input("Date: ").strip()
    tags=input("Tag:")
    content=input("Content: ")
    new_note=note(title,author,date,tags.split(" "),content)
    file_path=f"Notebooks/{notebook_name}/{title}.md"
    with open (file_path, "a+") as fopen_note:
        fopen_note.write(f"# Title: {new_note.title}\n")
        fopen_note.write(f"## Author: {new_note.author}\n")
        fopen_note.write(f"### Date: {new_note.date}\n")
        fopen_note.write(f"### Tag: {",".join(new_note.tag)}\n")
        fopen_note.write(f"*{new_note.content}*")
    insert_into_database(new_note.title,new_note.author,new_note.date,new_note.tag,notebook_name)

def list_note():
    print("Soon coming")



def view_note():
    print("coming soon")


def insert_into_database(Title,Author,Date,Tags,Notebook_name):
    print("Pushing data into database...")
    with sqlite3.connect("Database/main_database.db") as connection:
        cursor=connection.cursor()
        create_table='''
        CREATE TABLE IF NOT EXISTS Notes(
            Id INTEGER  PRIMARY KEY AUTOINCREMENT,
            Title TEXT,
            Author TEXT,
            Date TEXT,
            Tags TEXT,
            Notebook TEXT
        );
        '''
        cursor.execute(create_table)
        connection.commit()
        insert_query='''
        INSERT INTO Notes(Title,Author,Date,Tags,Notebook)
        VALUES (?, ?, ?, ?, ?);
        '''
        data=(Title,Author,Date,",".join(Tags),Notebook_name)
        cursor.execute(insert_query, data)
        connection.commit()
    print("Data uploaded....")

class notebook:
    def __init__(self,name,date):
        self.name=name
        self.date=date
    def __call__(self):
        return self.name
    def addnote(self):
        add_note()
    def listnote(self):
        list_note()
    def viewnote(self):
        view_note()
    def filternotes(self):
        pass
    def searchbykeywords(self):
        pass
    
def ask_user():
    # os.getcwd()
    main_prompt=input("1.Add notebook\n2.Open existing notebook\n3.Filter by tags\nEnter your option: ")
    if main_prompt.strip() == "1":
        notebook_name=input("Enter your notebook name: ").strip().capitalize()
        new_notebook=notebook(notebook_name,date.today())
        notebook_path=os.path.join("Notebooks",new_notebook.name)
        try:
            print("Creating notebook...")
            os.makedirs(notebook_path, exist_ok=True)
            print("Successfully created!")

        except Exception as e:
            print(f"An error occured:{e}")

    elif main_prompt.strip() == "2":
        ask_notebook_name=input("Enter Notebook:").strip().capitalize()
        if os.path.isdir(os.path.join("Notebooks" , ask_notebook_name)):
            print(f" 📓 Notebook:{ask_notebook_name}")
            ask_about_notebook=input("[1] Add new note\n[2] List notes\n[3] View notes\n[4] Search by keywords\n[5] Filter by tags\nEnter your choice: ").strip()
            if ask_about_notebook == "1":
                add_note(ask_notebook_name)
            elif ask_about_notebook == "2":
                pass #List notes
            elif ask_about_notebook =="3":
                pass #view notes
            elif ask_about_notebook == "4":
                pass #search by keywords
            elif ask_about_notebook =="5":
                pass #Filter by tags
        
            
        else:
            print("It doesnt exist.")

    elif main_prompt.strip() == "3":
        ask_tag_filter=input("Enter tag:").strip()
        print(ask_tag_filter)
        pass

        

ask_user()