
import os
import shelve
from datetime import date
import sqlite3
from tabulate import tabulate
from rich.console import Console
from rich.markdown import Markdown
from prompt_toolkit import prompt
# from prompt_toolkit.key_binding import KeyBindings


class note:
    def __init__(self,title,author,date,tag,content):
        self.title=title
        self.author=author
        self.date= date
        self.tag=tag
        self.content=content
    def editnote(self,notebook_name):
        edit_note(notebook_name,self.title)
    def deletenote(self,notebook_name):
        delete_note(notebook_name,self.title)

def edit_note(notebook,to_edit):
    try:
        print("\nEditing area:")
        print("NOTE:'#' and '*' are to be left untouched (it makes file compatible)\nPRESS Esc + Enter to save file and quit terminal simultaneously.")
        print()
        with open(f"Notebooks/{notebook}/{to_edit}.md" , "r") as file_read_open:
            lines=file_read_open.read()
        content=prompt(default=lines,multiline=True)
        with open(f"Notebooks/{notebook}/{to_edit}.md" , "w") as file_write_open:
            file_write_open.write(content)
        print("File succesfully edited..")
    except Exception as e:
        print(f"An error occured..")


def delete_note(notebook,ask_to_delete):
    with sqlite3.connect("Database/main_database.db") as connection:
        cursor=connection.cursor()
        delete_script =f'''
        DELETE FROM {notebook} WHERE Title = '{ask_to_delete}';

        '''
        cursor.execute(delete_script)
        connection.commit()
    filepath=f"Notebooks/{notebook}/{ask_to_delete}.md"
    if os.path.exists(filepath):
        os.remove(filepath)
    print("Note with code {} has been deleted..".format(ask_to_delete))
    with shelve.open("Object_database/note_object.db") as note_object_delete:
            del note_object_delete[ask_to_delete]



def note_manipulation(notebook_name):
    manipulation_mode=int(input("[1] Edit/Update note\n[2] Delete note\n Enter your choice: "))
    if manipulation_mode == 1:
        ask_edit_note=input("Enter title of note to be edited: ").strip().capitalize()
        with shelve.open('Object_database/note_object.db') as note_object_retrieve:
            target=note_object_retrieve[ask_edit_note]
        target.editnote(notebook_name)
    elif manipulation_mode == 2:
        ask_delete_note=input("Enter title of note to be deleted:").strip().capitalize()
        with shelve.open("Object_database/note_object.db") as note_object_retrieve:
            target= note_object_retrieve[ask_delete_note]
        target.deletenote(notebook_name)
    else:
        print("Invalid input!!!")
        


#add note
def add_note(notebook_name):
    print("\n")
    print("Creating note....")
    title=input("Title: ").strip().capitalize()
    author=input("Author: ").strip()
    date=input("Date: ").strip()
    tags=input("Tag(multiple tags require space in between):").strip()
    content=input("Content: ")
    new_note=note(title,author,date,tags.split(" "),content)
    with shelve.open("Object_database/note_object.db") as note_db:
        note_db[f"{new_note.title}"] = new_note
    file_path=f"Notebooks/{notebook_name}/{title}.md"
    with open (file_path, "w+") as fopen_note:
        fopen_note.write(f"# Title: {new_note.title}\n")
        fopen_note.write(f"## Author: {new_note.author}\n")
        fopen_note.write(f"### Date: {new_note.date}\n")
        fopen_note.write(f"### Tag: {", ".join(new_note.tag)}\n")
        fopen_note.write(f"*{new_note.content}*")
    insert_into_database(new_note.title,new_note.author,new_note.date,new_note.tag,new_note.content,notebook_name)

#Listing
def list_note(notebook_name):
    with sqlite3.connect("Database/main_database.db") as connection:
        cursor=connection.cursor()
        list_notes=f'''
        SELECT * FROM {notebook_name};
        '''
        cursor.execute(list_notes)
        output=cursor.fetchall()
    print(tabulate(output,headers=['Code','Title','Author','Date','Tags','Content','Notebook'],tablefmt="grid"))

