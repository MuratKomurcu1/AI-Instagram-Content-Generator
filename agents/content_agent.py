# agents/content_agent.py - Minimal versiyon (transformers olmadan)

class ContentAgent:
    def __init__(self, device=0):
        # Gaming caption template'leri
        self.gaming_templates = [
            "🎮 Bu oyunda en sevdiğim {feature}! {question} #gaming #mobilegaming",
            "🔥 {action} başardım! Kim daha ileride? #gaming #levelup", 
            "💥 Bu oyunun {aspect} muhteşem! Tavsiye ederim 👍 #gaming #oyun",
            "🎯 {achievement}! Sizin en büyük başarınız neydi? #gaming #başarı",
            "⚡ {gameplay_moment}! Bu sahneler çok epic 🚀 #gaming #gameplay",
            "🏆 Sonunda {goal} ulaştım! Çok heyecanlıyım 🎉 #gaming #victory",
            "🌟 {game_element} ile oyun deneyimi bambaşka oluyor! #gaming #feature",
            "🚀 Bu {level_type} seviyesinde rekor kırdım! Kim benimle yarışır? #gaming"
        ]
        
        self.emojis = ["🎮", "🔥", "💥", "🎯", "⚡", "🚀", "💯", "🏆", "⭐", "🎉", "👑", "💪", "🌟", "🎊"]
        
        # Gaming kelimeleri
        self.gaming_words = {
            'features': ['grafikler', 'kontroller', 'müzikler', 'karakter tasarımı', 'hikaye', 'animasyonlar'],
            'actions': ['Level up', 'Yeni rekor', 'Boss defeat', 'Görev tamamlama', 'Başarı kazanma', 'Perfect score'],
            'aspects': ['oynanışı', 'grafikleri', 'ses efektleri', 'hikayesi', 'karakterleri', 'mekaniği'],
            'achievements': ['Yüksek skor aldım', 'Zor seviyeyi geçtim', 'Gizli karakteri açtım', 'Tüm yıldızları topladım', 'Speedrun rekoru'],
            'moments': ['Bu combo harika', 'Perfect timing', 'Kritik vuruş', 'Süper hareket', 'Epic fail', 'Clutch moment'],
            'goals': ['final bossa', 'en yüksek seviyeye', 'tüm koleksiyonu', 'mükemmel skora', 'platinum trophy'],
            'game_elements': ['yeni karakter', 'özel ability', 'güçlü silah', 'rare item', 'secret area'],
            'level_types': ['boss', 'bonus', 'secret', 'final', 'challenge'],
            'questions': [
                'Sizce de öyle mi?', 'Kim katılıyor?', 'Ne düşünüyorsunuz?', 
                'Hanginiz denedi?', 'Yorumlarda paylaşın!', 'Kim bu skoru geçebilir?'
            ]
        }
        
        # Türkçe/İngilizce karışık template'ler
        self.mixed_templates = [
            "Just {action_eng}! 🔥 {tr_comment} #gaming #win",
            "OMG bu {feature} insane! 😱 {tr_reaction} #gaming #amazing", 
            "New personal best! 🏆 {tr_achievement} #gaming #record",
            "This game is fire! 🔥 {tr_opinion} #gaming #recommended"
        ]

    def generate_caption(self, trends, media_info, game_description=""):
        """Ana caption üretim metodu"""
        try:
            return self._generate_with_template(trends, media_info, game_description)
        except Exception as e:
            print(f"Caption üretim hatası: {e}")
            return self._emergency_caption()
    
    def _generate_with_template(self, trends, media_info, game_description):
        """Template ile caption üret"""
        import random
        
        # Template seç (90% gaming, 10% mixed)
        if random.random() < 0.9:
            template = random.choice(self.gaming_templates)
        else:
            template = random.choice(self.mixed_templates)
        
        # Template'i doldur
        filled_template = self._fill_template(template)
        
        # Game description'ı context olarak kullan
        if game_description:
            # Game description'dan anahtar kelimeler çıkar
            game_words = game_description.lower().split()
            
            # Platform, action, vs gibi kelimeler varsa template'e ekle
            for word in game_words:
                if word in ['platform', 'action', 'puzzle', 'strategy']:
                    filled_template = filled_template.replace('#gaming', f'#{word} #gaming')
                    break
        
        # Trend bilgisini kullan (basit mention)
        if trends and 'popüler' in trends.lower():
            filled_template += " 📈"
        
        return self._enhance_caption(filled_template)
    
    def _fill_template(self, template):
        """Template'deki placeholder'ları doldur"""
        import random
        
        replacements = {
            '{feature}': random.choice(self.gaming_words['features']),
            '{action}': random.choice(self.gaming_words['actions']),
            '{aspect}': random.choice(self.gaming_words['aspects']),
            '{achievement}': random.choice(self.gaming_words['achievements']),
            '{gameplay_moment}': random.choice(self.gaming_words['moments']),
            '{goal}': random.choice(self.gaming_words['goals']),
            '{game_element}': random.choice(self.gaming_words['game_elements']),
            '{level_type}': random.choice(self.gaming_words['level_types']),
            '{question}': random.choice(self.gaming_words['questions']),
            # Mixed template için
            '{action_eng}': random.choice(['leveled up', 'got high score', 'beat the boss', 'unlocked achievement']),
            '{tr_comment}': random.choice(['Çok zordu ama başardım', 'Bu oyun gerçekten harika', 'Sonunda başardım']),
            '{tr_reaction}': random.choice(['Bu kadar iyi olacağını düşünmemiştim', 'Kesinlikle tavsiye ederim']),
            '{tr_achievement}': random.choice(['Kişisel rekorum kırıldı', 'Bu skoru beklemiyordum']),
            '{tr_opinion}': random.choice(['Herkese tavsiye ederim', 'Bu oyunu mutlaka oynayın'])
        }
        
        result = template
        for placeholder, value in replacements.items():
            result = result.replace(placeholder, value)
        
        return result
    
    def _enhance_caption(self, caption):
        """Caption'ı emoji ve format ile zenginleştir"""
        import random
        
        # Emoji yoksa ekle
        if not any(emoji in caption for emoji in self.emojis):
            emoji = random.choice(self.emojis)
            if not caption.startswith(emoji):
                caption = f"{emoji} {caption}"
        
        # Hashtag yoksa ekle
        if '#' not in caption:
            caption += " #gaming #mobilegaming"
        
        # Büyük harfle başladığından emin ol
        if caption and not caption[0].isupper() and not caption[0] in self.emojis:
            caption = caption[0].upper() + caption[1:]
        
        # Call-to-action ekle (bazen)
        if random.random() < 0.3:
            cta_options = [
                "\n\nYorumlarda skorunuzu paylaşın! 💬",
                "\n\nBu oyunu oynayan var mı? 🎮", 
                "\n\nTakip etmeyi unutmayın! 👆",
                "\n\nArkadaşlarınızı etiketleyin! 👥"
            ]
            caption += random.choice(cta_options)
        
        return caption
    
    def _emergency_caption(self):
        """Acil durum caption'ı"""
        import random
        
        emergency_options = [
            "🎮 Harika bir oyun deneyimi! Bu oyunu herkese tavsiye ederim 🔥 #gaming #mobilegaming",
            "🚀 Bugün oyun oynayarak harika zaman geçirdim! Kim benimle katılıyor? #gaming #fun",
            "⚡ Bu seviyeleri geçmek gerçekten zor ama çok eğlenceli! 💯 #gaming #challenge",
            "🏆 Yeni bir başarı daha! Oyun oynamayı çok seviyorum 🎉 #gaming #achievement"
        ]
        
        return random.choice(emergency_options)
    
    def generate_multiple_options(self, trends, media_info, count=3):
        """Birden fazla caption seçeneği üret"""
        captions = []
        
        for i in range(count):
            caption = self.generate_caption(trends, media_info)
            captions.append({
                'option': i + 1,
                'caption': caption,
                'length': len(caption),
                'style': self._detect_style(caption)
            })
        
        return captions
    
    def _detect_style(self, caption):
        """Caption stilini tespit et"""
        if any(word in caption.lower() for word in ['omg', 'insane', 'fire']):
            return 'trendy'
        elif '!' in caption and len([c for c in caption if c in self.emojis]) >= 2:
            return 'excited'
        elif '?' in caption:
            return 'engaging'
        else:
            return 'casual'
    
    def generate_story_text(self, media_info):
        """Instagram Story için kısa metin"""
        story_templates = [
            "Bu oyun çok sarıyor! 🎮",
            "Yeni seviyeye geçtim! 🔥", 
            "Bu sahneyi görün! 💥",
            "Oyun zamanı! ⚡",
            "Epic moment! 🚀",
            "Rekor kırdım! 🏆",
            "Level up! 💯",
            "GG! 🎉"
        ]
        
        import random
        return random.choice(story_templates)