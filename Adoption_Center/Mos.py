from flask import Flask, render_template, request, url_for, flash, redirect, session, escape, Markup
from forms import RegistrationForm, LoginForm, AddDogForm, EditDogForm, AddExpenseForm, addadoptionForm,AdoptionApplicationForm, appreviewform2
from flask_paginate import Pagination, get_page_args
from flask_mysqldb import MySQL
from wtforms import Form, StringField, validators, PasswordField, TextAreaField
from passlib.hash import sha256_crypt
import os
from datetime import date
import MySQLdb
import decimal
import email_validator

app = Flask(__name__)

#CSRF secret key to stop cross site request forgery
app.config['SECRET_KEY'] = 'e136d68bbc12329abd9a8ebe64d58d20'


#Mysql configs to enable DB connectivity 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'joanna'
app.config['MYSQL_DB'] = 'Dog_House'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

dbconn = MySQLdb.connect(host="localhost", user="root", passwd="joanna", db="Dog_House")
#route for root and home
#route for root and home
@app.route('/')
def mainpage():
	if  'username' in session:
		username = session['username']
		status2 = 'Logged in as: ' + username
		return redirect(url_for('dashboard'))
	else:
		return redirect(url_for('login' ))


#query to populate Breed list from DB
def filterDogs(filterval):
	doglistsqlf = "select d.DogID, d.DogName, d.DogSex, d.DogAlterStatus, d.Years, d.Months, d.AdoptStatus, d.SurrenderDate,  group_concat(b.BreedType separator '/') as Breed from Dog d left join Breed b on b.DogID = d.DogID WHERE d.AdoptStatus = " + str(filterval) + " group by d.DogID order by d.SurrenderDate;"
	curf = mysql.connection.cursor()
	curf.execute(doglistsqlf)
	global dogresultsf
	dogresultsf = curf.fetchall()
	return dogresultsf

def verifyforAdoption(dogid):
	doglistsqlva = "SELECT MicrochipID, DogAlterStatus From Dog where DogID = " + str(dogid)
	curva = mysql.connection.cursor()
	curva.execute(doglistsqlva)
	global validforadoption
	dogresultsva = curva.fetchone()
	print ('This is the dogresltsvs: ' + str(dogresultsva))
	if(dogresultsva['MicrochipID'] is None or dogresultsva['MicrochipID'] is 'NULL' or dogresultsva['MicrochipID'] is '' or dogresultsva['DogAlterStatus'] is 0):
		validforadoption = 0
	else:
		validforadoption = 1
	return validforadoption

#route for dashboard
#@app.route('/dashboard')
@app.route('/dashboard')
def dashboard():
	addbutton = '';dogresults='';
	if  'username' in session:
		username = session['username']
		status2 = 'Logged in as: ' + username
		cur = mysql.connection.cursor()
		cur2 = mysql.connection.cursor()
		cur3 = mysql.connection.cursor()
		dshsql = "SELECT count(dogID) FROM Dog WHERE DogID not in (Select dogid from Accepted)"
		cur.execute(dshsql)
		dataresults = cur.fetchall()
		dogtenancy = dataresults[0]['count(dogID)'] 
		status3 = "There are currently: " + str(dogtenancy) + " Dogs at Mos\'s" + Markup('<br><a href="/dashboard?action=filter1">Filter by available</a> / ') + Markup('<a href="/dashboard?action=filter0">Filter by adopted</a>')
		#Decide if to show the add dog button base on count being less than 15
		if (dataresults[0]['count(dogID)'] < 15):
			addbutton = Markup('<a href=addDog class=adddog_btn></a>')
		else:
			addbutton = ''
		doglistsql = "select d.DogID, d.DogName, d.DogSex, d.DogAlterStatus, d.Years, d.Months, d.AdoptStatus, d.SurrenderDate,  group_concat(b.BreedType separator '/') as Breed from Dog d left join Breed b on b.DogID = d.DogID group by d.DogID order by d.SurrenderDate asc;"
		cur2.execute(doglistsql)
		dogresults = cur2.fetchall()
		if request.args.get('action') == 'filter1':
			filterDogs(0)
			return render_template('dashboard.html', status=addbutton, dresults=dogresultsf, status2=status2, status3=status3)
		elif request.args.get('action') == 'filter0':
			filterDogs(1)
			return render_template('dashboard.html', status=addbutton, dresults=dogresultsf, status2=status2, status3=status3)
	else:
		return redirect(url_for('login' ))
	return render_template('dashboard.html', status=addbutton, dresults=dogresults, status2=status2, status3=status3)


#route for report
@app.route('/report_menu')
def report_menu():
	if  'username' in session:
		username = session['username']
		status2 = 'Logged in as: ' + username
		return render_template('report_menu.html')
	else:
		return redirect(url_for('login' ))


