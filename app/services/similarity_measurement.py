from math import sqrt

class SimilarityMeasurementService:
    def execute(self, a: list[float], b: list[float]) -> float:
        """
            Cosine similarity between two vectors aligned to the same vocabulary.
        """

        dot = sum(x * y for x, y in zip(a, b))          # Somatório a[i] . b[i]
        norm_a = sqrt(sum(x * x for x in a))            # Módulo(a)
        norm_b = sqrt(sum(y * y for y in b))            # Módulo(b)

        if norm_a == 0 or norm_b == 0:                  # Frase sem nenhum token sobrando
            return 0.0
        
        return dot / (norm_a * norm_b)

    def build_similarity_matrix(self, vectors: list[list[float]]) -> list[list[float]]:
        n = len(vectors)
        matrix = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                sim = self.execute(vectors[i], vectors[j])
                matrix[i][j] = sim
                matrix[j][i] = sim
        return matrix

    def similarity_sum(self, matrix: list[list[float]]) -> list[float]:
        """
            Score of each sentence = sum of its similarity with all other sentences.
            The diagonal is 0, so a sentence's similarity with itself is not counted.
        """
        return [sum(row) for row in matrix]
