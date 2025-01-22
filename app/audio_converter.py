import ffmpeg
import os

async def convert_audio(input_filename: str) -> str:
    # Define the output filename
    output_filename = input_filename.replace(".wav", ".mp3")
    
    # Convert audio using ffmpeg
    try:
        # Perform the conversion
        ffmpeg.input(input_filename).output(output_filename).run()
        
        return output_filename
    
    except ffmpeg.Error as e:
        print("FFmpeg error:", e)
        raise Exception("FFmpeg conversion failed")
