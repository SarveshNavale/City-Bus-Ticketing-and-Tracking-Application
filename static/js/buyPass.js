document.addEventListener('DOMContentLoaded', function() {
    // Quantity Selector
    const quantityDisplay = document.getElementById('quantityDisplay');
    const totalQuantity = document.getElementById('totalQuantity');
    const decreaseBtn = document.getElementById('decreaseQty');
    const increaseBtn = document.getElementById('increaseQty');
    const subtotal = document.getElementById('subtotal');
    const totalAmount = document.getElementById('totalAmount');
    const payAmount = document.getElementById('payAmount');
    const serviceFee = document.getElementById('serviceFee');
    
    let quantity = 1;
    const passPrice = 30.00;
    const feePerPass = 0.50;
    
    function updateTotals() {
        const calculatedSubtotal = quantity * passPrice;
        const calculatedFee = quantity * feePerPass;
        const calculatedTotal = calculatedSubtotal + calculatedFee;
        
        quantityDisplay.textContent = quantity;
        totalQuantity.textContent = quantity;
        subtotal.textContent = calculatedSubtotal.toFixed(2);
        serviceFee.textContent = calculatedFee.toFixed(2);
        totalAmount.textContent = calculatedTotal.toFixed(2);
        payAmount.textContent = calculatedTotal.toFixed(2);
    }
    decreaseBtn.addEventListener('click', function() {
        if (quantity > 1) {
            quantity--;
            updateTotals();
        }
    });
    increaseBtn.addEventListener('click', function() {
        if (quantity < 5) {
            quantity++;
            updateTotals();
        } else {
            alert('Maximum 5 passes per transaction');
        }
    });
    // Payment Option Selection
    const paymentOptions = document.querySelectorAll('.payment-option');
    paymentOptions.forEach(option => {
        option.addEventListener('click', function() {
            // Remove selected class from all options
            paymentOptions.forEach(opt => opt.classList.remove('selected'));
            // Add selected class to clicked option
            this.classList.add('selected');
        });
    });
     // Pay Button Functionality
    const payButton = document.getElementById('payButton');
    payButton.addEventListener('click', function() {
        const selectedPayment = document.querySelector('.payment-option.selected').dataset.payment;
        const totalPrice = parseFloat(totalAmount.textContent);
        
        alert(`Processing payment of ₹${totalPrice.toFixed(2)} via ${getPaymentMethodName(selectedPayment)}...\n\nYour pass will be activated immediately after successful payment.`);
    });
            
    function getPaymentMethodName(method) {
        switch(method) {
            case 'gpay': return 'Google Pay';
            case 'card': return 'Credit/Debit Card';
            case 'wallet': return 'Digital Wallet';
            default: return 'Selected Payment Method';
        }
    }
    // Ad Button
    const adBtn = document.querySelector('.ad-btn');
    adBtn.addEventListener('click', function() {
        alert('Redirecting to advertising information page...');
    });
    // Initialize totals
    updateTotals();
});