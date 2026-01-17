document.addEventListener('DOMContentLoaded', function() {
    checkLoginStatusOnLoad();
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
            paymentOptions.forEach(opt => opt.classList.remove('selected'));
            this.classList.add('selected');
        });
    });
    
    // Pay Button Functionality
    const payButton = document.getElementById('payButton');
    payButton.addEventListener('click', async function() {
        const isLoggedIn = await checkLoginStatus();
        if (!isLoggedIn) {
            return;
        }
        
        const selectedPayment = document.querySelector('.payment-option.selected').dataset.payment;
        const totalPrice = parseFloat(totalAmount.textContent);
        
        payButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
        payButton.disabled = true;
        
        try {
            const response = await fetch('/purchase_pass', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    quantity: quantity,
                    amount_per_pass: passPrice,
                    service_fee: feePerPass,
                    payment_method: selectedPayment,
                    total_amount: totalPrice
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                alert(`Pass Purchase Successful!\n\n` +
                      `Pass Holder: ${result.details.pass_holder}\n` +
                      `Mobile: ${result.details.mobile_no}\n` +
                      `Pass Number(s): ${result.details.pass_numbers.join(', ')}\n` +
                      `Amount Paid: ₹${result.details.total_amount.toFixed(2)}\n\n` +
                      `Your pass(es) have been activated!`);
                
                window.location.href = '/view_pass';
            } else {
                alert(`Purchase Failed: ${result.error}`);
                payButton.innerHTML = '<i class="fas fa-lock me-2"></i>Pay Now - ₹<span id="payAmount">' + totalPrice.toFixed(2) + '</span>';
                payButton.disabled = false;
            }
        } catch (error) {
            console.error('Purchase error:', error);
            alert('Network error. Please check your connection and try again.');
            payButton.innerHTML = '<i class="fas fa-lock me-2"></i>Pay Now - ₹<span id="payAmount">' + totalPrice.toFixed(2) + '</span>';
            payButton.disabled = false;
        }
    });
    
    const adBtn = document.querySelector('.ad-btn');
    if (adBtn) {
        adBtn.addEventListener('click', function() {
            alert('Redirecting to advertising information page...');
        });
    }
    updateTotals();
});

async function checkLoginStatus() {
    try {
        console.log('=== BUY PASS PAGE: Checking login status ===');
        const response = await fetch('/get_current_user');
        const result = await response.json();
        
        console.log('Buy Pass page login check result:', result);
        
        if (!result.success || !result.logged_in) {
            console.log('User not logged in on buy pass page');
            console.log('Error details:', result.error);
            console.log('Debug info:', result.debug);
            
            try {
                const debugResponse = await fetch('/debug_login_status');
                const debugResult = await debugResponse.json();
                console.log('Debug endpoint result:', debugResult);
            } catch (debugError) {
                console.error('Debug endpoint error:', debugError);
            }
            
            alert('Please login first to purchase a pass.');
            window.location.href = '/';
            return false;
        }
        
        console.log('User IS logged in on buy pass page:', result.user.name);
        return true;
    } catch (error) {
        console.error('Login check error:', error);
        alert('Network error. Please check your connection.');
        return false;
    }
}
async function checkLoginStatusOnLoad() {
    try {
        const response = await fetch('/get_current_user');
        const result = await response.json();
        
        if (!result.success || !result.logged_in) {
            console.log('No user logged in at page load');
            document.getElementById('payButton').disabled = true;
            document.getElementById('payButton').innerHTML = '<i class="fas fa-lock me-2"></i>Please Login First';
        } else {
            console.log('User logged in at page load:', result.user.name);
        }
    } catch (error) {
        console.error('Error checking login on load:', error);
    }
}
window.addEventListener('load', async function() {
    try {
        const response = await fetch('/get_current_user');
        const result = await response.json();
        
        if (!result.success || !result.logged_in) {
            alert('Please login first to access buy pass page.');
            window.location.href = '/';
        }
    } catch (error) {
        console.error('Login check error:', error);
    }
});