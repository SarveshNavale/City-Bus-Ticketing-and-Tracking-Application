document.addEventListener('DOMContentLoaded', function () {
//login toggle
    const mobileLoginRadio   = document.getElementById('mobileLogin');
    const emailLoginRadio    = document.getElementById('emailLogin');
    const mobileLoginSection = document.getElementById('mobileLoginSection');
    const emailLoginSection  = document.getElementById('emailLoginSection');

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
//registration form
    const registrationForm = document.getElementById('registrationForm');
    if (registrationForm) {
        registrationForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const name   = document.getElementById('name').value;
            const mobile = document.getElementById('mobile').value;
            const age    = document.getElementById('age').value;
            const email  = document.getElementById('email').value;
            if (name && mobile && age && email) {
                alert(`Registration successful!\n\nName: ${name}\nMobile: ${mobile}\nAge: ${age}\nEmail: ${email}\n\nYou can now log in to your account.`);
                registrationForm.reset();
            } else {
                alert('Please fill in all fields before submitting.');
            }
        });
    }
  //login button
    const loginBtn = document.getElementById('loginBtn');
    if (loginBtn) {
        loginBtn.addEventListener('click', function () {
            const checkedRadio = document.querySelector('input[name="loginMethod"]:checked');
            if (!checkedRadio) {
                alert('Please select a login method.');
                return;
            }
            const loginMethod = checkedRadio.id;
            let identifier = '';
            if (loginMethod === 'mobileLogin') {
                identifier = document.getElementById('loginMobile').value;
            } else {
                identifier = document.getElementById('loginEmail').value;
            }
            const password = document.getElementById('loginPassword').value;
            if (identifier && password) {
                alert(`Login successful with ${loginMethod === 'mobileLogin' ? 'mobile number' : 'email'}!\n\nYou will be redirected to the dashboard.`);
                document.getElementById('loginMobile').value = '';
                document.getElementById('loginEmail').value = '';
                document.getElementById('loginPassword').value = '';
            } else {
                alert('Please enter your login credentials.');
            }
        });
    }
//google button
    const googleBtn = document.querySelector('.btn-google');
    if (googleBtn) {
        googleBtn.addEventListener('click', function () {
            alert('Redirecting to Google authentication....');
        });
    }
