from PIL import Image

def ingest_image(image_path):
    img = Image.open(image_path).convert('RGB')
    # Here you would call vector DB API or external ML API
    print(f"Ingested Image: {image_path}, size: {img.size}")
