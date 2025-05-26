import pickle
import os
from transformers import GenerationConfig

class CaptionGenerator:
    def __init__(self):
        # Get absolute path to the models directory
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        models_dir = os.path.join(base_dir, 'models')
        
        try:
            # Load processor
            processor_path = os.path.join(models_dir, 'processor.pkl')
            if not os.path.exists(processor_path):
                raise FileNotFoundError(f"Processor file not found at {processor_path}")
                
            with open(processor_path, 'rb') as processor_file:
                self.processor = pickle.load(processor_file)

            # Load model
            model_path = os.path.join(models_dir, 'model.pkl')
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found at {model_path}")
                
            with open(model_path, 'rb') as model_file:
                self.model = pickle.load(model_file)

            # Patch model generation config to fix pickle issues
            self.model.generation_config = GenerationConfig()
            
        except Exception as e:
            print(f"❌ Error initializing caption generator: {e}")
            # Re-raise to propagate the error
            raise

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
