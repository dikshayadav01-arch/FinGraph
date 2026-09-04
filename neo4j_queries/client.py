import os

from neo4j import GraphDatabase


class Neo4jClient:

    def __init__(
        self,
        uri="bolt://172.19.176.1:7687",
        username="neo4j"
    ):
        password = os.getenv("NEO4J_PASSWORD")

        if not password:
            raise RuntimeError(
                "NEO4J_PASSWORD environment variable is not set."
            )

        self.driver = GraphDatabase.driver(
            uri,
            auth=(username, password)
        )

    def run_query(self, query):
        with self.driver.session() as session:
            result = session.run(query)
            return [record.data() for record in result]

    def close(self):
        self.driver.close()
