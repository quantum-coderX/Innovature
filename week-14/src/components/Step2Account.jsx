// Step2Account.jsx – email, username, password with strength meter, confirmPassword

import React, { useState } from 'react'
import { getPasswordStrength } from '../utils/validate'

export default function Step2Account({ data, onChange, errors }) {
  const [showPwd, setShowPwd]     = useState(false)
  const [showConfirm, setShowConfirm] = useState(false)

  const handleChange = (e) => {
    onChange({ [e.target.name]: e.target.value })
  }

  const strength = getPasswordStrength(data.password)

  const segClass = (i) => {
    if (!strength.level || i >= strength.level) return ''
    return strength.key
  }

  return (
    <div className="form-step" key="step2">
      {/* Email */}
      <div className="form-group">
        <label htmlFor="email">Email Address</label>
        <div className="input-wrapper">
          <input
            id="email"
            name="email"
            type="email"
            className={`form-input ${errors.email ? 'error' : ''}`}
            placeholder="jane@example.com"
            value={data.email}
            onChange={handleChange}
            autoComplete="email"
          />
          <span className="input-icon">✉️</span>
        </div>
        {errors.email && <p className="error-msg">⚠ {errors.email}</p>}
      </div>

      {/* Username */}
      <div className="form-group">
        <label htmlFor="username">Username</label>
        <div className="input-wrapper">
          <input
            id="username"
            name="username"
            type="text"
            className={`form-input ${errors.username ? 'error' : ''}`}
            placeholder="jane_doe42"
            value={data.username}
            onChange={handleChange}
            autoComplete="username"
          />
          <span className="input-icon">@</span>
        </div>
        {errors.username && <p className="error-msg">⚠ {errors.username}</p>}
      </div>

      {/* Password */}
      <div className="form-group">
        <label htmlFor="password">Password</label>
        <div className="input-wrapper">
          <input
            id="password"
            name="password"
            type={showPwd ? 'text' : 'password'}
            className={`form-input ${errors.password ? 'error' : ''}`}
            placeholder="Min. 8 chars, 1 upper, 1 number"
            value={data.password}
            onChange={handleChange}
            autoComplete="new-password"
          />
          <span className="input-icon">🔒</span>
          <button
            type="button"
            onClick={() => setShowPwd(v => !v)}
            style={{
              position: 'absolute', right: '10px', top: '50%',
              transform: 'translateY(-50%)',
              background: 'none', border: 'none',
              cursor: 'pointer', color: 'var(--text-muted)',
              fontSize: '1rem', padding: '2px'
            }}
            aria-label={showPwd ? 'Hide password' : 'Show password'}
          >
            {showPwd ? '🙈' : '👁'}
          </button>
        </div>

        {/* Strength meter */}
        {data.password && (
          <>
            <div className="strength-bar-row">
              {[0,1,2,3].map(i => (
                <div key={i} className={`strength-seg ${segClass(i)}`} />
              ))}
            </div>
            <p className="strength-text">
              Strength: <strong style={{
                color: strength.key === 'strong' ? 'var(--green)' :
                       strength.key === 'good'   ? 'var(--cyan)'  :
                       strength.key === 'fair'   ? 'var(--amber)' : 'var(--red)'
              }}>{strength.label}</strong>
            </p>
          </>
        )}

        {errors.password && <p className="error-msg">⚠ {errors.password}</p>}
      </div>

      {/* Confirm Password */}
      <div className="form-group">
        <label htmlFor="confirmPassword">Confirm Password</label>
        <div className="input-wrapper">
          <input
            id="confirmPassword"
            name="confirmPassword"
            type={showConfirm ? 'text' : 'password'}
            className={`form-input ${errors.confirmPassword ? 'error' : ''}`}
            placeholder="Repeat your password"
            value={data.confirmPassword}
            onChange={handleChange}
            autoComplete="new-password"
          />
          <span className="input-icon">🔑</span>
          <button
            type="button"
            onClick={() => setShowConfirm(v => !v)}
            style={{
              position: 'absolute', right: '10px', top: '50%',
              transform: 'translateY(-50%)',
              background: 'none', border: 'none',
              cursor: 'pointer', color: 'var(--text-muted)',
              fontSize: '1rem', padding: '2px'
            }}
            aria-label={showConfirm ? 'Hide confirm password' : 'Show confirm password'}
          >
            {showConfirm ? '🙈' : '👁'}
          </button>
        </div>
        {errors.confirmPassword && (
          <p className="error-msg">⚠ {errors.confirmPassword}</p>
        )}
        {!errors.confirmPassword && data.confirmPassword &&
          data.password === data.confirmPassword && (
          <p style={{ fontSize: '0.75rem', color: 'var(--green)', marginTop: '0.35rem' }}>
            ✓ Passwords match
          </p>
        )}
      </div>
    </div>
  )
}
