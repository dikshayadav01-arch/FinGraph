# FinGraph: Real-Time Fraud Syndicate Analytics

> A real-time FinTech and Anti-Money Laundering (AML) analytics system that combines Kafka, Apache Flink, Neo4j, FastAPI, and Streamlit to detect suspicious transaction patterns and fraud syndicates.

---

## 📌 Overview

**FinGraph** is a real-time fraud detection and investigation prototype designed to identify complex transaction patterns that can be difficult to detect using traditional transaction-level rules.

Traditional fraud detection may flag individual transactions based on simple conditions such as:

> "Flag transactions above ₹10,000."

However, sophisticated money-laundering patterns can involve many individually normal-looking transactions distributed across multiple accounts.

For example, a group of accounts may send multiple smaller transactions to the same target account. Individually, these transactions may not appear highly suspicious, but their **relationship and transaction pattern** can reveal a potential fraud syndicate.

FinGraph addresses this problem by combining **real-time stream processing with graph-based fraud analysis**.

---

## 🎯 Problem Statement

Financial fraud and money laundering can involve complex networks of accounts rather than isolated transactions.

Patterns such as:

* Multiple accounts sending money to one target
* Many small transactions used to avoid detection
* Money circulating through multiple accounts
* Suspicious accounts connected through transaction relationships

can be difficult to identify using only traditional relational transaction analysis.

### Goal

Build a system that can:

1. Receive transaction events in real time.
2. Process and classify transactions.
3. Assign transaction risk levels.
4. Store account relationships in a graph database.
5. Detect suspicious transaction patterns.
6. Expose fraud detections through an API.
7. Present investigation results through an interactive dashboard.

---

## 🏗️ System Architecture

```text
┌────────────────────────┐
│ Transaction Generator  │
│                        │
│ Normal + Fraud Patterns│
└───────────┬────────────┘
            │
            │ Transaction Events
            ▼
┌────────────────────────┐
│ Apache Kafka            │
│ Topic: fin_transactions│
└───────────┬────────────┘
            │
            │ Stream
            ▼
┌────────────────────────┐
│ Apache Flink            │
│                        │
│ • Deserialize events   │
│ • Fraud classification │
│ • Risk scoring         │
│ • Stream processing    │
└───────────┬────────────┘
            │
            │ Processed transactions
            ▼
┌────────────────────────┐
│ Neo4j Graph Database   │
│                        │
│ Account ──SENT──> Account
└───────────┬────────────┘
            │
            ├──────────────────┐
            ▼                  ▼
┌────────────────────┐  ┌────────────────────┐
│ Cypher Detection   │  │ FastAPI             │
│ Queries            │  │ Investigation API   │
│                    │  │                     │
│ • Starburst        │  │ /fraud/starburst    │
│ • Smurfing         │  │ /fraud/smurfing     │
│ • Circular         │  │ /fraud/circular     │
└──────────┬─────────┘  └──────────┬───────────┘
           │                       │
           └───────────┬───────────┘
                       ▼
              ┌──────────────────┐
              │ Streamlit        │
              │ Investigation    │
              │ Dashboard        │
              └──────────────────┘
```

---

## 🔄 Data Flow

```text
Transaction Generator
        ↓
      Kafka
        ↓
     Flink
        ↓
Fraud Classification
        ↓
    Risk Scoring
        ↓
      Neo4j
        ↓
Fraud Detection Queries
        ↓
     FastAPI
        ↓
   Streamlit Dashboard
```

---

## 🚨 Fraud Patterns Detected

### 1. Starburst Fraud

Detects a suspicious receiver receiving transactions from multiple distinct sender accounts.

Example:

```text
ACC001 ─────┐
ACC002 ─────┤
ACC003 ─────┤
ACC004 ─────┼──→ SHELL001
ACC005 ─────┤
...         │
ACC050 ─────┘
```

FinGraph identifies receivers with multiple suspicious incoming relationships.

---

### 2. Smurfing

Smurfing involves splitting larger amounts into multiple smaller transactions to reduce the chance of triggering simple transaction thresholds.

FinGraph detects target accounts receiving multiple `SMURFING` transactions from distinct sender accounts.

---

### 3. Circular Fraud

Detects transaction cycles where money moves between multiple accounts and eventually returns to the original account.

Example:

```text
ACC063
  ↓
ACC090
  ↓
ACC015
  ↓
ACC063
```

Graph traversal makes this type of relationship-based pattern easier to investigate.

---

## ⚙️ Fraud Classification

FinGraph uses an explainable rule-based classification approach.

