import logging
from fastapi import FastAPI, File, UploadFile, HTTPException
import shutil
import os
from app.audio_converter import convert_audio
from fastapi.middleware.cors import CORSMiddleware



# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend's URL for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/convert/")
async def convert_file(file: UploadFile = File(...)):
    try:
        # Save the uploaded file temporarily
        temp_filename = f"temp_{file.filename}"
        logger.info(f"Temporary file created: {temp_filename}")
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Call the conversion function to convert to MP3
        mp3_filename = await convert_audio(temp_filename)

        return {"message": "File converted successfully", "mp3_file": mp3_filename}
    
    except Exception as e:
        logger.error(f"Conversion failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")
    
    finally:
        # Clean up temporary files
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
