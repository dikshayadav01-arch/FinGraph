from pathlib import Path

from fastapi import FastAPI

from neo4j_queries.client import Neo4jClient


app = FastAPI(
    title="FinGraph Investigation API",
    description="Fraud investigation API for FinGraph",
    version="1.0.0",
)


QUERIES_DIR = Path(__file__).parent / "queries"


def run_query_file(filename):
    query_path = QUERIES_DIR / filename
    query = query_path.read_text(encoding="utf-8")

    client = Neo4jClient()

    try:
        return client.run_query(query)
    finally:
        client.close()


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "FinGraph Investigation API",
    }


@app.get("/fraud/starburst")
def detect_starburst():
    return run_query_file("starburst_detection.cypher")


@app.get("/fraud/smurfing")
def detect_smurfing():
    return run_query_file("smurfing_detection.cypher")


@app.get("/fraud/circular")
def detect_circular():
    return run_query_file("circular_detection.cypher")