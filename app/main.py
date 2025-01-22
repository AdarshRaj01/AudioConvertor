from fastapi import FastAPI, File, UploadFile, HTTPException
import shutil
import os
from app.audio_converter import convert_audio  # Ensure the convert_audio function is correctly imported

app = FastAPI()

# Endpoint for uploading the audio file
@app.post("/convert/")
async def convert_file(file: UploadFile = File(...)):
    try:
        # Save the uploaded file temporarily
        temp_filename = f"temp_{file.filename}"
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Call the conversion function to convert to MP3
        mp3_filename = await convert_audio(temp_filename)

        # You can now return the converted file or use it for further processing
        return {"message": "File converted successfully", "mp3_file": mp3_filename}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")
    
    finally:
        # Clean up temporary files
        if os.path.exists(temp_filename):
            os.remove(temp_filename)  # Use os.remove to delete the file