#Viewing
def view_note(notebook_name):
    header=['Code','Title','Author','Date','Tags','Content','Notebook']
    with sqlite3.connect("Database/main_database.db") as connection:
        cursor=connection.cursor()
        list_notes=f'''
        SELECT * FROM {notebook_name};
        '''
        cursor.execute(list_notes)
        output=cursor.fetchall()
    print(tabulate(output,headers=header,tablefmt="grid"))
        
    ask_code_no=int(input("Enter code to view: "))
    for ele in output:
        _no_ , _title_,*_info_,_notebook_ = ele
        if _no_ == ask_code_no:
            with open(f"Notebooks/{_notebook_}/{_title_}.md" ,"r") as fread:
                content=fread.read()
    
    console=Console()
    formatted_content =Markdown(content)
    console.print("\n")
    console.print(_notebook_,style="italic magenta")
    console.print(formatted_content)
    console.print("\n")
    
            
#Filtering
def filter_note(notebook_name):
    filtered_notes=[]
    ask_filter_tag=input("Enter filter tag(Multiple tags require space in between): ").strip().split(" ")
    header=['Code','Title','Author','Date','Tags','Content','Notebook']
    with sqlite3.connect("Database/main_database.db") as connection:
        cursor=connection.cursor()
        list_notes=f'''
        SELECT * FROM {notebook_name};
        '''
        cursor.execute(list_notes)
        output=cursor.fetchall()
    for ele in output:
        *_info_,_tags_,_content_,_notebook_ = ele
        for t in ask_filter_tag:
            if t.capitalize() in _tags_.split(",") or t.lower() in _tags_.split(","):
                filtered_notes.append(ele)
    print("Filtered data:\n")
    print(tabulate(filtered_notes,headers=header,tablefmt="grid"))


#Keyword searching
def search_by_keyword(notebook_name):
    header= ['Code','Title','Author','Date','Tags','Content','Notebook']
    searched_data=[]
    ask_keyword=input("Enter keyword(multiple keywords require space in between): ").strip()
    with sqlite3.connect("Database/main_database.db") as connection:
        cursor = connection.cursor()
        search_keywords=f'''
        SELECT * FROM {notebook_name};
        '''
        cursor.execute(search_keywords)
        output=cursor.fetchall()
    for ele in output:
        _code_,*_info_= ele
        for keyword in ask_keyword.split(" "):
            if any(keyword.lower() in str(x) for x in _info_ ) or any(keyword.upper() in str(x) for x in _info_ ) or any(keyword.capitalize() in str(x) for x in _info_ ):
                searched_data.append(ele)
    print(tabulate(searched_data,headers=header,tablefmt="grid"))

        
#inserting into database
def insert_into_database(Title,Author,Date,Tags,Content,Notebook_name):
    print("Pushing data into database...")
    with sqlite3.connect("Database/main_database.db") as connection:
        cursor=connection.cursor()
        create_table=f'''
        CREATE TABLE IF NOT EXISTS {Notebook_name}(
            Code INTEGER  PRIMARY KEY AUTOINCREMENT,
            Title TEXT,
            Author TEXT,
            Date TEXT,
            Tags TEXT,
            Content TEXT,
            Notebook TEXT
        );
        '''
        cursor.execute(create_table)
        connection.commit()
        insert_query=f'''
        INSERT INTO {Notebook_name}(Title,Author,Date,Tags,Content,Notebook)
        VALUES (?, ?, ?, ?, ?, ?);
        '''
        data=(Title,Author,Date,",".join(Tags),Content,Notebook_name)
        cursor.execute(insert_query, data)
        connection.commit()
    print("Data uploaded....")


def view_stats():
    try:
        if os.path.isdir("Notebooks/"):
            no_of_notebook = sum(os.path.isdir(os.path.join("Notebooks", d)) for d in os.listdir("Notebooks"))
            no_of_notes=0
            for dirpath,subdirs,files in  os.walk("Notebooks/"):
                for file_name in files:
                    if file_name.endswith(".md"):
                        no_of_notes+=1
            print(f"Total no of notebooks:{no_of_notebook}\nTotal no of notes:{no_of_notes}")

        else:
            print("No notebook has been created. Please add a notebook first")
    except Exception as e :
        print(e)



