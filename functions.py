# -*- coding: utf-8 -*-
import speech_recognition as sr
import pyttsx3
from gtts import gTTS
from nltk import word_tokenize
import psycopg2
import eel
import googletrans
from googletrans import Translator

#runtype = 'test' # test -> harcoded inputs
runtype = 'demo' # demo -> speech inputs

def db_connect():
    conn = psycopg2.connect(database="IVR_POS", user="postgres", password="Aru10oct", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    return conn,cur

@eel.expose
def basket_printer():
    conn,cur = db_connect()
    # return parent_category_selector(cur)
    return invoice_printer(cur)

@eel.expose
def inv_printer():
    conn,cur = db_connect()
    return item_printer(cur)

def speak(audio,language="english"):

    translator = Translator()
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    if language=="english":
        engine.setProperty('voice', voices[0].id)
    elif language =="hindi":
        for voice in voices:
            if voice.languages[0] == u'hi_IN':
                engine.setProperty('voice', voice.id)
                break
        result = translator.translate(audio, src='en', dest='hi')
        audio=result.text

    else:
        for voice in voices:
            if voice.languages[0] == u'es_ES':
                engine.setProperty('voice', voice.id)
                break
        result = translator.translate(audio, src='en', dest='es')
        audio=result.text
        print(audio)

    engine.say(audio)
    engine.runAndWait()

@eel.expose
def myCommand(param="Item name"):

    "listens for commands"
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print(param)
        r.pause_threshold = 0.5
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')

    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('....')
        command = myCommand(param);

    return command

def printer(current_pointer,p_type,quantity=0):

    rows = current_pointer.fetchall()

    if p_type == 1:
        print('Cat  |\t\n id  |\t','Category name',"\t|")
    elif p_type ==2:
        print('Cat  |\tSub Category\t|\n id  |\t','    name'," \t|")
    elif p_type ==3:
        print('Item  |\t\n id  |\t','Item name',"\t|")
    else:
        print("Invalid")

    print("--------------------------")

    x = []

    if p_type == 1 or p_type == 2:
        for row in rows:
            print(row[0],'  |\t',row[1],"    \t|")
    elif p_type == 3:
        for row in rows:
            print(row[0],'  |',row[2],"\t|")
            #x.append(row[0],row[2],row[3],quantity,row[3]*quantity)
        #return rows[0],rows[2],rows[3],quantity,rows[3]*quantity

    else :
        print("error")

    return rows

def parent_category_selector(cur_pointer):

    #print(runtype)
    cur_pointer.execute("SELECT category_id AS id,category_name AS name FROM category_table WHERE category_id=parent_id")
    rows = cur_pointer.fetchall()
    cat = []
    for row in rows:
        cat.append(row[1])
    text = "Available categories are " + "<li>" + "<li>".join(cat)
    eel.left_printer(text)
    speak("U can view the available categories on the screen")
    return printer(cur_pointer,1)

def parent_category_speak(cur):
    z=[]
    cur.execute("SELECT category_id AS id,category_name AS name FROM category_table WHERE category_id=parent_id")
    rows = cur.fetchall()

    for row in rows:
        z.append(row[1])

    text = 'Available categories are ' + " ".join(z[:-1]) + 'and' + z[-1]
    speak(text)

def child_category_selector(cur_pointer,p_id):

    query = str("SELECT category_id, category_name FROM category_table WHERE parent_id IN (SELECT parent_id FROM category_table WHERE category_name ='" + str(p_id)+"') AND parent_id!=category_id")
    cur_pointer.execute(query)
    rows = cur_pointer.fetchall()
    sub_cat = []
    for row in rows:
        sub_cat.append(row[1])
    text = 'Available subcategories are ' + "<li>" + "<li>".join(sub_cat)
    eel.left_printer(text)
    speak("Please check your screen for the Available sub-categories")
    printer(cur_pointer,2)

def child_category_speak(cur,p_id):
    z=[]
    query = str("SELECT category_id, category_name FROM category_table WHERE parent_id IN (SELECT parent_id FROM category_table WHERE category_name ='" + str(p_id)+"') AND parent_id!=category_id")
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows :
        z.append(row[1])
    text = "Available categories under "+ p_id  +" are " + ", ".join(z[:-1]) + " and " + z[-1]
    speak(text)


def item_selector(cur_pointer,p_id):

    query = "SELECT * FROM items WHERE category_id IN (SELECT category_id FROM category_table WHERE category_name ='"  + p_id + "')"
    cur_pointer.execute(query)
    rows = cur_pointer.fetchall()
    # print('Item  |\t\n id  |\t','Item name',"\t|")
    # print("--------------------------")
    items = []
    for row in rows :
        items.append(row[2])
    text = "Avaiailable items under " + p_id + " are " + "<li>" + "<li>".join(items)
    eel.left_printer(text)
    speak("Please choose from the items mentioned on the screen")
    return(rows)
    #printer(cur_pointer,3)

def item_speaker(cur,p_id):
    query = "SELECT * FROM items WHERE category_id IN (SELECT category_id FROM category_table WHERE category_name ='"  + p_id + "')"
    cur.execute(query)
    rows = cur.fetchall()
    items = []
    for row in rows :
        items.append(row[2])
    text = "Availaible items are " + " ".join(items[:-1]) + "and" + items[-1]
    speak(text)

def item_printer(cur_pointer):
    query = "SELECT * FROM items ORDER BY item_id"
    x = []
    #select invoice_id from invoice order by invoice_id desc limit 1
    cur_pointer.execute(query)
    rows = cur_pointer.fetchall()

    # for row in rows:
    #     x.append(row[2])

    # x = "<li>" + "<li>".join(x)
    # return x
    print('Item |\t\n id  |\t','Item name',"\t|")
    print("--------------------------")
    for row in rows :
        print(row[0],'   |',row[2],"\t|")
    return rows


def stopword_remover(text):
    req = []
    stop_words = ['i','want','to','order','and','some','would','like','go','visit','view']
    text = text.lower()
    text = word_tokenize(text)
    for word in text:
        if word not in stop_words:
            req.append(word)
    return req

def db_searcher(att,cur_pointer,quantt):

    x = ''
    y = []
    print("att  ")
    for i in range(len(att)):
        if i==0:
            x+= "'%" + att[i] + "%'"

        else:
            x += " and item_attributes LIKE '%" + att[i] + "%'"
    print( "x ---"+x)
    query = "SELECT * FROM items WHERE item_attributes LIKE " + x
    print(query)
    cur_pointer.execute(query)
    rows = cur_pointer.fetchall()
    for row in rows :
        #y.append(row[0])
        y.append([row[0],row[2],row[3],quantt,row[3]*quantt,row[5]])
        print(y)
    return y
    #r =
    printer(cur_pointer,3,quantt)

    #return r

def combiner(curr_pointer,inpp,inpp2,inpp3,quantity):
    parent_category_selector(curr_pointer)
    child_category_selector(curr_pointer,inpp)
    item_selector(curr_pointer,inpp2)
    return db_searcher(stopword_remover(inpp3),cur,quantity)

# def get_stock(cur,item_id):
#     query = "SELECT * FROM stocks_table WHERE item_id = " + item_id
#     cur.execute(query)
#     rows = cur.fetchall()
#     return rows

def stock_update(conn,cur,records_to_update):

    sql_update_query = """UPDATE items SET stock = stock - %s WHERE item_id = %s"""

    cur.executemany(sql_update_query, records_to_update)
    conn.commit()
    print(cur.rowcount, "Record updated successfully into stock")

def invoice_generator(cur,user_buy,conn):
    query = "SELECT nextval('invoice_seq')"
    cur.execute(query)
    rows = cur.fetchall()
    x = rows[0][0]
    records_to_update = []
    sql_update_query = """UPDATE stocks_table SET quantity = %s WHERE item_id = %s"""

    for i in range(len(user_buy)):
        joiner = str(user_buy[i][0][2]) + ", " + str(user_buy[i][0][3]) + ", " + str(user_buy[i][0][4])
        record_to_insert = str(x) + ", " + str(user_buy[i][0][0]) + ", '" + user_buy[i][0][1] + "', " + joiner

        query = "INSERT INTO invoice (invoice_id, item_id, item_name, coster, quantity, overall) \
                VALUES (" + record_to_insert + ")"

        records_to_update.append((user_buy[i][0][3],user_buy[i][0][0]))

        cur.execute(query);

    stock_update(conn,cur,records_to_update)
    conn.commit()
    eel.removevoicedots()
    print("All Successful...")


#result = cur.executemany(sql_update_query, records_to_update)
def invoice_printer(cur_pointer):

    cur_pointer.execute("SELECT invoice_id, item_name, coster, quantity, overall FROM invoice WHERE invoice_id = (SELECT invoice_id FROM invoice ORDER BY invoice_id DESC LIMIT 1)")
    return printer(cur_pointer,1)

@eel.expose
def bill_amount():
    conn,cur = db_connect()
    cur.execute("SELECT SUM(overall) FROM invoice WHERE invoice_id = (SELECT invoice_id FROM invoice ORDER BY invoice_id DESC LIMIT 1)")
    return printer(cur,0)


def known_item_voice(cur):
    inp1='yes'
    user_buy = []
    while(inp1 == 'yes'):
        #inp1 = 'britannia milk bread'
        inp1 = myCommand("Item name")
        inp1 = word_tokenize(inp1)

        #quantt = 6
        quantt = myCommand("Item quant")
        quantt = word_to_num(quantt)
        print("inpl1 ---"+inp1+ "    curr   "+cur+ "    quant   "+quantt)
        user_buy.append(db_searcher(inp1,cur,quantt))
        print(user_buy)
        speak("Anything else ?")
        #inp1 = input("Enter yes/no")
        inp1 = myCommand("Yes/no")
    return user_buy

def known_item(conn,cur,inp0='yes'):

    speak("Please check the screen to view all the items")
    x = "Available items are : \n" + item_printer(cur)
    eel.left_printer(x)

    user_buy = []

    while(inp0=='yes'):

        #inp1 = 'i want britannia milk bread'
        inp1 = myCommand("Item name")
        eel.right_printer(inp1.capitalize())
        inp1 = stopword_remover(inp1)

        speak("How much ?")
        eel.left_printer("How much ?")
        #quant = 6
        quant = myCommand("How much")
        eel.right_printer(quant)
        quant = word_to_num(quant)
        user_buy.append(db_searcher(inp1,cur,quant))

        speak("Would u like to add anything else ?")
        eel.left_printer("Would u like to add anything else ?")
        inp0 = myCommand("Anything else")
        #inp0 = inp_no
        #inp0 = input()

    invoice_generator(cur,user_buy,conn)

def unknown_item(conn,cur,inp0='yes'):

    user_buy = []
    print("unknown item")
    while(inp0=='yes'):
        parent_category_selector(cur)

        #inp1 = 'Bakery'
        inp1 = myCommand("Select a category")
        eel.right_printer(inp1)
        inp1=inp1.capitalize()
        child_category_selector(cur,inp1)

        #inp2 = 'Bread'
        inp2 = myCommand("Select a subcategory")
        inp2=inp2.capitalize()
        eel.right_printer(inp2)
        item_selector(cur,inp2)

        #inp3 = 'i want britannia milk bread'
        inp3 = myCommand("Item name")
        eel.right_printer(inp3.capitalize())
        inp3 = stopword_remover(inp3)
        eel.left_printer("How much")
        #quant = 1
        quant = myCommand("Enter quantity")
        eel.right_printer(quant)
        quant=word_to_num(quant)
        user_buy.append(db_searcher(inp3,cur,quant))

        speak("Would u like to add anything else ?")
        eel.left_printer("Would u like to add anything else ?")
        inp0 = myCommand("Anything else")
        #inp0 = inp_no
        #inp0 = input()

    invoice_generator(cur,user_buy,conn)


def unknown_item_voice(cur,conn):
    parent_category_speak(cur)

    #inp1 = 'Bakery'
    inp1 = myCommand("Which category")
    child_category_speak(cur,inp1)

    #inp1 = 'Bread'
    inp1 = myCommand("Which sub_category")
    item_speaker(cur,inp1)

    user_buy = known_item_voice(cur)
    invoice_generator(cur,user_buy,conn)

@eel.expose
def tryblock():
    inp_no = 'no'
    inp_yes = 'yes'
    conn,cur = db_connect()
    eel.left_printer("Do you know exactly what you want to buy?")
    speak("Do u know exactly what u want to buy ?")

    if runtype == 'test' :
        inp0 = inp_no
    else :
        inp0 = myCommand("Do u know exactly what u want to buy ?")

    eel.right_printer(inp0.capitalize())

    if inp0 == inp_yes:
        known_item(conn,cur)

    else :
        unknown_item(conn,cur)

def complete_voice(cur,conn,inp0):

    if inp0 == 'yes':
        user_buy = known_item_voice(cur)
        invoice_generator(cur,user_buy,conn)
    else :
        unknown_item_voice(cur,conn)

@eel.expose
def newPage():
    eel.start('index.html', size=(540, 960))


@eel.expose
def productReturns():
    inp_no = 'no'
    inp_yes = 'yes'
    conn,cur = db_connect()
    eel.left_printer("Thank you for contacting us about your defective product.")
    speak("Thank you for contacting us about your defective product")
    eel.left_printer("We are extremely sorry for the inconvenience.")
    speak("We are extremely sorry for the inconvenience.")
    eel.left_printer("What do you want to return?")
    speak("What do you want to return?")
    inp_user=myCommand("What do you want to return?")
    #inp_user="I did not like your pasta sauce"
    eel.right_printer(inp_user)
    query="SELECT row from customer_care order by row desc"
    cur.execute(query)
    rows = cur.fetchall()
    new_entry = rows[0][0]+1
    query = "INSERT INTO customer_care (cat_id,row,complain) \
             VALUES (1,"+str(new_entry)+",'"+inp_user+"')"
    cur.execute(query)
    conn.commit()
    eel.left_printer("Our sales team will get back to you as soon as possible ")
    speak("Our sales team will get back to you as soon as possible ")

@eel.expose
def billingIssues():
    inp_no = 'no'
    inp_yes = 'yes'
    conn,cur = db_connect()
    eel.left_printer("We are extremely sorry for the inconvenience.")
    speak("We are extremely sorry for the inconvenience")
    eel.left_printer("Please help us understand what issue you are facing:")
    speak("Please help us understand what issue you are facing:")
    eel.left_printer("1. Totaling issue")
    speak("1. Totaling issue")
    eel.left_printer("2. Unnecessary items added to list")
    speak("2. Unnecessary items added to list")
    eel.left_printer("3. None of these")
    speak("3. None of these")
    eel.left_printer("Please select an option from above")
    speak("Please select an option from above")
    inp_user=myCommand("Please select an option from above with the use of numbers corresponding to the option")
    eel.right_printer(inp_user)
    inp_user=word_to_num(inp_user)
    query="SELECT row from billing_issue order by row desc"
    cur.execute(query)
    rows = cur.fetchall()
    new_entry = rows[0][0]+1
    query = "INSERT INTO billing_issue (rand_id,row,issueoption) \
             VALUES (2,"+str(new_entry)+","+str(inp_user)+")"
    cur.execute(query)
    conn.commit()
    eel.left_printer("Our sales team will get back to you as soon as possible ")
    speak("Our sales team will get back to you as soon as possible ")

@eel.expose
def feedBack():
    conn,cur = db_connect()
    eel.left_printer("Out of 5 how would you rate us? Please use whole numbers.")
    speak("Out of 5 how would you rate us Please use whole numbers")
    inpl1=myCommand("Out of 5 how would you rate us Please use whole numbers")
    eel.right_printer(inpl1)
    eel.left_printer("Do you have any other improvements to mention?")
    speak("Do you have any improvements to mention")
    inpl2=myCommand("Do you have any other improvements to mention")
    eel.right_printer(inpl2)
    inpl1=word_to_num(inpl1)
    query="SELECT row from feedback order by row desc"
    cur.execute(query)
    rows = cur.fetchall()
    new_entry = rows[0][0]+1
    query = "INSERT INTO feedback (rand_id,row,starvalue,comments) \
             VALUES (2,"+str(new_entry)+","+str(inpl1)+",'"+inpl2+"')"
    print(query)
    cur.execute(query)
    conn.commit()

    eel.left_printer("Thankyou for taking your time to help us")
    speak("Thankyou for taking your time to help us")

def word_to_num(valer):
    a={'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'0':0}
    b=a[valer]
    return b

def word_tokenize(sent):
    z=sent.split(" ")
    return z