//login scroll
    const loginLink = document.querySelector('.login-link a');
    if (loginLink) {
        loginLink.addEventListener('click', function (e) {
            e.preventDefault();
            const loginPanel = document.getElementById('loginLink');
            if (loginPanel) {
                loginPanel.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }
//age validation
    const ageInput = document.getElementById('age');
    if (ageInput) {
        ageInput.addEventListener('change', function () {
            const age = parseInt(this.value);
            if (age < 12) {
                alert('You must be at least 12 years old to register.');
                this.value = '';
            } else if (age > 100) {
                alert('Please enter a valid age.');
                this.value = '';
            }
        });
    }
//mobile validation
    const mobileInput = document.getElementById('mobile');
    if (mobileInput) {
        const mobileRegex = /^[0-9]{10}$/;
        mobileInput.addEventListener('blur', function () {
            if (this.value && !mobileRegex.test(this.value)) {
                alert('Please enter a valid 10-digit mobile number.');
                this.focus();
            }
        });
    }
});
// Toggle between registration and login sections
const registrationPanel = document.getElementById('registrationPanel');
const loginPanel        = document.getElementById('loginLink');  
const showLoginLink     = document.getElementById('showLogin');
const showRegisterLink  = document.getElementById('showRegister');

console.log({ registrationPanel, loginPanel, showLoginLink, showRegisterLink });

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
} else {
    console.error('Toggle elements missing');
}
// registration
const registrationForm = document.getElementById('registrationForm');
if (registrationForm) {
    registrationForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        
        // Get form data
        const formData = {
            name: document.getElementById('name').value,
            mobile: document.getElementById('mobile').value,
            age: document.getElementById('age').value,
            email: document.getElementById('email').value,
            password: document.getElementById('password').value
        };
        
        console.log("Sending registration:", formData);
        
        try {
            // Send to server
            const response = await fetch('/register', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (result.success) {
                alert("Registration successful!\nUser data stored in database.");
                registrationForm.reset(); // Clear form
            } else {
                alert("Error: " + result.error);
            }
        } catch (error) {
            console.error("Network error:", error);
            alert("Cannot connect to server. Make sure Flask is running.");
        }
    });
}
// LOGIN function
const loginBtn = document.getElementById('loginBtn');
if (loginBtn) {
    loginBtn.addEventListener('click', async function () {
        console.log('Login button clicked');
        
        const checkedRadio = document.querySelector('input[name="loginMethod"]:checked');
        if (!checkedRadio) {
            alert('Please select a login method.');
            return;
        }
        
        const loginMethod = checkedRadio.id;
        let identifier = '';
        let method = 'mobile';
        
        // Get identifier based on selected method
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
        
        console.log('Login data:', { identifier, method, password: '***' });
        
        const loginData = {
            identifier: identifier,
            password: password,
            method: method
        };
        
        try {
            console.log('Sending login request to /login...');
            
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(loginData)
            });
            
            console.log('Login response status:', response.status);
            
            const result = await response.json();
            console.log('Login result:', result);
            
            if (result.success) {
                alert('Login successful! Redirecting to homepage...');
                console.log('Redirecting to:', result.redirect);
                window.location.href = result.redirect;
            } else {
                alert('Login failed: ' + result.error);
                console.error('Login error:', result.error);
            }
        } catch (error) {
            console.error('Network error:', error);
            alert('Cannot connect to server. Please check:\n1. Flask server is running\n2. URL: http://127.0.0.1:5000');
        }
    });
}
//registration form 
if (registrationForm) {
    registrationForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        console.log('Registration form submitted');
        
        const name = document.getElementById('name').value.trim();
        const mobile = document.getElementById('mobile').value.trim();
        const age = document.getElementById('age').value;
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        
        console.log('Form data collected:', { name, mobile, age, email });
        
        if (!name || !mobile || !age || !email || !password) {
            alert('Please fill in all fields before submitting.');
            return;
        }
        
        // Mobile validation
        const mobileRegex = /^[0-9]{10}$/;
        if (!mobileRegex.test(mobile)) {
            alert('Please enter a valid 10-digit mobile number.');
            document.getElementById('mobile').focus();
            return;
        }
        
        // Age validation
        if (age < 12 || age > 100) {
            alert('Age must be between 12 and 100.');
            document.getElementById('age').focus();
            return;
        }
        
        // Email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            alert('Please enter a valid email address.');
            document.getElementById('email').focus();
            return;
        }
        
        // Password validation
        if (password.length < 6) {
            alert('Password must be at least 6 characters long.');
            document.getElementById('password').focus();
            return;
        }

        const userData = {
            name: name,
            mobile: mobile,
            age: age,
            email: email,
            password: password
        };
        
        console.log('Sending registration data to server:', userData);
        
        try {
            const response = await fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            });
            
            console.log('Server response status:', response.status);
            
            // Parse response
            const result = await response.json();
            console.log('Server response data:', result);
            
            if (result.success) {
                alert('Registration successful! Redirecting to homepage...');
                console.log('Redirecting to:', result.redirect);
                
                registrationForm.reset();
                
                if (result.redirect) {
                    window.location.href = result.redirect;
                }
            } else {
                alert('Registration failed: ' + result.error);
                console.error('Registration error:', result.error);
            }
        } catch (error) {
            // Network error
            console.error('Network error:', error);
            alert('Network error. Please check if Flask server is running.');
        }
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

if (result.success) {
    sessionStorage.setItem('justLoggedIn', 'true');
    
    alert('Login successful! Redirecting...');
    window.location.href = result.redirect;
}
if (result.success) {
    sessionStorage.setItem('justLoggedIn', 'true');
    
    alert('Registration successful! Redirecting...');
    window.location.href = result.redirect;
}