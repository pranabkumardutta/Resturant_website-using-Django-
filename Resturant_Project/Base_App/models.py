from django.db import models

# Create your models here.
class ItemList(models.Model):
    Category_name = models.CharField(max_length=15)

    def __str__(self):
        return self.Category_name
    

class Items(models.Model):
    Item_name = models.CharField(max_length=40)
    description = models.TextField(blank=False)
    Price = models.IntegerField()
    Category = models.ForeignKey(ItemList, related_name='Name', on_delete=models.CASCADE)
    Image = models.ImageField(upload_to='items/')

    def __str__(self):
        return self.Item_name

class AboutUs(models.Model):
    Description = models.TextField(blank=False)

class Feedback(models.Model):
    User_name = models.CharField(max_length=15)
    Description = models.TextField(blank=False)
    Rating = models.IntegerField()
    Image = models.ImageField(upload_to='items/', blank=True)

    def __str__(self):
        return self.User_name
    

class BookTable(models.Model):
    Name = models.CharField(max_length=15)
    Phone_number = models.IntegerField()
    Email = models.EmailField()
    Total_person = models.IntegerField()
    Booking_date = models.DateField()

    def __str__(self):
        return self.Name
    

class Cart(models.Model):
    user = models.CharField(max_length=50)  # For simplicity; replace with ForeignK
    items = models.ManyToManyField('CartItem')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user}"

    def total_price(self):
        return sum(item.item.Price * item.quantity for item in self.items.all())

# Cart Item Model
class CartItem(models.Model):
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.Item_name}"

# Order Model
class Order(models.Model):
    user = models.CharField(max_length=50)  # Replace with ForeignKey to User for authenticated users
    items = models.ManyToManyField(CartItem)
    total_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending')

    def __str__(self):
        return f"Order #{self.id} by {self.user}"
