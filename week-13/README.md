# Week 13 - React Basics Dashboard

Week 13 is a Vite + React admin dashboard built as a frontend-only coursework project. It demonstrates component composition, prop-driven rendering, CSS Modules, and a mock-data layout that looks and behaves like a lightweight operations console.

## What This Project Shows

- A persistent left sidebar with active navigation state
- A top header with page title and user context
- A dashboard canvas with KPI cards, recent activity, and announcements
- Mock data rendered through reusable components
- Responsive layout behavior for tablet and mobile widths
- Decorative gradients and CSS variables for a more polished UI

## Tech Stack

- React 18
- Vite
- CSS Modules
- Plain CSS for global tokens and layout rules

## Run Locally

From the `week-13` folder:

```bash
npm install
npm run dev
```

Production build:

```bash
npm run build
```

Preview the production build locally:

```bash
npm run preview
```

## Project Structure

- `src/main.jsx` boots the React app
- `src/App.jsx` controls the dashboard shell and page switching
- `src/App.module.css` defines the overall app layout and background decoration
- `src/index.css` provides global theme tokens and resets
- `src/components/Sidebar` renders the navigation rail
- `src/components/Header` renders the top bar
- `src/components/Dashboard` assembles the dashboard content
- `src/components/StatCard` renders a single KPI card
- `src/components/StatsGrid` arranges KPI cards into a responsive grid
- `src/components/RecentItems` renders the activity table
- `src/components/Announcements` renders the notice feed
- `src/data/mockData.js` stores the static demo content

## Data Model

The dashboard is intentionally driven by static data so the UI stays easy to demo and extend.

- `statsData` holds KPI labels, values, trends, and colors
- `recentItems` holds recent user or order activity rows
- `announcements` holds announcement cards with priority levels
- `currentUser` stores the header/sidebar identity block
- `navItems` defines the sidebar navigation list

## Behavior Notes

- The Dashboard route is the only fully implemented view right now.
- Other sidebar items show a simple placeholder state to keep navigation functional.
- Search, filter, export, and action controls are presentational and not wired to a backend.
- The app uses mock content so it can run without any external services.

## Responsive Design

The layout adapts across screen sizes:

- The sidebar collapses away on smaller screens
- The main content spacing tightens on tablet and mobile widths
- The dashboard content stacks into a single column as the viewport narrows
- The header controls remain compact instead of overflowing

## Deliverable Notes

- This folder contains the complete source for the Week 13 dashboard.
- The checked-in `dist` folder reflects a production build generated from the current source.
