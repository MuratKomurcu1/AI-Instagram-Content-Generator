# agents/quality_agent.py
from PIL import Image
import cv2
import os

class QualityControlAgent:
    def __init__(self):
        # Instagram limitleri
        self.max_caption_length = 125
        self.min_caption_length = 10
        self.min_image_resolution = 720
        self.optimal_hashtag_count = (3, 11)  # Min, Max
        
        # Gaming context için özel kelimeler
        self.gaming_keywords = ['oyun', 'game', 'gaming', 'level', 'karakter', 'gameplay']

    def check_text_quality(self, text):
        """Metin kalitesini kontrol et"""
        issues = []
        
        if not text or not text.strip():
            return ["❌ Metin boş"]
        
        text = text.strip()
        
        # Uzunluk kontrolü
        if len(text) < self.min_caption_length:
            issues.append(f"❌ Metin çok kısa (minimum {self.min_caption_length} karakter, şu an {len(text)})")
        
        if len(text) > self.max_caption_length:
            issues.append(f"❌ Metin çok uzun (maksimum {self.max_caption_length} karakter, şu an {len(text)})")
        
        # Format kontrolü
        if not text[0].isupper():
            issues.append("❌ Büyük harfle başlamalı")
        
        # Emoji kontrolü
        common_emojis = "🎮🔥💥🎯⚡🚀💯🏆⭐🎉👑💪"
        if not any(emoji in text for emoji in common_emojis):
            issues.append("❌ En az bir emoji eklenmeli")
        
        # Hashtag kontrolü
        hashtag_count = text.count('#')
        if hashtag_count == 0:
            issues.append("❌ Hashtag eksik")
        elif hashtag_count > 11:
            issues.append("❌ Çok fazla hashtag (Instagram spamı)")
        
        # Gaming context kontrolü
        if not any(keyword in text.lower() for keyword in self.gaming_keywords):
            issues.append("⚠️ Gaming ile ilgili kelime eklenebilir")
        
        # Başarılı durumu
        if not issues:
            return ["✅ Metin kalitesi uygun"]
        
        return issues

    def check_image_quality(self, image_path):
        """Görsel kalitesini kontrol et"""
        issues = []
        
        try:
            if not os.path.exists(image_path):
                return ["❌ Dosya bulunamadı"]
            
            # Resmi aç
            image = Image.open(image_path)
            width, height = image.size
            
            # Çözünürlük kontrolü
            min_dimension = min(width, height)
            if min_dimension < self.min_image_resolution:
                issues.append(f"❌ Düşük çözünürlük: {width}x{height} (minimum {self.min_image_resolution}x{self.min_image_resolution})")
            
            # Instagram aspect ratio kontrolü
            aspect_ratio = width / height
            if aspect_ratio < 0.8 or aspect_ratio > 1.91:
                issues.append(f"⚠️ Instagram için ideal olmayan oran: {aspect_ratio:.2f} (ideal: 0.8-1.91)")
            
            # Dosya boyutu kontrolü (basit)
            file_size = os.path.getsize(image_path)
            if file_size > 8 * 1024 * 1024:  # 8MB
                issues.append("⚠️ Büyük dosya boyutu (8MB+)")
            
            # Format kontrolü
            if image.format not in ['JPEG', 'PNG', 'JPG']:
                issues.append(f"⚠️ Desteklenen format: JPEG/PNG (şu an: {image.format})")
            
            # Başarılı durum
            if not issues:
                return ["✅ Görsel kalitesi uygun"]
                
        except Exception as e:
            issues.append(f"❌ Görsel analiz hatası: {str(e)}")
        
        return issues

    def check_video_quality(self, video_path):
        """Video kalitesini kontrol et"""
        issues = []
        
        try:
            if not os.path.exists(video_path):
                return ["❌ Video dosyası bulunamadı"]
            
            # Video aç
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                return ["❌ Video açılamadı"]
            
            # Video bilgileri
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps if fps > 0 else 0
            
            cap.release()
            
            # Çözünürlük kontrolü
            min_dimension = min(width, height)
            if min_dimension < self.min_image_resolution:
                issues.append(f"❌ Video çözünürlüğü düşük: {width}x{height}")
            
            # FPS kontrolü
            if fps < 24:
                issues.append(f"❌ Düşük FPS: {fps:.1f} (minimum 24)")
            elif fps > 60:
                issues.append(f"⚠️ Yüksek FPS: {fps:.1f} (dosya boyutu büyük olabilir)")
            
            # Süre kontrolü (Instagram limits)
            if duration < 3:
                issues.append(f"❌ Video çok kısa: {duration:.1f}s (minimum 3s)")
            elif duration > 60:
                issues.append(f"⚠️ Instagram feed için uzun: {duration:.1f}s (maksimum 60s)")
            
            # Aspect ratio kontrolü
            aspect_ratio = width / height
            if aspect_ratio < 0.56 or aspect_ratio > 1.91:
                issues.append(f"⚠️ Sosyal medya için uygun olmayan oran: {aspect_ratio:.2f}")
            
            # Dosya boyutu kontrolü
            file_size = os.path.getsize(video_path)
            if file_size > 100 * 1024 * 1024:  # 100MB
                issues.append("⚠️ Çok büyük dosya boyutu (100MB+)")
            
            # Başarılı durum
            if not issues:
                return [f"✅ Video kalitesi uygun ({width}x{height}, {duration:.1f}s)"]
                
        except Exception as e:
            issues.append(f"❌ Video analiz hatası: {str(e)}")
        
        return issues

    def check_hashtags(self, hashtags):
        """Hashtag kalitesini kontrol et"""
        issues = []
        
        if not hashtags:
            return ["❌ Hashtag listesi boş"]
        
        # Liste formatı kontrolü
        if isinstance(hashtags, str):
            hashtags = hashtags.split()
        
        hashtag_count = len(hashtags)
        
        # Sayı kontrolü
        if hashtag_count < self.optimal_hashtag_count[0]:
            issues.append(f"⚠️ Az hashtag: {hashtag_count} (önerilen minimum {self.optimal_hashtag_count[0]})")
        elif hashtag_count > self.optimal_hashtag_count[1]:
            issues.append(f"❌ Çok fazla hashtag: {hashtag_count} (maksimum {self.optimal_hashtag_count[1]})")
        
        # Format kontrolü
        for i, hashtag in enumerate(hashtags):
            if not hashtag.startswith('#'):
                issues.append(f"❌ Hashtag # ile başlamalı: '{hashtag}'")
            
            if len(hashtag) < 3:
                issues.append(f"❌ Hashtag çok kısa: '{hashtag}'")
            
            if ' ' in hashtag:
                issues.append(f"❌ Hashtag boşluk içeremez: '{hashtag}'")
            
            # Özel karakter kontrolü
            if not hashtag[1:].replace('_', '').isalnum():
                issues.append(f"⚠️ Hashtag özel karakter içeriyor: '{hashtag}'")
        
        # Gaming hashtag kontrolü
        gaming_hashtags = ['#gaming', '#game', '#oyun', '#mobilegaming']
        if not any(tag.lower() in [h.lower() for h in hashtags] for tag in gaming_hashtags):
            issues.append("⚠️ Gaming hashtag'i eklenmeli (#gaming, #oyun, vb.)")
        
        # Başarılı durum
        if not issues:
            return [f"✅ Hashtag kalitesi uygun ({hashtag_count} adet)"]
        
        return issues

    def overall_quality_check(self, content_data):
        """Genel kalite kontrolü"""
        all_issues = []
        scores = []
        
        # Metin kontrolü
        if 'caption' in content_data and content_data['caption']:
            text_issues = self.check_text_quality(content_data['caption'])
            if "✅" in str(text_issues):
                scores.append(10)
            else:
                scores.append(max(1, 10 - len(text_issues)))
                all_issues.extend([f"📝 {issue}" for issue in text_issues])
        
        # Hashtag kontrolü
        if 'hashtags' in content_data and content_data['hashtags']:
            hashtag_issues = self.check_hashtags(content_data['hashtags'])
            if "✅" in str(hashtag_issues):
                scores.append(10)
            else:
                scores.append(max(1, 10 - len(hashtag_issues)))
                all_issues.extend([f"🏷️ {issue}" for issue in hashtag_issues])
        
        # Görsel kontrolü (varsa)
        if 'image_path' in content_data:
            image_issues = self.check_image_quality(content_data['image_path'])
            if "✅" in str(image_issues):
                scores.append(10)
            else:
                scores.append(max(1, 10 - len(image_issues)))
                all_issues.extend([f"🖼️ {issue}" for issue in image_issues])
        
        # Video kontrolü (varsa)
        if 'video_path' in content_data:
            video_issues = self.check_video_quality(content_data['video_path'])
            if "✅" in str(video_issues):
                scores.append(10)
            else:
                scores.append(max(1, 10 - len(video_issues)))
                all_issues.extend([f"🎬 {issue}" for issue in video_issues])
        
        # Genel skor hesapla
        if scores:
            average_score = sum(scores) / len(scores)
        else:
            average_score = 5
        
        # Status belirle
        if average_score >= 8:
            status = 'excellent'
            status_emoji = '🏆'
        elif average_score >= 6:
            status = 'good' 
            status_emoji = '✅'
        elif average_score >= 4:
            status = 'needs_improvement'
            status_emoji = '⚠️'
        else:
            status = 'poor'
            status_emoji = '❌'
        
        return {
            'status': status,
            'score': round(average_score, 1),
            'emoji': status_emoji,
            'message': f'{status_emoji} Kalite skoru: {average_score:.1f}/10',
            'issues': all_issues,
            'recommendations': self._get_recommendations(all_issues)
        }
    
    def _get_recommendations(self, issues):
        """Sorunlara göre öneriler ver"""
        recommendations = []
        
        issue_text = ' '.join(issues).lower()
        
        if 'kısa' in issue_text:
            recommendations.append("💡 Caption'ı biraz uzatın, daha fazla detay ekleyin")
        
        if 'emoji' in issue_text:
            recommendations.append("💡 Gaming emojileri ekleyin: 🎮🔥💥🎯⚡")
        
        if 'hashtag' in issue_text:
            recommendations.append("💡 #gaming #mobilegaming #oyun hashtag'lerini ekleyin")
        
        if 'çözünürlük' in issue_text:
            recommendations.append("💡 Daha yüksek çözünürlüklü görseller kullanın (min 720p)")
        
        if 'oran' in issue_text:
            recommendations.append("💡 Instagram için kare (1:1) veya dikey (4:5) format kullanın")
        
        if 'fps' in issue_text:
            recommendations.append("💡 Video'yu 30 FPS'ye export edin")
        
        if not recommendations:
            recommendations.append("🎉 Harika! Kalite standartlarını karşılıyor")
        
        return recommendations