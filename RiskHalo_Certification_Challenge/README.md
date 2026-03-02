# AIE09 Certification Challenge

# RiskHalo - A Behavioral Risk Intelligence Engine for Intraday Traders

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
   uv sync
   ```

2. Run the Streamlit app:
   ```bash
   streamlit run ui/streamlit_app.py
   ```
