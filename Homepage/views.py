from .models import FeaturesSection, FAQ, BillingDetails, OrderDetails, Product,OrderItem
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages


def home(request):
    sections = FeaturesSection.objects.prefetch_related('features').all()
    faqs = FAQ.objects.all()
    products = Product.objects.all()

    product_id = request.GET.get('product_id')

    if request.GET.get('qty'):
        product_id = request.GET.get('product_id')
        if not product_id:
            return HttpResponse("Product ID is missing", status=400)

        cart = request.session.get('cart', {})

        if product_id in cart:
            # Safely update the quantity
            cart[product_id]['quantity'] += 1
            request.session['cart'] = cart
            request.session.modified = True
            print(cart[product_id]['quantity'])
            return HttpResponse('Done')
        else:
            return HttpResponse("Product not found in cart", status=404)


    if product_id:
        product = get_object_or_404(Product, id=product_id)

        if 'cart' not in request.session:
            request.session['cart'] = {}

        cart = request.session['cart']

        if product_id not in cart:
            cart[product_id] = {
                'title': product.title,
                'price': float(product.discount_price or product.price),
                'image': product.image.url,
                'quantity': 1,
            }
            messages.success(request, f"Added {product.title} to cart.")
        else:
            # cart[product_id]['quantity'] += 1
            # cart[product_id]['total_price'] = cart[product_id]['price'] * cart[product_id]['quantity']
            # messages.info(request, f"{product.title} quantity increased.")
            messages.warning(request, f"{product.title} is already in your cart.")

        request.session['cart'] = cart
        return redirect('home')

    if 'order_now' in request.POST:
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        if 'cart' not in request.session:
            request.session['cart'] = {}

        cart = request.session['cart']

        if product_id not in cart:
            cart[product_id] = {
                'title': product.title,
                'price': float(product.discount_price or product.price),
                'image': product.image.url,
                'quantity': 1,
            }
            messages.success(request, f"Added {product.title} to cart.")
        else:
            cart[product_id]['quantity'] += 1
            messages.info(request, f"{product.title} quantity increased.")

        request.session['cart'] = cart
        return redirect('home')

    if request.method == 'POST' and 'order_now' not in request.POST:
        try:
            name = request.POST.get('name')
            phone_number = request.POST.get('phone')
            city = request.POST.get('city')
            address = request.POST.get('address')
            shipping_cost = float(request.POST.get('shipping_cost'))

            cart = request.session.get('cart', {})

            if not cart:
                messages.error(request, "Your cart is empty.")
                return redirect('home')

            billing_details = BillingDetails.objects.create(
                name=name,
                phone_number=phone_number,
                city=city,
                address=address
            )

            subtotal = sum(item['price'] * item['quantity'] for item in cart.values())
            total = subtotal + shipping_cost

            order = OrderDetails.objects.create(
                shipping_cost=shipping_cost,
                subtotal=subtotal,
                total=total,
                billing_details=billing_details,
                payment_method='Cash on Delivery'
            )

            for product_id, product_data in cart.items():
                product = get_object_or_404(Product, id=product_id)
                total_price = float(product_data['price']) * product_data['quantity']
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=product_data['quantity'],
                    total_price=total_price,
                )

            request.session['cart'] = {}
            messages.success(request, "Order created successfully!")
            return redirect('home')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('home')

    cart = request.session.get('cart', {})
    return render(request, 'base.html', {
        'sections': sections,
        'products': products,
        'faqs': faqs,
        'cart': cart,
    })