#route for DogDetails
#TODO add details for query and populate template with editable items 07/06
@app.route('/DogDetails', methods = ['GET', 'POST'])
def DogDetails():
	if  'username' in session:
		username = session['username']
		form = EditDogForm()
		if request.method != 'POST':
			dogid = request.args.get('dogID')
			print ("DogID is populated " + str(dogid))

			#Expense retrieval
			curex = mysql.connection.cursor()
			sqlex = "SELECT ExpenseID,  DogID,  VendorID,  ExpenseDate,  ExpenseAmount,  ExpenseDescripton FROM Expense WHERE Expense.DogID=" + str(dogid)
			print("This is the SQL for expense: " + str(sqlex))
			curex.execute(sqlex)			
			expenseresults = curex.fetchall()

			#Dog Details
			cur = mysql.connection.cursor()
			form.DogBreed.choices = [];
			sql = "SELECT * from BreedTypeAppendix"
			cur.execute(sql)
			Breedresults = cur.fetchall()
			i=0; 
			for row in (Breedresults):
				Breedval = str(row['BreedList']); 
				i = i + 1;
				form.DogBreed.choices += [Breedval]
			cur2 = mysql.connection.cursor()
			dshsql = "SELECT count(dogID) FROM Dog WHERE DogId not in (SELECT DogID from Accepted)"
			cur.execute(dshsql)
			dataresults = cur.fetchall()
			dogtenancy = len(dataresults)
			#Decide if to show the add dog button base on count being less than 15
			if (dataresults[0]['count(dogID)'] < 15):
				global addbutton
				addbutton = Markup('<a href=addDog class=adddog_btn></a>')
			else:
				addbutton = ''
			doglistsql = "SELECT Dog.DogId, Dog.DogName, Dog.AdoptStatus, Dog.Dogsex, Dog.DogAlterStatus, Dog.SurrenderAnimalControl, Dog.SurrenderDate, Dog.SurrenderReason, Dog.DogDescription, Dog.Months, Dog.MicrochipID, Dog.UserEmail,GROUP_CONCAT(Breed.BreedType SEPARATOR '/') AS combinedBreed FROM Dog LEFT OUTER JOIN Breed ON Dog.DogID = Breed.DogID WHERE Dog.DogID =" + dogid + " ORDER by Dog.SurrenderDate asc;"
			cur2.execute(doglistsql)
			print("This is the doglist SQL: " + str(doglistsql)) 
			dogresults = cur2.fetchone()
			isadopted = dogresults['AdoptStatus']
			return render_template('DogDetails.html', status=addbutton, dresults=dogresults, eresults=expenseresults, form=form)
		if request.method == 'POST':
			global sqlupd
			sqlupd = "Update Dog SET "
			print("This is the count of form fields: " + str(len(request.form)))
			if len(request.form) > 2:
				f = request.form
				for key in f.keys():
					if key not in 'csrf_token' and key not in 'submit':
						for value in f.getlist(key):
							if key == 'MicrochipID' and value == '':
								sqlupd += str(key) + "=NULL ,"
							else:
								sqlupd += str(key) + "='" + str(value) + "', "
				sqlupd = sqlupd[:-2]
				sqlupd += " WHERE DogID =" + str(request.args.get('dogID'))
				if hasattr(request.form, 'DogBreed') and 'Bulldog' in (request.form['DogBreed']):
					sqlupd += " AND DogName !=Uga;"
				else:
					sqlupd += ";"
				curupd = dbconn.cursor()
				print("This is the update value " + str(sqlupd))
				curupd.execute(sqlupd)
				dbconn.commit()
				did = str(request.args.get('dogID'))
				return redirect(url_for('DogDetails', dogID = str(did)))
			else:
				did = str(request.args.get('dogID'))
				return redirect(url_for('DogDetails', dogID = str(did)))

	else:
		return redirect(url_for('login' ))
		

