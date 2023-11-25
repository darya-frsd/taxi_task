from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import Address, Taxi, Driver, TripDetails, User, Disabilities, UserDisabilities, OrderStatuses
from .forms import CustomUserCreationForm
from .models import Address, Taxi, Driver, TripDetails, User, Products, OrderDetails, Orders, CartItem
import json
from django.http import JsonResponse
from django.utils import timezone
from .forms import CustomUserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import CartItem

def delete_cart_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        try:
            cart_item = CartItem.objects.get(id=item_id)
            cart_item.delete()
            return JsonResponse({'message': 'Item deleted successfully'})
        except CartItem.DoesNotExist:
            return JsonResponse({'message': 'Item not found'}, status=404)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)

def get_cart_items(request):
    cart_items = CartItem.objects.all()
    data = []

    for item in cart_items:
        product = Products.objects.get(name=item.product)
        price = product.price if product else 0

        data.append({
            'id': item.id,
            'product': item.product,
            'price': price,
        })

    return JsonResponse(data, safe=False)


def buy_product(request, product_id):
    product = get_object_or_404(Products, product_id=product_id)

    cart_item, created = CartItem.objects.get_or_create(product=product.name, purchased=False)
    cart_item.purchased = True
    cart_item.save()

    return redirect('equipment_page')


def cart_page(request):
    user_cart, created = OrderStatuses.objects.get_or_create(status_id=1, description=request.user.id)
    purchased_items = user_cart.products.all()

    return render(request, 'your_cart_template.html', {'purchased_items': purchased_items})


