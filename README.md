# 🤖 AI QE Agent

**An AI-powered Quality Engineering assistant for intelligent test analysis, execution, failure investigation, and quality workflows.**

AI QE Agent explores how **Generative AI, RAG, MCP and test automation** can be combined to augment traditional Quality Engineering practices.

The goal is not to replace automation engineers, but to build an intelligent QE assistant that can understand testing context, retrieve relevant knowledge, interact with testing tools, analyze failures, and provide actionable quality insights.

---

## 🎯 Problem Statement

Modern QA teams often need to work across multiple sources of information:

* Requirements and acceptance criteria
* Test cases
* API specifications
* Application data
* Database state
* UI workflows
* Automated test results
* Application logs
* Defects and Jira tickets

Investigating a failed transaction can therefore require several manual steps:


Requirement
    ↓
Understand the business workflow
    ↓
Check application/API state
    ↓
Execute or inspect tests
    ↓
Validate database state
    ↓
Analyze logs
    ↓
Identify root cause
    ↓
Create/update defect


The AI QE Agent explores how an AI-driven workflow can connect these activities and assist the QE engineer with faster investigation and decision-making.

---

# 🏗️ Architecture


                         ┌──────────────────────┐
                         │      QE Engineer     │
                         │    / User Query      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     AI QE Agent      │
                         │                      │
                         │ LLM + Reasoning      │
                         │ Context Management   │
                         │ Tool Selection       │
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┼────────────────┐
                    │               │                │
                    ▼               ▼                ▼
             ┌────────────┐  ┌────────────┐  ┌────────────┐
             │    RAG     │  │ MCP Tools  │  │    Jira    │
             │ Knowledge  │  │            │  │ Integration│
             └─────┬──────┘  └──────┬─────┘  └────────────┘
                   │                │
                   │       ┌────────┼────────┐
                   │       │        │        │
                   │       ▼        ▼        ▼
                   │      API       UI       DB
                   │     Tests     Tests   Validation
                   │
                   ▼
          ┌─────────────────────┐
          │ Semantic Retrieval  │
          │                     │
          │ Embeddings + FAISS  │
          └──────────┬──────────┘
                     │
                     ▼
             Relevant QE Context
                     │
                     ▼
             AI Reasoning / RCA
                     │
                     ▼
              Quality Insights


---

# 🚀 Key Capabilities

## 🧠 Retrieval-Augmented Generation

The agent can retrieve relevant information from a QE knowledge base before generating an answer.

The RAG pipeline uses:


Documents
    ↓
Chunking
    ↓
Embeddings
    ↓
Vector Index
    ↓
Semantic Search
    ↓
Relevant Context
    ↓
LLM
    ↓
Grounded Response


This helps reduce reliance on the LLM's general knowledge and provides application-specific context.

---

## 🔌 MCP-based Tool Integration

The project explores **Model Context Protocol (MCP)** as a mechanism for allowing the AI agent to interact with external QE capabilities through controlled tools.

Example tools include:


query_database
run_api_test
run_ui_test
search_logs


The agent can reason about the problem and determine which tool or combination of tools can provide the required evidence.

---

## 🧪 API Test Execution

The agent can interact with API testing capabilities to support workflows such as:


Identify transaction
        ↓
Query API state
        ↓
Execute API validation
        ↓
Inspect response
        ↓
Correlate with DB / logs


This enables API-level validation to become part of an intelligent investigation workflow.

---

## 🎭 UI Test Execution

UI automation can be used when application behavior needs to be validated from the user-interface perspective.

Typical workflow:


Business scenario
      ↓
Agent identifies UI validation
      ↓
Execute UI test
      ↓
Capture result
      ↓
Analyze failure


The architecture is designed so that UI automation is treated as a tool available to the agent rather than being tightly coupled to the reasoning layer.

---

## 🗄️ Database Validation

Database queries provide another source of evidence during investigation.

For example:


User reports payment cancellation issue
             ↓
Agent identifies payment
             ↓
Query transaction state
             ↓
Validate expected DB state
             ↓
Compare with API response
             ↓
Analyze discrepancy


This enables correlation across multiple layers of the application.

---

# 🔍 Failure Investigation & RCA

One of the key goals of the project is to demonstrate **AI-assisted failure analysis**.

Instead of simply reporting:


Test Failed
Expected: CANCELLED
Actual:   PENDING

the agent can investigate multiple evidence sources:


Test Result
     +
API Response
     +
Database State
     +
Application Logs
     +
Relevant QE Knowledge
     ↓
AI Reasoning
     ↓
Potential Root Cause
     +
Supporting Evidence
     +
Recommended Next Action


The intention is to move from:

**"What failed?"**

toward:

**"Why did it fail, what evidence supports that conclusion, and what should the QE engineer investigate next?"**

---

# 📋 Jira Integration

The project also explores integration with Jira-based workflows.

Potential workflow:


Failure detected
      ↓
Agent investigates
      ↓
Collect evidence
      ↓
Identify likely root cause
      ↓
Generate defect information
      ↓
Create / update Jira issue


This helps connect automated testing with the broader software delivery lifecycle.

---

# 🧠 AI / RAG Technology Stack

| Component         | Technology            |
| ----------------- | --------------------- |
| Language          | Python                |
| LLM               | Ollama                |
| Embeddings        | Sentence Transformers |
| Vector Search     | FAISS                 |
| Agent Tooling     | MCP                   |
| UI Automation     | Playwright            |
| API Testing       | REST API automation   |
| AI Evaluation     | DeepEval              |
| Defect Management | Jira                  |
| Version Control   | Git / GitHub          |

