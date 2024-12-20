from .models import FeaturesSection,Feature,FAQ,BillingDetails,OrderDetails,Product
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.

def home(request):
    sections = FeaturesSection.objects.prefetch_related('features').all()
    faqs = FAQ.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone')
        city = request.POST.get('city')
        address = request.POST.get('address')

        billing_details = BillingDetails.objects.create(
            name=name,
            phone_number=phone_number,
            city=city,
            address=address
        )

        product_id = float(request.POST.get('product_id'))
        quantity = float(request.POST.get('quantity'))
        product = Product.objects.get(id=product_id)
        print(product_id,quantity)


        product_price = product.discount_price if product.discount_price else product.price
        subtotal = float(product_price) * quantity
        print(request.POST.get('shipping_cost'))
        shipping_cost = float(request.POST.get('shipping_cost'))
        total = subtotal + shipping_cost

        order_details = OrderDetails.objects.create(
            product_name=product.title,
            product_price=product_price,
            quantity=quantity,
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            total=total,
            billing_details=billing_details,
            payment_method='Cash on Delivery'
        )
        messages.success(request, "Order created successfully!")
        return redirect('home')

    else:
        products = Product.objects.all()

    return render(request, 'base.html', {
        'sections': sections,
        'products': products,
        'faqs': faqs,
    })