def rent_product(request, product_id):
    product = Products.objects.get(pk=product_id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def search_results(request):
    return render(request, 'search_results.html')


def account(request):
    return render(request, 'account.html')


def last_trip_detail(request):
    dict_sample = {1: 'Адаптивный такси', 2: 'Автобус', 3: 'Групповой транспорт'}

    last_trip_detail = TripDetails.objects.last()
    taxi = Taxi.objects.get(pk=last_trip_detail.taxi_id).registration_number
    driver = (Driver.objects.get(pk=last_trip_detail.driver_id).first_name + " "
              + Driver.objects.get(pk=last_trip_detail.driver_id).last_name)
    data = {
        'trip_id': last_trip_detail.trip_id,
        'amount': last_trip_detail.amount,
        'start_time': last_trip_detail.start_time,
        'start_address': last_trip_detail.start_address,
        'end_address': last_trip_detail.end_address,
        'service_type_id': dict_sample[last_trip_detail.service_type_id],
        'taxi_id': taxi,
        'driver_id': driver
    }
    return JsonResponse(data)


def update_taxi_type(request, taxi_id, taxi_type):
    try:
        taxi = Taxi.objects.get(taxi_id=taxi_id)
        taxi.taxi_type_id = taxi_type
        taxi.save()
        return JsonResponse({'success': True})
    except Taxi.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Такси не найдено'})


def save_trip_amount(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')  # Save pickup_address value
        customer_id = 1
        customer = User.objects.get(pk=customer_id)
        dict_sample = {1: 'Адаптивный такси', 2: 'Автобус', 3: 'Групповой транспорт'}

        model = Taxi.objects.get(pk=1)
        x = model.taxi_type_id
        taxi_type = dict_sample[model.taxi_type_id]
        matching_taxis = Taxi.objects.filter(model=taxi_type, status=1)
        nearby_drivers = []
        for taxi in matching_taxis:
            nearby_drivers.append(Driver.objects.get(driver_id=taxi.driver_id))
        driver = nearby_drivers[0]
        taxi = Taxi.objects.get(driver_id=driver)
        all_addresses = Address.objects.all()

        start_time = timezone.now()
        end_time = timezone.now()

        address1 = Address.objects.get(pk=len(all_addresses) - 2)
        address2 = Address.objects.get(pk=len(all_addresses) - 1)
        location = address1.location
        end_address = address2.location

        trip_details = TripDetails.objects.create(
            amount=amount,
            start_time=start_time,
            end_time=end_time,
            start_address=location,
            end_address=end_address,
            service_type_id=x,
            taxi=taxi,
            driver=driver
        )

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'})


def get_matching_drivers(request):
    if request.method == 'POST':
        dict_sample = {1: 'Адаптивный такси', 2: 'Автобус', 3: 'Групповой транспорт'}
        customer_id = 1

        model = Taxi.objects.get(pk=1)
        taxi_type = dict_sample[model.taxi_type_id]
        matching_taxis = Taxi.objects.filter(model=taxi_type, status=1)
        nearby_drivers = []
        last_trip_details = TripDetails.objects.last()
        taxiw = Taxi.objects.get(pk=last_trip_details.taxi_id).registration_number
        driver = (Driver.objects.get(pk=last_trip_details.driver_id).first_name + " "
                  + Driver.objects.get(pk=last_trip_details.driver_id).last_name)

        for taxi in matching_taxis:
            try:
                nearby_drivers.append(Driver.objects.get(driver_id=taxi.driver_id))
            except Driver.DoesNotExist:
                pass

        response_data = {
            'id': last_trip_details.trip_id,
            'name': driver,
            'carNumber': taxiw
        }

        return JsonResponse(response_data, safe=False)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def save_coordinates(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            location = data.get('location')
            coordinates = data.get('coordinates')

            print(f'Местоположение: {location}, Координаты: {coordinates}')

            if location and coordinates and len(coordinates) == 2:
                address = Address(
                    location=location,
                    latitude=coordinates[0],
                    longitude=coordinates[1],
                )
                address.save()

                return JsonResponse({'status': 'success', 'message': 'Координаты успешно получены и сохранены'})
            else:
                raise ValueError('Неверные или отсутствующие данные в запросе')

        except Exception as e:
            print(f'Ошибка при обработке координат: {str(e)}')
            return JsonResponse({'status': 'error', 'message': f'Ошибка при обработке координат: {str(e)}'})

    return JsonResponse({'status': 'error', 'message': 'Неверный метод запроса'})


def pickup_submit(request):
    if request.method == 'POST':
        pickup_address = request.POST.get('pickup_address')
        address = Address.objects.create(location=pickup_address)

    return redirect('index')


def destination_submit(request):
    if request.method == 'POST':
        destination_address = request.POST.get('destination_address')
        address = Address.objects.create(location=destination_address)

    return redirect('index')


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


class CustomLogoutView(LogoutView):
    pass


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


def index(request):
    context = {
        'products': ['Перевозка', 'Доставка товаров', 'Развлечения'],
    }
    return render(request, 'taxi_app/index.html')


def order_page(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pickup_location = data.get('location')
            destination_location = data.get('location')
            pickup_coordinates = [43.22984785, 76.90109223280969]
            destination_coordinates = [43.22851695, 76.89760375324497]

        except Exception as e:
            print(f'Ошибка при обработке заказа: {str(e)}')

    return render(request, 'taxi_app/order_page.html')


def get_coordinates_for_location(location):
    try:
        address = Address.objects.get(location=location)
        return [address.latitude, address.longitude]
    except Address.DoesNotExist:
        print(f'Местоположение {location} не найдено в базе данных')
        return None


def medicine_page(request):
    return render(request, 'taxi_app/medicine_page.html')


def equipment_page(request):
    return render(request, 'taxi_app/equipment_page.html')


def nutrition_page(request):
    return render(request, 'taxi_app/nutrition_page.html')


def taxi_page(request):
    return render(request, 'taxi_app/taxi_page.html')


def account_page(request):
    return render(request, 'taxi_app/account_page.html')

def cart(request):
    return render(request, 'taxi_app/cart.html')


def account(request):
    return render(request, 'account.html')

def logout_view(request):
    logout(request)
    return redirect('logout_page')


def logout_page(request):
    return render(request, 'taxi_app/logout_page.html')


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm


class CustomSignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = '/login/'

def feedback(request):
    return render(request, 'taxi_app/feedback.html')



def start_page(request):
    return render(request, 'taxi_app/start_page.html')


def cart(request):
    return render(request, 'taxi_app/cart.html')


def save_profile(request):
    user_id = 1

    disabilities_ids = [1, 2, 3]


    # for disability_id in disabilities_ids:
    #     disability = get_object_or_404(Disabilities, disabilities_id=disability_id)
    #
    #     user_disabilities, created = UserDisabilities.objects.get_or_create(
    #         user_id=user_id,
    #         defaults={'disabilities': disability}
    #     )

    return render(request, 'your_template.html', {'user_disabilities': user_disabilities, 'created': created})


def profile(request):
    user_id = 1
    user = User.objects.get(pk=user_id)
    return render(request, 'profile.html', {'user': user})
