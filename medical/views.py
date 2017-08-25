from django.db import connection
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
import MySQLdb
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import datetime
from django.contrib import messages

from forms import *

Item_threshold = 10

# Create your views here.
def get_home_context(Username):
	is_Root = not is_Employee(Username)
 	print "is_Root: ",is_Root
 	context = {'is_Root':is_Root}
	if(is_Root):
		name = "root"
	else:
		name = get_emp_name(Username)
	context['username']=name
	context['store_det']=None
	try:
		c = connection.cursor()

		Store_ID=get_store_id(Username)
		sql = "select * from Store where Store_ID=%s"%Store_ID;
		print sql
		c.execute(sql)
		res=c.fetchone();
		context['store_det']=res
	except Exception,e:
		print repr(e)
	return context

def home(request):
	if(not request.user.is_authenticated()):
		messages.error(request, 'Please Log In First!!')
		return HttpResponseRedirect('/login/')
 	title   = "Home"

 	context = {"title":title}
 	Username=request.user.username
 	context2 = get_home_context(Username)
 	context['is_Root'] = context2['is_Root']
 	context['username'] = context2['username']
 	context['store_det'] = context2['store_det']

	return render(request,"home.html",context)

def get_emp_name(Emp_ID):
	
	try:
		c = connection.cursor()
		sql = "select Name from Employee where Emp_ID=%s"%Emp_ID;
		print sql
		c.execute(sql)
		res=c.fetchone();
		print res
		id=str(res[0]);
		return id
	except Exception,e:
		print repr(e)
		return "root user"


def get_prev_order():
	id=0
	try:
		c = connection.cursor()
		sql = "select max(Order_ID) from Orders";
		print sql
		c.execute(sql)
		res=c.fetchone();
		print res
		id=int(res[0]);
		return id
	except Exception,e:
		print repr(e)
		return id

def get_prev_demand():
	id=0
	try:
		c = connection.cursor()
		sql = "select max(Demand_ID) from Demand";
		print sql
		c.execute(sql)
		res=c.fetchone();
		print res
		id=int(res[0]);
		return id
	except Exception,e:
		print repr(e)
		return id

def get_store_id(emp_id):

	try:
 		c = connection.cursor()
 		sql = "Select Store_ID from Employee where Emp_ID=%s"%(emp_id);
 		print sql
 		c.execute(sql)
 		res = c.fetchone();
 		res = int(res[0])
 		return res
 	except Exception,e:
 		print repr(e)

def get_prev_cust():

	id=0
	try:
		c = connection.cursor()
		sql = "select max(Cust_ID) from Customer";
		print sql
		c.execute(sql)
		res=c.fetchone();
		id=int(res[0]);
		return id
	except Exception,e:
		print repr(e)
		return id

def get_cust_name(cust_id):

	try:
		c = connection.cursor()
		sql = "select Name from Customer where Cust_ID=%s"%cust_id;
		print sql
		c.execute(sql)
		res=c.fetchone();
		print res
		id=str(res[0]);
		return id
	except Exception,e:
		print repr(e)
		return "arpit"

def get_supp_name(supp_id):

	try:
		c = connection.cursor()
		sql = "select Name from Supplier where Supp_ID=%s"%supp_id;
		print sql
		c.execute(sql)
		res=c.fetchone();
		print res
		id=str(res[0]);
		return id
	except Exception,e:
		print repr(e)
		return "arpit"

def product(request,prod_id):
	if(not request.user.is_authenticated()):
		messages.error(request, 'Please Log In First!!')
		return HttpResponseRedirect('/login/')
	context={}
	Username=request.user.username
 	context2 = get_home_context(Username)
 	context['is_Root'] = context2['is_Root']
 	context['username'] = context2['username']
 	context['store_det'] = context2['store_det']
	try:

 		c = connection.cursor()
 		Store_ID = get_store_id(request.user.username)

 		sql = "select * from Items,Inventory where Items.Items_ID=Inventory.Items_ID and Store_ID=%s"%Store_ID;
 		c.execute(sql)
 		res_products = c.fetchall()
 		context["products"] = res_products
 		lst=[]
 		print context["products"]
 		for i in range(len(context["products"])):
 			l=list(context["products"][i])
 			l.append(u'0')
	 		lst.append(tuple(l))
	 	context["products"] = lst
	 	context['cart_total'] = 0
	 	print context["products"]
 	
 	except Exception,e:
 		print repr(e)
 	finally:
 		c.close()
 	template = "product.html"
 	title = "Products"
 	prod_cnt = 0
 	context["title"] = title
 	context['prod_cnt'] = prod_cnt;



 	return render(request,template,context)

