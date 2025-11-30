import unittest
from backend.cosdata_client import CosDataClient

class TestCosDataClient(unittest.TestCase):
    def setUp(self):
        self.client = CosDataClient()

    def test_embed_text(self):
        text = "Hello world!"
        embedding = self.client.embed_text(text)
        self.assertIsInstance(embedding, list)
        self.assertEqual(len(embedding), 384)

    def test_embed_image(self):
        # Use a small test image
        from PIL import Image
        import numpy as np
        img = Image.fromarray(np.zeros((224,224,3), dtype=np.uint8))
        img.save("test_img.png")
        embedding = self.client.embed_image("test_img.png")
        self.assertIsInstance(embedding, list)
        self.assertEqual(len(embedding), 512)  # CLIP default

    def tearDown(self):
        import os
        if os.path.exists("test_img.png"):
            os.remove("test_img.png")

if __name__ == "__main__":
    unittest.main()