---

# 🔬 AI Evaluation

AI systems require evaluation beyond traditional pass/fail testing.

This project explores **DeepEval** for evaluating AI/agent behavior.

Potential evaluation dimensions include:

* Answer relevance
* Context relevance
* Faithfulness
* Retrieval quality
* Agent behavior
* Tool usage
* End-to-end workflow quality

The objective is to apply **Quality Engineering principles to the AI system itself**.

AI Application
      ↓
AI Test Cases
      ↓
Execution
      ↓
Evaluation
      ↓
Metrics
      ↓
Feedback
      ↓
Improved AI Workflow


---

# 💳 Example Use Case — Payment Cancellation

A representative workflow is a payment cancellation scenario.

User:
"Why is payment FX-12345 still pending after cancellation?"


The agent can potentially:


1. Retrieve relevant cancellation requirements
                  ↓
2. Query transaction state
                  ↓
3. Execute API validation
                  ↓
4. Validate database state
                  ↓
5. Search application logs
                  ↓
6. Correlate evidence
                  ↓
7. Identify potential root cause
                  ↓
8. Provide investigation summary


Example reasoning output:


Transaction: FX-12345

Expected:
Payment should transition from PENDING → CANCELLED.

Observed:
API response indicates PENDING.
Database state remains PENDING.

Evidence:
- Cancellation request was accepted by the API.
- Expected state transition was not observed.
- Relevant application logs indicate downstream processing did not complete.

Assessment:
The cancellation request appears to have been accepted,
but the downstream state transition requires further investigation.

Recommended next step:
Investigate the downstream cancellation processor and
correlate the transaction/correlation ID with application logs.


The important principle is that the agent should provide **evidence-backed analysis rather than simply guessing a root cause**.

---

# 🧩 Project Structure


ai-qe-agent/
│
├── app/
│   ├── agent/
│   ├── rag/
│   ├── mcp/
│   ├── tools/
│   └── evaluation/
│
├── knowledge/
│   └── documents/
│
├── tests/
│
├── scripts/
│
├── requirements.txt
│
├── README.md
│
└── .env.example

> The structure may evolve as the project develops.

---

# ⚙️ Local Setup

## Prerequisites

Install:

* Python 3.x
* Git
* Ollama

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

### macOS / Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🧠 Configure the Local LLM

This project uses Ollama for local LLM experimentation.

Example:

```bash
ollama pull llama3.2:3b
```

Verify:

```bash
ollama list
```

---

## 🔎 Build / Prepare the Knowledge Base

The RAG workflow follows:

Documents
    ↓
Load
    ↓
Chunk
    ↓
Generate embeddings
    ↓
Store vectors
    ↓
FAISS similarity search


The knowledge base can contain application-specific:

* Requirements
* API documentation
* Test scenarios
* Business rules
* Troubleshooting information
* Test results
* QE documentation

---

# ▶️ Example Workflow

A typical interaction can look like:


User
 ↓
Ask question about failed payment
 ↓
Agent retrieves relevant knowledge
 ↓
Agent determines required tools
 ↓
MCP tool execution
 ↓
Collect API / UI / DB / log evidence
 ↓
LLM analyzes evidence
 ↓
Return grounded QE recommendation


---

# 🛡️ Engineering Principles

The project follows several important principles.

### Evidence over assumptions

AI responses should be supported by retrieved information or tool results wherever possible.

### Tool isolation

The reasoning layer should not directly own implementation details of every testing capability.

Tools expose controlled capabilities to the agent.

### Reusability

Testing capabilities should be reusable independently of the AI layer.

### Observability

Agent decisions, tool calls and test results should be traceable.

### Explainability

The system should make it possible for a QE engineer to understand **why** a recommendation was produced.

### Human-in-the-loop

AI should assist the QE engineer while keeping engineering judgment and critical decisions under human control.

---

# 🎯 Vision

The long-term vision is to evolve the project from an AI assistant into an **AI-enabled Quality Engineering platform**.


Traditional Test Automation
            ↓
API + UI + DB Automation
            ↓
CI/CD + Observability
            ↓
AI-assisted Test Analysis
            ↓
RAG + MCP
            ↓
AI Agents
            ↓
Intelligent Quality Engineering


The focus is on building **practical, explainable and engineering-driven AI solutions** that augment Quality Engineers and improve software delivery quality.

---

# 🔮 Future Enhancements

Potential areas for further exploration:

* Intelligent test-case generation
* AI-assisted test data generation
* Automated regression selection
* Failure clustering
* Root-cause analysis
* Autonomous test execution planning
* Test impact analysis
* Production-to-test feedback loops
* AI-generated defect summaries
* Agent evaluation and observability
* CI/CD integration
* Multi-agent QE workflows

---

# 📚 Learning Goals

This project is also an exploration of how established Quality Engineering practices can be applied to modern AI systems.

Key areas of experimentation include:

**Quality Engineering + Automation + RAG + LLMs + MCP + AI Agents**

The project is continuously evolving as new AI engineering and testing patterns are explored.

---

## 👨‍💻 Author

**Udaya Albert**

Senior SDET | Quality Engineering | Test Automation Architect | AI-enabled QE

12+ years of experience in software quality engineering, test automation and enterprise application testing.

### Core areas

`Java` · `Python` · `Playwright` · `Selenium` · `RestAssured` · `TestNG` · `API Testing` · `CI/CD` · `RAG` · `LLMs` · `MCP` · `AI Agents`

---

⭐ **This project is an ongoing exploration of AI-enabled Quality Engineering.**
