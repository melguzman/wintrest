from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)
import cs304dbi as dbi 

'''**************** Queries for getting info ****************'''

def find_profile(conn, wemail):
    '''Returns the info associated with a given wemail'''
    curs = dbi.dict_cursor(conn)
    curs.execute('''SELECT * FROM userAccount WHERE wemail =
         %s''', [wemail])
    person = curs.fetchone()
    # returns a string in the case where the person has not filled info out
    # otherwise, returns the demographics
    if len(person) != 0:
        return person
    return "No user by that name yet"

def find_dem(conn, wemail):
    '''Returns a user's demographic information; singular row returned'''
    curs = dbi.dict_cursor(conn)
    curs.execute('''SELECT country, state, city FROM userAccount 
            WHERE wemail = %s''', [wemail])
    demographics = curs.fetchall()
    # returns a string in the case where the person has not filled info out
    # otherwise, returns the demographics
    if len(demographics) != 0:
        return demographics
    return "No demographics input yet"

def find_phoneNum(conn, wemail):
    '''Returns a user's phone number'''
    curs = dbi.dict_cursor(conn)
    curs.execute('''SELECT phoneNumber FROM contact WHERE 
        wemail = %s''', [wemail])
    phoneNum = curs.fetchall()
    # returns a string in the case where the person has not filled info out
    # otherwise, returns the demographics
    if len(phoneNum) != 0:
        return phoneNum
    return "No phone number input yet"

'''**************** Queries for changing tables ****************'''

############ INSERT, UPDATE User Profile

def insert_profile(conn, wemail, fname, lname, country,
            state, city, major, year, onCampus): #got rid of password and MBCode
    '''Takes new user's initial inputs and adds them into the table'''
    # assumption: user MUST input all categories 
    curs = dbi.dict_cursor(conn)
    curs.execute('''SELECT * FROM userAccount WHERE wemail = %s''', [wemail])
    checkUser = curs.fetchall()
    # if account for this user doesn't already exist, we will add them to
    # the userAccounts table
    if len(checkUser) == 0: 
        curs.execute('''INSERT INTO userAccount (wemail, fname, lname, country, 
            state, city, major, year, onCampus) VALUES (%s, %s, %s, %s, 
            %s, %s, %s, %s, %s)''', 
            [wemail, fname, lname, country, state, city, major, year, onCampus])
    conn.commit()

def update_profile(conn, wemail, fname, lname, country,
            state, city, major, year, onCampus): #got rid of password
    '''Takes user's changed inputs for their profile and updates the
    profile accordingly'''

    curs = dbi.dict_cursor(conn)

    #curs.execute('''UPDATE userAccount SET password = %s 
         #WHERE wemail = %s''', [password, wemail]) 
    curs.execute('''UPDATE userAccount SET fname = %s 
        WHERE wemail = %s''', [fname, wemail])
    curs.execute('''UPDATE userAccount SET lname = %s
        WHERE wemail = %s''', [lname, wemail])
    curs.execute('''UPDATE userAccount SET country = %s
        WHERE wemail = %s''', [country, wemail])
    curs.execute('''UPDATE userAccount SET state = %s
        WHERE wemail = %s''', [state, wemail])
    curs.execute('''UPDATE userAccount SET city = %s
        WHERE wemail = %s''', [city, wemail])
    #curs.execute('''UPDATE userAccount SET MBCode = %s
        #WHERE wemail = %s''', [MBCode, wemail])
    curs.execute('''UPDATE userAccount SET major = %s
        WHERE wemail = %s''', [major, wemail])
    curs.execute('''UPDATE userAccount SET year = %s
        WHERE wemail = %s''', [year, wemail])
    curs.execute('''UPDATE userAccount SET onCampus = %s
        WHERE wemail = %s''', [onCampus, wemail])

    conn.commit()

def delete_profile(conn, wemail):
    '''Deletes a user profile given their ID'''
    curs = dbi.dict_cursor(conn)
    user = find_profile(conn, wemail)
    if len(user) != 0:
        curs.execute('''DELETE FROM userAccount WHERE wemail = %s''', [wemail])

    conn.commit()

############ INSERT, UPDATE User Profile

def insert_contact(conn, wemail, phoneNumber, handle, url, platform):
    '''Takes new user's contact information (phone number and info
    about most used social medial platform) so others can reach out
    Note: users can only insert one row of their contact information''' 

    curs = dbi.dict_cursor(conn)
    curs.execute('''SELECT * FROM contact WHERE wemail = %s''', [wemail])
    checkContact = curs.fetchall()
    # if contact for this user doesn't already exist, we will add their info to
    # the contact table
    if len(checkContact) == 0: 
        curs.execute('''INSERT INTO contact (wemail, phoneNumber, 
            handle, url, platform) VALUES (%s, %s, %s, %s, %s)''', 
            [wemail, phoneNumber, handle, url, platform])
    conn.commit()

def update_contact(conn, wemail, phoneNumber, handle, url, platform): 
    '''Takes user's changed inputs for their contacts and updates the
    profile accordingly'''

    curs = dbi.dict_cursor(conn)

    curs.execute('''UPDATE contact SET phoneNumber = %s
        WHERE wemail = %s''', [phoneNumber, wemail])
    curs.execute('''UPDATE contact SET handle = %s
        WHERE wemail = %s''', [handle, wemail])
    curs.execute('''UPDATE contact SET url = %s
        WHERE wemail = %s''', [url, wemail])
    curs.execute('''UPDATE contact SET platform = %s
        WHERE wemail = %s''', [platform, wemail])

    conn.commit()

def delete_contact(conn, wemail):
    '''Deletes a user's contact information given their wemail'''
    curs = dbi.dict_cursor(conn)
    phone = find_phoneNum(conn, wemail)
    if len(phone) != 0:
        curs.execute('''DELETE FROM contact WHERE wemail = %s''', [wemail])
    conn.commit()

if __name__ == '__main__':
    dbi.cache_cnf()   # defaults to ~/.my.cnf
    dbi.use('wellesleymatch_db')
    conn = dbi.connect()
    #print(find_profile(conn, 'aEstrada'))
    #print(find_dem(conn, 'aEstrada'))
    #print(find_phoneNum(conn, 'aEstrada'))
    #insert_profile(conn, 'mTuzman', 'Melissa', 'Tuzman', 'USA',
            #'CA', 'Bellflower', 'Data Science', 2020, 'no')
    #update_profile(conn, 'mTuzman', 'Melissa', 'Tuzman', 'USA',
            #'CA', 'Los Angeles', 'Data Science', 2020, 'no')
    #insert_contact(conn, 'mTuzman', 703, 'somehandle11', 'someurlq', 'facebook')
    #update_contact(conn, 'mTuzman', 703, 'somehandle11', 'someurlq', 'instagram')
    #delete_contact(conn, 'mTuzman')
    