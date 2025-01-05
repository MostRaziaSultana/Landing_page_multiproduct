# from .models import FeaturesSection, FAQ, BillingDetails, OrderDetails, Product,OrderItem
# from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
# from django.contrib import messages
# from django.http import JsonResponse
#
#
# def home(request):
#     sections = FeaturesSection.objects.prefetch_related('features').all()
#     faqs = FAQ.objects.all()
#     products = Product.objects.all()
#
#     def safe_float(value):
#         try:
#             return float(value)
#         except (ValueError, TypeError):
#             return 0.0
#
#     if request.GET.get('get_cart'):
#         return JsonResponse(request.session.get('cart', {}))
#
#     product_id = request.GET.get('product_id')
#
#     if request.GET.get('remove'):
#         product_id = request.GET.get('product_id')
#         if not product_id:
#             return HttpResponse("Product ID is missing", status=400)
#
#         cart = request.session.get('cart', {})
#         if product_id in cart:
#             del cart[product_id]
#             request.session['cart'] = cart
#             request.session.modified = True
#             messages.success(request, "Product removed from cart.")
#             return HttpResponse('Product removed from cart.')
#         else:
#             return HttpResponse("Product not found in cart.", status=404)
#
#     if request.GET.get('qty'):
#         product_id = request.GET.get('product_id')
#         if not product_id:
#             return HttpResponse("Product ID is missing", status=400)
#
#         cart = request.session.get('cart', {})
#
#         if product_id in cart:
#             # Safely update the quantity
#             cart[product_id]['quantity'] += 1
#             request.session['cart'] = cart
#             request.session.modified = True
#             print(cart[product_id]['quantity'])
#             return HttpResponse('Done')
#         else:
#             return HttpResponse("Product not found in cart", status=404)
#
#
#     if product_id:
#         product = get_object_or_404(Product, id=product_id)
#
#         if 'cart' not in request.session:
#             request.session['cart'] = {}
#
#         cart = request.session['cart']
#
#         if product_id not in cart:
#             cart[product_id] = {
#                 'title': product.title,
#                 'price': safe_float(product.discount_price or product.price),
#                 'image': product.image.url,
#                 'quantity': 1,
#             }
#             messages.success(request, f"Added {product.title} to cart.")
#         else:
#             cart[product_id]['quantity'] += 1
#
#         request.session['cart'] = cart
#         request.session.modified = True
#         return HttpResponse('Product added to cart.')
#
#     if 'order_now' in request.POST:
#         product_id = request.POST.get('product_id')
#         product = get_object_or_404(Product, id=product_id)
#
#         request.session['cart'] = {
#             product_id: {
#                 'title': product.title,
#                 'price': safe_float(product.discount_price or product.price),
#                 'image': product.image.url,
#                 'quantity': 1,
#             }
#         }
#         request.session.modified = True
#         return redirect('home')
#
#     if request.method == 'POST' and 'order_now' not in request.POST:
#         try:
#             name = request.POST.get('name')
#             phone_number = request.POST.get('phone')
#             city = request.POST.get('city')
#             address = request.POST.get('address')
#             shipping_cost = safe_float(request.POST.get('shipping_cost'))
#
#             cart = request.session.get('cart', {})
#
#             if not cart:
#                 messages.error(request, "Your cart is empty.")
#                 return redirect('home')
#
#             billing_details = BillingDetails.objects.create(
#                 name=name,
#                 phone_number=phone_number,
#                 city=city,
#                 address=address
#             )
#
#             subtotal = sum(item['price'] * item['quantity'] for item in cart.values())
#             total = subtotal + shipping_cost
#
#             order = OrderDetails.objects.create(
#                 shipping_cost=shipping_cost,
#                 subtotal=subtotal,
#                 total=total,
#                 billing_details=billing_details,
#                 payment_method='Cash on Delivery'
#             )
#
#             for product_id, product_data in cart.items():
#                 product = get_object_or_404(Product, id=product_id)
#                 total_price = safe_float(product_data['price']) * product_data['quantity']
#                 OrderItem.objects.create(
#                     order=order,
#                     product=product,
#                     quantity=product_data['quantity'],
#                     total_price=total_price,
#                 )
#
#             request.session['cart'] = {}
#             messages.success(request, "Order created successfully!")
#             return redirect('home')
#
#         except Exception as e:
#             messages.error(request, f"An error occurred: {str(e)}")
#             return redirect('home')
#
#     cart = request.session.get('cart', {})
#     return render(request, 'base.html', {
#         'sections': sections,
#         'products': products,
#         'faqs': faqs,
#         'cart': cart,
#     })


