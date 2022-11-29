from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=50, default="name")
    email = models.EmailField(max_length=50, default="email")
    phone = models.IntegerField(default="0")
    message = models.TextField()

    def __str__(self):
        return self.email


class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class ResetProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    category_image = models.ImageField(upload_to="cat_images/", default="")

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory_name = models.CharField(max_length=100)

    def __str__(self):
        return self.subcategory_name


class Book(models.Model):
    isbn = models.CharField(max_length=10, unique=True)
    book_title = models.CharField(max_length=100)
    edition = models.SmallIntegerField(default=1)
    book_desc = models.TextField(max_length=1000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    publication = models.CharField(max_length=100)
    price = models.IntegerField()
    author = models.CharField(max_length=100)
    pub_date = models.DateField()
    quantity = models.IntegerField()
    book_image = models.ImageField(upload_to='book_images/', default="")

    def __str__(self):
        return self.book_title + " " + str(self.edition)


class Wishlist(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    desc = models.CharField(max_length=50, default='wishlist')


class Cart(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    desc = models.CharField(max_length=50, default='cart')
    quantity = models.IntegerField(default=1)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default='Your Name')
    bio = models.CharField(max_length=200, default='Your Bio')
    phone = models.CharField(max_length=20, default="0000000000")
    address = models.CharField(max_length=200, default='Your address')
    photo = models.ImageField(
        upload_to='profile_image/', default='image/user.png')


class Issued_Status(models.Model):
    status = models.CharField(max_length=50, default="requested")

    def __str__(self):
        return self.status


class BookPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    transaction_status = models.CharField(max_length=50, default="defaults")
    transaction_code = models.CharField(max_length=200)
    transaction_time = models.DateTimeField(auto_now_add=True)


class BookOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    issue_status = models.ForeignKey(Issued_Status, on_delete=models.CASCADE)
    payment_id = models.ForeignKey(BookPayment, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)


class BookRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    issue_status = models.ForeignKey(Issued_Status, on_delete=models.CASCADE)
    payment_id = models.ForeignKey(BookPayment, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)


class RoomPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    month = models.IntegerField()
    start_date = models.DateField(auto_now_add=False)
    upto_date = models.DateField(auto_now_add=False)
    payment_id = models.CharField(max_length=200, default="null")
    table_block = models.CharField(max_length=10, default="defaults")
    seat_alloted = models.CharField(max_length=20, default="defaults")
    transaction_status = models.CharField(max_length=50, default="defaults")