### Fraud status

A transaction is classified as **SUSPICIOUS** when:

* Amount is at least ₹9,000, or
* Transaction type is `SMURFING`, `STARBURST`, or `CIRCULAR`.

Otherwise, it is classified as:

```text
NORMAL
```

### Risk levels

| Condition                | Risk   |
| ------------------------ | ------ |
| High-risk amount/pattern | HIGH   |
| Amount ≥ ₹5,000          | MEDIUM |
| Lower-risk transaction   | LOW    |

This approach is intentionally deterministic and explainable.

> **Note:** FinGraph is currently a rule-based fraud analytics system, not a machine-learning fraud prediction model.

---

## 🛠️ Technology Stack

| Technology   | Purpose                                      |
| ------------ | -------------------------------------------- |
| Python       | Transaction generation, API, dashboard       |
| Apache Kafka | Real-time transaction streaming              |
| Apache Flink | Stream processing                            |
| Java 21      | Flink processing application                 |
| Maven        | Java project build and dependency management |
| Neo4j        | Graph database and relationship analysis     |
| Cypher       | Fraud detection queries                      |
| FastAPI      | Investigation REST API                       |
| Streamlit    | Interactive fraud investigation dashboard    |
| Pandas       | Data handling                                |
| Git & GitHub | Version control                              |

---

## 📁 Project Structure

```text
FinGraph/
│
├── simulator/
│   ├── transaction_generator.py
│   └── stream_producer.py
│
├── flink_jobs/
│   ├── pom.xml
│   └── src/
│       └── main/
│           └── java/
│               └── com/
│                   └── fingraph/
│                       ├── FinGraphProcessor.java
│                       ├── FraudClassifier.java
│                       ├── RiskScorer.java
│                       ├── Neo4jSink.java
│                       ├── Neo4jWriter.java
│                       └── model/
│
├── neo4j_queries/
│   ├── client.py
│   ├── api.py
│   └── queries/
│       ├── starburst_detection.cypher
│       ├── smurfing_detection.cypher
│       └── circular_detection.cypher
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🔧 Prerequisites

Install the following before running FinGraph:

* Python 3.x
* Java 21
* Apache Kafka
* Apache Flink 2.2.1
* Neo4j
* Maven
* Git

The project was developed and tested locally using Windows with WSL for the Flink environment.

---

## 📦 Python Dependencies

The main Python dependencies are listed in `requirements.txt`.

Install them using:

```bash
pip install -r requirements.txt
```

Main packages include:

```text
fastapi
uvicorn
streamlit
neo4j
pandas
requests
```

---

## 🔐 Environment Configuration

FinGraph requires the following environment variable for Neo4j authentication:

```text
NEO4J_PASSWORD
```

The Neo4j password should **never be committed to Git**.

For a local session, set the variable through your operating system environment.

Example for WSL:

```bash
read -s -p "Enter Neo4j password: " NEO4J_PASSWORD
echo
export NEO4J_PASSWORD
```

The password is intentionally not included anywhere in this repository.

---

## ▶️ Running FinGraph

### 1. Start Neo4j

Start the Neo4j database and make sure it is running.

The project connects to Neo4j through:

```text
bolt://172.19.176.1:7687
```

---

### 2. Start Kafka

Start Kafka and ensure the transaction topic exists:

```text
fin_transactions
```

Verify the topic:

```bash
kafka-topics --bootstrap-server localhost:9092 --list
```

---

### 3. Start Flink

Start the Flink standalone cluster.

From the Flink installation directory:

```bash
./bin/jobmanager.sh start
```

Then start the TaskManager with the Neo4j password available to the TaskManager JVM:

```bash
read -s -p "Enter Neo4j password: " NEO4J_PASSWORD
echo
export NEO4J_PASSWORD
export FLINK_ENV_JAVA_OPTS_TM="-DNEO4J_PASSWORD=$NEO4J_PASSWORD"