#route for Add Expense
#TODO add SQL insert and redirect
@app.route('/addExpense', methods = ['GET', 'POST'])
def addExpense():	
	if  'username' in session:
		dogid = request.args.get('dogID')
		username = session['username']
		form = AddExpenseForm()
		#run the functions to populate the Breedlist and present the form
		if request.method != 'POST':
			cur = mysql.connection.cursor()
			form.VendorName.choices = [];
			sql = "SELECT VendorID, VendorName from Vendor"
			cur.execute(sql)
			Vendorresults = cur.fetchall()
			i=0; 
			for row in (Vendorresults):
				VendorIDval = str(row['VendorID']); 
				Vendorval = str(row['VendorName']);
				formval = str(VendorIDval)  + ":" + str(Vendorval)
				i = i + 1;
				print ('This is VID: ' + str(VendorIDval) + 'This is VName: ' + str(Vendorval))
				form.VendorName.choices += [str(formval)]
			return render_template('addExpense.html', title='Add A New Expense', form=form, vendors=Vendorresults)
		else:
			dogID = request.args.get('dogID')			
			vid = (request.form['VendorName']).split(':')[0]
			today = date.today();d1 = today.strftime("%Y-%m-%d")
			expamt = request.form['ExpenseAmount']
			expdesc = request.form['ExpenseDescription']
			#SQL insert statements and input validation
			sqlexins = "INSERT INTO Expense(DogID, VendorID, ExpenseDate, ExpenseAmount, ExpenseDescripton) SELECT %s, %s, %s, %s, %s FROM (SELECT 1) t WHERE NOT EXISTS (SELECT ExpenseID FROM Expense WHERE DogId = %s AND VendorID = %s AND ExpenseDate = %s)"
			curexins = dbconn.cursor()
			curexins.execute(sqlexins,(str(dogID),str(vid),str(today),str(expamt), str(expdesc),str(dogid),str(vid),str(today)))
			dbconn.commit()
			return redirect(url_for('DogDetails', dogID = str(dogid)))
	else:
		return redirect(url_for('login' ))


#query to populate Breed list from DB
def getBreed():
	cur = mysql.connection.cursor()
	sql = "SELECT * from BreedTypeAppendix"
	cur.execute(sql)
	global Breedresults
	Breedresults = cur.fetchall()
	return Breedresults

#query to populate Breed list from DB
def setnewDogID():
	cur = mysql.connection.cursor()
	sql = "SELECT MAX(DogID) FROM Dog;"
	cur.execute(sql)
	global newDogID
	newDogID = cur.fetchone()
	return newDogID


#route for Add Dog
#TODO add SQL insert and redirect
@app.route('/addDog', methods = ['GET', 'POST'])
def addDog():		
	if  'username' in session:		
		username = session['username']
		form = AddDogForm()
		#run the functions to populate the Breedlist and present the form
		if request.method != 'POST':
			form.DogBreed.choices = [];
			getBreed()
			form.DogBreed.choices += ['unknown']
			form.DogBreed.choices += ['mixed']
			i=0; 
			for row in (Breedresults):
				Breedval = str(row['BreedList']); 
				i = i + 1;
				form.DogBreed.choices += [Breedval]
			return render_template('addDog.html', title='Add A New Dog', form=form)
		else:
			#Breed = request.form.getlist["DogBreed"]
			#SQL insert statements and input validation
			age =  (int(request.form["DogAgeYears"]) * 12) + int(request.form["DogAgeMonths"])
			Breeds = (request.form.getlist('DogBreed'))
			if ('unknown' in Breeds and 'mixed' not in Breeds):
				dogtype = 'unknown'
			elif ('mixed' in Breeds and 'unknown' not in Breeds ):
				dogtype = 'unknown'
			elif ('mixed' in Breeds and 'unknown' in Breeds ):
				status = 'You CANNOT select both unknown and mixed as Breed selections'
				getBreed()
				form.DogBreed.choices += ['unknown']
				form.DogBreed.choices += ['mixed']
				i=0; 
				for row in (Breedresults):
					Breedval = str(row['BreedList']); 
					i = i + 1;
					form.DogBreed.choices += [Breedval]
				return render_template('addDog.html', title='Add A New Dog', status=status, form=form, Breeds=form)
			setnewDogID()
			nextDogID = (newDogID['MAX(DogID)'] + 1);
			print (str(nextDogID))
			mchipval = str(request.form['MicrochipID'])
			print("This is the mchip val: " + str(mchipval))
			if (mchipval == '') :
				mchip = 'NULL';
			else:
				mchip = "'" + str(mchipval) + "'"
			today = date.today();d1 = today.strftime("%Y-%m-%d")
			cur0 = dbconn.cursor()
			sqlins = "INSERT INTO Dog (DogID, UserEmail, MicrochipID, DogName, DogAlterStatus, Months, DogSex, SurrenderAnimalControl, SurrenderReason, SurrenderDate, DogDescription, AdoptStatus) VALUES (%s,%s," + str(mchip) + ",%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			cur0.execute(sqlins,(str(nextDogID),str(username),str(request.form.get('DogName')),str(request.form.get('DogAlterStatus')),str(age),str(request.form.get('DogSex')),str(request.form.get('SurrenderAnimalControl')),str(request.form.get('SurrenderReason')),str(d1),str(request.form.get('DogDescription')),0))
			curins1 = mysql.connection.cursor()
			dshsql = "SELECT count(dogID) FROM Dog WHERE DogID not in (Select dogid from Accepted)"
			curins1 .execute(dshsql)
			dataresultsins1 = curins1.fetchall()
			if (request.form.get('DogName') == 'Uga' and request.form['DogBreed'] == 'Bulldog' and len(Breeds) == 1):
				dbconn.rollback()
				fail = "Dog Addition failed please check input values"
				return render_template('addDogComplete.html', title='Dog Addition Failed', dogidval=nextDogID, fail=fail)
			else:
				if (dataresultsins1[0]['count(dogID)'] > 14):
					dbconn.rollback()
					fail2 = "Dog House at capacity!!!"
					return render_template('addDogComplete.html', title='Dog Addition Failed', dogidval=nextDogID, fail=fail2)
				else:
					dbconn.commit()
					for bchoice in (Breeds):
						cur2 = dbconn.cursor()
						sqlstatement2 = "INSERT INTO Breed (DogID, BreedType) VALUES(%s,%s)"
						cur2.execute(sqlstatement2,(str(nextDogID),str(bchoice)))
						dbconn.commit()
						dataresults2 = cur2.fetchall()
				return render_template('addDogComplete.html', title='Dog Addition Complete', dogidval=nextDogID)
	else:
		return redirect(url_for('login' ))