def all_suppliers(request):

	if(not request.user.is_authenticated()):
		messages.error(request, 'Please Log In First!!')
		return HttpResponseRedirect('/login/')
	context={}
	Username=request.user.username
 	context2 = get_home_context(Username)
 	context['is_Root'] = context2['is_Root']
 	context['username'] = context2['username']
 	context['store_det'] = context2['store_det']
	try:
 		c = connection.cursor()

 		sql = "select * from Supplier,Supplier_Phone where Supplier.Supp_ID=Supplier_Phone.Supp_ID";
 		c.execute(sql)
 		res_products = c.fetchall()
 		context["suppliers"] = res_products
 		print res_products
 	
 	except Exception,e:
 		print repr(e)
 	finally:
 		c.close()
 	template = "all_suppliers.html"
 	title = "suppliers"
 	context["title"] = title

 	return render(request,template,context)

def add_cart(request,prod_id):
	if(not request.user.is_authenticated()):
		messages.error(request, 'Please Log In First!!')
		return HttpResponseRedirect('/login/')
	print "add_cart: "+str(prod_id)
	if request.method == "POST":
		form = AddCartForm(request.POST)
		if form.is_valid():
			context={}
			Username=request.user.username
		 	context2 = get_home_context(Username)
		 	context['is_Root'] = context2['is_Root']
		 	context['username'] = context2['username']
		 	context['store_det'] = context2['store_det']
			template = "product.html"
			title = "Products"
			context["title"] = title
			prod_qty =  int(form.cleaned_data['qty'])
			order_id = get_prev_order()+1;
			print "ORDER ID: ",order_id
			Store_ID = get_store_id(request.user.username)
			print  "prod: "+str(prod_id) + "qty: " +str(prod_qty)+"strore: "+str(Store_ID)
			c = connection.cursor()
			try:
				sql = "select * from Items,Inventory where Items.Items_ID=Inventory.Items_ID and Store_ID=%s"%Store_ID;
		 		c.execute(sql)
		 		res_products = c.fetchall()
		 		context["products"] = res_products
		 		prod_mx=0
		 		for i in range(len(res_products)):
		 			print int(res_products[i][0])
		 			if(int(res_products[i][0])==int(prod_id)):
		 				print "True"
		 				prod_mx = int(res_products[i][11])	
				try:
			 		c = connection.cursor()
			 		sql = "Select * from Order_Checkout where Items_ID=%s and Order_ID=%s"%(prod_id,order_id)
			 		print sql
			 		c.execute(sql)
			 		res = c.fetchall();

			 		prod_qty = min(prod_qty,prod_mx)
			 		prod_qty = max(prod_qty,0)
			 		if(len(res)!=0):
			 			if(prod_qty!=0):
				 			sql = "update Order_Checkout set Qty=%s where Items_ID=%s and Order_ID=%s"%(prod_qty,prod_id,order_id)
				 		else:
				 			sql = "delete from Order_Checkout where Items_ID=%s and Order_ID=%s"%(prod_id,order_id)
				 		print sql
				 		c.execute(sql)
				 	else:
				 		if(prod_qty!=0):
					 		sql = "Insert into Order_Checkout values(%s,%s,%s)"%(prod_id,order_id,prod_qty)
					 		print sql
					 		c.execute(sql)

			 	except Exception,e:
			 		print repr(e)
			 		
		 		sql = "select * from Order_Checkout where Order_ID = %s "%(order_id)
		 		print sql
		 		c.execute(sql)
		 		print 1
		 		res_products = c.fetchall()
		 		print res_products
		 		context["products_Order_Checkout"] = res_products
 				# sql = "select * from Items,Inventory where Items.Items_ID=Inventory.Items_ID and Store_ID=%s"%Store_ID;
		 		# c.execute(sql)
		 		# res_products = c.fetchall()
		 		# context["products"] = res_products

		 		inCart={}
		 		for i in range(len(context["products"])):
		 			id = int(context["products"][i][0])
		 			inCart[id]=0

		 		for i in range(len(context["products_Order_Checkout"])):
		 			id = int(context["products_Order_Checkout"][i][0])
		 			qt = int(context["products_Order_Checkout"][i][2])
		 			inCart[id]=qt

		 		lst=[]
		 		cart_amout=0
		 		for i in range(len(context["products"])):
		 			l=list(context["products"][i])
		 			if(inCart[context["products"][i][0]]):
		 				l.append(inCart[context["products"][i][0]])
		 			else:
		 				l.append(0)
			 		lst.append(tuple(l))
			 		cart_amout+=int(l[12])
			 	context["products"] = lst
			 	context['cart_total'] = cart_amout


		 	except Exception,e:
		 		print repr(e)
		 	finally:
		 		c.close()
			return render(request,template,context)


