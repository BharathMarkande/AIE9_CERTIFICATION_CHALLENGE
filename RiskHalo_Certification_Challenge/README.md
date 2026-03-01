# RiskHalo Certification Challenge

RiskHalo Certification Challenge application for trading psychology and risk management coaching.

## Project Structure

```
RiskHalo_Certification_Challenge/
│
├── app/                            # Deterministic Analytics Layer
│   ├── parser.py                   # Input parsing and preprocessing
│   ├── feature_engine.py           # Feature extraction and transformation
│   ├── behavioral_engine.py        # Behavioral pattern analysis
│   ├── expectancy_engine.py        # Expectancy metrics computation
│   ├── session_summary_builder.py  # Creates snapshot object ready for embedding and vector database storage
│
├── rag/                    # Memory & Retrieval Layer
│   ├── embedder.py         # Text embedding
│   ├── vector_store.py     # Vector storage and indexing
│   ├── retriever.py        # Semantic retrieval
│
├── agents/                 # Agentic RAG Layer
│   ├── guardrail_agent.py  # Safety and compliance guardrails
│   ├── coach_agent.py      # Coaching and guidance agent
│
├── evaluation/              # RAGAS Evaluation Layer
│   ├── synthetic_dataset.py # Synthetic data generation
│   ├── ragas_eval.py        # RAGAS evaluation metrics
│
├── ui/                     # Demo Interface
│   ├── streamlit_app.py    # Streamlit web application
│
├── README.md
└── requirements.txt
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Streamlit app:
   ```bash
   streamlit run ui/streamlit_app.py
   ```

## License

Proprietary - RiskHalo Certification Challenge