#route for login - checks the DB using Wenjiao's query to validate user and execute login
#Will update index to show dashboard once logged n
@app.route('/login', methods = ['GET', 'POST'])
def login():
	form = LoginForm()
	if request.method == 'POST':
		uid = request.form["email"]	
		pwd = request.form["password"]
		cur = mysql.connection.cursor()
		#had to concatenate the strings to get this working - someone who knows python better can clean this up.
		sql = "SELECT UserEmail, Passwrd FROM UserInfo WHERE UserEmail='" + str(uid) + "' AND Passwrd='" + str(pwd) + "'"
		cur.execute(sql)
		dataresults = cur.fetchall()
		#Validate form submission and that sql returns at least one row Since email is unique we should never get more than 1
		if form.validate_on_submit() and len(dataresults) > 0:
			flash('Logged in as: {form.email.data}!', 'success')
			session['username'] = str(uid);
			return redirect('dashboard')
		else:
			#redirect to login page if login unsuccessful
			flash('Login Unsuccessful. Please check credentials and try again', 'danger')
		return render_template('login.html', title='loginForm', form=form)	
	else:
		return render_template('login.html', title='loginForm', form=form)


    
    

@app.route('/Animal_con')
def Animal_con():
    tables={}
    cur = mysql.connection.cursor()
    show='''SELECT COUNT(DogID) AS tot, EXTRACT(YEAR_MONTH FROM SurrenderDate) AS month FROM Dog 
    WHERE SurrenderAnimalControl = 1 AND 
    SurrenderDate BETWEEN DATE_SUB(NOW(), INTERVAL 6 MONTH) AND NOW() 
    GROUP BY month'''
    tb=cur.execute(show)
    dat=cur.fetchall()
    if tb > 0:
        tables['tb'] = dat 
    cur.close()
    
    
    cur1=mysql.connection.cursor()
    show1='''SELECT COUNT(Dog.DogID) AS tot, Dog.DogID, DogSex, DogAlterStatus, MicrochipID,
    EXTRACT(YEAR_MONTH FROM SurrenderDate) AS month,SurrenderDate, GROUP_CONCAT(BreedType) AS Breed FROM Dog
    JOIN Breed ON Dog.DogID=Breed.DogID
    WHERE SurrenderAnimalControl=1 AND
    SurrenderDate BETWEEN DATE_SUB(NOW(), INTERVAL 6 MONTH) AND NOW()
    GROUP BY MONTH(DATE(SurrenderDate)), Dog.DogID
    ORDER BY Dog.DogID ASC;'''
    result=cur1.execute(show1)
    result1=cur1.fetchall()
    if result > 0:
        tables['tb1']=result1
    else:
        flash('No result Found for Surrendered Dog')
    
    cur1.close()
    
    cur2=mysql.connection.cursor()
    show2='''SELECT COUNT(Dog.DogID) AS tot, EXTRACT(YEAR_MONTH FROM AdoptionDate) AS month FROM Dog
    JOIN Adoption ON Adoption.DogID=Dog.DogID
    WHERE SurrenderAnimalControl=1 AND
    AdoptionDate BETWEEN DATE_SUB(NOW(), INTERVAL 6 MONTH) AND NOW()
    AND DATEDIFF(AdoptionDate, SurrenderDate) > 60
    GROUP BY Dog.DogID,month;'''
    
    tb2=cur2.execute(show2)
    result2=cur2.fetchall()
    if tb2 > 0:
        tables['tb2']=result2
    
    cur2.close()
    
    show3='''SELECT Dog.DogID, DogSex, DogAlterStatus, MicrochipID, SurrenderDate,
    EXTRACT(YEAR_MONTH FROM AdoptionDate) AS month, DATEDIFF(AdoptionDate, SurrenderDate) AS
    num_days , Breed FROM Dog
    JOIN
    (SELECT DogID, GROUP_CONCAT(BreedType) AS Breed FROM Breed
    GROUP BY DogID) j ON Dog.DogID=j.DogID
    JOIN Adoption ON Adoption.DogID=Dog.DogID
    WHERE DATEDIFF(AdoptionDate, SurrenderDate) > 60 AND 
    SurrenderAnimalControl=1 AND 
    AdoptionDate BETWEEN DATE_SUB(NOW(), INTERVAL 6 MONTH) AND NOW()
    ORDER BY month,num_days ASC, Dog.DogID DESC;'''
    
    cur3=mysql.connection.cursor()
    tb2_2=cur3.execute(show3)
    result3=cur3.fetchall()
    if tb2_2 > 0:
        tables['tb3']=result3
    
    cur3.close()
    
    show4='''SELECT SUM(ExpenseAmount) AS tot, EXTRACT(YEAR_MONTH FROM AdoptionDate) AS month, Expense.DogID FROM     Expense
    JOIN Dog ON Expense.DogID=Dog.DogID
    JOIN Adoption a ON a.DogID=Dog.DogID
    WHERE SurrenderAnimalControl=1 AND
    AdoptionDate BETWEEN DATE_SUB(NOW(), INTERVAL 6 MONTH) AND NOW()
    GROUP BY month, Expense.DogID;'''
    
    cur4 = mysql.connection.cursor()
    tb3 = cur4.execute(show4)
    get_result=cur4.fetchall()
    
    if tb3 > 0:
        tables['tb4']=get_result
  
    cur4.close()
    return render_template('Animal_con.html', tables=tables)
    

