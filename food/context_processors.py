from food.models import CustomUser, MenuItems, OrderItems, Basket, Notification

def orders(request):
    try:
        cust = CustomUser.objects.get(email=request.user)
        basket = Basket.objects.filter(customer_id = cust, status = 'Waiting').first()
        price = 0
        for items in OrderItems.objects.filter(basket_id=basket):
            price += items.price
        return {
            'orders':OrderItems.objects.filter(basket_id=basket),
            'total':price
        }
    except:
        return {}

def notifications(request):
    allnotifications = Notification.objects.all()
    return {'notification':allnotifications}
