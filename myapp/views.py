
import os
from sqlite3 import IntegrityError
from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from myapp.models import Item
from django.http import HttpResponseBadRequest, JsonResponse
from myapp.models import MyModel, User
import joblib
import pandas as pd
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from myapp.models import User 
from myapp.models import Customer 
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from datetime import datetime
from myapp.models import OrderItem 
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Order

def index(request):
    return render(request, 'index.html')

def welcome(request):
    return render(request, 'welcome.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username == 'admin' and password == 'admin123':
            request.session['username'] = 'admin'  
            return redirect('dashboard')
        
        try:
            customer = Customer.objects.get(uname=username)
            
            if check_password(password, customer.upassword): 
                request.session['username'] = customer.uname  
                return redirect('udashboard')
            else:
                messages.error(request, 'Invalid username or password')
        except Customer.DoesNotExist:
            messages.error(request, 'Invalid username or password')
            
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('index')

def dashboard(request):
 if 'username' in request.session:
    pending_orders = Order.objects.filter(status='pending').prefetch_related('order_items')

    if request.method == 'POST':
        pass

    return render(request, 'admin_dashboard.html', {'pending_orders': pending_orders})
 else:
    return redirect('login')

from django.http import JsonResponse

def udashboard(request):
 if 'username' in request.session:
    items = Item.objects.all()
    username = request.session.get('username')
    
    try:
        customer = Customer.objects.get(uname=username)
        upharmacy_name = customer.upharmacy_name
    except Customer.DoesNotExist:
        upharmacy_name = None
    
    if request.method == 'POST' and 'item_id' in request.POST:
        item_id = request.POST['item_id']
        quantity = int(request.POST['quantity'])
        
        item = Item.objects.get(pk=item_id)
        
        if 'cart' not in request.session:
            request.session['cart'] = []
        
        cart = request.session['cart']
        cart_item = {
            'item_id': item.id,
            'item_name': item.item_name,
            'price': item.price,
            'quantity': quantity,
            'total': item.price * quantity
        }
        
        cart.append(cart_item)
        request.session.modified = True
    
        return JsonResponse({'message': 'Item added to cart successfully'})
    
    return render(request, 'user_dashboard.html', {'items': items, 'username': username, 'upharmacy_name': upharmacy_name})
 else:
    return redirect('login')

def signup(request):
    return render(request, 'signup.html')

def add_item(request):
 if 'username' in request.session:
    if request.method == 'POST':
        item_id = request.POST.get('item-id')
        item_name = request.POST.get('item-name')
        expire_date = request.POST.get('expire-date')
        stocks = request.POST.get('stocks')
        price = request.POST.get('price')  
        if not price:
            alert_message = "Please Enter All The Required Fields."
            return render(request, 'add_item.html', {'alert_message': alert_message})

        if Item.objects.filter(item_id=item_id).exists():
            alert_message = f"An item with the Item ID '{item_id}' already exists."
            return render(request, 'add_item.html', {'alert_message': alert_message})
        else:
            item = Item(item_id=item_id, item_name=item_name, expire_date=expire_date, stocks=stocks, price=price)
            item.save()

            success_message = f"Item with Item ID '{item_id}' added successfully!"
            return render(request, 'add_item.html', {'success_message': success_message})

    return render(request, 'add_item.html')
 else:
    return redirect('login')


def item_list(request):
 if 'username' in request.session:
    items = Item.objects.all()
    return render(request, 'items.html', {'items': items})
 else:
    return redirect('login')


def registration_request_view(request):
    if request.method == 'POST':
        pharmacy_name = request.POST.get('pharmacyName')
        city = request.POST.get('city')
        address = request.POST.get('address')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobileNumber')

        #saving the data to the database
        my_model_instance = MyModel(
            pharmacy_name=pharmacy_name,
            city=city,
            address=address,
            email=email,
            mobile_number=mobile_number
        )
        my_model_instance.save()

    return render(request, 'welcome.html')


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
encoder_file_path = os.path.join(BASE_DIR, 'data', 'encoder.pkl')
model_file_path = os.path.join(BASE_DIR, 'data', 'HYSModel.pkl')


encoder = joblib.load(encoder_file_path)
model = joblib.load(model_file_path)


def predict_sales(item_id, year, month):
    input_data = pd.DataFrame({'Item ID': [item_id], 'year': [year], 'month': [month]})

    input_encoded = encoder.transform(input_data[['Item ID']])

    input_encoded = pd.DataFrame(input_encoded, columns=encoder.get_feature_names_out(['Item ID']), index=input_data.index)
    input_data = pd.concat([input_data.drop(columns=['Item ID']), input_encoded], axis=1)

    sales_prediction = model.predict(input_data)[0]

    sales_prediction = round(sales_prediction)
    return sales_prediction

def sales_prediction_view(request):
 if 'username' in request.session:
    items = Item.objects.all()
    registration_requests = MyModel.objects.all()

    if request.method == 'POST':
        item_id = request.POST.get('item-select')
        year = int(request.POST.get('year-select'))
        month = int(request.POST.get('month-select'))
        sales_prediction = predict_sales(item_id, year, month)
        selected_item_id = item_id
        return render(request, 'sales_prediction.html', {'sales_prediction': sales_prediction, 'items': items, 'registration_requests': registration_requests, 'selected_year': year, 'selected_month': month,'selected_item_id': selected_item_id})

    return render(request, 'sales_prediction.html', {'items': items})
 else:
    return redirect('login')

from django.contrib.auth.hashers import make_password

def register_user(request, request_id):
 if 'username' in request.session:
    if request.method == 'POST':
        try:
            registration_request = MyModel.objects.get(pk=request_id)
        except MyModel.DoesNotExist:
            return HttpResponseBadRequest("Invalid Request ID")

        username = request.POST.get('username')
        password = request.POST.get('password')

        if Customer.objects.filter(uname=username).exists():
            alert_message = "Username already exists. Please choose a different username."
            messages.error(request, alert_message)
        else:
            hashed_password = make_password(password)  # Hashing the password
            customer = Customer(
                uname=username,
                upassword=hashed_password, 
                upharmacy_name=registration_request.pharmacy_name,
                ucity=registration_request.city,
                uaddress=registration_request.address,
                uemail=registration_request.email,
                umobile_number=registration_request.mobile_number,
            )
            customer.save()

            subject = 'Registration Details'
            message = f"Hello {registration_request.pharmacy_name}, your registration has been successful. Please use the below username and password to login to the website.\nUsername: {username}\nPassword: {password}"
            from_email = 'ashan.sanjula1998@gmail.com' 
            recipient_list = [registration_request.email]

            send_mail(subject, message, from_email, recipient_list)

            registration_request.delete()

            items = Item.objects.all()
            registration_requests = MyModel.objects.all()
            success_message = "User registration successful!"
            messages.success(request, success_message)
        
        return redirect('reg_request')

    return render(request, 'admin_dashboard.html')
 else:
    return redirect('login')

def users(request):
 if 'username' in request.session:
    customers_list = Customer.objects.all()  
    context = {'customers_list': customers_list}
    return render(request, 'users.html', context)
 else:
    return redirect('login')


def delete_user(request, uid):
    customer = Customer.objects.get(uid=uid)  
    customer.delete()
    messages.success(request, f'User "{customer.uname}" has been deleted successfully.')
    return redirect('users')


def processed_orders(request):
 if 'username' in request.session:
    processed_orders = Order.objects.filter(status='processed').prefetch_related('order_items')

    if request.method == 'POST':
        pass

    return render(request, 'processed_orders.html', {'processed_orders': processed_orders})

    return redirect('dashboard')
 else:
    return redirect('login')




def reg_request(request):
 if 'username' in request.session:
    registration_requests = MyModel.objects.all()
    return render(request, 'reg_request.html', {'registration_requests': registration_requests})
 else:
    return redirect('login')


def shipped_orders(request):
 if 'username' in request.session:
    shipped_orders = Order.objects.filter(status='shipped').prefetch_related('order_items')

    if request.method == 'POST':
        pass

    return render(request, 'shipped_orders.html', {'shipped_orders': shipped_orders})

    return redirect('dashboard')
 else:
    return redirect('login')


def Rship_orders(request):
 if 'username' in request.session:
    ready_orders = Order.objects.filter(status='ready').prefetch_related('order_items')

    if request.method == 'POST':
        pass

    return render(request, 'ReadytoShip.html', {'ready_orders': ready_orders})

    return redirect('dashboard')
 else:
    return redirect('login')


from django.http import JsonResponse

def delivered_orders(request):
 if 'username' in request.session:
    delivered_orders = Order.objects.filter(status='delivered').prefetch_related('order_items')

    if request.method == 'POST':
        pass

    return render(request, 'deliveredorders.html', {'delivered_orders': delivered_orders})

    return redirect('dashboard')
 else:
    return redirect('login')

def cd_orders(request):
    if 'username' in request.session:
        cancelled_orders = Order.objects.filter(status='cancelled')
        return render(request, 'cancelledOrders.html', {'cancelled_orders': cancelled_orders})
    else:
        return redirect('login')

class UpdateStocksForm(forms.Form):
    item = forms.CharField(widget=forms.HiddenInput())
    add_stocks = forms.IntegerField(min_value=0)

def update_stocks(request):
 if 'username' in request.session:
    items = Item.objects.all()

    if request.method == 'POST':
        form = UpdateStocksForm(request.POST)
        if form.is_valid():
            item_id = form.cleaned_data['item']
            add_stocks = form.cleaned_data['add_stocks']
            
            try:
                item = Item.objects.get(item_id=item_id)
                item.stocks += add_stocks
                item.save()

                return JsonResponse({'success': True, 'item_name': item.item_name})
            except Item.DoesNotExist:
                pass  

            return JsonResponse({'success': False, 'message': 'Failed to update stocks'})

    else:
        form = UpdateStocksForm()

    return render(request, 'updateStocks.html', {'items': items, 'update_stocks_form': form})
 else:
    return redirect('login')


def user_pendingorders(request):
 if 'username' in request.session:
    username = request.session.get('username')  

    try:
        customer = Customer.objects.get(uname=username)
        upharmacy_name = customer.upharmacy_name
        uaddress = customer.uaddress 
    except Customer.DoesNotExist:
        customer = None
        upharmacy_name = None
        uaddress = None

    pending_orders = Order.objects.filter(username=username, status='pending')

    pending_orders = pending_orders.prefetch_related('order_items')

    pending_orders_list = list(pending_orders)

    return render(request, 'user_pendingorders.html', {
        'pending_orders': pending_orders_list,
        'customer': customer, 
        'username': username,
        'upharmacy_name': upharmacy_name,
        'uaddress': uaddress 
    })

 else:
    return redirect('login')

def user_processedorders(request):
 if 'username' in request.session:
    username = request.session.get('username') 
    
    try:
        customer = Customer.objects.get(uname=username)
        upharmacy_name = customer.upharmacy_name
        uaddress = customer.uaddress 
    except Customer.DoesNotExist:
        customer = None
        upharmacy_name = None
        uaddress = None
    
    processed_orders = Order.objects.filter(username=username, status='processed')

    processed_orders = processed_orders.prefetch_related('order_items')

    processed_orders_list = list(processed_orders)

    return render(request, 'user_processedorders.html', {
        'processed_orders': processed_orders_list,
        'customer': customer,
        'username': username,
        'upharmacy_name': upharmacy_name,
        'uaddress': uaddress 
    })
 else:
    return redirect('login')

def user_shippedorders(request):
 if 'username' in request.session:
    username = request.session.get('username') 
    
    try:
        customer = Customer.objects.get(uname=username)
        upharmacy_name = customer.upharmacy_name
        uaddress = customer.uaddress 
    except Customer.DoesNotExist:
        customer = None
        upharmacy_name = None
        uaddress = None
    
    shipped_orders = Order.objects.filter(username=username, status='shipped')

    shipped_orders = shipped_orders.prefetch_related('order_items')

    shipped_orders_list = list(shipped_orders)

    return render(request, 'user_shippedorders.html', {
        'shipped_orders': shipped_orders_list,
        'customer': customer,
        'username': username,
        'upharmacy_name': upharmacy_name,
        'uaddress': uaddress
    })
 else:
    return redirect('login')

def user_deliveredorders(request):
 if 'username' in request.session:
    username = request.session.get('username')
    
    try:
        customer = Customer.objects.get(uname=username)
        upharmacy_name = customer.upharmacy_name
        uaddress = customer.uaddress
    except Customer.DoesNotExist:
        customer = None
        upharmacy_name = None
        uaddress = None
    
    delivered_orders = Order.objects.filter(username=username, status='delivered')

    delivered_orders = delivered_orders.prefetch_related('order_items')

    delivered_orders_list = list(delivered_orders)

    return render(request, 'user_deliveredorders.html', {
        'delivered_orders': delivered_orders_list,
        'customer': customer, 
        'username': username,
        'upharmacy_name': upharmacy_name,
        'uaddress': uaddress 
    })
 else:
    return redirect('login')

def user_cancelledorders(request):
 if 'username' in request.session:
    username = request.session.get('username') 

    try:
        customer = Customer.objects.get(uname=username)
        upharmacy_name = customer.upharmacy_name  
    except Customer.DoesNotExist:
        upharmacy_name = None

    cancelled_orders = Order.objects.filter(username=username, status='cancelled').prefetch_related('order_items')

    return render(request, 'user_cancelledorders.html', {'username': username, 'upharmacy_name': upharmacy_name, 'cancelled_orders': cancelled_orders})
 else:
    return redirect('login')

import json
from django.http import JsonResponse
from .models import Order, OrderItem

def create_order(request):
    if request.method == 'POST':
        username = json.loads(request.body.decode('utf-8'))['username']
        order = Order.objects.create(username=username)
        return JsonResponse({'success': True, 'order_id': order.orderid})
    
    return JsonResponse({'success': False})

def place_order(request):
    if request.method == 'POST':
        order_items = json.loads(request.body.decode('utf-8'))['order_items']
        username = request.session.get('username')

        if not username:
            return JsonResponse({'success': False, 'error': 'Username not found'})

        order = Order.objects.create(username=username)
        for item in order_items:
            OrderItem.objects.create(order=order, item_name=item['item_name'], price=item['price'], quantity=item['quantity'], total=item['total'])

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

def cancel_order(request, order_id):
    try:
        order = Order.objects.get(orderid=order_id)
        if order.status == 'pending':
            order.status = 'cancelled'
            order.save()
            return JsonResponse({'success': True, 'message': 'Order has been successfully cancelled.'})
        else:
            return JsonResponse({'success': False, 'message': 'Order cannot be cancelled.'})
    except Order.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Order not found.'})
    
def admin_update_orderstatus_process(request, order_id):
 if 'username' in request.session:
    if request.method == 'POST':
        new_status = request.POST.get('status', 'processed')
        try:
            order = Order.objects.get(orderid=order_id)
            order.status = new_status
            order.save()
            return JsonResponse({'success': True, 'status': new_status})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Order not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'}) 
 else:
    return redirect('login')   

def admin_update_orderstatus_ready(request, order_id):
 if 'username' in request.session:
    if request.method == 'POST':
        new_status = request.POST.get('status', 'ready')
        try:
            order = Order.objects.get(orderid=order_id)
            order.status = new_status
            order.save()
            return JsonResponse({'success': True, 'status': new_status})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Order not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})  
 else:
    return redirect('login') 

