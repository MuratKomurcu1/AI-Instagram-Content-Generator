🎮 AI Instagram Content Generator
Oyun içeriklerinizi Instagram'a hazır hale getiren yapay zeka destekli çoklu ajan sistemi
🎮 AI Instagram Content Generator
Oyun içeriklerinizi Instagram'a hazır hale getiren yapay zeka destekli çoklu ajan sistemi
Show Image
Show Image
Show Image
Show Image

🚀 Özellikler

🤖 5 AI Ajanı: Trend analizi, içerik anlama, üretim, kalite kontrol ve finalizasyon
📱 Web Demo: Kolay kullanımlı Flask arayüzü
🎬 Çoklu Medya: Video, görsel, ses ve metin analizi
✍️ Otomatik İçerik: Trendle uyumlu caption ve hashtag üretimi
🔍 Kalite Kontrol: Instagram standartlarına uygunluk kontrolü
🎯 Gaming Odaklı: Oyun içerikleri için özelleştirilmiş


📋 İçindekiler

🚀 Özellikler
🛠️ Kurulum
📱 Kullanım
🤖 AI Ajanları
📊 Demo
🔧 API
📁 Proje Yapısı
🎯 Örnek Çıktılar
❓ SSS
🤝 Katkıda Bulunma


🛠️ Kurulum
Gereksinimler

Python 3.8+
pip (Python package manager)
8GB+ RAM önerilir
GPU (opsiyonel, performans için)

1. Repository'yi Klonlayın
bashgit clone https://github.com/MuratKomurcu1/AI-Instagram-Content-Generator.git
cd AI-Instagram-Content-Generator
2. Sanal Ortam Oluşturun
bash# Windows
python -m venv cuda_env
cuda_env\Scripts\activate

# Mac/Linux
python3 -m venv cuda_env
source cuda_env/bin/activate
3. Gereksinimleri Yükleyin
bashpip install -r requirements.txt
4. Sistemi Test Edin
bashpython test_system.py
5. Demo'yu Başlatın
bashpython app/main.py
Tarayıcınızda http://localhost:5000 adresine gidin! 🎉

📱 Kullanım
Web Arayüzü

Dosya Yükleme: Gameplay videosu, screenshot'lar yükleyin
Bilgi Girişi: Oyun açıklaması ve keywords ekleyin
İşlem: "İçerik Üret" butonuna tıklayın
Sonuç: Instagram'a hazır içeriğinizi alın!

API Kullanımı
pythonimport requests

# Trend analizi
response = requests.post('http://localhost:5000/api/trends', 
                        json={'keywords': ['gaming', 'mobile']})
trends = response.json()

# Sistem durumu
response = requests.get('http://localhost:5000/api/test')
status = response.json()

🤖 AI Ajanları
1. 📊 Trend Analiz Ajanı
pythonfrom agents.socialtrend_agent import socialtrend_agent

trend_agent = socialtrend_agent()
trends = trend_agent.analyze_trends(['gaming', 'mobile'])
hashtags = trend_agent.get_popular_hashtags(10)
Yetenekleri:

Gaming trendlerini analiz eder
Popüler hashtag'leri önerir
Platform-spesifik içgörüler sunar

2. 🧠 İçerik Anlama Ajanı
pythonfrom agents.understanding_agent import UnderstandingAgent

understanding_agent = UnderstandingAgent()
description = understanding_agent.describe_image('screenshot.jpg')
transcript = understanding_agent.transcribe_audio('game_audio.wav')
Kullanılan Modeller:

BLIP: Görsel açıklama (Salesforce/blip-image-captioning-base)
Whisper: Ses transkripsiyonu (OpenAI Whisper small)

3. ✍️ İçerik Üretim Ajanı
pythonfrom agents.content_agent import ContentAgent

content_agent = ContentAgent()
caption = content_agent.generate_caption(trends, media_info)
variations = content_agent.generate_multiple_options(trends, media_info, count=3)
Özellikler:

Template-based içerik üretimi
Gaming terminolojisi
Çoklu dil desteği (TR/EN)

4. 🔍 Kalite Kontrol Ajanı
pythonfrom agents.quality_agent import QualityControlAgent

quality_agent = QualityControlAgent()
text_issues = quality_agent.check_text_quality(caption)
image_issues = quality_agent.check_image_quality('image.jpg')
overall = quality_agent.overall_quality_check(content_data)
Kontrol Kriterleri:

Metin uzunluğu ve formatı
Görsel çözünürlük ve aspect ratio
Hashtag optimizasyonu
Instagram standartları

5. 🎯 Finalizasyon Ajanı
pythonfrom agents.finalization_agent import FinalizationAgent

final_agent = FinalizationAgent()
hashtags = final_agent.generate_hashtags(keywords)
final_post = final_agent.finalize_post(caption, hashtags)
variations = final_agent.generate_content_variations(caption, hashtags)
Çıktılar:

Platform-optimized içerik
Hashtag stratejisi
İçerik varyasyonları


📊 Demo
Örnek Girdi:

Video: gameplay.mp4 (30 saniye)
Screenshots: menu.png, character.png
Açıklama: "Aksiyon dolu platform oyunu"
Keywords: "action, platform, mobile"

Örnek Çıktı:
🎮 Bu platform oyununda aksiyonlar hiç bitmiyor! 
Karakterimle yeni seviyeleri keşfetmek çok heyecanlı 🔥
Kim benimle yarışmak ister? 🚀

#gaming #platformgame #mobilegaming #action #gameplay 
#oyun #platform #aksiyon #mobiloyun #gamer

Kalite Skoru: 9/10 ✅