./bin/taskmanager.sh start
```

Verify the Flink cluster:

```bash
./bin/flink list
```

---

### 4. Build the Flink Application

From the project:

```bash
cd flink_jobs
mvn clean package -DskipTests
```

The packaged JAR is generated under:

```text
flink_jobs/target/
```

---

### 5. Submit the Flink Job

Submit the generated JAR:

```bash
./bin/flink run /mnt/c/Users/Diksha/FinGraph/flink_jobs/target/fingraph-flink-1.0-SNAPSHOT.jar
```

Verify:

```bash
./bin/flink list
```

The job should appear as:

```text
FinGraph Transaction Processor
RUNNING
```

---

### 6. Start the Transaction Producer

From the project root:

```bash
python simulator/stream_producer.py
```

Transactions are published to:

```text
fin_transactions
```

---

## 🔍 Fraud Detection Queries

The project includes three main Cypher detection queries.

### Starburst

```text
neo4j_queries/queries/starburst_detection.cypher
```

### Smurfing

```text
neo4j_queries/queries/smurfing_detection.cypher
```

### Circular

```text
neo4j_queries/queries/circular_detection.cypher
```

These queries operate on the transaction relationships stored in Neo4j.

---

## 🌐 Investigation API

FinGraph exposes fraud detections through FastAPI.

Start the API:

```bash
uvicorn neo4j_queries.api:app --reload
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### Available endpoints

| Endpoint               | Purpose                              |
| ---------------------- | ------------------------------------ |
| `GET /health`          | API health check                     |
| `GET /fraud/starburst` | Detect starburst patterns            |
| `GET /fraud/smurfing`  | Detect smurfing patterns             |
| `GET /fraud/circular`  | Detect circular transaction patterns |

Example health response:

```json
{
  "status": "ok",
  "service": "FinGraph Investigation API"
}
```

---

## 📊 Streamlit Dashboard

Start the dashboard:

```bash
streamlit run dashboard/app.py
```

The dashboard provides:

* Total fraud alerts
* Starburst detections
* Smurfing detections
* Circular detections
* Detected exposure
* Fraud pattern overview
* Detailed investigation tabs
* API health status
* Neo4j detection engine status

The dashboard is designed to provide a simple investigation interface for a risk analyst.

---

## 📈 Example Results

During testing, the system successfully detected:

| Fraud Pattern | Detected Cases |
| ------------- | -------------: |
| Starburst     |              3 |
| Smurfing      |              2 |
| Circular      |              3 |
| Total Alerts  |              8 |

One observed starburst target was:

```text
SHELL001
50 distinct senders
₹484,339.72 total amount
```

One observed smurfing target was:

```text
SMURF_TARGET
30 transactions
₹265,652.70 total amount
```

The exact results may change when new transaction events are generated and processed.

---

## 🧪 System Validation

The following components were tested during development:

* Kafka transaction streaming
* Flink job submission
* Flink transaction processing
* Fraud classification
* Risk scoring
* Neo4j transaction storage
* Starburst detection
* Smurfing detection
* Circular fraud detection
* FastAPI health endpoint
* FastAPI fraud endpoints
* Streamlit dashboard
* Neo4j connectivity

---

## 💡 Why Graph-Based Fraud Detection?

Traditional transaction analysis often focuses on individual records.

FinGraph instead models:

```text
Account ──SENT──> Account
```

This makes it possible to investigate relationships such as:

```text
Many Accounts
      ↓
 One Target
```

or:

```text
Account A
    ↓
Account B
    ↓
Account C
    ↓
Account A
```

The graph representation therefore complements transaction-level rules by providing relationship-based investigation.

---

## 🚧 Limitations

This project is a **functional fraud analytics prototype**, not a production banking system.

Current limitations include:

* Rule-based fraud classification
* Synthetic transaction data
* Local deployment
* No production authentication layer
* No distributed production deployment
* No advanced machine-learning anomaly detection
* Limited fault-tolerance configuration
* No production monitoring/observability stack

---

## 🔮 Future Scope

Possible future improvements include:

* Machine-learning-based anomaly detection
* Graph machine learning
* Community detection for fraud rings
* Advanced transaction risk scoring
* Real-time alert notifications
* Role-based dashboard authentication
* Kafka replication and production configuration
* Flink checkpointing and recovery
* Prometheus/Grafana monitoring
* Cloud deployment
* Historical fraud investigation and case management
* More complex graph-based AML rules

---

## 🎓 Project Highlights

FinGraph demonstrates the integration of:

```text
Real-Time Streaming
        +
Stream Processing
        +
Graph Database
        +
Graph-Based Fraud Detection
        +
REST API
        +
Interactive Dashboard
```

The project focuses on making complex fraud relationships **observable, explainable, and easier to investigate**.

---

## 👩‍💻 Author

**Diksha Yadav**

FinGraph — Real-Time Fraud Syndicate Analytics

Built as a solo developer project using Python, Java, Apache Kafka, Apache Flink, Neo4j, FastAPI, and Streamlit.

---

## 📄 Project Status

**Status: Completed**

The current implementation demonstrates an end-to-end fraud analytics pipeline from transaction generation and streaming through fraud detection and dashboard-based investigation.
