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
    const passPrice = 5.00;
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
        if (quantity < 10) {
            quantity++;
            updateTotals();
        } else {
            alert('Maximum 10 passes per transaction');
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
    // Initialize totals
    updateTotals();
});