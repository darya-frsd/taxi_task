# models.py

from django.db import models


class Gender(models.Model):
    gender_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)


class Disabilities(models.Model):
    disabilities_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile_phone = models.CharField(max_length=100)
    gender = models.ForeignKey(Gender, on_delete=models.RESTRICT)
    email = models.EmailField(max_length=100)
    home_address = models.CharField(max_length=100)
    diseases = models.ManyToManyField(Disabilities, blank=True)


class UserDisabilities(models.Model):
    user = models.OneToOneField(User, on_delete=models.RESTRICT, primary_key=True)
    disabilities = models.ForeignKey(Disabilities, on_delete=models.RESTRICT, null=True, blank=True)


class Vendor(models.Model):
    vendor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    address = models.CharField(max_length=45)
    rating = models.FloatField()


class TaxiStatuses(models.Model):
    status_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=45)


class Taxi(models.Model):
    taxi_id = models.AutoField(primary_key=True)
    registration_number = models.IntegerField()
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    taxi_type_id = models.IntegerField()
    status = models.ForeignKey(TaxiStatuses, on_delete=models.RESTRICT)
    driver = models.ForeignKey('Driver', on_delete=models.RESTRICT)


class TripDetails(models.Model):
    trip_id = models.AutoField(primary_key=True)
    amount = models.FloatField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    start_address = models.CharField(max_length=100)
    end_address = models.CharField(max_length=100)
    service_type_id = models.IntegerField()
    taxi = models.ForeignKey(Taxi, on_delete=models.RESTRICT)
    driver = models.ForeignKey('Driver', on_delete=models.RESTRICT)


class Driver(models.Model):
    driver_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.ForeignKey(Gender, on_delete=models.RESTRICT, db_column='gender_id')
    mobile_phone = models.CharField(max_length=100)
    rating = models.FloatField()
    age = models.IntegerField()


class OrderStatuses(models.Model):
    status_id = models.IntegerField(primary_key=True)
    description = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('Products')

class CartItem(models.Model):
    product = models.CharField(max_length=100)
    purchased = models.BooleanField(default=False)

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(User, on_delete=models.RESTRICT, db_column='customer_id')
    total = models.FloatField()
    datetime = models.DateTimeField()
    status = models.ForeignKey(OrderStatuses, on_delete=models.RESTRICT)


class OrderDetails(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.RESTRICT, db_column='order_id')
    product = models.ForeignKey('Products', on_delete=models.RESTRICT)
    quantity = models.IntegerField()
    total_price = models.FloatField()


class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    category_id = models.IntegerField()
    price = models.FloatField()
    vendor_id = models.IntegerField()
    disability = models.ForeignKey(Disabilities, on_delete=models.RESTRICT, db_column='disability_id')


class Services(models.Model):
    service_id = models.IntegerField(primary_key=True)


class OwnerTaxi(models.Model):
    owner_id = models.AutoField(primary_key=True)
    taxi = models.OneToOneField(Taxi, on_delete=models.RESTRICT, db_column='taxi-d', unique=True)


class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)
    email = models.CharField(max_length=45)
    customer = models.ForeignKey(User, on_delete=models.RESTRICT, db_column='customer_id')
    bill = models.ForeignKey('BillDetails', on_delete=models.RESTRICT, db_column='bill_id')

class Accompanying(models.Model):
    accompanying_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.ForeignKey('Gender', on_delete=models.RESTRICT)
    mobile_phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    ratimg = models.IntegerField()
    status = models.CharField(max_length=45)
    price_per_hour = models.FloatField()


class BillDetails(models.Model):
    bill_id = models.AutoField(primary_key=True)
    bill_date = models.DateField()
    advance_amount = models.FloatField()
    discount_amount = models.FloatField()
    total_amount = models.FloatField()
    customer = models.ForeignKey(User, on_delete=models.RESTRICT, db_column='customer_id')
    trip = models.ForeignKey(TripDetails, on_delete=models.RESTRICT, db_column='trip_id')

class GroupEntertainment(models.Model):
    gr_enter_id = models.AutoField(primary_key=True)
    accomp = models.ForeignKey(Accompanying, on_delete=models.RESTRICT)
    taxi = models.ForeignKey(Taxi, on_delete=models.RESTRICT)
    people_amount = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total = models.CharField(max_length=45)
    start_address = models.CharField(max_length=45)
    end_address = models.CharField(max_length=45)

class Address(models.Model):
    location = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()


class OrderStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)


class ServiceAccompany(models.Model):
    srv_accomp_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey('User', on_delete=models.RESTRICT)
    accomp = models.ForeignKey('Accompanying', on_delete=models.RESTRICT)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    details = models.CharField(max_length=100, null=True)
    total = models.FloatField()


