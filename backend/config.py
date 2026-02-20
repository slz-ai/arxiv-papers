from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DAILY_DIR = DATA_DIR / "daily"
CONFERENCE_DIR = DATA_DIR / "conferences"
INDEX_FILE = DATA_DIR / "index.json"

# arXiv settings
ARXIV_CATEGORIES = ["cs.CL", "cs.AI", "cs.LG", "cs.IR", "cs.MA"]
ARXIV_MAX_RESULTS = 500
ARXIV_DELAY_SECONDS = 3.0

# Keywords: tag_name -> list of search patterns (case-insensitive)
KEYWORDS = {
    "LLM": [
        "large language model", "LLM", "LLMs",
        "language model pretraining", "instruction tuning",
        "foundation model", "pre-trained language model",
        "GPT", "ChatGPT", "LLaMA", "Llama", "Mistral", "Gemini",
        "fine-tuning", "RLHF", "alignment",
    ],
    "RAG": [
        "retrieval-augmented generation", "retrieval augmented",
        "RAG", "retrieve-and-generate",
        "knowledge-grounded generation", "grounded generation",
    ],
    "Information Retrieval": [
        "information retrieval",
        "dense retrieval", "sparse retrieval", "neural retrieval",
        "document retrieval", "passage retrieval",
        "re-ranking", "reranking", "neural ranking",
        "bi-encoder", "cross-encoder",
        "BM25", "query understanding", "query expansion",
        "search ranking", "relevance ranking",
        "embedding retrieval", "semantic search",
    ],
    "Personalization": [
        "personalization", "personalized",
        "user preference", "user modeling", "user profile",
        "recommendation system", "collaborative filtering",
    ],
    "Multi-Modal RAG": [
        "multi-modal retrieval", "multimodal RAG",
        "vision-language retrieval", "cross-modal retrieval",
        "multimodal retrieval-augmented",
    ],
    "Agentic AI": [
        "agentic", "AI agent", "AI agents",
        "autonomous agent", "tool-use", "tool use",
        "function calling", "agent framework",
        "multi-agent", "multi agent", "LLM agent",
    ],
    "Search Agent": [
        "search agent", "web search agent",
        "information retrieval agent", "browsing agent",
        "web agent", "search-augmented",
    ],
    "Context Compression": [
        "context compression", "prompt compression",
        "context distillation", "context pruning",
        "context window", "long context",
        "key-value cache", "KV cache compression",
    ],
}

# All unique tags
ALL_TAGS = sorted(KEYWORDS.keys())

# Semantic Scholar settings
S2_API_KEY = None  # Set via S2_API_KEY environment variable
S2_RATE_LIMIT = 1.0  # seconds between requests

# Conferences to track
# OpenReview conferences (AI三大会) - no API key needed
# Semantic Scholar conferences (NLP三大会) - needs S2_API_KEY
CONFERENCES = {
    # OpenReview-based (fetched via openreview_fetcher.py)
    "iclr_2026":    {"name": "ICLR 2026",    "venue": "ICLR",    "year": "2026"},
    "iclr_2025":    {"name": "ICLR 2025",    "venue": "ICLR",    "year": "2025"},
    "neurips_2025": {"name": "NeurIPS 2025", "venue": "NeurIPS", "year": "2025"},
    "neurips_2024": {"name": "NeurIPS 2024", "venue": "NeurIPS", "year": "2024"},
    "icml_2025":    {"name": "ICML 2025",    "venue": "ICML",    "year": "2025"},
    "icml_2024":    {"name": "ICML 2024",    "venue": "ICML",    "year": "2024"},
    # Semantic Scholar-based (NLP三大会)
    "acl_2025":     {"name": "ACL 2025",     "venue": "ACL",     "year": "2025"},
    "emnlp_2025":   {"name": "EMNLP 2025",   "venue": "EMNLP",   "year": "2025"},
    "naacl_2025":   {"name": "NAACL 2025",   "venue": "NAACL",   "year": "2025"},
}
