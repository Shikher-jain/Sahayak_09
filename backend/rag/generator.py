from transformers import pipeline

class Generator:
    def __init__(self, model_name="Qwen/Qwen2.5-7B-Instruct"):
        self.generator = pipeline("text-generation", model=model_name)

    def generate_answer(self, context, question):
        prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
        result = self.generator(prompt, max_length=512, do_sample=False)
        return result[0]["generated_text"].strip()