class TaxiDisabilities(models.Model):
    taxi = models.OneToOneField(Taxi, on_delete=models.RESTRICT, primary_key=True)
    disabilities = models.ForeignKey('Disabilities', on_delete=models.RESTRICT)


class Trip(models.Model):
    trip_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey('User', on_delete=models.RESTRICT)
    total = models.FloatField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    taxi = models.ForeignKey(Taxi, on_delete=models.RESTRICT)
    driver = models.ForeignKey('Driver', on_delete=models.RESTRICT)
    start_address = models.CharField(max_length=100)
    end_address = models.CharField(max_length=100)


class BillAccomp(models.Model):
    bill_id = models.AutoField(primary_key=True)
    bill_date = models.DateTimeField()
    advance_amount = models.FloatField()
    discount_amount = models.FloatField()
    total_amount = models.FloatField()
    customer = models.ForeignKey(User, on_delete=models.RESTRICT)
    srv_accomp = models.ForeignKey(ServiceAccompany, on_delete=models.RESTRICT)


class BillEntertainment(models.Model):
    bill_id = models.AutoField(primary_key=True)
    bill_date = models.DateField()
    advance_amount = models.FloatField()
    discount_amount = models.FloatField()
    total_amount = models.FloatField()
    customer = models.ForeignKey(User, on_delete=models.RESTRICT)
    group_entertainment = models.ForeignKey(GroupEntertainment, on_delete=models.RESTRICT)


class BillOrder(models.Model):
    bill_id = models.AutoField(primary_key=True)
    bill_date = models.DateField()
    advance_amount = models.FloatField()
    discount_amount = models.FloatField()
    total_amount = models.FloatField()
    customer = models.ForeignKey(User, on_delete=models.RESTRICT)
    order = models.ForeignKey(Orders, on_delete=models.RESTRICT)


class BillTaxi(models.Model):
    bill_id = models.AutoField(primary_key=True)
    bill_date = models.DateField()
    advance_amount = models.FloatField()
    discount_amount = models.FloatField()
    total_amount = models.FloatField()
    customer = models.ForeignKey(User, on_delete=models.RESTRICT)
    trip = models.ForeignKey(Trip, on_delete=models.RESTRICT)


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    description = models.IntegerField()


class Delivery(models.Model):
    delivery_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Orders, on_delete=models.RESTRICT)
    price_for_delivery = models.FloatField()
    end_address = models.CharField(max_length=100)
    start_address = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.CharField(max_length=45)


class FeedbackAccompany(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)
    email = models.CharField(max_length=45)
    customer = models.ForeignKey(User, on_delete=models.RESTRICT)
    srv_accomp = models.ForeignKey(ServiceAccompany, on_delete=models.RESTRICT)
    bill_accomp = models.ForeignKey(BillAccomp, on_delete=models.RESTRICT)
    rating = models.IntegerField()


class FeedbackEnter(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)
    email = models.CharField(max_length=45)
    rating = models.IntegerField()
    customer = models.ForeignKey(User, on_delete=models.RESTRICT)
    bill_entertainment = models.ForeignKey(BillEntertainment, on_delete=models.RESTRICT)
    group_entertainment = models.ForeignKey(GroupEntertainment, on_delete=models.RESTRICT)


class FeedbackOrder(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    rating = models.IntegerField()
    customer = models.ForeignKey(User, on_delete=models.RESTRICT)
    bill_order = models.ForeignKey(BillOrder, on_delete=models.RESTRICT)
    order = models.ForeignKey(Orders, on_delete=models.RESTRICT)


class FeedbackProduct(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)
    email = models.CharField(max_length=45)
    customer = models.ForeignKey(User, on_delete=models.RESTRICT)
    product = models.ForeignKey(Products, on_delete=models.RESTRICT)
    rating = models.IntegerField()


class FeedbackTaxi(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)
    email = models.CharField(max_length=45)
    customer = models.ForeignKey(User, on_delete=models.RESTRICT)
    bill_taxi = models.ForeignKey(BillTaxi, on_delete=models.RESTRICT)
    trip = models.ForeignKey(Trip, on_delete=models.RESTRICT)

class Additionalls(models.Model):
    additionals_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=100)
    price_per_hour = models.FloatField()
    main_dis = models.ForeignKey('Disabilities', on_delete=models.RESTRICT, null=True)


class GroupEntertainmentDetails(models.Model):
    gr_enter_id = models.OneToOneField(GroupEntertainment, primary_key=True, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.RESTRICT)
    additionals = models.ForeignKey(Additionalls, on_delete=models.RESTRICT, null=True)
    pickup_address = models.CharField(max_length=100)
    amount = models.FloatField()


class AccompDisabilities(models.Model):
    accomp = models.OneToOneField(Accompanying, on_delete=models.RESTRICT, primary_key=True)
    disabilities = models.ForeignKey('Disabilities', on_delete=models.RESTRICT)
