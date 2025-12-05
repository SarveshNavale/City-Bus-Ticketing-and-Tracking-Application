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
