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

            # Input streams
            background_video = ffmpeg.input(self.background_video)
            narration_audio = ffmpeg.input(audio_path)
            background_music = ffmpeg.input(self.background_music)

            # Get audio duration to determine video length
            probe = ffmpeg.probe(audio_path)
            duration = float(probe['streams'][0]['duration'])

            # Process video: trim to audio duration and scale for YouTube Shorts (9:16)
            video = (
                background_video
                .video
                .filter('scale', 1080, 1920)  # YouTube Shorts format
                # Adjust speed if needed
                .filter('setpts', f'PTS*{duration}/60')
                # Loop if shorter than audio
                .filter('loop', loop=-1, size=1, start=0)
            )

            # Mix audio: narration + background music (lower volume)
            audio_mix = ffmpeg.filter(
                [narration_audio.audio,
                    background_music.audio.filter('volume', 0.2)],
                'amix',
                inputs=2,
                duration='longest'
            )

            # Add subtitles if provided
            if subtitle_path and Path(subtitle_path).exists():
                video = video.filter('subtitles', subtitle_path)

            # Output with video and mixed audio
            output = ffmpeg.output(
                video,
                audio_mix,
                str(final_output),
                vcodec='libx264',
                acodec='aac',
                t=duration,
                **{'b:v': '2M', 'b:a': '128k'}
            )

            # Run the FFmpeg command
            ffmpeg.run(output, overwrite_output=True, quiet=True)

            return str(final_output)

        except Exception as e:
            print(f"Error creating video: {str(e)}")
            return None

    def create_simple_srt(self, text, duration, output_path):
        """
        Create a simple SRT subtitle file
        This is a basic implementation - you might want to enhance it
        """
        try:
            # Split text into chunks for subtitles
            words = text.split()
            words_per_subtitle = 8
            subtitle_chunks = [' '.join(words[i:i+words_per_subtitle])
                               for i in range(0, len(words), words_per_subtitle)]

            subtitle_duration = duration / len(subtitle_chunks)

            srt_content = ""
            for i, chunk in enumerate(subtitle_chunks):
                start_time = i * subtitle_duration
                end_time = (i + 1) * subtitle_duration

                start_formatted = self._format_time(start_time)
                end_formatted = self._format_time(end_time)

                srt_content += f"{i + 1}\n"
                srt_content += f"{start_formatted} --> {end_formatted}\n"
                srt_content += f"{chunk}\n\n"

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
