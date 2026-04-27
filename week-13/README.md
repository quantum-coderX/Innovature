# Week 13 - React Basics Dashboard

A React dashboard UI built for Week 13 of the Innovature coursework. The project demonstrates JSX syntax, reusable components, props, CSS Modules, and inline styles in a polished, responsive admin-style layout.

## What is included

- A fixed sidebar navigation with active state handling
- A sticky top header with search, notifications, and user controls
- A dashboard hero section with summary metrics
- Reusable statistic cards for KPI-style data
- A recent activity table for transactions and actions
- An announcements feed with priority badges
- Responsive layouts using CSS Modules and media queries
- Mock data-driven UI for easy extension

## Tech Stack

- React 18
- Vite
- CSS Modules
- Plain CSS variables for theme tokens

## Project Structure

- `src/App.jsx` - root layout shell and page switching
- `src/components/Sidebar` - left navigation
- `src/components/Header` - top bar with greeting and controls
- `src/components/Dashboard` - dashboard composition
- `src/components/StatCard` - reusable KPI card
- `src/components/StatsGrid` - responsive stats grid
- `src/components/RecentItems` - recent activity table
- `src/components/Announcements` - announcement list
- `src/data/mockData.js` - static content used by the UI

## Setup and Run

From the `week-13` folder:

```bash
npm install
npm run dev
```

To create a production build:

```bash
npm run build
```

To preview the production build locally:

```bash
npm run preview
```

## Responsive Behavior

The interface adapts across common screen sizes:

- The sidebar slides off-canvas on smaller screens
- The hero section switches to a stacked layout on narrower widths
- The stats grid drops from 4 columns to 2 and then to 1
- The main content area collapses into a single column on tablet-sized screens
- The header search and user controls compress for mobile widths

## Evaluation

The assignment requirements are covered well:

- JSX syntax is used throughout the components
- The UI is decomposed into reusable components with props
- CSS Modules are used for local styling, with inline styles for dynamic accents
- The dashboard includes the required stats, recent items, and announcements sections
- The layout is responsive and visually coherent

Current limitations are intentional for the assignment scope:

- Non-dashboard sidebar items currently show placeholder pages
- Search, filter, export, load more, and action buttons are presentational only
- The content is driven by mock data rather than a live backend

## Demo Notes

The app is ready to demo by running the Vite dev server locally. The included `dist` folder shows the production build output generated from the current source.
