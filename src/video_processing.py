import json
import ffmpeg
from pathlib import Path


class VideoProcessor:
    def __init__(self):
        config_path = Path(__file__).parent.parent / 'config' / 'config.json'
        with open(config_path) as f:
            config = json.load(f)

        self.background_video = config['video']['background_video_path']
        self.background_music = config['video']['background_music_path']
        self.output_path = config['video']['output_path']

    def create_video(self, audio_path, subtitle_path, output_filename):
        """
        Create final video using FFmpeg with background video, audio, subtitles and background music
        """
        try:
            # Create output directory if it doesn't exist
            output_dir = Path(self.output_path)
            output_dir.mkdir(parents=True, exist_ok=True)

            final_output = output_dir / output_filename

            # Input streams with looping for background video
            background_video = ffmpeg.input(
                self.background_video, stream_loop=-1)  # Infinite loop
            narration_audio = ffmpeg.input(audio_path)

            # Get audio duration
            probe = ffmpeg.probe(audio_path)
            duration = float(probe['streams'][0]['duration'])

            # Process video: scale for YouTube Shorts (9:16) and match audio duration
            video = (
                background_video
                .video
                .filter('scale', 1080, 1920)  # YouTube Shorts format
                .filter('trim', duration=duration)  # Match audio duration
            )

            # Add subtitles if provided
            if subtitle_path and Path(subtitle_path).exists():
                video = video.filter('subtitles', subtitle_path)

            # Output with video and audio
            output = ffmpeg.output(
                video,
                narration_audio,  # Use the entire input stream
                str(final_output),
                vcodec='libx264',
                acodec='copy',  # Copy audio without re-encoding
                shortest=None,
                t=duration
            )

            # Run the FFmpeg command
            ffmpeg.run(output, overwrite_output=True, quiet=True)

            return str(final_output)

        except Exception as e:
            print(f"Error creating video: {str(e)}")
            return None

    def create_simple_srt(self, text, duration, output_path):
        """
        Create a simple SRT subtitle file with smart sentence splitting
        """
        try:
            # Split text into meaningful chunks
            lines = text.split('\n')
            sentences = []

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Handle title specially
                if line.startswith('Title:'):
                    title_parts = line[6:].strip().split(
                        ' ', 1)  # Split after first word
                    if len(title_parts) > 1:
                        sentences.append(title_parts[0])  # First word of title
                        sentences.append(title_parts[1])  # Rest of title
                    else:
                        sentences.append(line[6:].strip())
                    continue

                # Remove "Fact:" prefix if present
                if line.startswith('Fact:'):
                    line = line[5:].strip()

                # Split long lines at natural pause points
                if len(line.split()) > 12:
                    parts = line.split(', ')
                    sentences.extend([p.strip() for p in parts if p.strip()])
                else:
                    sentences.append(line)

            # Clean up sentences
            sentences = [s.strip() for s in sentences if s.strip()]

            # Calculate timing
            subtitle_duration = duration / len(sentences)

            # Generate SRT content
            srt_content = ""
            for i, sentence in enumerate(sentences):
                start_time = i * subtitle_duration
                end_time = (i + 1) * subtitle_duration

                start_formatted = self._format_time(start_time)
                end_formatted = self._format_time(end_time)

                srt_content += f"{i + 1}\n"
                srt_content += f"{start_formatted} --> {end_formatted}\n"
                srt_content += f"{sentence}\n\n"

            # Create output directory if it doesn't exist
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(srt_content)

            return True

        except Exception as e:
            print(f"Error creating SRT file: {str(e)}")
            return False

    def _format_time(self, seconds):
        """Format time for SRT format (HH:MM:SS,mmm)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds % 1) * 1000)

        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"


if __name__ == "__main__":
    # Test video processing
    processor = VideoProcessor()
    print("Video processor initialized")
