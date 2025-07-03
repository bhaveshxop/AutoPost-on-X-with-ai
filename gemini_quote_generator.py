import google.generativeai as genai
import random
import logging
from typing import Optional
import time

class GeminiQuoteGenerator:
    def __init__(self, api_key: str):
        """Initialize Gemini API client"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.themes = [
            "motivation", "success", "productivity", "mindset", 
            "inspiration", "perseverance", "growth", "achievement",
            "leadership", "creativity", "wisdom", "courage"
        ]
        
    def generate_quote(self, theme: Optional[str] = None, max_length: int = 260) -> str:
        """Generate a motivational quote using Gemini AI"""
        try:
            if not theme:
                theme = random.choice(self.themes)
            
            prompt = f"""Generate a powerful, original motivational quote about {theme}. 
            Requirements:
            - Maximum {max_length} characters
            - Inspiring and actionable
            - Original and unique
            - No quotation marks
            - Include relevant hashtags at the end
            - Professional and positive tone
            
            Example format: "Your limitation—it's only your imagination. #Motivation #Success #Mindset"
            
            Generate one quote about {theme}:"""
            
            response = self.model.generate_content(prompt)
            quote = response.text.strip()
            
            # Clean up the quote
            quote = quote.replace('"', '').replace("'", "'")
            
            # Ensure it's within character limit
            if len(quote) > max_length:
                # Try to truncate at word boundary
                words = quote.split()
                truncated = ""
                for word in words:
                    if len(truncated + " " + word) <= max_length - 3:
                        truncated += " " + word if truncated else word
                    else:
                        break
                quote = truncated + "..."
            
            logging.info(f"Generated quote: {quote}")
            return quote
            
        except Exception as e:
            logging.error(f"Error generating quote: {e}")
            # Fallback quotes
            fallback_quotes = [
                "Success is not final, failure is not fatal: it is the courage to continue that counts. #Motivation #Success",
                "The only way to do great work is to love what you do. #Inspiration #Passion #Work",
                "Don't watch the clock; do what it does. Keep going. #Persistence #Motivation #Time",
                "The future belongs to those who believe in the beauty of their dreams. #Dreams #Future #Belief"
            ]
            return random.choice(fallback_quotes)
    
    def generate_multiple_quotes(self, count: int = 5, theme: Optional[str] = None) -> list[str]:
        """Generate multiple quotes for batch posting"""
        quotes = []
        for i in range(count):
            try:
                quote = self.generate_quote(theme)
                quotes.append(quote)
                # Add delay to respect rate limits
                if i < count - 1:
                    time.sleep(2)
            except Exception as e:
                logging.error(f"Error generating quote {i+1}: {e}")
                continue
        return quotes
