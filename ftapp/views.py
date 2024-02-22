from django.shortcuts import render,redirect,HttpResponse
from .models import Product,Customer,Cart,Order



# Create your views here.
def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

def logvalid(request):

    if request.method == "POST":
        nm = request.POST["name"]
        psw = request.POST["psw"]
        data = Customer.objects.all()
        c=0 
        request.session['name'] = nm
        for rec in data:
           # print(rec.name,rec.password,rec.phone)
            if rec.name == nm and rec.password == psw:
                c+=1
                return redirect('prod')
            
        if c==0:
            ermsg = {"error" : "Invalid Credentials / If 'new user' consider registration"}
            return render(request,'login.html',ermsg)
        
def reg(request):
    return render(request, 'registration.html')

def regsave(request):
    if request.method == "POST":
        name = request.POST["name"]
        psw = request.POST["pswd"]
        mobno = request.POST["mobno"]
        #print(name , psw ,mobno)
        ct=0
        regmsg={}
        cus_check = Customer.objects.all()
        for i in cus_check:
            if i.name.upper() == name or i.name.lower() == name or (i.name[0].upper()+i.name[1:].lower()) == name:
                ct+=1
        if ct == 0:
            ins = Customer(name = name, phone =mobno , password=psw)
            ins.save()
            regmsg = {"success_msg" : "Registration Successfull Please Log In" }
        else:
            regmsg = {"error" : "User name already exists" }
        return render(request,"registration.html",regmsg)

def prod(request):
    cusname = request.session['name']
    products = Product.objects.all()
    cont={}
    request.session['cust']=cusname
    for modprod in products:
        if modprod.quantity == 0:
            cont={"cont":"Out Of Stock"}
            render(request,'products.html',cont)
    return render(request, 'products.html',{'products':products,'cusname':cusname,'cont':cont})

def cart(request):
    if request.method == "POST":
        global prod,cus,prod_id
        cus = request.POST.get('list_data')
        prod_id= request.POST['prod_id']
        #request.session['prod']=prod_id
        pro = Product.objects.get(id=prod_id)
        ca = Cart.objects.all()
        #loop for not duplicating cart products
        for i in ca:
            if pro.name == i.prod and cus ==i.cname:
                return redirect('prod')
        #print(prod_id,cus,prod.name)
        ins = Cart(cname= cus,prod= pro.name,prc=pro.price, quan=pro.quantity ,img= pro.image,des=pro.desc)
        ins.save()
        return redirect('prod')
    
def cartg(request):
    if request.method == "GET":
        cust = request.session.get('cust',None)
        #pid = request.session.get('prod',None)
        print(cust)
        custfilter = Cart.objects.filter(cname=cust)
        print(custfilter,cust)
        if custfilter.exists():
            length = len(custfilter)
            print(length)
            if length == 1:
                cu = {"custfilter":custfilter,"cust":cust}
                return render(request,'cart.html',cu)
            else:
                cu = {"custfilter":custfilter,"cust":cust}
                print(custfilter,cust)
                return render(request,'cart.html',cu)
        else:
            context={'msg':'Cart Is Empty',"cust":cust}
            return render(request,'cart.html',context)

def rem(request):   
    product = request.POST.get('product')
    usr = request.POST.get('nm')
    print(usr)
    print(product)
    cont = Cart.objects.get(prod=product,cname=usr)
    cont.delete()
    return redirect('cartg')

def buy(request):
    if request.method == 'POST':
        values = request.POST.getlist('values[]')
        print(values)
        usr = request.POST.get('nm', '')
        cart1 = Cart.objects.filter(cname=usr)
        print(usr,len(cart1))
        q ,c,tot =0,0,0
        context = {}
        for i in cart1:
            modprod = Product.objects.get(name=i.prod)
            if int(modprod.quantity) >= int(values[q]):
                c +=1
                print(int(values[q]))
            q+=1
        if c == len(cart1):
            l=0
            for i in cart1:
                modprod = Product.objects.get(name=i.prod)
                modprod.quantity = str(int(modprod.quantity) - int(values[l]))
                modprod.save()
                print(i.prod,modprod.quantity)
                l+=1
            j=0
            for i in cart1:
                if i.cname == usr:
                    tot= tot+int(i.prc)*int(values[j])
                    j += 1  
            cust = Customer.objects.get(name=usr)
            k=0
            for i in cart1:
                if i.cname == usr:
                    v=(int(i.prc)*int(values[k]))
                    print(v)
                    ins = Order(product=i.prod,customer=i.cname,quantity=int(values[k]),phone=cust.phone,price=v,img1=i.img,des1=i.des)
                    ins.save()
                    k += 1
            for i in cart1:
                prod = Product.objects.get(name=i.prod)
                car = Cart.objects.filter(prod=i.prod)
                for i in car:
                    i.quan = prod.quantity
                    i.save()
            Cart.objects.filter(cname=usr).delete()
        else:
            context = {"msg":"Invalid Quantity Values"}
        print(tot)
        print(context)
        return render(request,'buy.html',{"tot":tot,"context":context})
    else:
        return render(request,'buy.html')

def myorders(request):
    usr = request.session.get('cust', None)
    context = Order.objects.filter(customer=usr)
    if len(context) == 0:
        context = {"msg":"Empty"}
    return render(request,'myorders.html',{"context":context,"usr":usr})

def clearorder(request):
    usr = request.session.get('cust', None)
    context = Order.objects.filter(customer=usr)
    context.delete()
    return redirect('myorders')



def remitem(request):
    usr = request.session.get('cust', None) 
    car=Cart.objects.filter(cname=usr).first()
    print(car.prod)
    car.delete()
    return redirect('cartg')

def contact(request):
    return render(request,'contact.html')


def work(request):
    return render(request, 'workoutplan.html')
