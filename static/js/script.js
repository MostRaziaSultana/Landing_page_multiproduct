//=========FAQ===========
function toggleAnswer(button) {
    const answer = button.nextElementSibling;
    const isVisible = answer.style.display === "block";
    answer.style.display = isVisible ? "none" : "block";
    button.setAttribute("aria-expanded", !isVisible);
}



//+++++++++quantity========


//function changeQuantity(productId, change) {
//  const quantityInput = document.getElementById(`quantity_${productId}`);
//  let currentQuantity = parseInt(quantityInput.value, 10);
//
//  const newQuantity = currentQuantity + change;
//
//  if (newQuantity < 1) {
//    removeProduct(productId);
//    return;
//  }
//
//  quantityInput.value = newQuantity;
//
//  const pricePerUnitElement = document.getElementById(`total_price_${productId}`);
//
//  if (!pricePerUnitElement) {
//    console.error(`Price per unit element not found for product ID: ${productId}`);
//    return;
//  }
//
//  const pricePerUnit = parseFloat(pricePerUnitElement.dataset.price);
//
//  const totalPriceElement = document.getElementById(`total_price_${productId}`);
//  if (totalPriceElement) {
//    totalPriceElement.innerText = `${(pricePerUnit * newQuantity).toFixed(2)} Tk`;
//  }
//
//  updateSubtotalAndTotal();
//
//  fetch(`?qty=true&product_id=${productId}&change=${change}`)
//    .then((res) => res.text())
//    .then(console.log)
//    .catch(console.error);
//}
//
//
//function updateSubtotalAndTotal() {
//  let subtotal = 0;
//
//  document.querySelectorAll('[id^="total_price_"]').forEach((totalPriceElement) => {
//    const totalPrice = parseFloat(totalPriceElement.innerText.replace(' Tk', ''));
//    subtotal += totalPrice;
//  });
//
//  const subtotalElement = document.getElementById("subtotal");
//  subtotalElement.innerText = `${subtotal.toFixed(2)} Tk`;
//
//  const selectedShipping = document.querySelector('input[name="shipping"]:checked');
//  const shippingCost = selectedShipping ? parseFloat(selectedShipping.value) : 0;
//
//  const total = subtotal + shippingCost;
//  const totalElement = document.getElementById("total");
//  totalElement.innerText = `${total.toFixed(2)} Tk`;
//
//  toggleSubmitButton();
//}
//
//// Function to enable or disable the submit button based on shipping selection
//function toggleSubmitButton() {
//  const selectedShipping = document.querySelector('input[name="shipping"]:checked');
//  const submitButton = document.getElementById("submit-button");
//  submitButton.disabled = !selectedShipping;
//}
//
//function attachShippingListeners() {
//  document.querySelectorAll('input[name="shipping"]').forEach((radio) => {
//    radio.addEventListener("change", updateSubtotalAndTotal);
//  });
//}
//
//function getCSRFToken() {
//  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
//  return csrfToken ? csrfToken.value : "";
//}
//
//document.addEventListener("DOMContentLoaded", () => {
//  updateSubtotalAndTotal();
//  attachShippingListeners();
//});


function addToCart(productId) {
    fetch(`?product_id=${productId}`, {
        method: 'GET',
    })
        .then((response) => {
            if (response.ok) {
                return response.json(); // Parse the JSON response
            } else {
                throw new Error('Failed to add product to cart.');
            }
        })
        .then((cart) => {
            syncCartUI(cart); // Update the cart UI dynamically
        })
        .catch((error) => console.error('Error:', error));
}

function changeQuantity(productId, change) {
    const quantityInput = document.getElementById(`quantity_${productId}`);
    let currentQuantity = parseInt(quantityInput.value, 10);

    const newQuantity = currentQuantity + change;

    if (newQuantity < 1) {
        removeProduct(productId);
        return;
    }

    quantityInput.value = newQuantity;

    const pricePerUnitElement = document.getElementById(`total_price_${productId}`);

    if (!pricePerUnitElement) {
        console.error(`Price per unit element not found for product ID: ${productId}`);
        return;
    }

    const pricePerUnit = parseFloat(pricePerUnitElement.dataset.price);

    const totalPriceElement = document.getElementById(`total_price_${productId}`);
    if (totalPriceElement) {
        totalPriceElement.innerText = `${(pricePerUnit * newQuantity).toFixed(2)} Tk`;
    }

    updateSubtotalAndTotal();

    fetch(`?qty=true&product_id=${productId}&change=${change}`)
        .then((res) => res.text())
        .then(console.log)
        .catch(console.error);
}