def add_product(request):
	if(not request.user.is_authenticated()):
		messages.error(request, 'Please Log In First!!')
		return HttpResponseRedirect('/login/')
	template = "product-add.html"
	context={}
	Username=request.user.username
 	context2 = get_home_context(Username)
 	context['is_Root'] = context2['is_Root']
 	context['username'] = context2['username']
 	context['store_det'] = context2['store_det']
	title = "ADD-Products"
	msg = ""
	context["title"] = title
	context['msg'] = msg;
	print "add_product"
	if(request.method=="POST"):
		print "post"
	
		Name = request.POST.get("productName")
		Description = request.POST.get("productDescription")
		ChemAmount = request.POST.get("ProductChemicalAmount")
		CostPrice = request.POST.get("ProductCostPrice")
		SellingPrice = request.POST.get("ProductSellingPrice")
		ExpiryDate = request.POST.get("ProductExpiryDate")
		Date_buy = request.POST.get("ProductDateBuy")
		isTaxable = request.POST.get("IsTaxable")
		msg=""
		try:
	 		c = connection.cursor()
	 		sql = "Insert into Items(Name,Description,ChemAmount,CostPrice,SellingPrice,ExpiryDate,Date_buy,isTaxable) values('%s','%s','%s',%s,%s,'%s','%s',%s)"%(Name,Description,ChemAmount,CostPrice,SellingPrice,ExpiryDate,Date_buy,isTaxable)
	 		print sql
	 		c.execute(sql)
	 		msg="Product added successfully"
	 	except Exception,e:
	 		print repr(e)
	 		msg="Error in adding this product please make changes"
	 	finally:
	 		c.close()
	 	if(Name==None):
	 		msg=""
	 	context['msg'] = msg;
	 	print "msg: "+str(msg)
		return render(request,template,context)
	return render(request,template,context)

def products_checkout(request):
	if(not request.user.is_authenticated()):
		messages.error(request, 'Please Log In First!!')
		return HttpResponseRedirect('/login/')
	template = "products_checkout.html"
	context={}
	Username=request.user.username
 	context2 = get_home_context(Username)
 	context['is_Root'] = context2['is_Root']
 	context['username'] = context2['username']
 	context['store_det'] = context2['store_det']
	title = "products-checkout"
	context["title"] = title

	try: 
		Order_ID = get_prev_order()+1;

		c = connection.cursor()
		sql = "select * from Items,Order_Checkout where Order_Checkout.Items_ID=Items.Items_ID and Order_Checkout.Order_ID=%s"%Order_ID
		print sql
		print Order_ID
		c.execute(sql)
		res = c.fetchall()
		print res
		new_res=[]
		sumtotal=0
		empty_cart=True
		for i in range(len(res)):
			rw = list(res[i])
			new_qt = int(rw[11]);
			if(new_qt>0):
				empty_cart=False
			sp = float(rw[5]);
			tp = sp*new_qt
			sumtotal+=tp
			print "tp: ",tp
			rw.append(tp)
			new_res.append(rw)
		print "Empty Cart ",empty_cart
		if(empty_cart):
			messages.error(request, 'Please Select Items Cart is Empty!!')
			return HttpResponseRedirect("/medical/products/0/")
		context["products"] = new_res
		context["sumtotal"] = sumtotal
		if(len(res)!=0):
			return render(request,template,context)
		else: 
			return HttpResponse("No Items in Cart") 

	except Exception,e:
		print repr(e)
		return HttpResponse("No Items in Cart")
	return HttpResponse("No Items in Cart")