from .models import FeaturesSection, FAQ, BillingDetails, OrderDetails, Product, OrderItem
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib import messages


def home(request):
    # Load static data
    sections = FeaturesSection.objects.prefetch_related('features').all()
    faqs = FAQ.objects.all()
    products = Product.objects.all()

    product_id = request.GET.get('product_id')

    def safe_float(value):
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    if request.GET.get('get_cart'):
        return JsonResponse(request.session.get('cart', {}))

    if request.GET.get('remove'):
        product_id = request.GET.get('product_id')
        if not product_id:
            return HttpResponse("Product ID is missing", status=400)

        cart = request.session.get('cart', {})
        if product_id in cart:
            del cart[product_id]
            request.session['cart'] = cart
            request.session.modified = True
            messages.success(request, "Product removed from cart.")
            return HttpResponse('Product removed from cart.')
        else:
            return HttpResponse("Product not found in cart.", status=404)

    if request.GET.get('qty'):
        product_id = request.GET.get('product_id')
        change = int(request.GET.get('change', 0))
        if not product_id:
            return HttpResponse("Product ID is missing", status=400)

        cart = request.session.get('cart', {})
        if product_id in cart:
            cart[product_id]['quantity'] += change
            request.session['cart'] = cart
            request.session.modified = True
            return HttpResponse('Quantity updated.')
        else:
            return HttpResponse("Product not found in cart.", status=404)

    if product_id:
        product = get_object_or_404(Product, id=product_id)

        if 'cart' not in request.session:
            request.session['cart'] = {}

        cart = request.session['cart']

        if product_id not in cart:
            cart[product_id] = {
                'title': product.title,
                'price': safe_float(product.discount_price or product.price),
                'image': product.image.url,
                'quantity': 1,
            }
        else:
            cart[product_id]['quantity'] += 1

        request.session['cart'] = cart
        request.session.modified = True
        return HttpResponse('Product added to cart.')

    if 'order_now' in request.POST:
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        request.session['cart'] = {
            product_id: {
                'title': product.title,
                'price': safe_float(product.discount_price or product.price),
                'image': product.image.url,
                'quantity': 1,
            }
        }
        request.session.modified = True
        return redirect('home')

    if request.method == 'POST' and 'order_now' not in request.POST:
        try:
            name = request.POST.get('name')
            phone_number = request.POST.get('phone')
            city = request.POST.get('city')
            address = request.POST.get('address')
            shipping_cost = safe_float(request.POST.get('shipping'))
            if shipping_cost == 0.0:
                messages.error(request, "Please select a valid shipping option.")
                return redirect('home')

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

            subtotal = sum(safe_float(item['price']) * item['quantity'] for item in cart.values())
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
                total_price = safe_float(product_data['price']) * product_data['quantity']
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=product_data['quantity'],
                    total_price=total_price,
                )

            # Clear cart and confirm success
            request.session['cart'] = {}
            messages.success(request, "Order created successfully!")
            return redirect('home')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('home')

    # Retrieve cart data for rendering
    cart = request.session.get('cart', {})
    return render(request, 'base.html', {
        'sections': sections,
        'products': products,
        'faqs': faqs,
        'cart': cart,
    })
