from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlmodel import Session, select
from .database import engine, User

class UsernameSearchService:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 3))
        self.users_list = []
        self.username_vectors = None

    def rebuild_index(self):
        with Session(engine) as session:
            self.users_list = session.exec(
                select(User)
            ).all()
            usernames = [user.username for user in self.users_list]

            if usernames:
                self.username_vectors = self.vectorizer.fit_transform(usernames)
            else:
                self.username_vectors = None

    def search(self, query, top_n=10):
        if self.username_vectors is None:
            return []

        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.username_vectors).flatten()
        top_indices = similarities.argsort()[::-1][:top_n]

        results = [
            self.users_list[i]
            for i in top_indices
            if similarities[i] > 0.1
        ]

        return results

# Global singleton instance
username_search_service = UsernameSearchService()