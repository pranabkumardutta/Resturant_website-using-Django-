from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from Base_App.models import BookTable, AboutUs, Feedback, ItemList, Items,Items, Cart, CartItem, Order

def HomeView(request):
    items =  Items.objects.all()
    list = ItemList.objects.all()
    review = Feedback.objects.all()
    return render(request, 'home.html',{'items': items, 'list': list, 'review': review})


def AboutView(request):
    data = AboutUs.objects.all()
    return render(request, 'about.html',{'data': data})


def MenuView(request):
    items =  Items.objects.all()
    list = ItemList.objects.all()
    return render(request, 'menu.html', {'items': items, 'list': list})


def BookTableView(request):
    if request.method=='POST':
        name = request.POST.get('user_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('user_email')
        total_person = request.POST.get('total_person')
        booking_data = request.POST.get('booking_data')

        if name != '' and len(phone_number) == 10 and email != '' and total_person != 0 and booking_data != '':
            data = BookTable(Name=name, Phone_number=phone_number,
                             Email=email,Total_person=total_person,
                             Booking_date=booking_data)
            data.save()
    return render(request, 'book_table.html')



def FeedbackView(request):
    return render(request, 'feedback.html')

 
from django.shortcuts import render, get_object_or_404, redirect


# View to add an item to the cart
def add_to_cart(request, item_id):
    item = get_object_or_404(Items, id=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user.username)  # Adjust for your user system
    cart_item, created = CartItem.objects.get_or_create(item=item)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    cart.items.add(cart_item)
    return redirect('view_cart')  # Replace with the name of your cart view

# View to display cart
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user.username)
    return render(request, 'cart.html', {'cart': cart})

# View to place an order
def place_order(request):
    cart, _ = Cart.objects.get_or_create(user=request.user.username)
    if not cart.items.exists():
        return redirect('view_cart')  # Handle empty cart case

    total_price = cart.total_price()
    order = Order.objects.create(user=request.user.username, total_price=total_price)
    order.items.set(cart.items.all())
    cart.items.clear()  # Empty the cart after placing an order

    return redirect('order_confirmation', order_id=order.id)

def order_confirmation(request, order_id):
    # Retrieve the order by its ID
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_confirmation.html', {'order': order})


     