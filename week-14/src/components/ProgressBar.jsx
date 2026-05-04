// ProgressBar.jsx – Shows step dots and an animated fill bar

import React from 'react'

const STEPS = ['Personal', 'Account', 'Preferences']

export default function ProgressBar({ currentStep, totalSteps }) {
  const pct = ((currentStep - 1) / (totalSteps - 1)) * 100

  return (
    <div className="progress-section">
      {/* Step labels + dots */}
      <div className="step-labels">
        {STEPS.map((label, i) => {
          const stepNum = i + 1
          const isDone   = stepNum < currentStep
          const isActive = stepNum === currentStep
          const cls = isDone ? 'done' : isActive ? 'active' : ''

          return (
            <div key={label} className={`step-label ${cls}`}>
              <div className="step-dot">
                {isDone ? '✓' : stepNum}
              </div>
              {label}
            </div>
          )
        })}
      </div>

      {/* Bar */}
      <div className="progress-bar-track" role="progressbar"
           aria-valuenow={currentStep} aria-valuemin={1} aria-valuemax={totalSteps}>
        <div
          className="progress-bar-fill"
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  )
}
