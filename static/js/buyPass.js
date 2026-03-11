document.addEventListener('DOMContentLoaded', function() {

    const quantityDisplay = document.getElementById('quantityDisplay');
    const totalQuantity = document.getElementById('totalQuantity');
    const totalQuantity2 = document.getElementById('totalQuantity2');
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
        totalQuantity2.textContent = quantity;
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
        }
    });

    const paymentOptions = document.querySelectorAll('.payment-option');
    paymentOptions.forEach(option => {
        option.addEventListener('click', function() {
            paymentOptions.forEach(opt => opt.classList.remove('selected'));
            this.classList.add('selected');
        });
    });

    const modal = document.getElementById('paymentModal');
    const modalIcon = document.getElementById('modalIcon');
    const modalTitle = document.getElementById('modalTitle');
    const modalText = document.getElementById('modalText');

    function showProcessingModal() {
        modalIcon.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        modalTitle.textContent = 'Processing Payment';
        modalText.textContent = 'Please wait...';
        modal.style.display = 'flex';
    }

    function showSuccessModal() {
        modalIcon.innerHTML = '<i class="fas fa-check-circle"></i>';
        modalTitle.textContent = 'Payment Successful!';
        modalText.textContent = 'Your pass has been activated.';
        setTimeout(() => {
            modal.style.display = 'none';
            window.location.href = '/view_pass';
        }, 1500);
    }

    const payButton = document.getElementById('payButton');
    payButton.addEventListener('click', function () {

    const selectedOption = document.querySelector('.payment-option.selected');

    if (!selectedOption) {
        alert("Please select payment method");
        return;
    }

    const selectedPayment = selectedOption.dataset.payment;

    showProcessingModal();

    fetch("/purchase_pass", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            quantity: quantity,
            amount_per_pass: passPrice,
            service_fee: feePerPass,
            payment_method: selectedPayment
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Server error");
        }
        return response.json();
    })
    .then(data => {

        if (data.success) {
            showSuccessModal();
        } else {
            modalTitle.textContent = "Payment Failed";
            modalText.textContent = data.error;
        }

    })
    .catch(error => {
        console.error("Fetch error:", error);
        modalTitle.textContent = "Server Error";
        modalText.textContent = "Something went wrong";
    });

});
        
    });
