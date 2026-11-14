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

    def textrank(self, matrix: list[list[float]], d: float = 0.85,
        max_iter: int = 100, tol: float = 1e-6) -> list[float]:
        n = len(matrix)
        if n == 0:
            return []
        row_sums = [sum(row) for row in matrix]
        scores = [1.0 / n] * n                      # everyone starts equal

        for _ in range(max_iter):
            new_scores = []
            for i in range(n):
                # each neighbour j gives i a share of its own score,
                # proportional to how much of j's similarity goes to i
                incoming = sum(
                    matrix[j][i] / row_sums[j] * scores[j]
                    for j in range(n)
                    if row_sums[j] > 0
                )
                new_scores.append((1 - d) / n + d * incoming)

            converged = max(abs(a - b) for a, b in zip(new_scores, scores)) < tol
            scores = new_scores
            if converged:
                break

        return scores