def admin_update_orderstatus_shipped(request, order_id):
 if 'username' in request.session:
    if request.method == 'POST':
        new_status = request.POST.get('status', 'shipped')
        try:
            order = Order.objects.get(orderid=order_id)
            order.status = new_status
            order.save()
            return JsonResponse({'success': True, 'status': new_status})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Order not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})
 else:
    return redirect('login')

def admin_update_orderstatus_delivered(request, order_id):
 if 'username' in request.session:
    if request.method == 'POST':
        new_status = request.POST.get('status', 'delivered')
        try:
            order = Order.objects.get(orderid=order_id)
            order.status = new_status
            order.save()
            return JsonResponse({'success': True, 'status': new_status})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Order not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})    
 else:
    return redirect('login')

class UpdatePriceForm(forms.Form):
    item = forms.CharField(widget=forms.HiddenInput())
    new_price = forms.DecimalField(min_value=0, decimal_places=2)

def admin_update_price(request):
 if 'username' in request.session:
    items = Item.objects.all()

    if request.method == 'POST':
        form = UpdatePriceForm(request.POST)
        if form.is_valid():
            item_id = form.cleaned_data['item']
            new_price = form.cleaned_data['new_price']
            
            try:
                item = Item.objects.get(item_id=item_id)
                item.price = new_price
                item.save()

               
                return JsonResponse({'success': True, 'item_name': item.item_name})
            except Item.DoesNotExist:
                pass  

            return JsonResponse({'success': False, 'message': 'Failed to update price'})

    else:
        form = UpdatePriceForm()

    return render(request, 'admin_update_price.html', {'items': items, 'update_price_form': form})
 else:
    return redirect('login')


