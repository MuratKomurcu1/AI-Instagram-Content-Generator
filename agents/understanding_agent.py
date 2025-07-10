# agents/understanding_agent.py
import whisper
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

class UnderstandingAgent:
    def __init__(self, device='cpu'):
        self.device = device
        
        try:
            # Whisper model (küçük model)
            self.audio_model = whisper.load_model("small")
            print("✅ Whisper model yüklendi")
        except Exception as e:
            print(f"⚠️ Whisper yüklenemedi: {e}")
            self.audio_model = None
        
        try:
            # BLIP model (görsel açıklama için)
            self.image_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
            self.image_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
            print("✅ BLIP model yüklendi")
        except Exception as e:
            print(f"⚠️ BLIP yüklenemedi: {e}")
            self.image_processor = None
            self.image_model = None

    def transcribe_audio(self, audio_path):
        """Ses dosyasını metne çevir"""
        try:
            if not self.audio_model:
                return "Ses modeli mevcut değil"
            
            result = self.audio_model.transcribe(audio_path)
            return result["text"]
            
        except Exception as e:
            return f"Ses analiz hatası: {str(e)}"

    def describe_image(self, image_path):
        """Görseli açıkla"""
        try:
            if not self.image_model or not self.image_processor:
                return self._simple_image_description(image_path)
            
            # Resmi aç ve RGB'ye çevir
            image = Image.open(image_path).convert('RGB')
            
            # BLIP ile açıklama üret
            inputs = self.image_processor(images=image, return_tensors="pt")
            out = self.image_model.generate(**inputs, max_length=50)
            caption = self.image_processor.decode(out[0], skip_special_tokens=True)
            
            # Gaming context ekle
            return self._enhance_gaming_description(caption)
            
        except Exception as e:
            return self._simple_image_description(image_path)
    
    def analyze_video(self, video_path):
        """Video'yu analiz et (basit)"""
        try:
            import cv2
            
            # Video aç
            cap = cv2.VideoCapture(video_path)
            
            # Video bilgileri
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps if fps > 0 else 0
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            cap.release()
            
            return {
                'duration': f"{duration:.1f} saniye",
                'resolution': f"{width}x{height}",
                'fps': f"{fps:.1f}",
                'description': f"Oyun videosu - {duration:.1f} saniye"
            }
            
        except Exception as e:
            return {'error': f"Video analiz hatası: {str(e)}"}
    
    def _simple_image_description(self, image_path):
        """Basit görsel açıklaması (model olmadığında)"""
        try:
            image = Image.open(image_path)
            width, height = image.size
            
            # Dosya isminden tahmin et
            filename = image_path.lower()
            
            if 'menu' in filename:
                return "Oyun menü ekranı"
            elif 'character' in filename:
                return "Oyun karakteri görseli"
            elif 'gameplay' in filename:
                return "Oynanış ekran görüntüsü"
            elif 'screenshot' in filename:
                return "Oyun ekran görüntüsü"
            else:
                return f"Oyun görseli ({width}x{height})"
                
        except:
            return "Oyun görseli"
    
    def _enhance_gaming_description(self, basic_description):
        """BLIP açıklamasını gaming context ile zenginleştir"""
        gaming_terms = {
            'screen': 'oyun ekranı',
            'character': 'karakter',
            'game': 'oyun',
            'menu': 'menü',
            'button': 'buton',
            'interface': 'arayüz'
        }
        
        enhanced = basic_description.lower()
        
        # Gaming terimlerini ekle
        for eng_term, tr_term in gaming_terms.items():
            if eng_term in enhanced:
                enhanced = enhanced.replace(eng_term, tr_term)
        
        # Gaming context ekle
        if 'oyun' not in enhanced:
            enhanced = f"Oyun içerisinde {enhanced}"
        
        return enhanced.capitalize()