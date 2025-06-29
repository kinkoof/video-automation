import json
from pathlib import Path
from f5_tts.api import F5TTS


class AudioProcessor:
    def __init__(self):
        self.tts = F5TTS()

    def text_to_speech(self, text, output_path):
        """
        Convert text to speech using F5-TTS
        """
        try:
            # Create output directory if it doesn't exist
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)

            # Reference files for voice style
            ref_file = Path(__file__).parent.parent / \
                'assets' / 'tts' / 'ref_voice.mp3'
            ref_text = Path(__file__).parent.parent / \
                'assets' / 'tts' / 'ref_text.txt'

            # Use F5TTS instance to generate audio
            audio_tuple = self.tts.infer(
                gen_text=text, ref_file=str(ref_file), ref_text=str(ref_text))
            # Unpack audio bytes from tuple
            audio = audio_tuple[0] if isinstance(
                audio_tuple, tuple) else audio_tuple
            # Save audio to output_path
            with open(output_path, "wb") as f:
                f.write(audio)
            return True

        except Exception as e:
            print(f"Error in text to speech conversion: {str(e)}")
            return False

    def generate_subtitles(self, audio_path, output_path):
        """
        Generate subtitles from audio - placeholder
        """
        print("STT functionality not yet implemented")
        return False


if __name__ == "__main__":
    # Test the audio processing
    processor = AudioProcessor()
    test_text = "This is a test of the text to speech conversion."
    result = processor.text_to_speech(test_text, "output/test_audio.mp3")
    if result:
        print("Audio file generated successfully")
