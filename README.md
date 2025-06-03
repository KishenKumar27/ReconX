# ReconX - AI-Powered Payment Reconciliation System

ReconX is an advanced payment reconciliation platform that leverages artificial intelligence to automatically detect, analyze, and resolve financial discrepancies across multiple payment methods. Built for the Deriv AI Hackathon, it provides real-time transaction monitoring, intelligent root cause analysis, and comprehensive reporting capabilities.

## 🚀 Features

### Core Capabilities
- **AI-Powered Discrepancy Detection**: Automatically identifies missing payments, amount mismatches, and status conflicts
- **Multi-Payment Method Support**: Handles Crypto, FPX, E-Wallet, and Mobile payments
- **Real-time Processing**: Continuous transaction scanning and analysis
- **Intelligent Root Cause Analysis**: Uses DeepSeek AI to provide detailed explanations for each discrepancy
- **Comprehensive Dashboard**: Interactive web interface with real-time statistics and visualizations
- **Automated Reconciliation**: Smart matching of transactions with payment gateway logs

### AI Features
- **Natural Language Analysis**: Generates human-readable explanations for financial discrepancies
- **Pattern Recognition**: Identifies trends and common issues across payment methods
- **Confidence Scoring**: Provides confidence levels for each analysis
- **Contextual Insights**: Considers transaction history and external factors

## 🏗️ Architecture

### Backend (Python/FastAPI)
- **FastAPI Framework**: High-performance async API server
- **MySQL Database**: Robust data storage with automated table creation
- **AI Integration**: DeepSeek AI for intelligent analysis
- **Real-time Processing**: Background tasks for continuous monitoring
- **RESTful APIs**: Comprehensive endpoint coverage

### Frontend (React/Material-UI)
- **React 18**: Modern component-based architecture
- **Material-UI**: Professional design system
- **Redux Toolkit**: State management
- **ApexCharts**: Interactive data visualizations
- **Responsive Design**: Mobile-friendly interface

### Database Schema
- **transactions**: Core transaction data
- **payment_logs**: Gateway payment records
- **reconciliation_records**: Discrepancy analysis results
- **crypto_payment_logs**: Cryptocurrency-specific logs
- **fpx_payment_logs**: FPX banking logs
- **ewallet_payment_logs**: E-wallet transaction logs
- **mobile_payment_logs**: Mobile payment records

## 📋 Prerequisites

### System Requirements
- **Python**: 3.13+ with pip
- **Node.js**: 16+ with npm
- **MySQL**: 8.0+ or Docker
- **Operating System**: macOS, Linux, or Windows

### API Keys
- **Together AI API Key**: Required for DeepSeek AI integration

## 🛠️ Installation & Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd ReconX
```

### 2. Database Setup
#### Option A: Using Docker (Recommended)
```bash
# Start MySQL container
docker-compose up -d

# Verify database is running
docker ps
```

#### Option B: Local MySQL Installation
```bash
# Install MySQL 8.0+
# Create database and user manually or use the provided scripts
```

### 3. Backend Setup
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your configuration
```

### 4. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend/complete-template

# Install Node.js dependencies
npm install

# Return to project root
cd ../..
```

### 5. Environment Configuration
Create a `.env` file in the project root:
```env
# AI Configuration
TOGETHER_API_KEY=your_together_ai_api_key_here

# Database Configuration
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=app_user
DB_PASSWORD=app_password
DB_NAME=payment_resolution_db
```

## 🚀 Running the Application

### 1. Start the Database
```bash
# If using Docker
docker-compose up -d

# Verify MySQL is running on port 3306
```

### 2. Generate Sample Data (Optional)
```bash
# Generate test transactions and payment logs
python3 generate_data.py
```

### 3. Start the Backend Server
```bash
# Activate virtual environment
source .venv/bin/activate

# Start FastAPI server
python3 main.py
```
The backend will be available at: `http://localhost:8000`

### 4. Start the Frontend Development Server
```bash
# In a new terminal window
cd frontend/complete-template

# Start React development server
npm run dev
```
The frontend will be available at: `http://localhost:5173`

## 📊 API Endpoints

### Core Reconciliation APIs
- `GET /reconcile_data` - Retrieve reconciliation records with filtering
- `GET /transaction_stats` - Get transaction statistics and metrics
- `GET /discrepancy_categories` - Analyze discrepancy distribution
- `GET /discrepancy_cases` - Time-based discrepancy analysis
- `GET /reconciliation_summaries` - AI-generated analysis summaries

