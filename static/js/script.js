//    <!-- Shipping cost logic -->
//
//
//
//      function changeQuantity(change) {
//        const quantityInput = document.getElementById("quantity");
//        const pricePerItem = parseFloat(document.getElementById("price").dataset.price); // Get price per item
//        const subtotalElement = document.getElementById("subtotal");
//
//        // Update quantity value
//        let quantity = parseInt(quantityInput.value) + change;
//        if (quantity < 1) quantity = 1; // Ensure quantity is at least 1
//        quantityInput.value = quantity;
//
//        // Update subtotal
//        const subtotal = pricePerItem * quantity;
//        subtotalElement.textContent = `${subtotal} Tk`;
//
//        // Update total
//        updateTotal();
//    }
//
//    function updateTotal() {
//        const subtotalElement = document.getElementById("subtotal");
//        const totalElement = document.getElementById("total");
//        const submitButton = document.getElementById("submit-button");
//        const shippingOption = document.querySelector("input[name='shipping']:checked");
//
//        // Get subtotal value
//        const subtotal = parseFloat(subtotalElement.textContent.split(" ")[0]);
//
//        if (shippingOption) {
//            // Add shipping cost if a shipping option is selected
//            const shippingCost = parseFloat(shippingOption.value);
//            const total = subtotal + shippingCost;
//            totalElement.textContent = `${total} Tk`;
//
//            // Enable submit button
//            submitButton.disabled = false;
//        } else {
//            // No shipping option selected
//            totalElement.textContent = `${subtotal} Tk`;
//
//            // Disable submit button
//            submitButton.disabled = true;
//        }
//    }
//
//    // Event listeners for shipping option changes
//    document.querySelectorAll("input[name='shipping']").forEach((radio) => {
//        radio.addEventListener("change", updateTotal);
//    });
//
//    // Initially disable the submit button
//    document.getElementById("submit-button").disabled = true;
//
//
//
//
//
//    function increaseQuantity() {
//        let quantityInput = document.getElementById('quantity');
//        quantityInput.value = parseInt(quantityInput.value) + 1;
//    }
//
//    function decreaseQuantity() {
//        let quantityInput = document.getElementById('quantity');
//        let currentValue = parseInt(quantityInput.value);
//        if (currentValue > 1) {
//            quantityInput.value = currentValue - 1;
//        }
//    }



//=========FAQ===========
function toggleAnswer(button) {
    const answer = button.nextElementSibling;
    const isVisible = answer.style.display === "block";
    answer.style.display = isVisible ? "none" : "block";
    button.setAttribute("aria-expanded", !isVisible);
}



//+++++++++quantity========


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


function updateSubtotalAndTotal() {
  let subtotal = 0;

  document.querySelectorAll('[id^="total_price_"]').forEach((totalPriceElement) => {
    const totalPrice = parseFloat(totalPriceElement.innerText.replace(' Tk', ''));
    subtotal += totalPrice;
  });

  const subtotalElement = document.getElementById("subtotal");
  subtotalElement.innerText = `${subtotal.toFixed(2)} Tk`;

  const selectedShipping = document.querySelector('input[name="shipping"]:checked');
  const shippingCost = selectedShipping ? parseFloat(selectedShipping.value) : 0;

  const total = subtotal + shippingCost;
  const totalElement = document.getElementById("total");
  totalElement.innerText = `${total.toFixed(2)} Tk`;

  toggleSubmitButton();
}

// Function to enable or disable the submit button based on shipping selection
function toggleSubmitButton() {
  const selectedShipping = document.querySelector('input[name="shipping"]:checked');
  const submitButton = document.getElementById("submit-button");
  submitButton.disabled = !selectedShipping;
}

function attachShippingListeners() {
  document.querySelectorAll('input[name="shipping"]').forEach((radio) => {
    radio.addEventListener("change", updateSubtotalAndTotal);
  });
}

function getCSRFToken() {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
  return csrfToken ? csrfToken.value : "";
}

document.addEventListener("DOMContentLoaded", () => {
  updateSubtotalAndTotal();
  attachShippingListeners();
});


// Function for add to cart
function addToCart(productId) {
    fetch(`?product_id=${productId}`, {
        method: 'GET',
    })
        .then((response) => {
            if (response.ok) {
                return response.text();
            } else {
                throw new Error('Failed to add product to cart.');
            }
        })
        .then(() => {
            updateCartUI(productId);
        })
        .catch((error) => console.error('Error:', error));
}

function updateCartUI(productId) {
    const quantityInput = document.getElementById(`quantity_${productId}`);
    const totalPriceElement = document.getElementById(`total_price_${productId}`);
    const pricePerUnit = parseFloat(totalPriceElement.dataset.price);

    if (quantityInput) {
        const currentQuantity = parseInt(quantityInput.value, 10) || 0;
        const newQuantity = currentQuantity + 1;
        quantityInput.value = newQuantity;

        if (totalPriceElement) {
            totalPriceElement.innerText = `${(pricePerUnit * newQuantity).toFixed(2)} Tk`;
        }
    } else {
        fetch('?get_cart=true', {
            method: 'GET',
        })
            .then((response) => response.json())
            .then((cart) => {
                if (cart[productId]) {
                    const cartContainer = document.querySelector('.order-details .details tbody');
                    const productData = cart[productId];
                    const row = `
                        <tr>
                            <td>
                                <div style="display: flex; align-items: center">
                                    <img src="${productData.image}" alt="product-img" style="width: 30px; height: 30px; margin-right: 10px" />
                                    <span>${productData.title}</span>
                                </div>
                            </td>
                            <td>
                                <span id="total_price_${productId}" data-price="${productData.price}">${productData.price} Tk</span>
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
                }
            })
            .catch((error) => console.error('Error updating cart UI:', error));
    }

    updateSubtotalAndTotal();
}


  // Toggle for display chat button
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



