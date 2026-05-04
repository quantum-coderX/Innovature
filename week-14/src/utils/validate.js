// validate.js – All form validation logic

// ---------- Step 1: Personal Info ----------
export function validateStep1(data) {
  const errors = {}

  if (!data.firstName.trim()) {
    errors.firstName = 'First name is required.'
  } else if (data.firstName.trim().length < 2) {
    errors.firstName = 'Must be at least 2 characters.'
  }

  if (!data.lastName.trim()) {
    errors.lastName = 'Last name is required.'
  } else if (data.lastName.trim().length < 2) {
    errors.lastName = 'Must be at least 2 characters.'
  }

  if (!data.dobMonth || !data.dobDay || !data.dobYear) {
    errors.dob = 'Please select a complete date of birth.'
  } else {
    const birthDate = new Date(`${data.dobYear}-${data.dobMonth}-${data.dobDay}T00:00:00`)
    if (isNaN(birthDate.getTime())) {
      errors.dob = 'Invalid date. Please check day/month combination.'
    } else {
      const age = Math.floor(
        (Date.now() - birthDate.getTime()) / (365.25 * 24 * 3600 * 1000)
      )
      if (age < 13) errors.dob = 'You must be at least 13 years old.'
    }
  }

  if (!data.gender) {
    errors.gender = 'Please select a gender.'
  }

  return errors
}

// ---------- Step 2: Account Info ----------
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

export function validateStep2(data) {
  const errors = {}

  if (!data.email.trim()) {
    errors.email = 'Email address is required.'
  } else if (!EMAIL_RE.test(data.email)) {
    errors.email = 'Enter a valid email address.'
  }

  if (!data.username.trim()) {
    errors.username = 'Username is required.'
  } else if (data.username.trim().length < 3) {
    errors.username = 'Username must be at least 3 characters.'
  } else if (!/^[a-zA-Z0-9_]+$/.test(data.username)) {
    errors.username = 'Only letters, numbers, and underscores allowed.'
  }

  if (!data.password) {
    errors.password = 'Password is required.'
  } else if (data.password.length < 8) {
    errors.password = 'Password must be at least 8 characters.'
  } else if (!/(?=.*[A-Z])/.test(data.password)) {
    errors.password = 'Include at least one uppercase letter.'
  } else if (!/(?=.*\d)/.test(data.password)) {
    errors.password = 'Include at least one number.'
  }

  if (!data.confirmPassword) {
    errors.confirmPassword = 'Please confirm your password.'
  } else if (data.password !== data.confirmPassword) {
    errors.confirmPassword = 'Passwords do not match.'
  }

  return errors
}

// ---------- Step 3: Preferences ----------
export function validateStep3(data) {
  const errors = {}

  if (!data.country) errors.country = 'Please select your country.'

  if (!data.agreeTerms) {
    errors.agreeTerms = 'You must accept the terms and conditions.'
  }

  return errors
}

// ---------- Password strength ----------
export function getPasswordStrength(password) {
  if (!password) return { level: 0, label: '' }
  let score = 0
  if (password.length >= 8)             score++
  if (/[A-Z]/.test(password))           score++
  if (/\d/.test(password))              score++
  if (/[^A-Za-z0-9]/.test(password))   score++

  const labels = ['', 'Weak', 'Fair', 'Good', 'Strong']
  const keys   = ['', 'weak', 'fair', 'good', 'strong']
  return { level: score, label: labels[score], key: keys[score] }
}
