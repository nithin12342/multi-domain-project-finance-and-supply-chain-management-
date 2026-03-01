# Context Document: Multi-Domain Supply Chain & Finance Platform
**Target Audience:** External AI Architect / Agent
**Objective:** Provide full architectural context to design a State-of-the-Art (SOTA) Graph Neural Network (GNN) and Temporal Fusion Transformer (TFT) Multi-Agent AI architecture. Generate exportable Python code tailored for Google Colab GPU training that can be easily integrated back into this Java Spring Boot ecosystem.

---

## 1. System Overview
The platform is a comprehensive, microservices-based enterprise application managing two heavily intertwined domains:
1. **Supply Chain:** Inventory tracking, shipment logistics, supplier management, and order fulfillment.
2. **Finance:** Invoice factoring, risk assessment, payment tracking, and DeFi/Blockchain integration.
3. **IoT:** Telemetry parsing (temperature, humidity, vibration) from Edge devices on shipments and warehouses.

The ultimate goal of the AI is to bridge these domains autonomously (e.g., predicting a supply chain shortage via weather data, analyzing the cascading financial impact on outstanding invoices, and executing a smart contract to adjust financing rates).

---

## 2. Current Architecture & Stack
*   **Backend Framework:** Java Spring Boot (Microservices Architecture).
*   **Databases:** PostgreSQL (Relational Data), currently storing entities as standard disconnected tables.
*   **Messaging Pipeline:** MQTT Broker (for incoming IoT JSON telemetry streams).
*   **Current AI Integration:** The Spring Boot `ai-service` calls a Python script (`ml_api.py`) via command-line sub-processes. The Python script returns JSON predictions.
*   **Current ML Tech Stack:**
    *   **Python 3.x**
    *   **Scikit-Learn:** Random Forest Regressors (Demand Forecasting) and Random Forest Classifiers (Fraud Detection, Risk Assessment).
    *   **PyTorch:** A rudimentary 2-layer LSTM for Time-Series Demand Forecasting.
    *   **Persistence:** `joblib` (for SKLearn) and `.pt` state dictionaries (for PyTorch).

---

## 3. Database Schema Mapping (Crucial for GNN Design)
To design the Graph Neural Network (GNN), the external agent must understand the relational layout that needs to be converted into Nodes and Edges.

### Supply Chain Domain Entities
*   `Supplier`: Has `id`, `name`, `rating`, `country`.
*   `Inventory`: Has `id`, `productId`, `location`, `quantity`, `threshold`.
*   `Order`: Has `id`, `customerId`, `productId`, `quantity`, `totalAmount`, `status` (PENDING, FULFILLED, etc.).
*   `Shipment`: Has `id`, `orderId`, `origin`, `destination`, `status`.

### Finance Domain Entities
*   `Invoice`: Has `id`, `supplierId`, `amount`, `dueDate`, `status` (PAID, OVERDUE, FINANCED).
*   `RiskAssessment`: Has `supplierId`, `score` (0-100), `riskLevel` (LOW, MEDIUM, HIGH).

### IoT Domain Entities
*   `SensorData`: Has `deviceId`, `timestamp`, `temperature`, `humidity`, `vibration`.

---

## 4. The Goal: The SOTA Architecture
The user desires a completely new architecture that is "State-of-the-Art".

**The external agent must output Python code (ready for Jupyter/Colab) to build the following:**

1.  **A Spatial-Temporal Graph Neural Network (ST-GNN) for Risk/Fraud:**
    *   *Input:* A graph constructed from the Entities above (e.g., Supplier -> owes -> Bank).
    *   *Task:* Predict "Cascading Risk" (if Supplier A fails, what is the probability Supplier B defaults on their invoice?).
    *   *Technology constraint:* Use PyTorch Geometric (PyG) or DGL.

2.  **Temporal Fusion Transformer (TFT) or Informer for Demand Forecasting:**
    *   *Input:* Multi-variate time-series data (historical sales + weather/IoT telemetry + static supplier metadata).
    *   *Task:* Predict future inventory demand with Attention Weights (so the business logic knows *why* the prediction was made).
    *   *Technology constraint:* Use PyTorch Forecasting or a custom PyTorch Transformer implementation.

3.  **Multi-Agent Reinforcement Learning (MARL) for Autonomous Optimization:**
    *   *Task:* Develop a digital twin environment using OpenAI Gym / PettingZoo where an "Inventory Agent" and a "Finance Agent" interact. The Inventory Agent is rewarded for fulfilling orders; the Finance Agent is penalized for high capital lockup. They must learn the optimal purchase order strategy.
    *   *Technology constraint:* Use Ray RLlib or stable-baselines3.

---

## 5. Required Output from the External Agent
When generating the solution, the external agent must provide:

1.  **Data Generation Script:** A Python script using `networkx` or Pandas to generate realistic synthetic data that fits the Graph/Transformer schemas defined above.
2.  **Model Definition Code:** The exact PyTorch Classes (`nn.Module`) for the ST-GNN, the TFT, and the RL Environment.
3.  **Google Colab Training Loop:** The exact Python cells to execute the training loop utilizing CUDA, compute the Loss, and perform backpropagation.
4.  **Export Logic:** The code to save the final weights as `.pt` files.
5.  **Inference Wrapper (`ml_api.py` v2.0):** A Python script that the Java Spring Boot service can call via CLI. It must load the generated `.pt` files, accept a JSON/String argument (e.g., `predict_demand --product_id 123`), evaluate the SOTA model, and return a JSON response.

Please generate the complete, self-contained Python source code for training and inference based on these parameters.