def products_buy(request):
	if(not request.user.is_authenticated()):
		messages.error(request, 'Please Log In First!!')
		return HttpResponseRedirect('/login/')
	template = "bill.html"
	context={}
	Username=request.user.username
 	context2 = get_home_context(Username)
 	context['is_Root'] = context2['is_Root']
 	context['username'] = context2['username']
 	context['store_det'] = context2['store_det']
	title = "bill"
	context["title"] = title

	try: 
		Order_ID = get_prev_order()+1;
		Store_ID = get_store_id(request.user.username)
		Emp_ID = request.user.username

		c = connection.cursor()
		sql = "select Items.Items_ID,Order_Checkout.Qty ,Items.SellingPrice from Items,Order_Checkout where Order_Checkout.Items_ID=Items.Items_ID and Order_Checkout.Order_ID=%s"%Order_ID;
		c.execute(sql)
		res = c.fetchall()
		print res
		context["products"] = res
		subtotal=0
		tax=0
		dt = datetime.datetime.now()
		dy = str(dt.day)
		mn = str(dt.month)
		yr = str(dt.year)

		Date_created = yr+'-'+mn+'-'+dy
		Cust_Id = get_prev_cust();
		mp_tp=[]
		for i in range(len(res)):
			rw = list(res[i])
			new_qt = int(rw[1])
			item_id = int(rw[0])
			rw[0]=i+1
			sp = float(rw[2])
			tp = sp*new_qt
			rw.append(tp)
			mp_tp.append(tp)
			subtotal+=tp
			sql = "Update Inventory set Qty = Qty-%s where Store_ID=%s and Items_ID=%s"%(new_qt,Store_ID,item_id)
			print sql
			c.execute(sql)
	   
		sql = "Insert into Orders values(%s,%s,%s,'%s',%s,%s,%s)"%(Order_ID,tax,subtotal,Date_created,Cust_Id,Store_ID,Emp_ID)
		print sql
		c.execute(sql)
		sql = "Select * from Orders where Order_ID=%s"%(Order_ID)
		print sql
		c.execute(sql)
		res2 = c.fetchone()
		print res2

		rw = list(res2)
		cust_id = int(rw[4])
		rw[4] = get_cust_name(cust_id);
		res2=rw

		sql = "select * from Items,Order_Checkout where Order_Checkout.Items_ID=Items.Items_ID and Order_Checkout.Order_ID=%s"%Order_ID
		c.execute(sql)
		res = c.fetchall()
		tmp_res=[]
		for i in range(len(res)):
			rw = list(res[i])
			item_id = int(rw[0])
			rw[0]=i+1
			rw.append(mp_tp[i])
			print "rw: ",rw
			tmp_res.append(rw);
		context['products'] = tmp_res 
		context['order'] = res2
		return render(request,template,context)

	
	except Exception,e:
		print repr(e)
		return HttpResponse("Transaction Cancelled") 
	return HttpResponse("Transaction Cancelled") 

def customer_detail(request):
	if(not request.user.is_authenticated()):
		messages.error(request, 'Please Log In First!!')
		return HttpResponseRedirect('/login/')
	template = "custoner_detail.html"
	context={}
	Username=request.user.username
 	context2 = get_home_context(Username)
 	context['is_Root'] = context2['is_Root']
 	context['username'] = context2['username']
 	context['store_det'] = context2['store_det']
	title = "custoner-detail"
	context["title"] = title

	Order_ID = get_prev_order()+1;
	c = connection.cursor()
	sql = "select * from Items,Order_Checkout where Order_Checkout.Items_ID=Items.Items_ID and Order_Checkout.Order_ID=%s"%Order_ID
	print sql
	print Order_ID
	c.execute(sql)
	res = c.fetchall()
	print res
	empty_cart=True
	for i in range(len(res)):
		rw = list(res[i])
		new_qt = int(rw[11]);
		if(new_qt>0):
			empty_cart=False
	print "Empty Cart ",empty_cart
	if(empty_cart):
		messages.error(request, 'Please Select Items Cart is Empty!!')
		return HttpResponseRedirect("/medical/products/0/")

	print "custoner_detail"
	if(request.method=="POST"):
		print "post"
	
		Name = request.POST.get("CustomerName")
		Email = request.POST.get("CustomerEmail")
		Datecreated = request.POST.get("Datecreated")
		Phone = request.POST.get("Phone")
		if(Name=="" or Email=="" or Datecreated=="" or Phone==""):
			messages.error(request, 'Please fill all details!!')
			return HttpResponseRedirect("/medical/customer-details/")

		try:
	 		c = connection.cursor()
	 		sql = "Insert into Customer(Name,Email,Datecreated,DateLastTrans) values('%s','%s','%s','%s')"%(Name,Email,Datecreated,Datecreated)
	 		print sql
	 		c.execute(sql)
	 		Cust_ID = get_prev_cust();
	 		sql = "insert into Customer_Phone values(%s, '%s')" %(Cust_ID, Phone)
	 		print sql
	 		c.execute(sql)
	 	
	 	except Exception,e:
	 		print repr(e)
	 		return HttpResponse("Transaction Cancelled")
	 	finally:
	 		c.close()
		return HttpResponseRedirect("/medical/products-checkout/")
	return render(request,template,context)

	