@app.route('/Monthly_ado')
def Monthly_ado():
    cur1=mysql.connection.cursor()
    show1='''SELECT COUNT(d.DogID) AS tot, BreedType, EXTRACT(YEAR_MONTH FROM AdoptionDate) AS month FROM Dog d
    JOIN Breed b ON d.DogID=b.DogID
    JOIN Adoption a ON d.DogID=a.DogID
    WHERE a.AdoptionDate BETWEEN DATE_SUB(NOW(), INTERVAL 1 YEAR) AND NOW()
    GROUP BY month,BreedType
    ORDER BY month DESC;'''
    col_da1=cur1.execute(show1)
    result1=cur1.fetchall()
    tables={}
    if col_da1 > 0:
        tables['tb1']=result1
    cur1.close()
    
    cur2=mysql.connection.cursor()
    show2='''SELECT BreedType, EXTRACT(YEAR_MONTH FROM SurrenderDate) AS month, COUNT(d.DogID) AS tot FROM Dog d
    JOIN Breed b ON d.DogID=b.DogID
    WHERE SurrenderDate BETWEEN DATE_SUB(NOW(), INTERVAL 1 YEAR) AND NOW()
    GROUP BY month, BreedType
    ORDER BY month DESC;'''
    col_da2=cur2.execute(show2)
    result2=cur2.fetchall()
    if col_da2 > 0:
        tables['tb2']=result2
    cur2.close()
    
    
    cur3=mysql.connection.cursor()
    show3='''SELECT SUM(ExpenseAmount) AS total_expense, SUM(AdoptionFee) AS total_fee, SUM(profit) AS     net_profit, 
    EXTRACT(YEAR_MONTH FROM ExpenseDate) AS month, b.BreedType FROM
    (SELECT e.DogID, ExpenseAmount, COALESCE(AdoptionFee, 0) AS AdoptionFee, ExpenseDate,
    CASE SurrenderAnimalControl 
    WHEN 1 THEN COALESCE(AdoptionFee, 0) 
    WHEN 0 THEN (COALESCE(AdoptionFee, 0) - ExpenseAmount) 
    END profit FROM Expense e 
    LEFT JOIN Adoption a ON e.DogID=a.DogID 
    JOIN Dog d ON d.DogID=e.DogID
    WHERE e.ExpenseDate BETWEEN DATE_SUB(NOW(), INTERVAL 1 YEAR) AND NOW()) AS s
    JOIN Breed b ON s.DogID=b.DogID
    GROUP BY month, b.BreedType
    ORDER BY month DESC;'''
    col_da3=cur3.execute(show3)
    result3=cur3.fetchall()
    if col_da3 > 0:
        tables['tb3']=result3
    cur3.close()
    return render_template('Monthly_ado.html', tables=tables)


