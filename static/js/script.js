document.addEventListener('DOMContentLoaded', function () {
    const mobileLoginRadio = document.getElementById('mobileLogin');
    const emailLoginRadio = document.getElementById('emailLogin');
    const mobileLoginSection = document.getElementById('mobileLoginSection');
    const emailLoginSection = document.getElementById('emailLoginSection');

    if (mobileLoginRadio && emailLoginRadio && mobileLoginSection && emailLoginSection) {
        mobileLoginRadio.addEventListener('change', function () {
            if (this.checked) {
                mobileLoginSection.classList.remove('d-none');
                emailLoginSection.classList.add('d-none');
            }
        });
        emailLoginRadio.addEventListener('change', function () {
            if (this.checked) {
                mobileLoginSection.classList.add('d-none');
                emailLoginSection.classList.remove('d-none');
            }
        });
    }

    const registrationForm = document.getElementById('registrationForm');
    if (registrationForm) {
        registrationForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            
            const formData = {
                name: document.getElementById('name').value,
                mobile: document.getElementById('mobile').value,
                age: document.getElementById('age').value,
                email: document.getElementById('email').value,
                password: document.getElementById('password').value
            };
            
            if (!formData.name || !formData.mobile || !formData.age || !formData.email || !formData.password) {
                alert('Please fill in all fields before submitting.');
                return;
            }
            
            const mobileRegex = /^[0-9]{10}$/;
            if (!mobileRegex.test(formData.mobile)) {
                alert('Please enter a valid 10-digit mobile number.');
                return;
            }
            
            if (formData.age < 12 || formData.age > 100) {
                alert('Age must be between 12 and 100.');
                return;
            }
            
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(formData.email)) {
                alert('Please enter a valid email address.');
                return;
            }
            
            if (formData.password.length < 6) {
                alert('Password must be at least 6 characters long.');
                return;
            }

            try {
                const response = await fetch('/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    window.location.href = result.redirect || '/homepage';
                } else {
                    alert(result.error || 'Registration failed. Please try again.');
                    location.reload();
                }
            } catch (error) {
                console.error("Network error:", error);
                alert("Cannot connect to server. Make sure Flask is running.");
            }
        });
    }

    const loginBtn = document.getElementById('loginBtn');
    if (loginBtn) {
        loginBtn.addEventListener('click', async function () {
            const checkedRadio = document.querySelector('input[name="loginMethod"]:checked');
            if (!checkedRadio) {
                alert('Please select a login method.');
                return;
            }
            
            const loginMethod = checkedRadio.id;
            let identifier = '';
            let method = 'mobile';
            
            if (loginMethod === 'mobileLogin') {
                identifier = document.getElementById('loginMobile').value.trim();
                method = 'mobile';
                if (!identifier) {
                    alert('Please enter mobile number.');
                    return;
                }
            } else {
                identifier = document.getElementById('loginEmail').value.trim();
                method = 'email';
                if (!identifier) {
                    alert('Please enter email address.');
                    return;
                }
            }
            
            const password = document.getElementById('loginPassword').value;
            if (!password) {
                alert('Please enter password.');
                return;
            }
            
            const loginData = {
                identifier: identifier,
                password: password,
                method: method
            };
            
            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(loginData)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    sessionStorage.setItem('justLoggedIn', 'true');
                    window.location.href = result.redirect || '/homepage';
                } else {
                    alert(result.error || 'Invalid credentials. Please try again.');
                    location.reload(); 
                }
            } catch (error) {
                console.error('Network error:', error);
                alert('Cannot connect to server. Please check if Flask server is running.');
            }
        });
    }

    const googleBtn = document.querySelector('.btn-google');
    if (googleBtn) {
        googleBtn.addEventListener('click', function () {
            alert('Redirecting to Google authentication...');
        });
    }

    const registrationPanel = document.getElementById('registrationPanel');
    const loginPanel = document.getElementById('loginLink');
    const showLoginLink = document.getElementById('showLogin');
    const showRegisterLink = document.getElementById('showRegister');

    if (registrationPanel && loginPanel && showLoginLink && showRegisterLink) {
        registrationPanel.classList.remove('d-none');
        loginPanel.classList.add('d-none');

        showLoginLink.addEventListener('click', function (e) {
            e.preventDefault();
            registrationPanel.classList.add('d-none');
            loginPanel.classList.remove('d-none');
        });

        showRegisterLink.addEventListener('click', function (e) {
            e.preventDefault();
            loginPanel.classList.add('d-none');
            registrationPanel.classList.remove('d-none');
        });
    }

    let isNavigating = false;

    document.addEventListener('click', function(e) {
        if (e.target.tagName === 'A' || e.target.closest('a')) {
            const link = e.target.closest('a');
            if (link.href && !link.target) { 
                isNavigating = true;
                console.log('Internal navigation detected, will not clear login');
            }
        }
    });

    window.addEventListener('submit', function() {
        isNavigating = true;
        console.log('Form submission, will not clear login');
    });

    window.addEventListener('pageshow', function() {
        isNavigating = false;
        console.log('Page shown, reset navigation flag');
    });

    if (window.location.pathname === '/' || window.location.pathname === '/registration.html') {
        sessionStorage.setItem('preventLoginClear', 'true');
    }

    window.addEventListener('beforeunload', function(e) {
        if (sessionStorage.getItem('preventLoginClear') === 'true') {
            sessionStorage.removeItem('preventLoginClear');
            return;
        }
        
        if (!isNavigating) {
            fetch('/clear_login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                keepalive: true
            }).catch(error => {
                console.log('Clear login error:', error);
            });
        }
    });
});