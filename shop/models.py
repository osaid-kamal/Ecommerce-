from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have username")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
 
class myuser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(
        verbose_name="last login", auto_now_add=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def _str_(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Product(models.Model):
    # product_id = models.AutoField()
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50,default="")
    sub_categrory=models.CharField(max_length=50,default="")
    price=models.IntegerField(default=0,blank=True)
    image=models.ImageField(upload_to="shop/images",default="")
    desc = models.CharField(max_length=150,default="")
    pub_date = models.DateField()



    def __str__(self):
    	return str(self.product_name)


class Customer(models.Model):
    user=models.OneToOneField(myuser,null=True,blank=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=200,null=True)
    email=models.EmailField(max_length=200)


    def __str__(self):
        return str(self.name)


class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False)
    t_id=models.CharField(max_length=100,null=True)

    def __str__(self):
        return str(self.id)

    # @property
    # def shipping(self):
    #     shipping=False
    #     orderitems=self.orderitem_set.all()
    #     for i in orderitems:
    #         if i.product.digital==False:
    #             shipping=True
    #     return shipping
    

    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.get_total for item in orderitems])
        return total
    @property
    def get_cart_items(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.quantity for item in orderitems])
        return total



class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total=self.product.price * self.quantity
        return total

    def __str__(self):
        return str(self.product)


class Shipping(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    address=models.CharField(max_length=200,null=False)
    city=models.CharField(max_length=200,null=False)
    state=models.CharField(max_length=200,null=False)
    pincode=models.IntegerField(null=False)
    data_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.address)
