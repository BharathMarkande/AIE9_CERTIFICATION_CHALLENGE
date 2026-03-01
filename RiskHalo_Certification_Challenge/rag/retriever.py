class RiskHaloRetriever:
    """
    Retrieves similar behavioral session snapshots
    using semantic similarity search.
    """

    def __init__(self, vector_store):
        self.collection = vector_store.collection

    def retrieve(self, query_embedding: list, top_k: int = 3):
        """
        Returns top-k similar sessions.

        Args:
            query_embedding (list): Embedded user query.
            top_k (int): Number of sessions to retrieve.

        Returns:
            dict: Retrieved documents and metadata.
        """

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results