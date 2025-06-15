let currentLanguage = 'english'; 

const translations = {
  english: {
    'app.title': 'MediAid NG',
    'signup.title': 'Create Your Account',
    'signup.name': 'Full Name',
    'signup.name.placeholder': 'e.g., Adeola Musa',
    'signup.phone': 'Phone Number',
    'signup.phone.placeholder': '08012345678',
    'signup.email': 'Email (Optional)',
    'signup.email.placeholder': 'adeola@example.com',
    'signup.occupation': 'Occupation',
    'signup.occupation.default': 'Select one',
    'occupation.farmer': 'Farmer',
    'occupation.trader': 'Trader',
    'occupation.health-worker': 'Health Worker',
    'occupation.student': 'Student',
    'occupation.other': 'Other',
    'signup.dob': 'Date of Birth',
    'signup.password': 'Password',
    'signup.password.placeholder': 'At least 6 characters',
    'signup.submit': 'Sign Up',
    'login.link': 'Already have an account?',
    'or.divider': 'OR',
    'ussd.button': 'No internet? Try USSD Demo',
    'ussd.demo': 'Dial *123*1# to register',
    'error.phone_email': 'Please provide either phone or email!',
    'error.password': 'Password too short (min 6 characters)',
    'error.otp': 'Invalid OTP (must be 6 digits)'
  },
  pidgin: {
    'app.title': 'MediAid NG',
    'signup.title': 'Make Your Account',
    'signup.name': 'Your Full Name',
    'signup.name.placeholder': 'e.g., Ade Musa',
    'signup.phone': 'Phone Number',
    'signup.phone.placeholder': '08012345678',
    'signup.email': 'Email (No Must)',
    'signup.email.placeholder': 'ade@example.com',
    'signup.occupation': 'Which work You Dey Do',
    'signup.occupation.default': 'Choose One',
    'occupation.farmer': 'Farmer',
    'occupation.trader': 'Market Person',
    'occupation.health-worker': 'Hospital Worker',
    'occupation.student': 'Student',
    'occupation.other': 'Others',
    'signup.dob': 'When dem born you',
    'signup.password': 'Password',
    'signup.password.placeholder': 'Small-Small 6 Letters',
    'signup.submit': 'Register',
    'login.link': 'You Get Account?',
    'or.divider': 'OR',
    'ussd.button': 'No Network? Try USSD',
    'ussd.demo': 'Dial *123*1# to register',
    'error.phone_email': 'Abeg, put phone or email!',
    'error.password': 'Password no reach 6 letters!',
    'error.otp': 'OTP no correct!'
  }
};

function setLanguage(lang) {
  currentLanguage = lang;
  updateUIText();
  updatePlaceholders();
  updateSelectOptions();
  updateActiveLanguageButton();
  console.log(`Language set to: ${lang}`);
}

function updateUIText() {
  document.querySelectorAll('[data-translate]').forEach(el => {
    const key = el.getAttribute('data-translate');
    if (translations[currentLanguage][key]) {
      el.textContent = translations[currentLanguage][key];
    }
  });
}

function updatePlaceholders() {
  document.querySelectorAll('[data-placeholder]').forEach(el => {
    const key = el.getAttribute('data-placeholder');
    if (translations[currentLanguage][key]) {
      el.placeholder = translations[currentLanguage][key];
    }
  });
}

function updateSelectOptions() {
  const occupationSelect = document.getElementById('occupation');
  if (occupationSelect) {
    const options = occupationSelect.querySelectorAll('option');
    options.forEach(option => {
      if (option.hasAttribute('data-translate')) {
        const key = option.getAttribute('data-translate');
        if (translations[currentLanguage][key]) {
          option.textContent = translations[currentLanguage][key];
        }
      }
    });
  }
}

function updateActiveLanguageButton() {
  document.querySelectorAll('.language-switcher button').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-lang') === currentLanguage);
  });
}

function validateSignupForm() {
  const phone = document.getElementById('phone').value;
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
d
  if (!phone && !email) {
    showError(translations[currentLanguage]['error.phone_email']);
    return false;
  }

  if (password.length < 6) {
    showError(translations[currentLanguage]['error.password']);
    return false;
  }

  return true; 
}

function showError(message) {
  let errorBox = document.getElementById('error-message');
  if (!errorBox) {
    errorBox = document.createElement('div');
    errorBox.id = 'error-message';
    errorBox.style.color = 'red';
    errorBox.style.margin = '10px 0';
    document.querySelector('form').prepend(errorBox);
  }
  errorBox.textContent = message;
}

function handleSignup(event) {
  event.preventDefault();
  
  if (!validateSignupForm()) return;

  const userData = {
    name: document.getElementById('full-name').value,
    phone: document.getElementById('phone').value,
    email: document.getElementById('email').value,
    occupation: document.getElementById('occupation').value,
    dob: document.getElementById('dob').value,
    language: currentLanguage
  };

  console.log('Submitting:', userData);
  setTimeout(() => simulateOTPSend(userData.phone), 1000);
}

function simulateOTPSend(phone) {
  console.log(`[MOCK] OTP sent to ${phone}`);
  alert(`${translations[currentLanguage]['ussd.demo']}\n\n${phone}`);
  window.location.href = `otp-verify.html?phone=${encodeURIComponent(phone)}&lang=${currentLanguage}`;
}

function toggleUSSD() {
  const ussdDemo = document.getElementById('ussd-demo');
  ussdDemo.classList.toggle('hidden');
}

function handleOTPVerification(event) {
  event.preventDefault();
  const otp = document.getElementById('otp-code').value;
  
  if (otp.length !== 6 || !/^\d+$/.test(otp)) {
    showError(translations[currentLanguage]['error.otp']);
    return;
  }

  alert(currentLanguage === 'english' 
    ? 'Account created successfully!' 
    : 'Account don ready!');
  window.location.href = 'dashboard.html';
}

document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.language-switcher button').forEach(btn => {
    btn.addEventListener('click', function() {
      setLanguage(this.getAttribute('data-lang'));
    });
  });

  const urlParams = new URLSearchParams(window.location.search);
  const langParam = urlParams.get('lang');
  setLanguage(langParam || 'english');
});