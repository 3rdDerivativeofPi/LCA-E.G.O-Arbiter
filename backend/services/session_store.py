import uuid
from services.vector_store import VectorStore


class Session:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.jd_text = None
        self.parsed_jd = None
        self.jd_embeddings = None
        self.candidates = []  # list of {id, name, parsed_cv, cv_embeddings}
        self.vector_store = VectorStore(dimension=768)

    def add_candidate(self, name: str, parsed_cv: dict, cv_embeddings: dict) -> str:
        candidate_id = str(uuid.uuid4())[:8]
        self.candidates.append({
            "id": candidate_id,
            "name": name,
            "parsed_cv": parsed_cv,
            "cv_embeddings": cv_embeddings,
        })
        self.vector_store.add(cv_embeddings["skills"], {"id": candidate_id, "name": name})
        return candidate_id


class SessionStore:
    def __init__(self):
        self._sessions: dict[str, Session] = {}

    def create(self) -> Session:
        session_id = str(uuid.uuid4())[:8]
        session = Session(session_id)
        self._sessions[session_id] = session
        return session

    def get(self, session_id: str) -> Session | None:
        return self._sessions.get(session_id)

    def delete(self, session_id: str):
        self._sessions.pop(session_id, None)


# Singleton
session_store = SessionStore()
