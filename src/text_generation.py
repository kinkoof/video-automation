import json
from pathlib import Path
import google.generativeai as genai


class TextGenerator:
    def __init__(self):
        config_path = Path(__file__).parent.parent / 'config' / 'config.json'
        with open(config_path) as f:
            config = json.load(f)

        self.api_key = config['gemini']['api_key']
        genai.configure(api_key=self.api_key)
        # Use gemini-pro model for text generation
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def generate_script(self, prompt):
        """
        Generate a script using the Gemini API
        """
        try:
            response = self.model.generate_content(prompt)

            if response.text:
                # Clean up the text - remove metadata comments and special characters like #
                clean_text = response.text
                # Remove anything in parentheses at the end
                clean_text = clean_text.split('(')[0].strip()
                # Remove any quotes if present
                clean_text = clean_text.strip('"')
                # Remove '#' and other special characters that might be read aloud
                for ch in ['#', '*', '_', '~', '`']:
                    clean_text = clean_text.replace(ch, '')
                # Remove "Fact:" from the text that will be spoken
                clean_text = clean_text.replace('Fact:', '')
                clean_text = clean_text.strip()

                return clean_text
            else:
                return None

        except Exception as e:
            print(f"Error generating text: {str(e)}")
            return None


if __name__ == "__main__":
    # Test the text generation
    generator = TextGenerator()
    test_prompt = """
    Create a viral-style video script about a trending topic. The text should be clear and engaging, ready to be converted to audio. Include:

    1. A catchy, intriguing title (e.g., “6 Surprising Facts About [Topic], #5 Will Blow Your Mind!”).
    2. Six interesting facts about the topic, each presented in a short, captivating way.

    Make sure the text flows well into the audio narration.
    """
    result = generator.generate_script(test_prompt)
    if result:
        print("Generated Text:")
        print(result)