def add_employee(request):

	if(not request.user.is_authenticated()):
		messages.error(request, 'Please Log In First!!')
		return HttpResponseRedirect('/login/')
	template = "employee-add.html"
	context={}
	Username=request.user.username
 	context2 = get_home_context(Username)
 	context['is_Root'] = context2['is_Root']
 	context['username'] = context2['username']
 	context['store_det'] = context2['store_det']
 	print context
	title = "ADD-Employee"
	msg=""
	context["title"] = title
	context['msg'] = msg;
	Username=request.user.username
 	is_Root = not is_Employee(Username)
 	print "is_Root: ",is_Root
 	context = {"is_Root":is_Root}
 	sql = "Select Store_ID from Store"
	print sql
	c = connection.cursor()
	c.execute(sql)
	res=c.fetchall()
	print res
	res2=[]
	for i in res:
		res2.append(int(i[0]))
 	context['stores'] = res2
	print "add_employee"
	if(request.method=="POST"):
		print "post"		

		Name = request.POST.get("EmployeeName","")
		Address = request.POST.get("EmployeeAddress","")
		Email = request.POST.get("EmployeeEmail","")
		PhoneNumber = request.POST.get("EmployeePhone","")
		Sex = request.POST.get("EmployeeSex","")
		Password = request.POST.get("EmployeePassword","")
		Date_Start = request.POST.get("EmployeeStartDate","")
		Date_End = "2018-10-10"
		Pay = request.POST.get("EmployeePay","")
		Store_ID = request.POST.get("EmployeeStoreID","")

		msg=""
		try:
			tmp = make_password(Password)
			print "pass: ",tmp
	 		c = connection.cursor()
	 		sql = "Insert into Employee(Name,Address,Email,Sex,Password,Date_Start,Date_End,Pay,Store_ID) values('%s','%s','%s','%s','%s','%s','%s',%s,%s)"%(Name,Address,Email,Sex,Password,Date_Start,Date_End,Pay,Store_ID)
	 		print sql
	 		c.execute(sql)
	 		print "done"
	 		sql = "Select Emp_ID from Employee where Name = '%s' and Password = '%s'"%(Name,Password);
	 		print sql
	 		c.execute(sql)
	 		print "done"
	 		res = c.fetchone()
	 		print res
	 		Emp_ID = int(res[0])
	 		print "Emp_Id: ",Emp_ID;
	 		context['Emp_ID'] = Emp_ID;
	 		context['Password'] = Password;
	 		sql = "insert into Employee_Phone values(%s, '%s')" %(Emp_ID, PhoneNumber)
	 		print sql
	 		c.execute(sql)
	 		print "done"
	 		msg="Employee added successfully"
	 		user = User.objects.create_user(Emp_ID, None, Password)
	 		pass_orig = user.password
	 		sql = "Update Employee set Password = '%s' where Emp_ID = %s and Password = '%s'"%(pass_orig,Emp_ID,Password);
	 		print sql
	 		c.execute(sql)
	 		print "done"

	 	except Exception,e:
	 		print repr(e)
	 		msg="Error in adding this Employee please check the details provided"

	 	finally:
	 		c.close()
	 	if(Name==None):
	 		msg=""
	 	context['msg'] = msg;
	 	print "msg: "+str(msg)
		return render(request,template,context)
	return render(request,template,context)

def is_Employee(Username):
	employee=False
	try:
		c = connection.cursor()
		c.execute('SELECT * FROM Employee WHERE Emp_ID = "%s"' %(Username))
		table = c.fetchall()
		if len(table) == 1:
			employee=True

	except Exception as e:
		print e
	finally:
		c.close()

	return employee


def notification_all(request):
	if(not request.user.is_authenticated()):
		messages.error(request, 'Please Log In First!!')
		return HttpResponseRedirect('/login/')
	# context_dict['slug'] = None
	template = 'notification.html'
	context = {}
	Username=request.user.username
 	context2 = get_home_context(Username)
 	context['is_Root'] = context2['is_Root']
 	context['username'] = context2['username']
 	context['store_det'] = context2['store_det']
	context['template'] = template
	try:
		c = connection.cursor()
		Store_ID=get_store_id(Username);
		sql = "Select Items.Items_ID,Items.Name,Inventory.Store_ID,Inventory.Qty from Items,Inventory where Items.Items_ID = Inventory.Items_ID and Inventory.Qty < %s and Inventory.Store_ID = %s"%(Item_threshold,Store_ID);
		print sql
		c.execute(sql)
		print "done"
		res = c.fetchall();
		context['notifications'] = res
	except Exception,e:
		print repr(e)
		msg="Error in adding this Employee please check the details provided"

	finally:
		c.close()	
 	return render(request,template,context)

