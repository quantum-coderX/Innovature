# Week 14 – Multi-Step Registration Form

**Topic:** Forms & State — Controlled Components, Form Validation, `useState` Hook

A polished, dark-themed 3-step registration form built with **React + Vite**, featuring real-time validation, a password strength meter, an animated progress bar, and automatic Local Storage persistence.

---

## 🚀 Getting Started

```bash
# Install dependencies
npm install

# Start the development server
npm run dev
```

Open **http://localhost:5173** in your browser.

---

## 📋 Features

| Requirement | Implementation |
|---|---|
| Controlled inputs with `useState` | Every field is a controlled input; `useFormStorage` custom hook manages global state |
| Email validation | Regex + empty-check in `validateStep2` |
| Password validation | Length ≥ 8, uppercase, digit — displayed inline with animated error messages |
| Password confirmation | Match check on `confirmPassword` field |
| Password strength meter | 4-segment coloured bar (Weak → Fair → Good → Strong) |
| Progress bar | Animated gradient fill bar + step dots (pending / active / done) |
| Local Storage | `useFormStorage` hook auto-saves on every keystroke; data survives page refresh |
| Multi-step form | 3 discrete steps: Personal → Account → Preferences |
| Success screen | Shows full data summary + "Saved to Local Storage" badge |

---

## 🗂️ Project Structure

```
week-14/
├── index.html
├── vite.config.js
├── package.json
└── src/
    ├── main.jsx                    # React entry point
    ├── App.jsx                     # Orchestrator: step state, navigation, validation
    ├── index.css                   # Design tokens, layout, all component styles
    ├── hooks/
    │   └── useFormStorage.js       # Custom hook – localStorage sync
    ├── utils/
    │   └── validate.js             # All validators + password strength logic
    └── components/
        ├── ProgressBar.jsx         # Animated progress bar with step dots
        ├── Step1Personal.jsx       # First name, last name, DOB, gender
        ├── Step2Account.jsx        # Email, username, password (strength meter)
        ├── Step3Preferences.jsx    # Country, phone (optional), newsletter, terms
        └── SuccessScreen.jsx       # Summary card + reset button
```

---

## 🧠 Concepts Demonstrated

### Controlled Components
Every `<input>` and `<select>` is controlled: its value comes from `formData` state and updates via `onChange` handlers. There is no uncontrolled DOM state anywhere.

```jsx
<input
  name="email"
  value={data.email}          // controlled value from state
  onChange={handleChange}     // updates state on every keystroke
/>
```

### useState Hook
- `step` — tracks which of the 3 steps is active
- `errors` — per-field error map, cleared as the user types
- `submitted` — toggles the success screen
- `formData` — the entire form's data, managed via `useFormStorage`

### Custom Hook – `useFormStorage`
Reads the initial state from `localStorage`, returns `[formData, setFormData, clearStorage]`, and uses `useEffect` to sync every change back automatically.

### Form Validation
Each step has its own validator in `validate.js`:
- **Step 1:** required fields + age ≥ 13
- **Step 2:** email regex, username rules, password rules, match check
- **Step 3:** country required, terms must be accepted

Validation runs on "Continue / Submit" — not before — to avoid early red highlights.

### Password Strength Meter
Scores 1 point each for: length ≥ 8, uppercase letter, digit, special character. Displayed as a 4-segment bar with colours: 🔴 Weak → 🟡 Fair → 🔵 Good → 🟢 Strong.

---

## 🎨 Design Highlights
- Dark glassmorphism card with ambient gradient blobs
- Gradient progress bar with smooth CSS transitions
- Step dots animate between pending / active (glow) / done (green ✓) states
- Slide-in animation per step (`slideIn` keyframes)
- Shake animation on error messages
- Pop-in animation on the success icon
