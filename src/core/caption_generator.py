import pickle
from transformers import GenerationConfig

class CaptionGenerator:
    def __init__(self):
        # Load processor and model from pickle
        with open('models/processor.pkl', 'rb') as processor_file:
            self.processor = pickle.load(processor_file)

        with open('models/model.pkl', 'rb') as model_file:
            self.model = pickle.load(model_file)

        # Patch model generation config to fix pickle issues
        self.model.generation_config = GenerationConfig()

    def generate_caption(self, image):
        """Generate caption for an image"""
        if image is None:
            return None

        inputs = self.processor(images=image, return_tensors='pt')
        pixel_values = inputs["pixel_values"]

        try:
            out = self.model.generate(
                pixel_values=pixel_values,
                max_length=16,
                num_beams=4,
                no_repeat_ngram_size=2,
                early_stopping=True
            )
            caption = self.processor.decode(out[0], skip_special_tokens=True)
            return caption
        except Exception as e:
            print(f'❌ Error while generating caption: {e}')
            return None