def login_user(request):
	if(request.user.is_authenticated()):
		return HttpResponseRedirect('/medical/home/')
	if request.method == "POST":
		print "logging.."
		Username = request.POST.get('user')
		Password = request.POST.get('pass')


		user = authenticate(username = Username, password = Password)
		employee=is_Employee(Username);

		if user :
			login(request,user)
			is_Root = not employee
			context = {"is_Root":is_Root}
			return HttpResponseRedirect('/medical/home/')
		else:
			messages.error(request, 'Wrong Credentials Please Check for Username or Password!!')
			return HttpResponseRedirect('/login/')

	return HttpResponse(render(request, "login.html"))


def logout_user(request):
		logout(request)
		return HttpResponseRedirect('/login/')

def select_supplier(request):
	if(not request.user.is_authenticated()):
		messages.error(request, 'Please Log In First!!')
		return HttpResponseRedirect('/login/')
	context={}
	Username=request.user.username
 	context2 = get_home_context(Username)
 	context['is_Root'] = context2['is_Root']
 	context['username'] = context2['username']
 	context['store_det'] = context2['store_det']
	template = "select_supplier.html"
	title = "select-supplier"
	print title
	context["title"] = title
	sup=[]
	try:
		c = connection.cursor()
		sql = "Select Supp_ID from Supplier"
		print sql
		c.execute(sql)
		res = c.fetchall()

		for i in range(len(res)):
			sup.append(res[i][0])
	except Exception,e:
 		print repr(e)
 	finally:
 		c.close()
	context["suppliers"] = sup
	if request.method == "POST":
		try:
			print "POST.."
	 		c = connection.cursor()
	 		Store_ID = get_store_id(request.user.username)
	 		Supp_ID = request.POST.get("supplier")
	 		Time_Limit = request.POST.get("time_limit")
	 		Emp_ID = request.user.username
	 		Demand_ID = get_prev_demand()+1
	 		print "Demand_ID ",Demand_ID
	 		dt = datetime.datetime.now()
			dy = str(dt.day)
			mn = str(dt.month)
			yr = str(dt.year)
			Date_created = yr+'-'+mn+'-'+dy

	 		sql = "Insert into Demand values(%s,'%s',%s,%s,%s,%s)"%(Demand_ID,Date_created,Time_Limit,Emp_ID,Store_ID,Supp_ID)
			print sql
			c.execute(sql)

	 	
	 	except Exception,e:
	 		print repr(e)
	 	finally:
	 		c.close()
	 	return HttpResponseRedirect("/medical/demand-supply/")
	 		
	return render(request,template,context)

def demand_supply(request):
	if(not request.user.is_authenticated()):
		messages.error(request, 'Please Log In First!!')
		return HttpResponseRedirect('/login/')
	context={}
	Username=request.user.username
 	context2 = get_home_context(Username)
 	context['is_Root'] = context2['is_Root']
 	context['username'] = context2['username']
 	context['store_det'] = context2['store_det']
	try:

 		c = connection.cursor()
 		Store_ID = get_store_id(request.user.username)
 	
 		sql = "select * from Items";
 		c.execute(sql)
 		res_products = c.fetchall()
 		context["products"] = res_products
 		lst=[]
 		print context["products"]
 		for i in range(len(context["products"])):
 			l=list(context["products"][i])
 			l.append(u'0')
	 		lst.append(tuple(l))
	 	context["products"] = lst
	 	context['cart_total'] = 0

	 	print context["products"]

 	
 	except Exception,e:
 		print repr(e)
 	finally:
 		c.close()
 	template = "demand_supply.html"
 	title = "demand-supply"
 	prod_cnt = 0
 	context["title"] = title
 	context['prod_cnt'] = prod_cnt;

 	return render(request,template,context)


