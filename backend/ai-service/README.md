# AI/ML Service

The AI/ML Service provides advanced analytics and machine learning capabilities for the Supply Chain Finance Platform.

## Features

1. **Demand Forecasting**
   - Predicts future demand for products based on historical data
   - Provides confidence intervals for predictions
   - Supports multiple time periods (daily, weekly, monthly)

2. **Fraud Detection**
   - Detects potentially fraudulent transactions in the supply chain
   - Provides risk scores and confidence levels
   - Integrates with transaction monitoring systems

3. **Risk Assessment**
   - Assesses supplier risk levels based on multiple factors
   - Provides detailed risk reports with recommendations
   - Supports continuous risk monitoring

4. **Model Management**
   - Automated model retraining with latest data
   - Model versioning and rollback capabilities
   - Performance monitoring and alerting

## Architecture

The AI service is built as a Spring Boot microservice that integrates with Python-based machine learning models:

```
[Java AI Service] ↔ [Python ML API] ↔ [ML Models]
```

## API Endpoints

### Demand Forecasting
- `POST /api/ai/demand-forecast` - Predict demand for a product
- `GET /api/ai/demand-forecast/product/{productId}` - Get demand forecasts for a product
- `GET /api/ai/demand-forecast/{id}` - Get a specific demand forecast

### Fraud Detection
- `POST /api/ai/fraud-detection` - Detect fraud in a transaction
- `GET /api/ai/fraud-detection/transaction/{transactionId}` - Get fraud detections for a transaction
- `GET /api/ai/fraud-detection/high-risk` - Get high-risk fraud detections

### Risk Assessment
- `POST /api/ai/risk-assessment/{supplierId}` - Assess risk for a supplier
- `GET /api/ai/risk-assessment/supplier/{supplierId}` - Get risk assessments for a supplier
- `GET /api/ai/risk-assessment/level/{riskLevel}` - Get risk assessments by risk level

### Model Management
- `POST /api/ai/models/retrain` - Retrain all ML models

### Analytics
- `GET /api/ai/analytics/summary` - Get AI analytics summary

## Python ML Components

The service integrates with Python-based ML models located in the [ai-ml](../../ai-ml) directory:

- `supply_chain_analytics.py` - Core analytics functions
- `ml_api.py` - Command-line interface for Java service
- `notebooks/` - Jupyter notebooks for model development
- `advanced/` - Advanced AutoML pipeline implementation

## Setup and Installation

1. **Java Service Setup**
   ```bash
   cd backend/ai-service
   mvn clean install
   mvn spring-boot:run
   ```

2. **Python Environment Setup**
   ```bash
   cd ai-ml
   pip install -r requirements.txt
   ```

3. **Database Configuration**
   - Configure PostgreSQL connection in `application.properties`
   - Run database migrations

## Model Training and Retraining

To retrain all models:
```bash
curl -X POST http://localhost:8082/api/ai/models/retrain
```

Or manually run the AutoML pipeline:
```bash
cd ai-ml/advanced
python automl-pipeline.py
```

## Monitoring and Maintenance

- Model performance metrics are tracked via MLflow
- Automated retraining schedules can be configured
- Alerts for model degradation are implemented

## Integration with Other Services

The AI service integrates with:
- Supply Chain Service (for demand forecasting)
- Finance Service (for fraud detection)
- Notification Service (for alerts)

## Security

- All API endpoints are secured with JWT authentication
- Model access is restricted to authorized services
- Data encryption is implemented for sensitive information

## Testing

Unit tests and integration tests are included:
```bash
mvn test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the Apache 2.0 License.