@app.route('/Expense_ans')
def Expense_ans():
    cur1=mysql.connection.cursor()
    show1='''SELECT VendorID, VendorName FROM Vendor;'''
    col_da1=cur1.execute(show1)
    result1=cur1.fetchall()
    tables={}
    if col_da1 > 0:
        tables['tb1']=result1
    cur1.close()
    
    
    cur2=mysql.connection.cursor()
    show2='''SELECT VendorID, SUM(ExpenseAmount) AS tot FROM Expense
    GROUP BY VendorID
    ORDER BY tot DESC;'''
    col_da2=cur2.execute(show2)
    result2=cur2.fetchall()
    if col_da2 > 0:
        tables['tb2']=result2
    cur2.close()
    return render_template('Expense_ans.html', tables=tables)

@app.route('/Volunteer_lo', methods=['GET', 'POST'])
def Volunteer_lo():
    if request.method == 'POST':
        # Get input string
        inputstr = request.form['inputstr']
        search="%" + inputstr + "%"
        cur = mysql.connection.cursor()
        result = cur.execute('''SELECT UserEmail, PhoneNumber, FirstName, LastName FROM UserInfo
        WHERE FirstName LIKE %s OR LastName LIKE %s
        ORDER BY LastName ASC;''', (search, search))
        
        if result > 0:
            data = cur.fetchall()
            return render_template('Volunteer_lo.html', tables=data)
        else:
            flash('No Users Found')
            return render_template('Volunteer_lo.html')
        cur.close()
    return render_template('Volunteer_lo.html')


#Fee calculation 
def calculatefee(dogid,acstat):
	cur = mysql.connection.cursor()
	sql = "select sum(ExpenseAmount) as exptotal from expense where dogid=" + str(dogid)
	cur.execute(sql)
	bills = cur.fetchone()
	global expensetot
	expensetotal = bills['exptotal']
	if expensetotal == None:
		expensetotal = 0
	print('This is where we caught expense Total: ' + str(expensetotal))
	if acstat == 0:
		expensetot = float(expensetotal) * float(1.15)
	if acstat == 1:
		expensetot = float(expensetotal) * float(1.15)
	return round(expensetot,2)

#####Abus inserts 
#Add Adoption Part
#####Abus inserts 
#Add Adoption Part
@app.route('/addadoption', methods=['GET', 'POST'])
def addadoption():
	if  'username' in session:		
		username = session['username']
		if request.method != 'POST':
			curadmin = mysql.connection.cursor()
			sql = "Select AdminEmail from Admin where AdminEmail = '" + str(username) + "'"
			curadmin.execute(sql)
			IsAdmin = curadmin.fetchone()
			if IsAdmin != None:
				status2 = 'Logged in as: ' + username
				form = addadoptionForm()
				dogid = request.args.get('dogID')
				verifyforAdoption(dogid)
				if validforadoption == 0:
					messageval = "True"
					return redirect(url_for('DogDetails', dogID=dogid, msgval=messageval))
				else:
						#Add logic to ensure microchip and altered status are updated
						return render_template('addadoption.html', form=form)
			else:
				retstat = "You're not allowed to add adoptionns, you need Admin permissions - Please check with Mo"
				return render_template('addadoption.html', retstat=retstat)

		if request.method == 'POST':
			form = addadoptionForm()
			dogid = request.form['dogID']
			adlastname = "%" + request.form['AdopterLname'] + "%"
			colastname = "%" + request.form['co_lname'] + "%"
			cur = mysql.connection.cursor()
			sql = "Select Adopter.AdopterLName, AdoptionApplication.Co_Lname, AdoptionApplication.ApplicationNumber,Adopter.AdopterEmail,Adopter.AdPhoneNumber From Adopter NATURAL JOIN AdoptionApplication Where AdoptionApplication.ApplicationNumber not in(Select ApplicationNumber from Accepted) AND (Adopter.AdopterLName like %s OR AdoptionApplication.Co_Lname like %s)"
			cur.execute(sql,(adlastname,colastname))
			result = cur.fetchall()   
			if len(result) < 1:
				return "Back to Dog Details"
			else:
				return render_template("test.html",a = adlastname,co=colastname,r=result, form=form, dogid=dogid)
	else:
		return redirect(url_for('login' ))

