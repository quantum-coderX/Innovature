// useFormStorage.js – Custom hook to persist form data in localStorage

import { useState, useEffect } from 'react'

const STORAGE_KEY = 'week14_registration_form'

export function useFormStorage(initialData) {
  const [formData, setFormData] = useState(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY)
      return saved ? { ...initialData, ...JSON.parse(saved) } : initialData
    } catch {
      return initialData
    }
  })

  // Sync to localStorage whenever formData changes
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(formData))
    } catch {
      // quota exceeded or private mode – silently ignore
    }
  }, [formData])

  const clearStorage = () => {
    localStorage.removeItem(STORAGE_KEY)
  }

  return [formData, setFormData, clearStorage]
}
