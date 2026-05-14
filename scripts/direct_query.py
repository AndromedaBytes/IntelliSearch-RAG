import sys
import pathlib

project_root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from backend.app.services.chromadb_service import chroma_service

res = chroma_service.query_corpus("Xeno", top_k=3)
print(res)
print("Corpus size:", chroma_service.get_corpus_size())