#notebook class
class notebook:
    def __init__(self,name,date):
        self.name=name
        self.date=date
    def __call__(self):
        return self.name
    def addnote(self):
        add_note(self.name)
    def listnote(self):
        list_note(self.name)
    def viewnote(self):
        view_note(self.name)
    def filternotes(self):
        filter_note(self.name)
    def searchbykeywords(self):
        search_by_keyword(self.name)


#main function
def main():
    while True:
        main_prompt=input("1.Add notebook\n2.Open existing notebook\n3.View Stats\nEnter your option: ")
        if main_prompt.strip() == "1":
            notebook_name=input("Enter your notebook name: ").strip().capitalize()
            new_notebook=notebook(notebook_name,date.today())
            notebook_path=os.path.join("Notebooks",new_notebook.name)
            try:
                if not os.path.isdir(notebook_path):
                    print("Creating notebook...")
                    os.makedirs(notebook_path, exist_ok=True)
                    print("Successfully created!")
                else:
                    print(f"Notebook with name '{notebook_name}' already exists!")
                if  not os.path.isdir("Database") :
                        os.mkdir("Database")
                with sqlite3.connect("Database/main_database.db") as connection:
                    cursor=connection.cursor()
                    create_table=f'''
                    CREATE TABLE IF NOT EXISTS {notebook_name}(
                        Code INTEGER  PRIMARY KEY AUTOINCREMENT,
                        Title TEXT,
                        Author TEXT,
                        Date TEXT,
                        Tags TEXT,
                        Content TEXT,
                        Notebook TEXT
                    );
                    '''
                    cursor.execute(create_table)
                    connection.commit()
                if not os.path.isdir("Object_database"):
                    os.mkdir("Object_database")
                with shelve.open("Object_database/notebook_object.db") as notebook_db:
                    notebook_db[f"{notebook_name}"]=new_notebook
            except Exception as e:
                print(f"An error occured:{e}")
            print("{} added....".format(notebook_name))
            prompt_user=input("Do you want to go back? ").strip().capitalize()
            if prompt_user in ["Y","Yes","Yeah"]:
                continue
            else:
                print("We are sorry to let you go")
                break

        elif main_prompt.strip() == "2":
            ask_notebook_name=input("Enter Notebook:").strip().capitalize()
            if os.path.isdir(os.path.join("Notebooks" , ask_notebook_name)):
                print(f" 📓 Notebook:{ask_notebook_name}")
                while True:
                    ask_about_notebook=input("[1] Add new note\n[2] List notes\n[3] View notes\n[4] Search by keywords\n[5] Filter by tags\n[6] Note Manipulation\nEnter your choice: ").strip()
                    with shelve.open("Object_database/notebook_object.db") as object_retrieve:
                        target_=object_retrieve[f"{ask_notebook_name}"]
                    if ask_about_notebook == "1":
                        target_.addnote()
                    elif ask_about_notebook == "2":
                        target_.listnote()
                    elif ask_about_notebook =="3":
                        target_.viewnote()
                    elif ask_about_notebook == "4":
                        target_.searchbykeywords()
                    elif ask_about_notebook =="5":
                        target_.filternotes()
                    elif ask_about_notebook == "6":
                        note_manipulation(ask_notebook_name)
                    else:
                        print("Invalid input!!!")
                    prompt_user=input("Do you want to continue? ").strip().capitalize()
                    if prompt_user in ["Y","Yes","Yeah"]:
                        continue
                    else:
                        print("We are sorry to let you go...")
                        break
                break
                
            else:
                print("{} doesnt exist.".format(ask_notebook_name))
                prompt_user=input("Do you want to go back? ").strip().capitalize()
                if prompt_user in ["Y","Yes","Yeah"]:
                    continue
                else:
                    print("We are sorry to let you go!")
                    break

        elif main_prompt.strip() == "3":
            view_stats()

        else:
            print("Invalid Output...")
            retry=input("Do you again want to try? ").strip().capitalize()
            if retry in ["Y","Yes","Yeah","Yup"]:
                continue
            else:
                print("Sorry..You have missed your last chance :(, Good luck next time :)")
                break


if __name__ == "__main__":
    main()