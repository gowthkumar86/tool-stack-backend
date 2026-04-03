from gliner import GLiNER

model = GLiNER.from_pretrained("urchade/gliner_base")

def extract_entities(text: str, labels: list):
    entities = model.predict_entities(text, labels)

    return [
        {
            "text": ent["text"],
            "label": ent["label"],
            "score": ent["score"]
        }
        for ent in entities
    ]