// =====================================================
// Mock Data — Week 13 React Dashboard
// =====================================================

export const statsData = [
  {
    id: 1,
    icon: '💰',
    label: 'Total Revenue',
    value: '$48,295',
    trend: '+12.5%',
    trendUp: true,
    color: '#7c3aed',
  },
  {
    id: 2,
    icon: '🛒',
    label: 'Total Orders',
    value: '3,842',
    trend: '+8.1%',
    trendUp: true,
    color: '#06b6d4',
  },
  {
    id: 3,
    icon: '👥',
    label: 'Active Users',
    value: '12,491',
    trend: '+23.4%',
    trendUp: true,
    color: '#10b981',
  },
  {
    id: 4,
    icon: '📦',
    label: 'Products Listed',
    value: '1,284',
    trend: '-2.3%',
    trendUp: false,
    color: '#f59e0b',
  },
];

export const recentItems = [
  {
    id: 1,
    avatar: '👩‍💼',
    name: 'Priya Sharma',
    action: 'Placed an order',
    date: 'Apr 26, 2026',
    status: 'Completed',
    statusType: 'success',
    amount: '$249.00',
  },
  {
    id: 2,
    avatar: '👨‍💻',
    name: 'Arjun Mehta',
    action: 'Signed up',
    date: 'Apr 25, 2026',
    status: 'Active',
    statusType: 'info',
    amount: '—',
  },
  {
    id: 3,
    avatar: '👩‍🎨',
    name: 'Sneha Patel',
    action: 'Requested refund',
    date: 'Apr 24, 2026',
    status: 'Pending',
    statusType: 'warning',
    amount: '$89.00',
  },
  {
    id: 4,
    avatar: '👨‍🔬',
    name: 'Rahul Verma',
    action: 'Placed an order',
    date: 'Apr 23, 2026',
    status: 'Processing',
    statusType: 'info',
    amount: '$512.50',
  },
  {
    id: 5,
    avatar: '👩‍🏫',
    name: 'Divya Nair',
    action: 'Left a review',
    date: 'Apr 22, 2026',
    status: 'Completed',
    statusType: 'success',
    amount: '—',
  },
  {
    id: 6,
    avatar: '🧑‍💼',
    name: 'Vikram Singh',
    action: 'Account suspended',
    date: 'Apr 21, 2026',
    status: 'Suspended',
    statusType: 'error',
    amount: '—',
  },
];

export const announcements = [
  {
    id: 1,
    title: '🚀 New Feature: Bulk Discount Engine',
    date: 'Apr 26, 2026',
    priority: 'high',
    body: 'The new bulk discount engine is now live. Admins can configure tiered discounts for wholesale customers directly from the Products panel.',
  },
  {
    id: 2,
    title: '🔧 Scheduled Maintenance — May 3rd',
    date: 'Apr 24, 2026',
    priority: 'medium',
    body: 'The platform will be unavailable from 2:00 AM to 4:00 AM IST on May 3rd for routine infrastructure upgrades. Plan accordingly.',
  },
  {
    id: 3,
    title: '📊 Q1 2026 Analytics Report Ready',
    date: 'Apr 20, 2026',
    priority: 'low',
    body: 'The Q1 2026 analytics report has been generated and is available for download in the Reports section. Revenue grew by 34% YoY.',
  },
  {
    id: 4,
    title: '🛡️ Security Patch Deployed',
    date: 'Apr 18, 2026',
    priority: 'high',
    body: 'A critical security patch has been applied to address a potential XSS vulnerability in the product review module. All users are safe.',
  },
];

export const currentUser = {
  name: 'Arjun Dev',
  role: 'Super Admin',
  avatar: '🧑‍💻',
};

export const navItems = [
  { id: 'dashboard', label: 'Dashboard', icon: '🏠' },
  { id: 'orders', label: 'Orders', icon: '🛒' },
  { id: 'products', label: 'Products', icon: '📦' },
  { id: 'users', label: 'Users', icon: '👥' },
  { id: 'analytics', label: 'Analytics', icon: '📊' },
  { id: 'announcements', label: 'Announcements', icon: '📢' },
  { id: 'settings', label: 'Settings', icon: '⚙️' },
];
