from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os
from services.vocabulary_service import VocabularyService
from services.dictionary_service import DictionaryService
from services.translation_service import TranslationService
from models.vocabulary import VocabularyRequest, VocabularyResponse
import tempfile
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Vocabulary App",
    description="An app to import vocabulary from txt files and export enriched data to CSV",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Initialize services
vocabulary_service = VocabularyService()
dictionary_service = DictionaryService()
translation_service = TranslationService()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api")
async def api_root():
    return {"message": "Welcome to Vocabulary App API"}

@app.post("/upload-vocabulary/")
async def upload_vocabulary_file(file: UploadFile = File(...)):
    """
    Upload a txt file containing vocabulary words (one word per line)
    """
    if not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="Only .txt files are allowed")
    
    try:
        content = await file.read()
        words = content.decode('utf-8').strip().split('\n')
        words = [word.strip() for word in words if word.strip()]
        
        return {
            "message": f"Successfully uploaded {len(words)} words",
            "words": words[:10],  # Show first 10 words as preview
            "total_count": len(words)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/process-vocabulary/")
async def process_vocabulary(file: UploadFile = File(...)):
    """
    Process vocabulary file and return enriched data with meanings, examples, IPA, and POS
    """
    if not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="Only .txt files are allowed")
    
    try:
        content = await file.read()
        words = content.decode('utf-8').strip().split('\n')
        words = [word.strip() for word in words if word.strip()]
        
        # Process each word
        processed_words = []
        for word in words:
            try:
                # Get dictionary data from Cambridge
                dict_data = await dictionary_service.get_word_data(word)
                
                # Translate example to Vietnamese and combine
                example_combined = ""
                if dict_data.get('example'):
                    vietnamese_example = await translation_service.translate_to_vietnamese(dict_data['example'])
                    if vietnamese_example and vietnamese_example != dict_data.get('example'):
                        example_combined = f"{dict_data.get('example')} | {vietnamese_example}"
                    else:
                        example_combined = dict_data.get('example', '')
                
                processed_word = {
                    "word": word,
                    "meaning_en": dict_data.get('meaning', ''),
                    "meaning_vi": await translation_service.translate_to_vietnamese(dict_data.get('meaning', '')),
                    "example": example_combined,
                    "ipa": dict_data.get('ipa', ''),
                    "pos": dict_data.get('pos', '')
                }
                processed_words.append(processed_word)
                
            except Exception as e:
                # If error processing individual word, add with empty data
                processed_word = {
                    "word": word,
                    "meaning_en": f"Error: {str(e)}",
                    "meaning_vi": "",
                    "example": "",
                    "ipa": "",
                    "pos": ""
                }
                processed_words.append(processed_word)
        
        return {
            "message": f"Successfully processed {len(processed_words)} words",
            "data": processed_words
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/export-csv/")
async def export_to_csv(file: UploadFile = File(...)):
    """
    Process vocabulary file and export to CSV format
    """
    if not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="Only .txt files are allowed")
    
    try:
        content = await file.read()
        words = content.decode('utf-8').strip().split('\n')
        words = [word.strip() for word in words if word.strip()]
        
        # Process words and create CSV
        csv_file_path = await vocabulary_service.create_csv_from_words(
            words, dictionary_service, translation_service
        )
        
        return FileResponse(
            csv_file_path,
            media_type='application/octet-stream',
            filename=f"vocabulary_export.csv"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating CSV: {str(e)}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("APP_HOST", "0.0.0.0")
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    uvicorn.run(
        app, 
        host=host, 
        port=port,
        reload=debug
    ) 