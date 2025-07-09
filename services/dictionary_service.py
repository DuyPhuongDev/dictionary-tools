import httpx
import asyncio
from typing import Dict, Optional
import re
from bs4 import BeautifulSoup

class DictionaryService:
    def __init__(self):
        self.base_url = "https://dictionary.cambridge.org/dictionary/english"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    async def get_word_data(self, word: str) -> Dict[str, str]:
        """
        Get word data from Cambridge Dictionary
        Returns dictionary with meaning, example, ipa, and pos
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                url = f"{self.base_url}/{word.lower().strip()}"
                response = await client.get(url, headers=self.headers)
                
                if response.status_code == 200:
                    return self._parse_cambridge_page(response.text, word)
                else:
                    # If Cambridge doesn't work, try alternative method
                    return await self._get_basic_definition(word)
                    
        except Exception as e:
            print(f"Error fetching data for '{word}': {str(e)}")
            return {
                'meaning': f'Unable to fetch definition for "{word}"',
                'example': '',
                'ipa': '',
                'pos': ''
            }
    
    def _parse_cambridge_page(self, html_content: str, word: str) -> Dict[str, str]:
        """
        Parse Cambridge Dictionary HTML page to extract word information
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract meaning
            meaning = ""
            definition_block = soup.find('div', {'class': 'def-block'}) or soup.find('div', {'class': 'ddef_d'})
            if definition_block:
                def_element = definition_block.find('div', {'class': 'def'}) or definition_block.find('div', {'class': 'ddef_d'})
                if def_element:
                    meaning = def_element.get_text().strip()
            
            # Extract example
            example = ""
            example_element = soup.find('span', {'class': 'eg'}) or soup.find('div', {'class': 'examp'})
            if example_element:
                example = example_element.get_text().strip()
            
            # Extract IPA pronunciation
            ipa = ""
            ipa_element = soup.find('span', {'class': 'ipa'}) or soup.find('span', {'class': 'pron'})
            if ipa_element:
                ipa = ipa_element.get_text().strip()
            
            # Extract part of speech
            pos = ""
            pos_element = soup.find('span', {'class': 'pos'}) or soup.find('span', {'class': 'gram'})
            if pos_element:
                pos = pos_element.get_text().strip()
            
            return {
                'meaning': meaning or f'Definition not found for "{word}"',
                'example': example,
                'ipa': ipa,
                'pos': pos
            }
            
        except Exception as e:
            print(f"Error parsing page for '{word}': {str(e)}")
            return {
                'meaning': f'Error parsing definition for "{word}"',
                'example': '',
                'ipa': '',
                'pos': ''
            }
    
    async def _get_basic_definition(self, word: str) -> Dict[str, str]:
        """
        Fallback method to get basic definition using a simpler API
        """
        try:
            # Using a free dictionary API as fallback
            async with httpx.AsyncClient(timeout=15.0) as client:
                url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
                response = await client.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    if data and len(data) > 0:
                        entry = data[0]
                        
                        # Extract meaning
                        meaning = ""
                        if 'meanings' in entry and len(entry['meanings']) > 0:
                            meaning_obj = entry['meanings'][0]
                            if 'definitions' in meaning_obj and len(meaning_obj['definitions']) > 0:
                                meaning = meaning_obj['definitions'][0].get('definition', '')
                        
                        # Extract example
                        example = ""
                        if 'meanings' in entry and len(entry['meanings']) > 0:
                            meaning_obj = entry['meanings'][0]
                            if 'definitions' in meaning_obj and len(meaning_obj['definitions']) > 0:
                                example = meaning_obj['definitions'][0].get('example', '')
                        
                        # Extract IPA
                        ipa = ""
                        if 'phonetics' in entry and len(entry['phonetics']) > 0:
                            for phonetic in entry['phonetics']:
                                if 'text' in phonetic:
                                    ipa = phonetic['text']
                                    break
                        
                        # Extract part of speech
                        pos = ""
                        if 'meanings' in entry and len(entry['meanings']) > 0:
                            pos = entry['meanings'][0].get('partOfSpeech', '')
                        
                        return {
                            'meaning': meaning or f'Definition not found for "{word}"',
                            'example': example,
                            'ipa': ipa,
                            'pos': pos
                        }
                        
        except Exception as e:
            print(f"Error with fallback API for '{word}': {str(e)}")
        
        return {
            'meaning': f'Unable to fetch definition for "{word}"',
            'example': '',
            'ipa': '',
            'pos': ''
        } 