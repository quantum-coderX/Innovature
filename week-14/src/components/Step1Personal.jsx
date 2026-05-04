// Step1Personal.jsx – Controlled inputs: firstName, lastName, DOB (MM-DD-YYYY), gender

import React from 'react'

const MONTHS = [
  { value: '01', label: 'January' },
  { value: '02', label: 'February' },
  { value: '03', label: 'March' },
  { value: '04', label: 'April' },
  { value: '05', label: 'May' },
  { value: '06', label: 'June' },
  { value: '07', label: 'July' },
  { value: '08', label: 'August' },
  { value: '09', label: 'September' },
  { value: '10', label: 'October' },
  { value: '11', label: 'November' },
  { value: '12', label: 'December' },
]

// Generate days 01–31
const DAYS = Array.from({ length: 31 }, (_, i) => String(i + 1).padStart(2, '0'))

// Generate years from current year down to 1920
const currentYear = new Date().getFullYear()
const YEARS = Array.from({ length: currentYear - 1919 }, (_, i) => String(currentYear - i))

export default function Step1Personal({ data, onChange, errors }) {
  const handleChange = (e) => {
    onChange({ [e.target.name]: e.target.value })
  }

  const dobError = errors.dobMonth || errors.dobDay || errors.dobYear || errors.dob

  return (
    <div className="form-step" key="step1">
      <div className="form-row">
        {/* First Name */}
        <div className="form-group">
          <label htmlFor="firstName">First Name</label>
          <div className="input-wrapper">
            <input
              id="firstName"
              name="firstName"
              type="text"
              className={`form-input ${errors.firstName ? 'error' : ''}`}
              placeholder="Jane"
              value={data.firstName}
              onChange={handleChange}
              autoComplete="given-name"
            />
            <span className="input-icon">👤</span>
          </div>
          {errors.firstName && <p className="error-msg">⚠ {errors.firstName}</p>}
        </div>

        {/* Last Name */}
        <div className="form-group">
          <label htmlFor="lastName">Last Name</label>
          <div className="input-wrapper">
            <input
              id="lastName"
              name="lastName"
              type="text"
              className={`form-input ${errors.lastName ? 'error' : ''}`}
              placeholder="Doe"
              value={data.lastName}
              onChange={handleChange}
              autoComplete="family-name"
            />
            <span className="input-icon">👤</span>
          </div>
          {errors.lastName && <p className="error-msg">⚠ {errors.lastName}</p>}
        </div>
      </div>

      {/* Date of Birth – MM / DD / YYYY selects */}
      <div className="form-group">
        <label>Date of Birth <span style={{ color: 'var(--text-muted)', fontWeight: 400, fontSize: '0.7rem' }}>(MM-DD-YYYY)</span></label>
        <div className="dob-row">
          {/* Month */}
          <div className="input-wrapper dob-seg">
            <select
              id="dobMonth"
              name="dobMonth"
              className={`form-select ${dobError ? 'error' : ''}`}
              value={data.dobMonth}
              onChange={handleChange}
              aria-label="Birth month"
            >
              <option value="">MM</option>
              {MONTHS.map(m => (
                <option key={m.value} value={m.value}>{m.value} – {m.label}</option>
              ))}
            </select>
            <span className="input-icon">🗓</span>
          </div>

          <span className="dob-sep">–</span>

          {/* Day */}
          <div className="input-wrapper dob-seg">
            <select
              id="dobDay"
              name="dobDay"
              className={`form-select ${dobError ? 'error' : ''}`}
              value={data.dobDay}
              onChange={handleChange}
              aria-label="Birth day"
            >
              <option value="">DD</option>
              {DAYS.map(d => (
                <option key={d} value={d}>{d}</option>
              ))}
            </select>
            <span className="input-icon" style={{ left: '8px' }}>📅</span>
          </div>

          <span className="dob-sep">–</span>

          {/* Year */}
          <div className="input-wrapper dob-seg dob-year">
            <select
              id="dobYear"
              name="dobYear"
              className={`form-select ${dobError ? 'error' : ''}`}
              value={data.dobYear}
              onChange={handleChange}
              aria-label="Birth year"
            >
              <option value="">YYYY</option>
              {YEARS.map(y => (
                <option key={y} value={y}>{y}</option>
              ))}
            </select>
            <span className="input-icon" style={{ left: '8px' }}>📅</span>
          </div>
        </div>
        {dobError && <p className="error-msg">⚠ {dobError}</p>}
      </div>

      {/* Gender */}
      <div className="form-group">
        <label htmlFor="gender">Gender</label>
        <div className="input-wrapper">
          <select
            id="gender"
            name="gender"
            className={`form-select ${errors.gender ? 'error' : ''}`}
            value={data.gender}
            onChange={handleChange}
          >
            <option value="">Select gender…</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="non-binary">Non-binary</option>
            <option value="prefer-not-to-say">Prefer not to say</option>
          </select>
          <span className="input-icon">⚧</span>
        </div>
        {errors.gender && <p className="error-msg">⚠ {errors.gender}</p>}
      </div>
    </div>
  )
}
