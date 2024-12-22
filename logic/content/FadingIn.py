import numpy as np

def fading_with_background(clip, background_clip, position_func, duration=0.2, initial_opacity=0.2):
        """
        Fade in clip by blending with background, starting from specified opacity
        
        Parameters:
        clip: VideoClip to fade in
        background_clip: Background video clip
        position_func: Function that returns position at given time
        duration: Duration of fade effect in seconds
        initial_opacity: Starting opacity of the clip (0.0 to 1.0)
        """
        def fading(get_frame, t):
            frame = get_frame(t)
            frame_h, frame_w = frame.shape[:2]
            
            # Get current position from position function
            pos_x, pos_y = position_func(t)
            pos_x, pos_y = int(pos_x), int(pos_y)
            
            # Get the corresponding section of background
            bg_frame = background_clip.get_frame(t)
            bg_y_start = max(0, pos_y)
            bg_y_end = min(bg_frame.shape[0], pos_y + frame_h)
            bg_x_start = max(0, pos_x)
            bg_x_end = min(bg_frame.shape[1], pos_x + frame_w)
            
            # Get the relevant section of background
            bg_section = bg_frame[bg_y_start:bg_y_end, bg_x_start:bg_x_end]
            
            # Ensure bg_section matches frame dimensions
            if bg_section.shape != frame.shape:
                # Create a new background section with matching dimensions
                bg_section = np.zeros_like(frame)
                # Fill with the average color of the visible background
                if bg_frame.size > 0:
                    avg_color = np.mean(bg_frame, axis=(0, 1))
                    bg_section[:] = avg_color
            
            if t < duration:
                # Calculate opacity for current time
                current_opacity = (t / duration) * (1 - initial_opacity) + initial_opacity
                
                # Convert to float32 for better precision in blending
                frame = frame.astype(np.float32) / 255
                bg_section = bg_section.astype(np.float32) / 255
                
                # Blend frames
                blended = frame * current_opacity + bg_section * (1 - current_opacity)
                
                # Convert back to uint8
                return (blended * 255).astype(np.uint8)
                
            return frame
        
        return clip.transform(lambda get_frame, t: fading(get_frame, t))