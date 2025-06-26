import json
from pathlib import Path
from elevenlabs import generate, save, Voice, VoiceSettings
from elevenlabs import set_api_key


class AudioProcessor:
    def __init__(self):
        config_path = Path(__file__).parent.parent / 'config' / 'config.json'
        with open(config_path) as f:
            config = json.load(f)

        self.api_key = config['elevenlabs']['api_key']
        self.voice_id = config['elevenlabs']['voice_id']
        set_api_key(self.api_key)

    def text_to_speech(self, text, output_path):
        """
        Convert text to speech using ElevenLabs API
        """
        try:
            audio = generate(
                text=text,
                voice=Voice(
                    voice_id=self.voice_id,
                    settings=VoiceSettings(
                        stability=0.5, similarity_boost=0.75)
                )
            )

            # Create output directory if it doesn't exist
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)

            # Save the audio file
            save(audio, output_path)
            return True

        except Exception as e:
            print(f"Error in text to speech conversion: {str(e)}")
            return False

    def generate_subtitles(self, audio_path, output_path):
        """
        Generate subtitles from audio using ElevenLabs API
        Note: This is a placeholder as ElevenLabs STT is not yet publicly available
        In the meantime, you might want to use other STT services like Google Speech-to-Text
        """
        try:
            # Placeholder for STT functionality
            # When ElevenLabs STT becomes available, implement it here
            print("STT functionality not yet implemented")
            return False

        except Exception as e:
            print(f"Error in speech to text conversion: {str(e)}")
            return False


if __name__ == "__main__":
    # Test the audio processing
    processor = AudioProcessor()
    test_text = "This is a test of the text to speech conversion."
    result = processor.text_to_speech(test_text, "output/test_audio.mp3")
    if result:
        print("Audio file generated successfully")
