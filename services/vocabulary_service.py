import pandas as pd
import tempfile
import os
from typing import List
import asyncio

class VocabularyService:
    def __init__(self):
        pass
    
    async def create_csv_from_words(
        self, 
        words: List[str], 
        dictionary_service, 
        translation_service
    ) -> str:
        """
        Process a list of words and create CSV file with format:
        Word | Meaning_EN | Meaning_VI | Example | Example_VI | IPA | POS
        """
        processed_data = []
        
        for word in words:
            try:
                print(f"Processing word: {word}")
                
                # Get dictionary data
                dict_data = await dictionary_service.get_word_data(word)
                
                # Translate meaning to Vietnamese
                meaning_vi = ""
                if dict_data.get('meaning'):
                    meaning_vi = await translation_service.translate_to_vietnamese(dict_data['meaning'])
                
                # Translate example to Vietnamese and combine
                example_combined = ""
                if dict_data.get('example'):
                    example_vi = await translation_service.translate_to_vietnamese(dict_data['example'])
                    if example_vi and example_vi != dict_data.get('example'):
                        example_combined = f"{dict_data.get('example')} | {example_vi}"
                    else:
                        example_combined = dict_data.get('example', '')
                
                # Create row data
                row_data = {
                    'Word': word,
                    'Meaning_EN': dict_data.get('meaning', ''),
                    'Meaning_VI': meaning_vi,
                    'Example': example_combined,
                    'IPA': dict_data.get('ipa', ''),
                    'POS': dict_data.get('pos', '')
                }
                
                processed_data.append(row_data)
                
                # Small delay to avoid overwhelming the APIs
                await asyncio.sleep(0.5)
                
            except Exception as e:
                print(f"Error processing word '{word}': {str(e)}")
                # Add error row
                error_row = {
                    'Word': word,
                    'Meaning_EN': f'Error: {str(e)}',
                    'Meaning_VI': '',
                    'Example': '',
                    'IPA': '',
                    'POS': ''
                }
                processed_data.append(error_row)
        
        # Create DataFrame and save to CSV
        df = pd.DataFrame(processed_data)
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        csv_path = temp_file.name
        temp_file.close()
        
        # Save CSV with proper encoding
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        
        return csv_path
    
    def read_vocabulary_file(self, file_path: str) -> List[str]:
        """
        Read vocabulary words from a text file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                words = [word.strip() for word in content.split('\n') if word.strip()]
                return words
        except Exception as e:
            raise Exception(f"Error reading file: {str(e)}")
    
    def validate_words(self, words: List[str]) -> List[str]:
        """
        Validate and clean vocabulary words
        """
        cleaned_words = []
        for word in words:
            # Remove extra whitespace and check if valid
            clean_word = word.strip()
            if clean_word and len(clean_word) > 0:
                # Basic validation - only letters and common characters
                if clean_word.replace(' ', '').replace('-', '').replace("'", "").isalpha():
                    cleaned_words.append(clean_word.lower())
        
        return list(set(cleaned_words))  # Remove duplicates 