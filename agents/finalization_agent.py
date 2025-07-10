# agents/finalization_agent.py

class FinalizationAgent:
    def __init__(self):
        # Popüler gaming hashtag'leri
        self.gaming_hashtags = [
            '#gaming', '#mobilegaming', '#gameplay', '#gamer', '#gamedev',
            '#indiegame', '#esports', '#mobilegame', '#oyun', '#mobiloyun',
            '#platform', '#action', '#puzzle', '#adventure', '#strategy',
            '#arcade', '#casual', '#indie', '#retro', '#multiplayer'
        ]
        
        # Platform spesifik hashtag'ler
        self.platform_hashtags = {
            'instagram': ['#insta', '#ig', '#instaphoto', '#instagaming'],
            'tiktok': ['#fyp', '#viral', '#trending', '#foryou'],
            'general': ['#fun', '#amazing', '#cool', '#awesome', '#epic']
        }

    def generate_hashtags(self, keywords, max_count=10):
        """Anahtar kelimelerden hashtag'ler üret"""
        hashtags = []
        
        # Anahtar kelimeleri hashtag'e çevir
        if keywords:
            for keyword in keywords:
                if keyword and keyword.strip():
                    # Temizle ve hashtag yap
                    clean_keyword = keyword.strip().lower().replace(' ', '').replace('-', '')
                    if clean_keyword and not clean_keyword.startswith('#'):
                        hashtags.append(f"#{clean_keyword}")
        
        # Gaming hashtag'leri ekle
        import random
        available_gaming = [tag for tag in self.gaming_hashtags if tag not in hashtags]
        gaming_count = min(5, len(available_gaming))
        hashtags.extend(random.sample(available_gaming, gaming_count))
        
        # Genel hashtag'ler ekle
        if len(hashtags) < max_count:
            remaining = max_count - len(hashtags)
            general_tags = random.sample(self.platform_hashtags['general'], min(remaining, 2))
            hashtags.extend(general_tags)
        
        # Maksimum sayıyı aşmasın
        return hashtags[:max_count]

    def finalize_post(self, caption, hashtags, platform='instagram'):
        """Caption ve hashtag'leri birleştirip final post oluştur"""
        
        # Caption kontrolü
        if not caption or not caption.strip():
            caption = "🎮 Harika bir oyun deneyimi!"
        
        # Hashtag kontrolü
        if not hashtags:
            hashtags = self.generate_hashtags(['gaming', 'mobile'])
        
        # Hashtag'leri string'e çevir
        if isinstance(hashtags, list):
            hashtag_str = ' '.join(hashtags)
        else:
            hashtag_str = str(hashtags)
        
        # Platform'a göre format
        if platform == 'instagram':
            # Instagram: Caption + boşluk + hashtag'ler
            final_post = f"{caption.strip()}\n\n{hashtag_str}"
        elif platform == 'tiktok':
            # TikTok: Caption ile hashtag'ler karışık
            final_post = f"{caption.strip()} {hashtag_str}"
        else:
            # Genel format
            final_post = f"{caption.strip()}\n\n{hashtag_str}"
        
        return final_post

    def optimize_for_platform(self, content, platform):
        """Platform'a göre içeriği optimize et"""
        
        optimizations = {
            'instagram': {
                'max_caption_length': 125,
                'optimal_hashtags': 11,
                'style': 'Aesthetic and engaging'
            },
            'tiktok': {
                'max_caption_length': 100,
                'optimal_hashtags': 5,
                'style': 'Short and catchy'
            },
            'twitter': {
                'max_caption_length': 220,  # Tweet character limit'i hesaba katarak
                'optimal_hashtags': 3,
                'style': 'Concise and direct'
            }
        }
        
        if platform not in optimizations:
            platform = 'instagram'  # Default
        
        platform_config = optimizations[platform]
        
        # Caption uzunluğu kontrolü
        caption = content.get('caption', '')
        if len(caption) > platform_config['max_caption_length']:
            # Kısalt
            caption = caption[:platform_config['max_caption_length'] - 3] + '...'
        
        # Hashtag sayısı kontrolü
        hashtags = content.get('hashtags', [])
        if len(hashtags) > platform_config['optimal_hashtags']:
            hashtags = hashtags[:platform_config['optimal_hashtags']]
        
        # Platform spesifik hashtag'ler ekle
        platform_specific = self.platform_hashtags.get(platform, [])
        if platform_specific and len(hashtags) < platform_config['optimal_hashtags']:
            import random
            additional = random.choice(platform_specific)
            if additional not in hashtags:
                hashtags.append(additional)
        
        return {
            'caption': caption,
            'hashtags': hashtags,
            'platform': platform,
            'style_guide': platform_config['style'],
            'optimized_post': self.finalize_post(caption, hashtags, platform)
        }

    def add_call_to_action(self, caption):
        """Caption'a call-to-action ekle"""
        
        cta_options = [
            "💬 Yorumlarda düşüncelerinizi paylaşın!",
            "👥 Arkadaşlarınızı etiketleyin!",
            "❤️ Beğendiyseniz kalp bırakın!",
            "🔄 Bu postu paylaşmayı unutmayın!",
            "👆 Takip etmeyi unutmayın!",
            "📤 DM'den oyun önerilerinizi gönderin!",
            "🎮 Siz hangi oyunları oynuyorsunuz?",
            "⭐ Puan verirseniz ne kadar verirsiniz?"
        ]
        
        import random
        cta = random.choice(cta_options)
        
        # Caption'ın sonuna ekle
        if not caption.endswith('!') and not caption.endswith('?'):
            caption += '!'
        
        return f"{caption}\n\n{cta}"

    def generate_content_variations(self, base_caption, hashtags, count=3):
        """Aynı içerik için farklı varyasyonlar üret"""
        variations = []
        
        # Emoji varyasyonları
        emoji_sets = [
            ['🎮', '🔥', '💥'],
            ['🚀', '⚡', '🎯'],
            ['🏆', '💯', '⭐'],
            ['🎉', '👑', '💪']
        ]
        
        # Caption style varyasyonları
        styles = [
            'excited',  # Heyecanlı
            'informative',  # Bilgilendirici
            'casual',  # Rahat
            'professional'  # Profesyonel
        ]
        
        import random
        
        for i in range(count):
            # Emoji set seç
            emoji_set = random.choice(emoji_sets)
            
            # Style seç
            style = random.choice(styles)
            
            # Caption'ı varyasyona göre düzenle
            varied_caption = self._apply_style_variation(base_caption, style, emoji_set)
            
            # Hashtag'leri karıştır
            shuffled_hashtags = hashtags.copy()
            random.shuffle(shuffled_hashtags)
            
            variations.append({
                'variation': i + 1,
                'style': style,
                'caption': varied_caption,
                'hashtags': shuffled_hashtags,
                'final_post': self.finalize_post(varied_caption, shuffled_hashtags)
            })
        
        return variations

    def _apply_style_variation(self, caption, style, emoji_set):
        """Caption'a stil varyasyonu uygula"""
        
        if style == 'excited':
            # Daha fazla emoji ve ünlem
            caption = caption.replace('!', '! ')
            if not any(emoji in caption for emoji in emoji_set):
                caption = f"{emoji_set[0]} {caption}"
            return caption + f" {emoji_set[1]}{emoji_set[2]}"
        
        elif style == 'informative':
            # Daha az emoji, daha fazla bilgi
            caption = caption.replace('!', '.')
            return f"💡 {caption}"
        
        elif style == 'casual':
            # Günlük konuşma tarzı
            casual_starters = ["Bugün ", "Az önce ", "Şu an ", "Geçen "]
            import random
            starter = random.choice(casual_starters)
            return f"{starter.lower()}{caption} 😊"
        
        elif style == 'professional':
            # Daha resmi ton
            return f"🎯 {caption}"
        
        return caption

    def get_posting_schedule(self, content_count=1):
        """Optimal posting zamanlaması öner"""
        
        # Gaming content için optimal saatler (Türkiye saati)
        optimal_times = {
            'weekdays': ['19:00', '20:00', '21:00', '22:00'],
            'weekend': ['14:00', '16:00', '19:00', '20:00', '21:00']
        }
        
        # Günler
        best_days = {
            'instagram': ['Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi'],
            'tiktok': ['Salı', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar'],
            'twitter': ['Salı', 'Çarşamba', 'Perşembe']
        }
        
        return {
            'optimal_times': optimal_times,
            'best_days': best_days,
            'recommendation': 'Gaming içerikleri için akşam saatleri (19:00-22:00) ideal',
            'frequency': 'Günde 1-2 post optimal, haftada 5-7 post'
        }