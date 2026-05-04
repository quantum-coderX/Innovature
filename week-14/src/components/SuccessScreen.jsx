// SuccessScreen.jsx – Final congratulation screen with data summary

import React from 'react'

export default function SuccessScreen({ data, onReset }) {
  return (
    <div className="success-screen">
      <div className="success-icon">🎉</div>

      <h2>Registration Complete!</h2>
      <p>Welcome aboard, <strong>{data.firstName}</strong>! Your account has been created.</p>

      <div className="badge-saved">
        <span>💾</span> Data saved to Local Storage
      </div>

      <div className="summary-card">
        <div className="summary-row">
          <span>Name</span>
          <span>{data.firstName} {data.lastName}</span>
        </div>
        <div className="summary-row">
          <span>Email</span>
          <span>{data.email}</span>
        </div>
        <div className="summary-row">
          <span>Username</span>
          <span>@{data.username}</span>
        </div>
        <div className="summary-row">
          <span>Date of Birth</span>
          <span>
            {data.dobMonth && data.dobDay && data.dobYear
              ? `${data.dobMonth}-${data.dobDay}-${data.dobYear}`
              : '—'}
          </span>
        </div>
        <div className="summary-row">
          <span>Gender</span>
          <span style={{ textTransform: 'capitalize' }}>{data.gender || '—'}</span>
        </div>
        <div className="summary-row">
          <span>Country</span>
          <span>{data.country}</span>
        </div>
        {data.phone && (
          <div className="summary-row">
            <span>Phone</span>
            <span>{data.phone}</span>
          </div>
        )}
        <div className="summary-row">
          <span>Newsletter</span>
          <span>{data.newsletter ? '✅ Subscribed' : '❌ Not subscribed'}</span>
        </div>
      </div>

      <button
        id="btn-register-again"
        className="btn btn-primary"
        style={{ width: '100%' }}
        onClick={onReset}
      >
        ✨ Register Another Account
      </button>
    </div>
  )
}
