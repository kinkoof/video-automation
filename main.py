import json
from pathlib import Path
from src.text_generation import TextGenerator
from src.audio_processing import AudioProcessor
from src.video_processing import VideoProcessor


class VideoAutomation:
    def __init__(self):
        self.text_generator = TextGenerator()
        self.audio_processor = AudioProcessor()
        self.video_processor = VideoProcessor()

        # Create necessary directories
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)

    def create_video(self, prompt):
        """
        Complete video creation pipeline:
        1. Generate script from prompt
        2. Convert script to audio
        3. Generate subtitles
        4. Create final video
        """
        try:
            print("🧠 Generating script...")
            script = self.text_generator.generate_script(prompt)
            if not script:
                raise Exception("Failed to generate script")

            print("🎙️ Converting to speech...")
            audio_path = self.output_dir / "narration.mp3"
            if not self.audio_processor.text_to_speech(script, str(audio_path)):
                raise Exception("Failed to convert text to speech")

            print("🎬 Creating subtitles...")
            subtitle_path = self.output_dir / "subtitles.srt"
            # Get audio duration for subtitle timing
            import ffmpeg
            probe = ffmpeg.probe(str(audio_path))
            duration = float(probe['streams'][0]['duration'])

            if not self.video_processor.create_simple_srt(script, duration, str(subtitle_path)):
                raise Exception("Failed to create subtitles")

            print("🎬 Creating final video...")
            final_video = self.video_processor.create_video(
                str(audio_path),
                str(subtitle_path),
                "final_video.mp4"
            )

            if not final_video:
                raise Exception("Failed to create video")

            print(f"✅ Video created successfully: {final_video}")
            return final_video

        except Exception as e:
            print(f"❌ Error in video creation pipeline: {str(e)}")
            return None

    def cleanup(self):
        """
        Clean up temporary files
        """
        try:
            # Remove temporary files but keep the final video
            temp_files = ["narration.mp3", "subtitles.srt"]
            for file in temp_files:
                temp_path = self.output_dir / file
                if temp_path.exists():
                    temp_path.unlink()
        except Exception as e:
            print(f"Warning: Cleanup failed: {str(e)}")


def main():
    # Example usage
    automation = VideoAutomation()

    # Example prompt
    prompt = """
    Create an engaging short video script about space exploration.
    The script should be concise and suitable for a YouTube Short.
    Include interesting facts and maintain an engaging tone.
    """

    try:
        final_video = automation.create_video(prompt)
        if final_video:
            print("\n🎉 Video creation completed!")
            print(f"📁 Video saved to: {final_video}")
        else:
            print("\n❌ Video creation failed")
    finally:
        automation.cleanup()


if __name__ == "__main__":
    main()