### Payment Method APIs
- `GET /fetch_three_tables` - Crypto, E-wallet, FPX payment logs
- `GET /fetch_four_tables` - All payment method logs
- `GET /fetch_consolidated_table` - Unified payment log view
- `POST /upload_csv` - Upload payment data via CSV

### Health & Monitoring
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

## 🎯 Usage Examples

### Dashboard Overview
The main dashboard provides:
- **Real-time Statistics**: Transaction counts, resolution rates
- **Discrepancy Analysis**: Categorized issue breakdown
- **Transaction History**: Detailed reconciliation records
- **AI Insights**: Automated analysis and recommendations

### API Usage
```python
import requests

# Get transaction statistics
response = requests.get("http://localhost:8000/transaction_stats")
stats = response.json()

# Retrieve reconciliation data with filters
params = {
    "discrepancy_category": "Amount Mismatch",
    "resolution_status": "Unresolved"
}
response = requests.get("http://localhost:8000/reconcile_data", params=params)
records = response.json()
```

### AI Analysis Example
The system automatically generates detailed analysis like:
```
"The root cause of the discrepancy is likely **missing or incomplete payment log data**, based on the absence of payment log information and no search results despite the transaction showing as 'Success.' Confidence level: **Medium**."
```

## 🔧 Configuration

### Database Configuration
Modify `docker-compose.yaml` for custom database settings:
```yaml
environment:
  MYSQL_ROOT_PASSWORD: your_root_password
  MYSQL_DATABASE: your_database_name
  MYSQL_USER: your_username
  MYSQL_PASSWORD: your_password
```

### AI Model Configuration
The system uses DeepSeek-V3 for analysis. You can modify the model in `main.py`:
```python
response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V3",  # Change model here
    messages=[...]
)
```

### Frontend API Configuration
Update `frontend/complete-template/src/apiconfig/config.dev.js` for different backend URLs:
```javascript
const apiconfig = {
    summarydata: "http://your-backend-url:8000/transaction_stats",
    // ... other endpoints
};
```

## 📈 Performance & Scalability

### Optimization Features
- **Async Processing**: Non-blocking database operations
- **Connection Pooling**: Efficient database connection management
- **Token Usage Tracking**: AI API cost monitoring
- **Batch Processing**: Efficient bulk data operations

### Monitoring
- Real-time token usage logging
- Database query performance tracking
- API response time monitoring
- Error logging and alerting

## 🧪 Testing

### Backend Testing
```bash
# Test API endpoints
curl http://localhost:8000/transaction_stats
curl http://localhost:8000/reconcile_data

# Check API documentation
open http://localhost:8000/docs
```

### Frontend Testing
```bash
cd frontend/complete-template

# Run linting
npm run lint

# Fix linting issues
npm run lint:fix

# Format code
npm run format
```

## 🚀 Deployment

### Production Build
```bash
# Build frontend for production
cd frontend/complete-template
npm run build

# The built files will be in the dist/ directory
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build -d
```

### Environment Variables for Production
```env
# Production database
DB_HOST=your-production-db-host
DB_PORT=3306
DB_USER=production_user
DB_PASSWORD=secure_production_password

# Production AI API
TOGETHER_API_KEY=your_production_api_key
```

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -m 'Add amazing feature'`
5. Push to the branch: `git push origin feature/amazing-feature`
6. Open a Pull Request

### Code Standards
- **Python**: Follow PEP 8 guidelines
- **JavaScript**: Use ESLint configuration provided
- **Database**: Follow naming conventions in existing schema
- **API**: Maintain RESTful principles


## 🏆 Hackathon Information

**Event**: Deriv AI Hackathon  
**Team**: Code Lah  
**Category**: AI-Powered Financial Technology  
**Year**: 2025

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the API documentation at `http://localhost:8000/docs`
- Review the troubleshooting section below

## 🔍 Troubleshooting

### Common Issues

#### Database Connection Errors
```bash
# Check if MySQL is running
docker ps
# or
brew services list | grep mysql

# Verify connection settings in .env file
```

#### Frontend Build Issues
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### API Key Issues
```bash
# Verify API key in .env file
# Check Together AI account for usage limits
# Ensure API key has proper permissions
```

#### Port Conflicts
```bash
# Check if ports are in use
lsof -i :8000  # Backend
lsof -i :5173  # Frontend
lsof -i :3306  # Database

# Kill processes if needed
kill -9 <PID>
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/)
- [Material-UI Documentation](https://mui.com/)
- [Together AI API Documentation](https://docs.together.ai/)
- [MySQL Documentation](https://dev.mysql.com/doc/)

---

**Built with ❤️ for the Deriv AI Hackathon 2025**
