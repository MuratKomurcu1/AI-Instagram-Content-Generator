# agents/socialtrend_agent.py - Minimal versiyon (transformers olmadan)

class socialtrend_agent:
    def __init__(self):
        # Popüler gaming hashtag'leri
        self.popular_hashtags = [
            "#gaming", "#mobilegaming", "#gameplay", "#gamer", 
            "#gamedev", "#indiegame", "#esports", "#mobilegame",
            "#oyun", "#mobiloyun", "#aksiyon", "#platform", "#puzzle"
        ]
        
        # Gaming trend template'leri
        self.trend_templates = [
            "Şu anda {platform} oyunları çok popüler ve gaming community'de büyük ilgi görüyor",
            "Gaming dünyasında {feature} trendi yükselişte, özellikle mobil platformlarda",
            "Oyuncular {content_type} içeriklerini çok seviyor ve aktif olarak paylaşıyor", 
            "{genre} türü oyunlar Instagram ve TikTok'ta viral olmaya devam ediyor",
            "Gaming influencer'lar {trend} konusunda çok konuşuyor ve engagement yüksek"
        ]
        
        # Gaming kelime havuzu
        self.gaming_words = {
            'platforms': ['mobile', 'PC', 'konsol', 'cross-platform'],
            'features': ['grafikler', 'oynanış', 'hikaye', 'karakter tasarımı', 'müzik'],
            'content_types': ['gameplay videoları', 'screenshotlar', 'live streamler', 'reviewlar'],
            'genres': ['action', 'platform', 'puzzle', 'RPG', 'strategy', 'indie'],
            'trends': ['retro gaming', 'speedrun', 'multiplayer', 'battle royale', 'indie games']
        }
     
    def analyze_trends(self, keywords):
        """Gaming trendlerini analiz et (template-based)"""
        try:
            import random
            
            # Keywords'leri işle
            if not keywords:
                keywords = ['gaming']
            
            # Rastgele template seç
            template = random.choice(self.trend_templates)
            
            # Template'i doldur
            filled_template = self._fill_template(template, keywords)
            
            # Keywords'leri ekle
            keyword_str = ", ".join(keywords[:3])  # İlk 3 keyword
            result = f"{filled_template} {keyword_str} kategorisinde özellikle yoğun aktivite var."
            
            return result
            
        except Exception as e:
            return self._get_fallback_trends(keywords)
    
    def get_popular_hashtags(self, count=10):
        """Popüler hashtag'leri döndür"""
        return self.popular_hashtags[:count]
    
    def get_trending_keywords(self):
        """Şu anda trending olan gaming keywords"""
        import random
        
        trending = []
        for category in self.gaming_words.values():
            trending.extend(random.sample(category, min(2, len(category))))
        
        return trending[:8]
    
    def _fill_template(self, template, keywords):
        """Template'deki placeholder'ları doldur"""
        import random
        
        # Keywords'lerden genre çıkarmaya çalış
        user_genre = None
        for keyword in keywords:
            for genre in self.gaming_words['genres']:
                if keyword.lower() in genre.lower() or genre.lower() in keyword.lower():
                    user_genre = genre
                    break
        
        # Replacements oluştur
        replacements = {
            '{platform}': random.choice(self.gaming_words['platforms']),
            '{feature}': random.choice(self.gaming_words['features']),
            '{content_type}': random.choice(self.gaming_words['content_types']),
            '{genre}': user_genre or random.choice(self.gaming_words['genres']),
            '{trend}': random.choice(self.gaming_words['trends'])
        }
        
        # Template'i doldur
        result = template
        for placeholder, value in replacements.items():
            result = result.replace(placeholder, value)
        
        return result
    
    def _get_fallback_trends(self, keywords):
        """Hata durumunda kullanılacak trend analizi"""
        if not keywords:
            return "Gaming content şu anda çok popüler, özellikle mobile gaming ve indie oyunlar trending."
        
        keyword_str = ", ".join(keywords)
        return f"Gaming trendleri: {keyword_str} kategorisinde yüksek aktivite. Mobile gaming ve indie oyunlar öne çıkıyor."
    
    def get_optimal_posting_times(self):
        """Optimal posting zamanları"""
        return {
            'instagram': ['19:00', '20:00', '21:00', '22:00'],
            'tiktok': ['18:00', '19:00', '20:00', '21:00'],
            'twitter': ['20:00', '21:00', '22:00']
        }
    
    def get_engagement_tips(self):
        """Gaming content için engagement ipuçları"""
        return [
            "🎮 Gaming emojileri kullanın",
            "🔥 Exciting moment'ları vurgulayın", 
            "💬 Community'den soru sorun",
            "🏆 Achievement'larınızı paylaşın",
            "📱 Mobile-friendly format kullanın",
            "⚡ Kısa ve etkili caption yazın"
        ]