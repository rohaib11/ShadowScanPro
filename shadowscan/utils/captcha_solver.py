"""
SHADOWSCAN PRO - Captcha Solver
Automated captcha solving for attacks
Developed by ROHAIB TECHNICAL | +92 306 3844400
"""

import asyncio
import base64
import re
from typing import Optional, Tuple
from io import BytesIO
import logging

logger = logging.getLogger(__name__)


class CaptchaSolver:
    """Solve various types of captchas"""
    
    def __init__(self):
        self.tesseract_available = self._check_tesseract()
        self.easyocr_available = self._check_easyocr()
        self.api_key = None
        
        if self.easyocr_available:
            import easyocr
            self.reader = easyocr.Reader(['en'], gpu=False)
    
    def _check_tesseract(self) -> bool:
        try:
            import pytesseract
            from PIL import Image
            return True
        except ImportError:
            return False
    
    def _check_easyocr(self) -> bool:
        try:
            import easyocr
            return True
        except ImportError:
            return False
    
    async def solve_image(self, image_data: bytes) -> Optional[str]:
        """Solve image captcha"""
        if self.easyocr_available:
            return await self._solve_easyocr(image_data)
        elif self.tesseract_available:
            return await self._solve_tesseract(image_data)
        return None
    
    async def _solve_easyocr(self, image_data: bytes) -> Optional[str]:
        """Solve using EasyOCR"""
        try:
            from PIL import Image
            
            image = Image.open(BytesIO(image_data))
            image = self._preprocess_image(image)
            
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(None, self.reader.readtext, image)
            
            if results:
                text = ' '.join(r[1] for r in results)
                text = self._clean_text(text)
                if text:
                    return text
        except Exception as e:
            logger.error(f"EasyOCR failed: {e}")
        return None
    
    async def _solve_tesseract(self, image_data: bytes) -> Optional[str]:
        """Solve using Tesseract"""
        try:
            import pytesseract
            from PIL import Image
            
            image = Image.open(BytesIO(image_data))
            image = self._preprocess_image(image)
            
            config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
            
            loop = asyncio.get_event_loop()
            text = await loop.run_in_executor(None, lambda: pytesseract.image_to_string(image, config=config))
            
            text = self._clean_text(text)
            if text:
                return text
        except Exception as e:
            logger.error(f"Tesseract failed: {e}")
        return None
    
    def _preprocess_image(self, image):
        """Preprocess image for better OCR"""
        try:
            from PIL import ImageFilter, ImageOps, ImageEnhance
            
            image = image.convert('L')
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            image = image.point(lambda x: 0 if x < 128 else 255, '1')
            
            if image.getpixel((0, 0)) == 0:
                image = ImageOps.invert(image)
            
            image = image.filter(ImageFilter.MedianFilter(size=3))
            return image
        except:
            return image
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text"""
        if not text:
            return ""
        text = re.sub(r'[^a-zA-Z0-9]', '', text)
        text = text.upper()
        text = text.replace('O', '0').replace('I', '1').replace('L', '1')
        text = text.replace('S', '5').replace('Z', '2').replace('B', '8')
        return text.strip()
    
    async def solve_math(self, question: str) -> Optional[str]:
        """Solve math captcha"""
        try:
            pattern = r'(\d+)\s*([+\-*/])\s*(\d+)'
            match = re.search(pattern, question)
            
            if match:
                num1 = int(match.group(1))
                op = match.group(2)
                num2 = int(match.group(3))
                
                if op == '+':
                    return str(num1 + num2)
                elif op == '-':
                    return str(num1 - num2)
                elif op == '*':
                    return str(num1 * num2)
                elif op == '/':
                    return str(num1 // num2) if num2 != 0 else "0"
        except Exception as e:
            logger.error(f"Math captcha failed: {e}")
        return None
    
    async def solve_recaptcha_v2(self, site_key: str, url: str) -> Optional[str]:
        """Solve reCAPTCHA v2 (requires 2captcha API)"""
        # This would integrate with 2captcha or similar service
        logger.info(f"reCAPTCHA solving requires API key")
        return None
    
    async def solve_hcaptcha(self, site_key: str, url: str) -> Optional[str]:
        """Solve hCaptcha"""
        logger.info(f"hCaptcha solving requires API key")
        return None