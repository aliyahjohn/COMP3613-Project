import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import create_db, get_migrate
from App.main import create_app

# from App.controllers import ( create_user, get_all_users_json, get_all_users, create_student, get_all_students, get_all_students_json )
from App.controllers import ( 
    create_user, 
    get_all_users_json, 
    get_all_users, 
    search_all_students, 
    search_all_students_json,
    get_all_students,
    get_all_students_json, 
    create_student, 
    get_all_reviews_json, 
    search_all_reviews,
    search_all_reviews_json
)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    create_db(app)
    print('database intialized')


# '''
# Student Commands
# '''

student_cli = AppGroup('student', help='student object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@student_cli.command("create", help="Creates a student profile")
@click.argument("name", default="jenny")
@click.argument("studentId", default="816000000")
@click.argument("faculty", default="FST")
@click.argument("year", default="2022")
@click.argument("kpoints", default="0")
def create_student_command(name, studentId, faculty, year, kpoints):
    create_student(name, studentId, faculty, year, kpoints)
    print(f'Profile for {name} created!')

# this command will be : flask user create bob bobpass

@student_cli.command("list", help="Lists students in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_students())
    else:
        print(get_all_students_json())

app.cli.add_command(student_cli) # add the group to the cli



'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users_json())
    else:
        print(get_all_users())


# this command will be: flask find/get user
@user_cli.command("find", help = "Gets user by username in the database")
@click.argument("username", default="rob")
# @click.argument("format", default = "string")
def get_user_command(username):
    get_user_by_username(username)
    # if format == 'string':
    #     print(get_user_by_username_json())
    # else:
    print(get_user_by_username_json(username))

app.cli.add_command(user_cli)  # add the group to the cli

student_cli = AppGroup('student', help='Conduct object commands') 

@student_cli.command("list", help="Lists students in the database")
@click.argument("format", default="string")
def list_student_command(format):
    if format == 'string':
        print(get_all_students_json())
    else:
        print(get_all_students_json())

@student_cli.command("search", help = "Searches for student")
@click.argument("id", default ="1")
def search_user_command(id): 
    id = str(id)
    search_all_students_json(id)
    print(search_all_students_json(id))

@student_cli.command("create", help="Creates a student profile")
@click.argument("faculty", default="FST")
@click.argument("kpoints", default="0")
@click.argument("name", default="jenny")
@click.argument("studentId", default="816000")
@click.argument("year", default="2022")
def create_student_command(faculty, kpoints, name, studentId, year):
    create_student(faculty, kpoints, name, studentId, year)
    print(f'Profile for {name} created!')

@student_cli.command("delete", help = "Deletes student profile")
@click.argument("id", default ="1")
def search_user_command(id): 
    id = str(id)
    delete_student(id)
    print(f'Student {id} has been removed')

app.cli.add_command(student_cli)


review_cli = AppGroup('review', help='Review object commands') 

@review_cli.command("list", help = 'List reviews for student id')
@click.argument("id", default="1")
def list_user_command(id):
        id = str(id)
        student = search_all_students_json(id)
        print(get_all_reviews_json(student))

@review_cli.command("search", help = " View reviews by review id")
@click.argument("id", default="0")
def list_review_command(id):
        id = str(id)
        print(search_all_reviews_json(id))

@review_cli.command("delete", help = "Delete review")
@click.argument("id", default ="1")
def search_user_command(id): 
    id = str(id)
    delete_review(id)
    print(f'Review {id} has been removed')






  
app.cli.add_command(review_cli)

'''
Generic Commands
'''

@app.cli.command("init")
def initialize():
    create_db(app)
    print('database intialized')

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)