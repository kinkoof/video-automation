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
            # Print first 100 chars of script
            print(f"Generated script: {script[:100]}...")
            tts_result = self.audio_processor.text_to_speech(
                script, str(audio_path))
            if not tts_result:
                raise Exception("Failed to convert text to speech")
            print(f"Audio file should be at: {audio_path}")
            if not audio_path.exists():
                raise Exception(f"Audio file was not created at {audio_path}")

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
    Create a viral-style video script about a current trending topic. Follow this exact format:

    Title: 6 shocking facts about [choose a current trending topic]

    Start with: "Here are 6 mind-blowing facts about [topic]"

    Then list 6 facts, one per line, starting each with "Fact:" followed by the information.
    Make each fact brief, engaging, and easy to understand.
    Focus on recent events, discoveries, or trending news.

    End with: "Which fact surprised you the most? Let us know in the comments!"

    Important:
    - Do not use numbers, hashtags, or special characters
    - Keep each fact under 15 words
    - Make it conversational and easy to read aloud
    - Focus on verified, factual information
    """

    try:
        final_video = automation.create_video(prompt)
        if final_video:
            print("\n🎉 Video creation completed!")
            print(f"📁 Video saved to: {final_video}")

            # Upload to YouTube
            try:
                from src.youtube_uploader import YouTubeUploader
                uploader = YouTubeUploader()

                # Extract title from the script
                title = prompt.split('\n')[0].strip()
                if not title:
                    title = "AI Generated Video"

                video_id = uploader.upload_video(
                    final_video,
                    title=title,
                    privacy_status="private"  # Start as private for safety
                )

                if video_id:
                    print(f"\n🎥 Video uploaded to YouTube!")
                    print(f"🔗 Watch here: https://youtu.be/{video_id}")
                    print("\nNote: The video is set to PRIVATE by default.")
                    print("You can change privacy settings in YouTube Studio.")
            except Exception as e:
                print(f"\n⚠️ YouTube upload failed: {str(e)}")
                print("The video was created successfully but couldn't be uploaded.")
                print("You can upload it manually or try again later.")
        else:
            print("\n❌ Video creation failed")
    finally:
        # Temporarily disable cleanup to debug audio issues
        pass  # automation.cleanup()


if __name__ == "__main__":
    main()