def add_demand_cart(request,prod_id):
	if(not request.user.is_authenticated()):
		messages.error(request, 'Please Log In First!!')
		return HttpResponseRedirect('/login/')
	print "add_demand_cart: "+str(prod_id)
	if request.method == "POST":
		form = AddCartForm(request.POST)
		if form.is_valid():
			context={}
			Username=request.user.username
		 	context2 = get_home_context(Username)
		 	context['is_Root'] = context2['is_Root']
		 	context['username'] = context2['username']
		 	context['store_det'] = context2['store_det']
			template = "demand_supply.html"
			title = "demand-supply"
			context["title"] = title
			prod_qty =  int(form.cleaned_data['qty'])
			demand_id = get_prev_demand();
			print "demand ID: ",demand_id
			Store_ID = get_store_id(request.user.username)
			print  "prod: "+str(prod_id) + "qty: " +str(prod_qty)+"strore: "+str(Store_ID)
			try:
				try:
			 		c = connection.cursor()
			 		sql = "Select * from Demand_Checkout where Items_ID=%s and Demand_ID=%s"%(prod_id,demand_id)
			 		print sql
			 		c.execute(sql)
			 		res = c.fetchall();
			 		prod_qty = max(prod_qty,0)

			 		if(len(res)!=0):
			 			if(prod_qty!=0):
				 			sql = "update Demand_Checkout set Qty=%s where Items_ID=%s and Demand_ID=%s"%(prod_qty,prod_id,demand_id)
				 		else:
				 			sql = "delete from Demand_Checkout where Items_ID=%s and Demand_ID=%s"%(prod_id,demand_id)
				 		print sql
				 		c.execute(sql)
				 	else:
				 		if(prod_qty!=0):
					 		sql = "Insert into Demand_Checkout values(%s,%s,%s)"%(demand_id,prod_id,prod_qty)
					 		print sql
					 		c.execute(sql)

			 	except Exception,e:
			 		print repr(e)
			 		
		 		sql = "select * from Demand_Checkout where Demand_ID = %s "%(demand_id)
		 		print sql
		 		c.execute(sql)
		 		print 1
		 		res_products = c.fetchall()
		 		print res_products
		 		context["products_Order_Checkout"] = res_products
 				sql = "select * from Items";
		 		c.execute(sql)
		 		res_products = c.fetchall()
		 		context["products"] = res_products

		 		inCart={}
		 		for i in range(len(context["products"])):
		 			id = int(context["products"][i][0])
		 			inCart[id]=0

		 		for i in range(len(context["products_Order_Checkout"])):
		 			id = int(context["products_Order_Checkout"][i][1])
		 			qt = int(context["products_Order_Checkout"][i][2])
		 			inCart[id]=qt

		 		lst=[]
		 		cart_total=0	
		 		for i in range(len(context["products"])):
		 			l=list(context["products"][i])
		 			if(inCart[context["products"][i][0]]):
		 				l.append(inCart[context["products"][i][0]])
		 			else:
		 				l.append(0)
			 		lst.append(tuple(l))
			 		cart_total+=int(l[9])
			 	context["products"] = lst
			 	context["cart_total"]=cart_total
		 	except Exception,e:
		 		print repr(e)
		 	finally:
		 		c.close()
			return render(request,template,context)


def demand_checkout(request):
	if(not request.user.is_authenticated()):
		messages.error(request, 'Please Log In First!!')
		return HttpResponseRedirect('/login/')
	template = "demand_checkout.html"
	context={}
	Username=request.user.username
 	context2 = get_home_context(Username)
 	context['is_Root'] = context2['is_Root']
 	context['username'] = context2['username']
 	context['store_det'] = context2['store_det']
	title = "demand-checkout"
	context["title"] = title
	empty_cart=True
	try: 
		Demand_ID = get_prev_demand();

		c = connection.cursor()
		sql = "select Items.Name, Demand_Checkout.Qty from Items,Demand_Checkout where Demand_Checkout.Items_ID=Items.Items_ID and Demand_Checkout.Demand_ID=%s"%Demand_ID
		print sql
		print Demand_ID
		c.execute(sql)
		res = c.fetchall()
		print res

		context["products"] = res
		if(len(res)!=0):
			return render(request,template,context)
		else: 
			if(empty_cart):
				messages.error(request, 'Please Select Items Cart is Empty!!')
				return HttpResponseRedirect("/medical/demand-supply/")

	except Exception,e:
		print repr(e)
		return HttpResponse("No Items in Cart")
	return HttpResponse("No Items in Cart")