@app.route('/adoptionfee',methods=['GET','POST'])
def fee():
    if request.method != 'POST':
        cur = mysql.connection.cursor()
        cur2 = mysql.connection.cursor()
        dogid = request.args.get('dogid')
        appid = request.args.get('appid')
        sql = "Select SurrenderAnimalControl from Dog where DogID =" + str(dogid)
        cur2.execute(sql)
        acstat = cur2.fetchone()
        acstat2 = acstat['SurrenderAnimalControl']
        calculatefee(dogid,acstat2)
        today = date.today();AppDate = date.today();d1 = today.strftime("%Y-%m-%d")    
        result = cur.execute("Select AdoptionApplication.ApplicationNumber,AdoptionApplication.AdopterEmail,AdoptionApplication.ApplicationDate, Adoption.AdoptionFee From AdoptionApplication natural join Adoption Where AdoptionApplication.ApplicationNumber = Adoption.ApplicationNumber Order by AdoptionApplication.ApplicationDate DESC")
        vendors = cur.fetchone()
        return render_template('fee.html', Details=vendors, dogid=dogid,date=d1, appid=appid, acstat=acstat, exptot=round(expensetot,3))

    if request.method == 'POST':
        DogID = request.form['DogID']
        AdoptionDate = request.form['AdoptionDate']
        AdoptionFee = request.form['AdoptionFee']
        AdopterEmail = request.form['Aemail']
        ApplicationNumber = request.form['ApplicationNumber']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Adoption VALUES(%s,%s,%s,%s,%s)",(int(DogID),int(ApplicationNumber),str(AdopterEmail),str(AdoptionDate),str(AdoptionFee)))
        mysql.connection.commit()
        curadopt = dbconn.cursor()
        curadopt.execute("Update Dog set AdoptStatus = 1 where DogID =" + str(DogID))
        dbconn.commit()
        cur.close()
        return render_template("adoptioncomplete.html", dogidval=DogID)
    return render_template('fee.html')


#Add Adoption Application
@app.route('/adoptionapplication')
def adoptionapplication():
    cur = mysql.connection.cursor()
    cur.execute('Select * From Adopter AS ad Left Join AdoptionApplication AS aa ON ad.AdopterEmail = aa.AdopterEmail')
    appnumber = cur.fetchall()
    return render_template("adoptionapplication.html",appnumber=appnumber)


@app.route('/newapplication',methods=['GET','POST'])
def newapplication():
    form=AdoptionApplicationForm()
    if request.method == 'POST':
        #AppNumber has to auto increment
        today = date.today();AppDate = date.today();d1 = today.strftime("%Y-%m-%d")
        AdopterEmail = request.form['AdopterEmail']
        FirstName = request.form['AdopterFName']
        LastName = request.form['AdopterLName']
        Phone = request.form['AdPhoneNumber']
        Street = request.form['Street']
        City = request.form['City']
        State = request.form['State']
        Zip = request.form['Zip']
        CoFname = request.form['Co_Fname']
        CoLname = request.form['Co_Lname']
        cur = mysql.connection.cursor()
        cur2 = mysql.connection.cursor()
        cur2.execute("Insert Into Adopter Values(%s,%s,%s,%s,%s,%s,%s,%s)",(str(AdopterEmail),int(Phone),str(FirstName),str(LastName),str(Street),str(City),str(State),int(Zip)))
        cur.execute("Insert Into AdoptionApplication (AdopterEmail, ApplicationDate, Co_Fname, co_Lname) Values(%s,%s,%s,%s)",(str(AdopterEmail), str(AppDate), str(CoFname),str(CoLname)))
        mysql.connection.commit()
        cur.close()
        cur2.close()
        cur3 = mysql.connection.cursor()
        cur3.execute("Select ApplicationNumber From AdoptionApplication Where AdopterEmail ='" + str(AdopterEmail) + "' ")
        appnumber = cur3.fetchall()
        return render_template("applicationnumber.html",appnumber=appnumber)    

    return render_template('newapplication.html', form=form)


@app.route('/contactinfo',methods=['GET','POST'])
def contactinfo():
    if request.method == 'POST':
        Phone = request.form['AdPhoneNumber']
        Street = request.form['Street']
        City = request.form['City']
        State = request.form['State']
        Zip = request.form['Zip']
        CoFname = request.form['Co_Fname']
        CoLname = request.form['Co_Lname']
        cur = mysql.connection.cursor()
        cur2 = mysql.connection.cursor()
        #sqlnewapplication2 = "Insert Into Adopter Values(AdopterEmail,Phone,FirstName,LastName,Street,City,State,Zip)"
        cur.execute("Update AdoptionApplication Set Co_Fname = %s, Co_Lname = %s Where ApplicationNumber = %s",(str(CoFname),str(CoLname),request.form["AppNumber"]))
        #cur2.execute("Update Adopter Set CoLname = %s Where AdopterEmail = %s",(C))
        cur2.execute("Update Adopter Set AdPhoneNumber = '"+str(Phone) + "',Street = '" + str(Street) + "',City = '" + str(City) + "',State = '"+ str(State) + "',Zip = '" + str(Zip) + "' Where AdopterEmail = '" + str(request.form['AdopterEmail']) + "'")
        mysql.connection.commit()
        cur.close()
        #cur2.close()
        return "success"
    
    if request.method == "GET":
        appid = request.args.get('appid')
        useremail = request.args.get('useremail')
        cur = mysql.connection.cursor()
        cur.execute("Select * From Adopter Left Join AdoptionApplication ON Adopter.AdopterEmail = AdoptionApplication.AdopterEmail Where Adopter.AdopterEmail = '" + str(useremail) + "' AND AdoptionApplication.ApplicationNumber = " + str(appid))
        #print("Select * From Adopter Left Join AdoptionApplication ON Adopter.AdopterEmail = AdoptionApplication.AdopterEmail Where Adopter.AdopterEmail = '" + str(useremail) + "' AND AdoptionApplication.ApplicationNumber = " + int(appid) + ")
        appnumber = cur.fetchone()
        #return appnumber
        return render_template('contactinfo.html',appnumber=appnumber)

    return render_template('contactinfo.html')