def generate_monthly_sales_report(request):
 if 'username' in request.session:
    current_month = datetime.now().month
    current_year = datetime.now().year

    delivered_orders = OrderItem.objects.filter(order__status='delivered', order__order_date__month=current_month, order__order_date__year=current_year)

    item_stats = {}  
    for order_item in delivered_orders:
        item_name = order_item.item_name
        total_price = order_item.price * order_item.quantity
        if item_name in item_stats:
            total_sales, num_items_sold = item_stats[item_name]
            total_sales += total_price
            num_items_sold += order_item.quantity
            item_stats[item_name] = (total_sales, num_items_sold)
        else:
            item_stats[item_name] = (total_price, order_item.quantity)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="monthly_sales_report_{current_month}_{current_year}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    title = Paragraph("Monthly Sales Report", style=None)
    elements.append(title)

    data = [['Item Name', 'Total Sales', 'Number of Items Sold']]
    for item_name, (total_sales, num_items_sold) in item_stats.items():
        data.append([item_name, total_sales, num_items_sold])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)

    doc.build(elements)
    return response
 else:
    return redirect('login')
 
def search_items(request):
    query = request.GET.get('q', '')
    
    if query:
        # Search for items matching the query
        items = Item.objects.filter(item_name__icontains=query)
        items_data = [{'item_name': item.item_name} for item in items]
    else:
        items_data = []

    return JsonResponse({'items': items_data})
 
def check_availability(request):
    if request.method == 'POST':
        item_names = request.POST.getlist('item_name[]')  # Getting item names from the form
        quantities = request.POST.getlist('quantity[]')  # Getting quantities
        
        report = []
        for item_name, quantity in zip(item_names, quantities):
            try:
                # Correct field name used here
                item = Item.objects.get(item_name=item_name)  
                
                # Check stock availability
                if item.stocks >= int(quantity):
                    status = 'Available'
                else:
                    status = 'Out of stock'
            except Item.DoesNotExist:
                status = 'Item not found'

            # Add the result to the report
            report.append({
                'item_name': item_name,
                'quantity': quantity,
                'status': status
            })
        
        return render(request, 'check_availability.html', {'report': report})
    
    return render(request, 'check_availability.html')

def base_design(request):
    return render(request, 'base_design.html')