def demand_buy(request):
	if(not request.user.is_authenticated()):
		messages.error(request, 'Please Log In First!!')
		return HttpResponseRedirect('/login/')
	template = "demand-bill.html"
	context={}
	Username=request.user.username
 	context2 = get_home_context(Username)
 	context['is_Root'] = context2['is_Root']
 	context['username'] = context2['username']
 	context['store_det'] = context2['store_det']
	title = "demand-bill"
	context["title"] = title
	
	if(not request.user.is_authenticated()):
		messages.error(request, 'Please Log In First!!')
		return HttpResponseRedirect('/login/')

	try: 
		Demand_ID = get_prev_demand();
		Store_ID = get_store_id(request.user.username)
		Emp_ID = request.user.username
		print "Demand_ID ",Demand_ID
		c = connection.cursor()
		sql = "select Items.Items_ID,Demand_Checkout.Qty from Items,Demand_Checkout where Demand_Checkout.Items_ID=Items.Items_ID and Demand_Checkout.Demand_ID=%s"%Demand_ID
		c.execute(sql)
		print sql
		res = c.fetchall()
		print res
		context["products"] = res

		dt = datetime.datetime.now()
		dy = str(dt.day)
		mn = str(dt.month)
		yr = str(dt.year)

		Date_created = yr+'-'+mn+'-'+dy
		Cust_Id = get_prev_cust();
		for i in range(len(res)):
			rw = list(res[i])
			new_qt = int(rw[1]);
			item_id = int(rw[0]);
			print rw
			sql = "Select * from Inventory where Store_ID=%s and Items_ID=%s"%(Store_ID,item_id)
			print sql
			c.execute(sql)
			res2 = c.fetchall()
			print res2
			if(len(res2)!=0):
				sql = "Update Inventory set Qty = Qty+%s where Store_ID=%s and Items_ID=%s"%(new_qt,Store_ID,item_id)
				print sql
				c.execute(sql)
			else:
				sql = "Insert into Inventory values(%s,%s,%s)"%(Store_ID,item_id,new_qt)
				print sql
				c.execute(sql)

				
	   
	
		sql = "Select * from Demand where Demand_ID=%s"%(Demand_ID)
		print sql
		c.execute(sql)
		res2 = c.fetchone()
		print res2
		rw = list(res2)
		supp_id = int(rw[5])
		rw[5] = get_supp_name(supp_id);
		res2=rw
		sql = "select Items.Name,Demand_Checkout.Qty from Items,Demand_Checkout where Demand_Checkout.Items_ID=Items.Items_ID and Demand_Checkout.Demand_ID=%s"%Demand_ID
		c.execute(sql)
		res = c.fetchall()
		tmp_res=[]
		for i in range(len(res)):
			rw = list(res[i])
			print "rw: ",rw
			tmp_res.append([i+1,rw[0],rw[1]]);

		context['products'] = tmp_res 
		context['order'] = res2
		return render(request,template,context)

	
	except Exception,e:
		print repr(e)
		return HttpResponse("Transaction Cancelled") 
	return HttpResponse("Transaction Cancelled") 

def update_profile(request):
	if(not request.user.is_authenticated()):
		messages.error(request, 'Please Log In First!!')
		return HttpResponseRedirect('/login/')
	template = "update_profile.html"
	context={}
	Username=request.user.username
 	context2 = get_home_context(Username)
 	context['is_Root'] = context2['is_Root']
 	context['username'] = context2['username']
 	context['store_det'] = context2['store_det']
	title = "Update-Profile"
	msg=""
	context["title"] = title
	context['msg'] = msg;
	Username=request.user.username
 	is_Root = not is_Employee(Username)
 	print "is_Root: ",is_Root
 	context = {"is_Root":is_Root}
	sql = "Select Store_ID from Store"
	print sql
	c = connection.cursor()
	c.execute(sql)
	res=c.fetchall()
	print res
	res2=[]
	for i in res:
		res2.append(int(i[0]))
 	context['stores'] = res2
	if(request.method=="POST"):
		print "post"		

		Name = request.POST.get("EmployeeName","")
		Address = request.POST.get("EmployeeAddress","")
		Email = request.POST.get("EmployeeEmail","")
		PhoneNumber = request.POST.get("EmployeePhone","")
		Sex = request.POST.get("EmployeeSex","")
		# Password = request.POST.get("EmployeePassword","")
		Date_Start = request.POST.get("EmployeeStartDate","")
		Date_End = "2018-10-10"
		# Pay = request.POST.get("EmployeePay","")
		Store_ID = request.POST.get("EmployeeStoreID","")

		msg=""
		try:
			# tmp = make_password(Password)
			# print "pass: ",tmp
	 		c = connection.cursor()
	 		Emp_ID = int(request.user.username)
	 		sql = "Update Employee set Name='%s',Address='%s',Email='%s',Sex='%s',Date_Start='%s',Date_End='%s',Store_ID=%s where Emp_ID=%s"%(Name,Address,Email,Sex,Date_Start,Date_End,Store_ID,Emp_ID)
	 		print sql
	 		c.execute(sql)
	 		print "done"

	 		sql = "Update Employee_Phone set Phone='%s' where Emp_ID=%s" %(PhoneNumber,Emp_ID)
	 		print sql
	 		c.execute(sql)
	 		print "done"
	 		msg="Profile Updated successfully"
	 	except Exception,e:
	 		print repr(e)
	 		msg="Error in Updating Profile please check the details provided"

	 	finally:
	 		c.close()
	 	if(Name==None):
	 		msg=""
	 	context['msg'] = msg;

	 	print "msg: "+str(msg)
		return render(request,template,context)
	return render(request,template,context)
