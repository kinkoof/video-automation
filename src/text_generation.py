import json
import requests
from pathlib import Path


class TextGenerator:
    def __init__(self):
        config_path = Path(__file__).parent.parent / 'config' / 'config.json'
        with open(config_path) as f:
            config = json.load(f)

        self.api_key = config['openrouter']['api_key']
        self.model = config['openrouter']['model']
        self.base_url = config['openrouter']['base_url']

    def generate_script(self, prompt):
        """
        Generate a script using the OpenRouter API with deepseek model
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        data = {
            'model': self.model,
            'messages': [{'role': 'user', 'content': prompt}]
        }

        try:
            response = requests.post(
                f'{self.base_url}/chat/completions',
                headers=headers,
                json=data
            )
            response.raise_for_status()

            result = response.json()
            generated_text = result['choices'][0]['message']['content']
            return generated_text

        except requests.exceptions.RequestException as e:
            print(f"Error generating text: {str(e)}")
            return None


if __name__ == "__main__":
    # Test the text generation
    generator = TextGenerator()
    test_prompt = "Write a short creative story about space exploration"
    result = generator.generate_script(test_prompt)
    if result:
        print("Generated Text:")
        print(result)
