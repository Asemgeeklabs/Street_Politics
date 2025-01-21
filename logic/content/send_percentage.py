import requests , math
from moviepy import *
from moviepy.video.io.ffmpeg_writer import FFMPEG_VideoWriter

class WebhookLogger:
    def __init__(self, total_frames, webhook_url):
        self.total_frames = total_frames
        self.webhook_url = webhook_url
        self.last_percentage = 0

    def callback(self, frame_number):
        # Calculate progress percentage
        percentage = math.floor((frame_number / self.total_frames) * 100)
        
        # Only send updates if the percentage changes
        if percentage > self.last_percentage:
            self.last_percentage = percentage
            self.send_update(percentage)

    def send_update(self, percentage):
        data = {"progress": percentage}
        try:
            response = requests.post(self.webhook_url, json=data)
            if response.status_code == 200:
                ...
            else:
                print(f"Failed to send progress. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error sending progress: {e}")

# Custom FFMPEG Writer to integrate progress tracking
class CustomFFMPEG_VideoWriter(FFMPEG_VideoWriter):
    def __init__(self, *args, webhook_logger=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.webhook_logger = webhook_logger
        self.current_frame = 0

    def write_frame(self, img_array):
        # Call the parent method to handle writing the frame
        super().write_frame(img_array)
        
        # Update the current frame count and notify the webhook logger
        self.current_frame += 1
        if self.webhook_logger:
            self.webhook_logger.callback(self.current_frame)

def render_video_with_progress(video, output_path, webhook_url):
    # Get total frames for progress calculation
    total_frames = int(video.fps * video.duration)
    
    # Create a WebhookLogger instance
    webhook_logger = WebhookLogger(total_frames, webhook_url)

    # Use the custom FFMPEG writer with the webhook logger
    writer = CustomFFMPEG_VideoWriter(
        filename=output_path,
        size=video.size,
        fps=video.fps,
        codec="libx264",
        audiofile=None,
        threads=4,
        webhook_logger=webhook_logger
    )

    # Render the video frame by frame
    for frame in video.iter_frames(fps=video.fps, dtype="uint8"):
        writer.write_frame(frame)

    # Close the writer
    writer.close()
