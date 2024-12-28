from .models import FeaturesSection, FAQ, BillingDetails, OrderDetails, Product
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

def home(request):
    sections = FeaturesSection.objects.prefetch_related('features').all()
    faqs = FAQ.objects.all()
    products = Product.objects.all()

    # Initialize the cart in session if not present
    if 'cart' not in request.session:
        request.session['cart'] = {}

    cart = request.session['cart']

    # Handle "Add to Cart" functionality via GET request
    product_id = request.GET.get('product_id')
    if product_id:
        product = get_object_or_404(Product, id=product_id)

        # Add product to cart or increase quantity
        if product_id in cart:
            cart[product_id]['quantity'] += 1
            cart[product_id]['total_price'] = cart[product_id]['quantity'] * cart[product_id]['price']
            messages.success(request, f"Increased quantity of {product.title}.")
        else:
            cart[product_id] = {
                'title': product.title,
                'price': float(product.discount_price or product.price),
                'image': product.image.url,
                'quantity': 1,
                'total_price': float(product.discount_price or product.price),
            }
            messages.success(request, f"Added {product.title} to cart.")

        # Save the updated cart to session
        request.session['cart'] = cart
        return redirect('home')

    # Handle increase or decrease quantity via GET request
    action = request.GET.get('action')
    if action and product_id:
        product_id = str(product_id)
        if product_id in cart:
            if action == 'increase':
                cart[product_id]['quantity'] += 1
                cart[product_id]['total_price'] = cart[product_id]['quantity'] * cart[product_id]['price']
                messages.success(request, f"Increased quantity of {cart[product_id]['title']}.")
            elif action == 'decrease':
                if cart[product_id]['quantity'] > 1:
                    cart[product_id]['quantity'] -= 1
                    cart[product_id]['total_price'] = cart[product_id]['quantity'] * cart[product_id]['price']
                    messages.success(request, f"Decreased quantity of {cart[product_id]['title']}.")
                else:
                    product_title = cart[product_id]['title']
                    del cart[product_id]
                    messages.info(request, f"Removed {product_title} from the cart.")

            request.session['cart'] = cart
        return redirect('home')

    # Handle "Checkout" functionality via POST request
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            phone_number = request.POST.get('phone')
            city = request.POST.get('city')
            address = request.POST.get('address')
            shipping_cost = float(request.POST.get('shipping_cost'))

            # Retrieve cart from session
            if not cart:
                messages.error(request, "Your cart is empty.")
                return redirect('home')

            # Create BillingDetails
            billing_details = BillingDetails.objects.create(
                name=name,
                phone_number=phone_number,
                city=city,
                address=address
            )

            # Calculate subtotal and total
            subtotal = sum(item['total_price'] for item in cart.values())
            total = subtotal + shipping_cost

            # Create OrderDetails for each product in the cart
            for product_id, product_data in cart.items():
                product = Product.objects.get(id=product_id)

                OrderDetails.objects.create(
                    product_name=product.title,
                    product_price=product_data['price'],
                    quantity=product_data['quantity'],
                    subtotal=subtotal,
                    shipping_cost=shipping_cost,
                    total=total,
                    billing_details=billing_details,
                    payment_method='Cash on Delivery'
                )

            # Clear the cart after successful checkout
            request.session['cart'] = {}
            messages.success(request, "Order created successfully!")
            return redirect('home')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('home')

    return render(request, 'base.html', {
        'sections': sections,
        'products': products,
        'faqs': faqs,
        'cart': cart,
    })