function syncCartUI(cart) {
    const cartContainer = document.querySelector('.order-details .details tbody');
    cartContainer.innerHTML = ''; // Clear existing cart UI

    // Add cart items
    Object.entries(cart).forEach(([productId, productData]) => {
        const row = `
            <tr>
                <td>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <button type="button" class="remove-button" onclick="removeProduct('${productId}')" style="padding: 4px 8px; background-color: #088178; color: white; border: none; border-radius: 3px; cursor: pointer;">
                            <i class="fas fa-times"></i>
                        </button>
                        <img src="${productData.image}" alt="product-img" style="width: 30px; height: 30px; margin-right: 10px" />
                        <span>${productData.title}</span>
                    </div>
                </td>
                <td>
                    <span id="total_price_${productId}" data-price="${productData.price}">${(productData.price * productData.quantity).toFixed(2)} Tk</span>
                </td>
            </tr>
            <tr>
                <td>Quantity</td>
                <td>
                    <div class="quantity-container">
                        <button type="button" class="quantity-button decrement" onclick="changeQuantity('${productId}', -1)">-</button>
                        <input type="text" name="quantity_${productId}" id="quantity_${productId}" value="${productData.quantity}" class="quantity-input" readonly />
                        <button type="button" class="quantity-button increment" onclick="changeQuantity('${productId}', 1)">+</button>
                    </div>
                </td>
            </tr>
        `;
        cartContainer.innerHTML += row;
    });

    // Add subtotal, shipping, and total rows
    const summaryRows = `
        <tr>
            <td>Subtotal</td>
            <td id="subtotal">0 Tk</td>
        </tr>
        <tr>
            <td>Shipping</td>
            <td>
                <div class="radio-group">
                    <div class="radio-item">
                        <input type="radio" name="shipping" value="50" onchange="updateSubtotalAndTotal()" />
                        <label class="radio-title">ঢাকার ভিতরে: 50 Tk</label>
                    </div>
                    <div class="radio-item">
                        <input type="radio" name="shipping" value="100" onchange="updateSubtotalAndTotal()" />
                        <label class="radio-title">ঢাকার বাহিরে: 100 Tk</label>
                    </div>
                </div>
            </td>
        </tr>
        <tr>
            <td>Total</td>
            <td id="total">0 Tk</td>
        </tr>
    `;
    cartContainer.innerHTML += summaryRows;

    // Recalculate totals after adding rows
    updateSubtotalAndTotal();
}

function updateSubtotalAndTotal() {
    let subtotal = 0;

    document.querySelectorAll('[id^="total_price_"]').forEach((totalPriceElement) => {
        const totalPrice = parseFloat(totalPriceElement.innerText.replace(' Tk', '')) || 0;
        subtotal += totalPrice;
    });

    const subtotalElement = document.getElementById('subtotal');
    const totalElement = document.getElementById('total');
    subtotalElement.innerText = `${subtotal.toFixed(2)} Tk`;

    const selectedShipping = document.querySelector('input[name="shipping"]:checked');
    const shippingCost = selectedShipping ? parseFloat(selectedShipping.value) : 0;

    const total = subtotal + shippingCost;
    totalElement.innerText = `${total.toFixed(2)} Tk`;

    toggleSubmitButton();
}

function toggleSubmitButton() {
    const selectedShipping = document.querySelector('input[name="shipping"]:checked');
    const submitButton = document.getElementById('submit-button');
    submitButton.disabled = !selectedShipping;
}

function attachShippingListeners() {
    document.querySelectorAll('input[name="shipping"]').forEach((radio) => {
        radio.addEventListener('change', updateSubtotalAndTotal);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    updateSubtotalAndTotal();
    attachShippingListeners();
});





  // Toggle the display of chat buttons
function toggleChatButtons() {
    var chatButtons = document.querySelector('.chat-buttons');
    if (chatButtons.style.display === 'none' || chatButtons.style.display === '') {
        chatButtons.style.display = 'flex';
        chatButtons.classList.add('slide-in');
    } else {
        chatButtons.style.display = 'none';
        chatButtons.classList.remove('slide-in');
    }
}



