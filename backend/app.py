import json
from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.sqlite3'
app.config['SQLALCHEMY_BINDS'] = {
    'books': 'sqlite:///books.sqlite3',
    'customers': 'sqlite:///customers.sqlite3',
    'loans': 'sqlite:///loans.sqlite3'
}
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)
 
# model
class books(db.Model):
    __bind_key__ = 'books'
    id = db.Column('book_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    author = db.Column(db.String(50))
    year_published = db.Column(db.String(200))
    type = db.Column(db.String(10))
 
    def __init__(self, name, author, year_published,type):
        self.name = name
        self.author = author
        self.year_published = year_published
        self.type = type

class customers(db.Model):
    __bind_key__ = 'customers'
    id = db.Column('customer_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    age = db.Column(db.String(200))
 
    def __init__(self, name, city, age):
        self.name = name
        self.city = city
        self.age = age

class loans(db.Model):
    __bind_key__ = 'loans'
    id = db.Column('loan_id', db.Integer, primary_key = True)
    book_id = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    loan_date = db.Column(db.String(50))
    return_date = db.Column(db.String(50))
 
    def __init__(self, book_id, customer_id, loan_date,return_date):
        self.book_id = book_id
        self.customer_id = customer_id
        self.loan_date = loan_date
        self.return_date = return_date

#Default page
@app.route('/')
def welcome():
    return "Welcome to MyLibrary book loans interface"



@app.route('/books')
def show_all_books():
    res=[]
    for book in books.query.all():
        res.append({'id':book.id,'name':book.name,'author':book.author,'year_published':book.year_published,'type':book.type})
    return  (json.dumps(res))

@app.route('/customers')
def show_all_customers():
    res=[]
    for customer in customers.query.all():
        res.append({'id':customer.id,'name':customer.name,'city':customer.city,'age':customer.age})
    return  (json.dumps(res))
   
@app.route('/loans')
def show_all_loans():
    res=[]
    for loan in loans.query.all():
        res.append({'id':loan.id,'book_id':loan.book_id,'customer_id':loan.customer_id,'loan_date':loan.loan_date,'return_date':loan.return_date})
    return  (json.dumps(res))


#Methods for creating new items

@app.route('/books/new', methods = ['GET', 'POST'])
def new_book():
    request_data = request.get_json()
    print(request_data['name'],request_data['author'],request_data['year_published'],request_data['type'])
    name= request_data['name']
    author = request_data['author']
    year_published= request_data['year_published']
    type= request_data['type']
 
    newBooks= books(name,author,year_published,type)
    db.session.add (newBooks)
    db.session.commit()
    return "a new book record was create"
 
@app.route('/customers/new', methods = ['GET', 'POST'])
def new_customer():
    request_data = request.get_json()
    name= request_data['name']
    city = request_data['city']
    age= request_data['age']
 
    newCustomers= customers(name,city,age)
    db.session.add (newCustomers)
    db.session.commit()
    return "a new customer record was create"


@app.route('/loans/new', methods = ['GET', 'POST'])
def new_loan():
    request_data = request.get_json()
    book_id= request_data['book_id']
    customer_id = request_data['customer_id']
    loan_date= request_data['loan_date']
    return_date= request_data['return_date']
 
    newLoans= loans(book_id,customer_id,loan_date,return_date)
    db.session.add (newLoans)
    db.session.commit()
    return "a new loan record was create"
 
#Methods for deleting items

@app.route('/books/del/<id>', methods = ['DELETE'])
@app.route('/books/del/', methods = ['DELETE'])
def delete_book(id=-1):
    del_row = books.query.filter_by(id=id).first()
    if del_row:
        db.session.delete(del_row)
        db.session.commit()
        return "a row was delete"
    return "no such book...."    


@app.route('/customers/del/<id>', methods = ['DELETE'])
@app.route('/customers/del/', methods = ['DELETE'])
def delete_customer(id=-1):
    del_row = customers.query.filter_by(id=id).first()
    if del_row:
        db.session.delete(del_row)
        db.session.commit()
        return "a row was delete"
    return "no such customer...."   
   
@app.route('/loans/del/<id>', methods = ['DELETE'])
@app.route('/loans/del/', methods = ['DELETE'])
def delete_loan(id=-1):
    del_row = loans.query.filter_by(id=id).first()
    if del_row:
        db.session.delete(del_row)
        db.session.commit()
        return "a row was delete"
    return "no such customer...."   


#Methods for updating items

@app.route('/books/upd/<id>', methods = ['PUT'])
@app.route('/books/upd/', methods = ['PUT'])
def update_book(id=-1):
    request_data = request.get_json()
    upd_row = books.query.filter_by(id=id).first()
    if upd_row:
        upd_row.name =request_data['name']
        upd_row.author =request_data['author']
        upd_row.year_published =request_data['year_published']
        upd_row.type =request_data['type']
        db.session.commit()
        return "a row was update"
    return "no such book...."
   
@app.route('/customers/upd/<id>', methods = ['PUT'])
@app.route('/customers/upd/', methods = ['PUT'])
def update_customer(id=-1):
    request_data = request.get_json()
    upd_row = customers.query.filter_by(id=id).first()
    if upd_row:
        upd_row.name =request_data['name']
        upd_row.city =request_data['city']
        upd_row.age =request_data['age']
        db.session.commit()
        return "a row was update"
    return "no such book...."

@app.route('/loans/upd/<id>', methods = ['PUT'])
@app.route('/loans/upd/', methods = ['PUT'])
def update_loan(id=-1):
    request_data = request.get_json()
    upd_row = loans.query.filter_by(id=id).first()
    if upd_row:
        upd_row.book_id =request_data['book_id']
        upd_row.customer_id =request_data['customer_id']
        upd_row.loan_date =request_data['loan_date']
        upd_row.return_date =request_data['return_date']
        db.session.commit()
        return "a row was update"
    return "no such book...."

if __name__ == '__main__':
    with app.app_context():
        db.create_all(bind_key='books')
        db.create_all(bind_key='customers')
        db.create_all(bind_key='loans')
    app.run(debug=True)


