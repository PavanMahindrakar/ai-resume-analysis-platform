# AI Resume Intelligence - Frontend

Production-quality React application for AI Resume Intelligence & Career Copilot.

## Features

- 🔐 Authentication with JWT
- 📄 Resume upload with drag-and-drop
- 💼 Job description creation with auto-save
- 🔍 Resume-to-job matching analysis
- 📊 Interactive dashboard with charts
- ✨ Real-time validation and feedback
- 🎨 Modern, responsive UI

## Tech Stack

- React 18 with TypeScript
- React Router for navigation
- Context API for global state
- Custom hooks for API calls
- Recharts for data visualization
- React Dropzone for file uploads
- Vite for fast development

## Getting Started

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
src/
├── components/       # Reusable UI components
│   ├── common/      # Shared components (Button, Input, Card, etc.)
│   ├── analysis/    # Analysis-specific components
│   ├── job/         # Job description components
│   └── resume/      # Resume upload components
├── context/         # React Context providers
├── hooks/           # Custom React hooks
├── pages/           # Page components
│   ├── auth/        # Login/Register pages
│   ├── dashboard/   # Dashboard page
│   ├── resume/      # Resume upload page
│   ├── job/         # Job description page
│   └── analysis/    # Analysis pages
├── services/        # API service layer
├── types/           # TypeScript type definitions
└── utils/           # Utility functions
```

## Environment Variables

Create a `.env` file:

```
VITE_API_URL=http://localhost:8000
```

## Features Overview

### Authentication
- Real-time form validation
- Loading states
- Error handling
- JWT token management

### Resume Upload
- Drag-and-drop interface
- File type validation
- Upload progress
- Success feedback

### Job Description
- Auto-save drafts
- Character counter
- Quick role selector
- Form validation

### Analysis
- Interactive score visualization
- Expandable sections
- Highlighted skills
- Detailed explanations

### Dashboard
- Interactive charts
- Filterable data
- Clickable history
- Summary statistics
