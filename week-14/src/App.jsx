// App.jsx – Multi-step registration form orchestrator

import React, { useState } from 'react'
import ProgressBar       from './components/ProgressBar'
import Step1Personal     from './components/Step1Personal'
import Step2Account      from './components/Step2Account'
import Step3Preferences  from './components/Step3Preferences'
import SuccessScreen     from './components/SuccessScreen'
import { useFormStorage } from './hooks/useFormStorage'
import {
  validateStep1,
  validateStep2,
  validateStep3,
} from './utils/validate'

// ── Initial data shape ──────────────────────────────────────────────────────
const INITIAL_DATA = {
  // Step 1
  firstName: '',
  lastName:  '',
  dobMonth:  '',
  dobDay:    '',
  dobYear:   '',
  gender:    '',
  // Step 2
  email:           '',
  username:        '',
  password:        '',
  confirmPassword: '',
  // Step 3
  country:     '',
  phone:       '',
  newsletter:  false,
  agreeTerms:  false,
}

const TOTAL_STEPS = 3

export default function App() {
  // Persisted form data (reads from localStorage on first render)
  const [formData, setFormData, clearStorage] = useFormStorage(INITIAL_DATA)

  // Which step we're on: 1 | 2 | 3
  const [step, setStep] = useState(1)

  // Per-field validation errors for the current step
  const [errors, setErrors] = useState({})

  // Whether the form has been successfully submitted
  const [submitted, setSubmitted] = useState(false)

  // ── Helpers ──────────────────────────────────────────────────────────────
  /** Merge a partial update into formData (mirrors setState style) */
  const handleChange = (partial) => {
    setFormData(prev => ({ ...prev, ...partial }))
    // Clear errors for the changed fields on every keystroke
    setErrors(prev => {
      const next = { ...prev }
      Object.keys(partial).forEach(k => delete next[k])
      return next
    })
  }

  /** Validate the current step, return true if clean */
  const validate = () => {
    const validators = [validateStep1, validateStep2, validateStep3]
    const errs = validators[step - 1](formData)
    setErrors(errs)
    return Object.keys(errs).length === 0
  }

  const handleNext = () => {
    if (!validate()) return
    setErrors({})
    setStep(s => s + 1)
  }

  const handleBack = () => {
    setErrors({})
    setStep(s => s - 1)
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!validate()) return
    // localStorage is already up to date via the hook — just mark done
    setSubmitted(true)
  }

  const handleReset = () => {
    clearStorage()
    setFormData(INITIAL_DATA)
    setStep(1)
    setErrors({})
    setSubmitted(false)
  }

  // ── Step content map ─────────────────────────────────────────────────────
  const stepComponents = {
    1: <Step1Personal  data={formData} onChange={handleChange} errors={errors} />,
    2: <Step2Account   data={formData} onChange={handleChange} errors={errors} />,
    3: <Step3Preferences data={formData} onChange={handleChange} errors={errors} />,
  }

  const stepTitles = {
    1: 'Personal Information',
    2: 'Account Details',
    3: 'Preferences & Review',
  }

  // ── Render ───────────────────────────────────────────────────────────────
  return (
    <div className="app-bg">
      <div className="card">
        {/* Header */}
        <div className="card-header">
          <div className="logo-ring">🚀</div>
          <h1>Create Your Account</h1>
          <p>Join thousands of users — it only takes 3 steps</p>
        </div>

        {submitted ? (
          <SuccessScreen data={formData} onReset={handleReset} />
        ) : (
          <form onSubmit={handleSubmit} noValidate>
            {/* Progress bar */}
            <ProgressBar currentStep={step} totalSteps={TOTAL_STEPS} />

            {/* Step counter */}
            <p className="step-counter">
              Step <span>{step}</span> of <span>{TOTAL_STEPS}</span> — {stepTitles[step]}
            </p>

            {/* Active step */}
            {stepComponents[step]}

            {/* Navigation buttons */}
            <div className="btn-row">
              {step > 1 && (
                <button
                  id="btn-back"
                  type="button"
                  className="btn btn-secondary"
                  onClick={handleBack}
                >
                  ← Back
                </button>
              )}

              {step < TOTAL_STEPS ? (
                <button
                  id="btn-next"
                  type="button"
                  className="btn btn-primary"
                  onClick={handleNext}
                >
                  Continue →
                </button>
              ) : (
                <button
                  id="btn-submit"
                  type="submit"
                  className="btn btn-primary"
                >
                  🎉 Create Account
                </button>
              )}
            </div>
          </form>
        )}
      </div>
    </div>
  )
}
