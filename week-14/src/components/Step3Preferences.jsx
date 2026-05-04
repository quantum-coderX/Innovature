// Step3Preferences.jsx – country, newsletter checkbox, terms agreement

import React from 'react'

const COUNTRIES = [
  'India', 'United States', 'United Kingdom', 'Canada', 'Australia',
  'Germany', 'France', 'Japan', 'Brazil', 'South Africa', 'Other'
]

export default function Step3Preferences({ data, onChange, errors }) {
  const handleChange = (e) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value
    onChange({ [e.target.name]: value })
  }

  return (
    <div className="form-step" key="step3">
      {/* Country */}
      <div className="form-group">
        <label htmlFor="country">Country / Region</label>
        <div className="input-wrapper">
          <select
            id="country"
            name="country"
            className={`form-select ${errors.country ? 'error' : ''}`}
            value={data.country}
            onChange={handleChange}
          >
            <option value="">Select your country…</option>
            {COUNTRIES.map(c => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
          <span className="input-icon">🌍</span>
        </div>
        {errors.country && <p className="error-msg">⚠ {errors.country}</p>}
      </div>

      {/* Phone (optional) */}
      <div className="form-group">
        <label htmlFor="phone">Phone Number <span style={{ color: 'var(--text-muted)', fontWeight: 400 }}>(optional)</span></label>
        <div className="input-wrapper">
          <input
            id="phone"
            name="phone"
            type="tel"
            className="form-input"
            placeholder="+91 98765 43210"
            value={data.phone}
            onChange={handleChange}
            autoComplete="tel"
          />
          <span className="input-icon">📞</span>
        </div>
      </div>

      {/* Newsletter */}
      <div className="form-group">
        <label
          className="checkbox-group"
          htmlFor="newsletter"
          style={{ cursor: 'pointer' }}
        >
          <input
            id="newsletter"
            name="newsletter"
            type="checkbox"
            checked={data.newsletter}
            onChange={handleChange}
          />
          <span className="checkbox-label">
            📧 Subscribe to our newsletter for updates, tips, and special offers.
          </span>
        </label>
      </div>

      {/* Terms */}
      <div className="form-group">
        <label
          className={`checkbox-group ${errors.agreeTerms ? 'error' : ''}`}
          htmlFor="agreeTerms"
          style={{
            cursor: 'pointer',
            borderColor: errors.agreeTerms ? 'var(--red)' : undefined
          }}
        >
          <input
            id="agreeTerms"
            name="agreeTerms"
            type="checkbox"
            checked={data.agreeTerms}
            onChange={handleChange}
          />
          <span className="checkbox-label">
            I agree to the <a href="#terms" onClick={e => e.preventDefault()}>Terms of Service</a> and{' '}
            <a href="#privacy" onClick={e => e.preventDefault()}>Privacy Policy</a>. *
          </span>
        </label>
        {errors.agreeTerms && <p className="error-msg">⚠ {errors.agreeTerms}</p>}
      </div>
    </div>
  )
}
