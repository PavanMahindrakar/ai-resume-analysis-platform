# Frontend Architecture & Design Decisions

## Why Context API Was Chosen

### 1. **Simplicity for Small-Medium Apps**
- **No External Dependencies**: Context API is built into React, reducing bundle size
- **Easy to Understand**: Beginner-friendly, no complex concepts like reducers or middleware
- **Perfect for Our Use Case**: We have 3 main contexts (Auth, Toast, Analysis) - manageable complexity

### 2. **State Sharing Patterns**
- **Auth State**: Needs to be accessible everywhere (routes, API calls, UI)
- **Toast Notifications**: Global UI feedback that any component can trigger
- **Analysis State**: Shared between analysis page and result page

### 3. **Performance Considerations**
- **Selective Re-renders**: Only components using specific context values re-render
- **No Over-fetching**: Each context is scoped to its domain
- **Future Scalability**: Can easily migrate to Redux/Zustand if needed

### 4. **Developer Experience**
- **TypeScript Support**: Full type safety with context
- **Easy Testing**: Mock contexts in tests
- **Clear Data Flow**: Easy to trace where state comes from

## State Flow Through the App

```
┌─────────────────────────────────────────────────────────┐
│                    User Action                          │
│              (Click, Form Submit, etc.)                 │
└────────────────────┬──────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Custom Hook (useResumeUpload)              │
│  - Manages local state (uploading, error, progress)     │
│  - Calls API service                                    │
│  - Updates Context (AnalysisContext)                   │
│  - Shows Toast (ToastContext)                          │
└────────────────────┬──────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              API Service Layer                          │
│  - Axios instance with interceptors                     │
│  - Automatic JWT attachment                             │
│  - Global error handling                                │
└────────────────────┬──────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Backend API                                │
│  - Validates request                                    │
│  - Processes data                                       │
│  - Returns response                                     │
└────────────────────┬──────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Response Handling                          │
│  - Success: Update Context → Show Toast → Navigate      │
│  - Error: Show Error Toast → Update Error State         │
└─────────────────────────────────────────────────────────┘
```

### Example: Resume Upload Flow

1. **User drops file** → `ResumeUploadPage` component
2. **Hook called** → `useResumeUpload().uploadResume(file)`
3. **Validation** → File type, size checks
4. **API call** → `resumeService.uploadResume(file)`
5. **Axios interceptor** → Adds JWT token automatically
6. **Backend processes** → Uploads file, extracts text
7. **Response received** → Hook updates state
8. **Context updated** → `AnalysisContext.setSelectedResume()`
9. **Toast shown** → `ToastContext.showToast('Success!')`
10. **UI updates** → Success message, navigation options

## How UX Improves User Trust

### 1. **Immediate Feedback**
- **Loading States**: Users know something is happening
- **Progress Indicators**: Shows upload progress (0-100%)
- **Skeleton Loaders**: Prevents "blank screen" anxiety
- **Button Disabled States**: Prevents double-submission

**Trust Factor**: Users feel in control, know the system is working

### 2. **Error Handling**
- **Clear Error Messages**: Not just "Error 500", but "Failed to upload. Please try again."
- **Retry Options**: Users can fix issues without losing work
- **Toast Notifications**: Non-intrusive error feedback
- **Form Validation**: Real-time validation prevents errors before submission

**Trust Factor**: Users trust the system will help them succeed

### 3. **Optimistic UI Updates**
- **Immediate Visual Feedback**: Button shows "Saving..." immediately
- **Auto-save Indicators**: "💾 Draft auto-saved" shows work is preserved
- **Smooth Animations**: Score animates from 0 to actual value
- **State Preservation**: Navigation state preserved on auth redirect

**Trust Factor**: Users feel the app is fast and responsive

### 4. **Transparency**
- **Loading Messages**: "Analyzing your resume..." not just a spinner
- **Progress Bars**: Visual representation of upload progress
- **Character Counters**: Users know limits before hitting them
- **Auto-save Status**: Users know their work is saved

**Trust Factor**: Users understand what's happening at all times

### 5. **Error Recovery**
- **Preserved State**: Drafts saved to localStorage
- **Navigation State**: Redirects preserve intended destination
- **Retry Mechanisms**: Easy to retry failed operations
- **Graceful Degradation**: App works even if some features fail

**Trust Factor**: Users don't lose work, can recover from errors

## State Management Strategy

### Context API Structure

```typescript
// AuthContext - Global authentication state
- user: User | null
- loading: boolean
- login/register/logout functions
- isAuthenticated: boolean

// ToastContext - Global notifications
- showToast(message, type, duration)
- toasts: Toast[]

// AnalysisContext - Analysis workflow state
- selectedResume: Resume | null
- selectedJobDescription: JobDescription | null
- currentAnalysis: AnalysisResult | null
- isAnalyzing: boolean
```

### Custom Hooks Pattern

Each feature has a custom hook that:
1. Manages local state
2. Calls API services
3. Updates relevant contexts
4. Handles errors
5. Shows toasts

**Benefits**:
- Reusable logic
- Testable in isolation
- Clear separation of concerns
- Easy to add features

## Performance Optimizations

1. **Selective Re-renders**: Contexts split by domain
2. **Memoization**: useCallback for functions, useMemo for computed values
3. **Lazy Loading**: Code splitting for routes
4. **Debouncing**: Auto-save debounced to reduce API calls
5. **Optimistic Updates**: UI updates before API confirms

## Future Scalability

If the app grows, we can:
1. **Add Redux**: For complex state management
2. **Add React Query**: For server state caching
3. **Add Zustand**: Lightweight alternative to Redux
4. **Keep Contexts**: For truly global state (auth, theme)

The current architecture supports growth without major refactoring.
