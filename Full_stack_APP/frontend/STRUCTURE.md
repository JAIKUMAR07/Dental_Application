# React Project Structure

## ✅ Proper Folder Organization

```
frontend/src/
├── pages/                          # Page-level components
│   ├── HomePage.jsx               # Landing page with hero & features
│   ├── AnalysisPage.jsx           # AI Analysis page with all prediction logic
│   ├── ClinicLocatorPage.jsx      # Clinic finder with map integration
│   └── AboutPage.jsx              # About system, tech stack, disclaimers
│
├── components/
│   ├── layout/                    # Layout components
│   │   ├── Header.jsx            # App header with navigation menu
│   │   └── Footer.jsx            # App footer
│   │
│   ├── common/                    # Reusable components
│   │   └── ProbabilityChart.jsx  # Chart for displaying probabilities
│   │
│   └── [Analysis Components]      # Feature-specific components
│       ├── ModelSelector.jsx
│       ├── UploadSection.jsx
│       ├── ResultsDisplay.jsx
│       ├── BatchResults.jsx
│       └── InfoPanel.jsx (deprecated - moved to AboutPage)
│
├── services/                      # API and external services
│   └── api.js                    # Backend API calls
│
├── App.jsx                        # Main app router (clean & simple)
├── App.css                        # Global styles
└── main.jsx                       # Entry point
```

## 🎯 Architecture Principles

### 1. **Separation of Concerns**

- **Pages**: Handle page-level logic and state
- **Components**: Reusable UI pieces
- **Services**: External API communication
- **App.jsx**: Simple routing logic only

### 2. **Component Organization**

- `layout/`: Components that appear on every page (Header, Footer)
- `common/`: Reusable components used across features
- Feature folders: Group related components together

### 3. **State Management**

- Page-level state in respective pages
- Shared state (models, currentView) in App.jsx
- Props drilling for simple cases
- (Future: Context API for complex state)

## 📄 File Responsibilities

### App.jsx

- **Purpose**: Main application router
- **Responsibilities**:
  - View switching (analysis vs locator)
  - Shared state management
  - Layout composition
- **Does NOT**: Contain business logic

### Pages

- **AnalysisPage.jsx**:
  - All AI prediction logic
  - Model selection
  - Upload handling
  - Results display
- **ClinicLocatorPage.jsx**:
  - Map integration
  - Clinic search
  - Location services

### Components

- **Focused & Reusable**: Each component has a single responsibility
- **Props-based**: Receive data and callbacks via props
- **No direct API calls**: Use services or receive data from pages

## 🔄 Data Flow

```
App.jsx (Router)
    ↓ (props)
Pages (Business Logic)
    ↓ (props)
Components (UI)
```

## 🚀 Benefits

1. **Maintainability**: Easy to find and update code
2. **Scalability**: Simple to add new pages/features
3. **Reusability**: Components can be used across pages
4. **Testability**: Isolated components are easier to test
5. **Team Collaboration**: Clear structure for multiple developers

## 📝 Next Steps (Optional Improvements)

1. **Add React Router**: For proper URL-based routing
2. **Context API**: For complex state management
3. **Custom Hooks**: Extract reusable logic
4. **TypeScript**: Add type safety
5. **Testing**: Add unit and integration tests
