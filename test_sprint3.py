from services.embedding_service import build_vector_store, search

# نبنيها مرة واحدة بس
build_vector_store()

# نجرب نسأل سؤال
results = search("كام يوم إجازة سنوية؟")
for r in results:
    print("Source:", r["source"])
    print("Text:", r["chunk"][:150])
    print("---")