🔧 API Endpoints
GET /api/test
Sistem durumunu kontrol eder
json{
  "status": "success",
  "message": "AI Instagram Content Generator API is running!",
  "agents": {
    "trend_analyzer": "✅ Active",
    "understanding_agent": "✅ Active",
    "content_generator": "✅ Active",
    "quality_controller": "✅ Active",
    "finalizer": "✅ Active"
  }
}
POST /api/trends
Trend analizi yapar
json// Request
{
  "keywords": ["gaming", "mobile", "action"]
}

// Response
{
  "success": true,
  "trends": "Gaming dünyasında mobile trendi yükselişte...",
  "popular_hashtags": ["#gaming", "#mobilegaming", "#action"]
}
POST /process
Tam pipeline'ı çalıştırır (form-data ile dosya yükleme)

📁 Proje Yapısı
AI-Instagram-Content-Generator/
├── 📂 agents/                     # AI Ajanları
│   ├── 📄 socialtrend_agent.py   # Trend analizi
│   ├── 📄 understanding_agent.py # Görsel/ses anlama
│   ├── 📄 content_agent.py       # İçerik üretimi
│   ├── 📄 quality_agent.py       # Kalite kontrolü
│   └── 📄 finalization_agent.py  # Finalizasyon
├── 📂 app/                        # Ana uygulama
│   └── 📄 main.py                 # Flask web server
├── 📂 uploads/                    # Yüklenen dosyalar
├── 📄 requirements.txt            # Python gereksinimleri
├── 📄 test_system.py             # Test scripti
├── 📄 .gitignore                 # Git ignore dosyası
└── 📄 README.md                  # Bu dosya

🎯 Örnek Çıktılar
Gameplay Showcase Post:
🎮 Bu boss fight'ta strategy çok önemli! 
Hangi tactic'i kullanırsınız? 🤔

#gaming #bossfight #strategy #mobilegaming #tips
Achievement Post:
🏆 Sonunda platinum trophy aldım! 
100 saat sürdü ama değdi 💪

#gaming #achievement #platinum #dedication #victory
Review Post:
📱 Bu indie game gerçekten şaşırttı! 
Pixel art'ı muhteşem 🎨

#indiegame #pixelart #review #mobilegaming #recommended

🔧 Konfigürasyon
Model Ayarları
python# GPU kullanımı
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

# Model boyutları
WHISPER_MODEL = 'small'  # tiny, small, medium, large
BLIP_MODEL = 'Salesforce/blip-image-captioning-base'
Kalite Kontrol Limitleri
pythonMAX_CAPTION_LENGTH = 125    # Instagram limit
MIN_IMAGE_RESOLUTION = 720  # Minimum pixels
OPTIMAL_HASHTAG_COUNT = 11  # Instagram optimal

🐛 Sorun Giderme
ModuleNotFoundError: cv2
bashpip install opencv-python
CUDA out of memory
python# Device'i CPU'ya çevir
understanding_agent = UnderstandingAgent(device='cpu')
content_agent = ContentAgent(device=-1)
Transformers import error
bashpip install --upgrade transformers huggingface-hub
Port 5000 kullanımda
python# main.py'de port değiştir
app.run(debug=True, port=5001)

📈 Performans
İşlem Süreleri

Trend Analizi: ~1 saniye
Görsel Analizi: ~3-5 saniye
Video İşleme: ~30 saniye/dakika
İçerik Üretimi: ~2 saniye
Toplam Pipeline: ~1-2 dakika

Sistem Gereksinimleri

Minimum: 4GB RAM, CPU
Önerilen: 8GB+ RAM, GPU
Model Boyutları: ~3GB toplam


🎨 Customization
Yeni Template Ekleme
python# agents/content_agent.py içinde
self.gaming_templates.append(
    "🎮 Yeni template: {custom_field}! #gaming"
)

self.gaming_words['custom_field'] = ['değer1', 'değer2']
Yeni Platform Desteği
python# agents/finalization_agent.py
self.platform_hashtags['yeni_platform'] = ['#platform_tag']

🧪 Test
Birim Testler
bash# Tüm ajanları test et
python test_system.py

# Specific agent test
python -c "from agents.content_agent import ContentAgent; print('OK')"
API Testleri
bash# Health check
curl http://localhost:5000/api/test

# Trend test
curl -X POST http://localhost:5000/api/trends \
  -H "Content-Type: application/json" \
  -d '{"keywords": ["gaming"]}'

🚀 Geliştirme Roadmap
v1.1 (Gelecek)

 GPT-4 entegrasyonu
 Gerçek Instagram API
 Batch processing
 Analytics dashboard

v1.2 (Planlanan)

 Multi-language support
 A/B testing
 Scheduled posting
 Content calendar

v2.0 (Vizyon)

 TikTok desteği
 Video editing
 AI voice generation
 Brand guidelines


🤝 Katkıda Bulunma
Pull Request Süreci

Fork yapın
Feature branch oluşturun (git checkout -b feature/amazing-feature)
Commit yapın (git commit -m 'Add amazing feature')
Push yapın (git push origin feature/amazing-feature)
Pull Request açın

Issue Reporting

Bug raporları için issue açın
Feature istekleri için discussion başlatın
Dokümantasyon güncellemeleri için PR gönderin


📄 Lisans
Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için LICENSE dosyasına bakın.

👨‍💻 Geliştirici
Murat Kömürcü

GitHub: @MuratKomurcu1
Email: muratkomurrcu@gmail.com
LinkedIn:https://www.linkedin.com/in/murat-komurcu-0b3b54173/


🙏 Teşekkürler