#Adoption Application Review Part
@app.route('/applicationreview',methods=['GET','POST'])
def applicationreview():
		if  'username' in session:
			username = session['username']
			curadmin = mysql.connection.cursor()
			sql = "Select AdminEmail from Admin where AdminEmail = '" + str(username) + "'"
			curadmin.execute(sql)
			IsAdmin = curadmin.fetchone()
			if IsAdmin != None:
				status2 = 'Logged in as: ' + username
				form=appreviewform2()
				cur = mysql.connection.cursor()
				cur2 = dbconn.cursor()
				cur4 = mysql.connection.cursor()
				cur.execute("Select AdoptionApplication.ApplicationNumber,Adopter.AdopterFname,Adopter.AdopterLname,AdoptionApplication.Co_Lname,AdoptionApplication.Co_Fname,Adopter.AdopterEmail,Adopter.AdPhoneNumber From Adopter Natural Join AdoptionApplication Where AdoptionApplication.ApplicationNumber not in(Select ApplicationNumber from Accepted) AND AdoptionApplication.ApplicationNumber in (Select ApplicationNumber From Adoption)")
				result = cur.fetchall()

				if request.method != 'POST':
					cur3 = mysql.connection.cursor()
					doappwork = request.args.get('appID')
					if doappwork is not None:
						sqlqry2 = "SELECT DogID from Adoption where ApplicationNumber = " + str(doappwork)
						cur4.execute(sqlqry2)
						dogidresult = cur4.fetchone()
						dogid = dogidresult['DogID']
						cur3.execute("Select AdoptionApplication.ApplicationNumber,Adopter.AdopterFname,Adopter.AdopterLname,AdoptionApplication.Co_Lname,AdoptionApplication.Co_Fname,Adopter.AdopterEmail,Adopter.AdPhoneNumber From Adopter Natural Join AdoptionApplication Where AdoptionApplication.ApplicationNumber = " +  str(doappwork))
						appresult = cur3.fetchone()
						return render_template('completereview.html', Applications=appresult, form=form, dogid=dogid)


				if request.method == 'POST':
					DogID = request.form['dogidval'] #request.args.get('dogID') #coming from the previous part
					#appid = request.form['submit'].split(':')[1]
					#print("This is appid: " + str(appid))
					print("This is dogid: " + str(DogID))
					select = request.form['appreview']
					print("Value: " + str(select))
					if select == 'Accept':
						print("We are doing post")
						cur2.execute("Insert Into Accepted Values(%s,%s)",(str(request.form['currentapp']),str(DogID)))
						curadopt = dbconn.cursor()
						curadopt.execute("Update Dog set AdoptStatus = 1 where DogID =" + str(DogID))
						dbconn.commit()
						applicationstatus = "Application " + request.form['currentapp'] + ' has been Approved'
						return render_template('reviewcomplete.html',applicationstatus=applicationstatus)     
					if select == 'Reject':
						#return request.form['currentapp']
						appid = request.form['currentapp']
						cur2.execute("Insert into Rejected (ApplicationNumber) VALUES (" + (str(appid) ) + ")")
						dbconn.commit()
						curadopt = dbconn.cursor()
						curadopt.execute("Update Dog set AdoptStatus = 0 where DogID =" + str(DogID))
						dbconn.commit()
						applicationstatus = "Application " + request.form['currentapp'] + ' has been Rejected'
						return render_template('reviewcomplete.html',applicationstatus=applicationstatus)
				return render_template('applicationreview.html',Applications=result, form=form)
			else:
				retstat = "You're not allowed to add adoptionns, you need Admin permissions - Please check with Mo"
				return render_template('addadoption.html', retstat=retstat)


		else:
			return redirect(url_for('login' ))

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)




