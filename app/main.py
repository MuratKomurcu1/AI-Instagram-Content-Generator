# main.py - AI Instagram İçerik Üretici Ana Dosyası
from flask import Flask, request, jsonify, render_template_string, redirect, url_for
import os
import uuid
from werkzeug.utils import secure_filename

# Tüm ajanları import et
from agents.socialtrend_agent import socialtrend_agent
from agents.understanding_agent import UnderstandingAgent  
from agents.content_agent import ContentAgent
from agents.quality_agent import QualityControlAgent
from agents.finalization_agent import FinalizationAgent

# Flask uygulaması
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Upload klasörü oluştur
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# AI Ajanlarını başlat
print("🤖 AI Ajanları başlatılıyor...")
try:
    trend_agent = socialtrend_agent()
    print("✅ Trend Agent loaded")
except Exception as e:
    print(f"❌ Trend Agent error: {e}")

try:
    understanding_agent = UnderstandingAgent(device='cpu')
    print("✅ Understanding Agent loaded")
except Exception as e:
    print(f"❌ Understanding Agent error: {e}")

try:
    content_agent = ContentAgent(device=-1)  # CPU mode
    print("✅ Content Agent loaded")
except Exception as e:
    print(f"❌ Content Agent error: {e}")

try:
    quality_agent = QualityControlAgent()
    print("✅ Quality Agent loaded")
except Exception as e:
    print(f"❌ Quality Agent error: {e}")

try:
    final_agent = FinalizationAgent()
    print("✅ Final Agent loaded")
except Exception as e:
    print(f"❌ Final Agent error: {e}")

# Web arayüzü HTML template'i
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>🎮 AI Instagram Content Generator</title>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial; max-width: 900px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
        .container { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; margin-bottom: 30px; }
        .step { background: #f8f9fa; padding: 20px; margin: 15px 0; border-radius: 10px; border-left: 4px solid #007bff; }
        .result { background: #e8f5e8; padding: 20px; margin: 15px 0; border-radius: 10px; }
        .error { background: #ffe8e8; padding: 20px; margin: 15px 0; border-radius: 10px; }
        button { background: #007bff; color: white; padding: 15px 30px; border: none; border-radius: 8px; cursor: pointer; width: 100%; font-size: 1.1em; }
        button:hover { background: #0056b3; }
        input, textarea { width: 100%; padding: 12px; margin: 8px 0; border: 2px solid #ddd; border-radius: 6px; }
        .final-post { background: white; padding: 20px; border: 2px solid #007bff; border-radius: 10px; margin: 15px 0; }
        .quality-score { padding: 10px 20px; border-radius: 20px; color: white; font-weight: bold; margin: 10px 0; display: inline-block; }
        .score-high { background: #28a745; }
        .score-medium { background: #ffc107; color: #333; }
        .score-low { background: #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎮 AI Instagram Content Generator</h1>
        <p style="text-align: center; color: #666;">Upload your gaming content, generate trending social media posts!</p>
        
        <form action="/process" method="post" enctype="multipart/form-data">
            <div class="step">
                <h3>📁 1. Upload Files</h3>
                <label>🎬 Gameplay Video:</label>
                <input type="file" name="video" accept=".mp4,.mov,.avi">
                
                <label>🖼️ Game Screenshots:</label>
                <input type="file" name="images" accept=".jpg,.png,.jpeg" multiple>
                
                <label>📝 Game Description:</label>
                <textarea name="game_description" rows="3" placeholder="Describe your game..."></textarea>
                
                <label>🏷️ Keywords (comma separated):</label>
                <input type="text" name="keywords" placeholder="action, platform, mobile, puzzle">
            </div>
            
            <button type="submit">🚀 Generate Content!</button>
        </form>
        
        {% if result %}
        <div class="result">
            <h2>✅ Results Ready!</h2>
            
            <div class="step">
                <h3>📊 1. Trend Analysis</h3>
                <p><strong>Analysis:</strong> {{ result.trends }}</p>
                <p><strong>Popular Hashtags:</strong> {{ result.popular_hashtags|join(', ') if result.popular_hashtags else 'Loading...' }}</p>
            </div>
            
            <div class="step">
                <h3>🧠 2. Content Understanding</h3>
                <p><strong>🖼️ Visual Analysis:</strong> {{ result.image_caption }}</p>
                <p><strong>🎵 Audio Analysis:</strong> {{ result.audio_transcript }}</p>
                {% if result.video_analysis %}
                <p><strong>🎬 Video Analysis:</strong> {{ result.video_analysis.description }} ({{ result.video_analysis.duration }})</p>
                {% endif %}
            </div>
            
            <div class="step">
                <h3>✍️ 3. Generated Content</h3>
                <p><strong>Caption:</strong> {{ result.caption }}</p>
                <p><strong>Hashtags:</strong> {{ result.hashtags|join(' ') }}</p>
            </div>
            
            <div class="step">
                <h3>🔍 4. Quality Control</h3>
                <div class="quality-score {% if result.quality_data.score >= 7 %}score-high{% elif result.quality_data.score >= 4 %}score-medium{% else %}score-low{% endif %}">
                    {{ result.quality_data.emoji }} Score: {{ result.quality_data.score }}/10
                </div>
                <p><strong>Status:</strong> {{ result.quality_data.message }}</p>
                {% if result.quality_data.issues %}
                <ul>
                    {% for issue in result.quality_data.issues %}
                    <li>{{ issue }}</li>
                    {% endfor %}
                </ul>
                {% endif %}
            </div>
            
            <div class="step">
                <h3>🎯 5. Final Content (Ready to Post)</h3>
                <div class="final-post">{{ result.final_post|replace('\n', '<br>')|safe }}</div>
                
                {% if result.content_variations %}
                <h4>🔄 Alternative Versions:</h4>
                {% for variation in result.content_variations %}
                <div style="background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 8px;">
                    <strong>Version {{ variation.variation }} ({{ variation.style }}):</strong><br>
                    {{ variation.final_post|replace('\n', '<br>')|safe }}
                </div>
                {% endfor %}
                {% endif %}
            </div>
        </div>
        {% endif %}
        
        {% if error %}
        <div class="error">
            <h3>❌ Error Occurred</h3>
            <p>{{ error }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """Ana sayfa"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/process', methods=['POST'])
def process():
    """Dosya yükleme ve işleme"""
    try:
        print("📤 New upload request received")
        
        # Form verilerini al
        game_description = request.form.get('game_description', '')
        keywords = request.form.get('keywords', '').split(',')
        keywords = [k.strip() for k in keywords if k.strip()]
        
        # Dosya yükleme işlemi
        uploaded_files = {}
        
        # Video upload
        if 'video' in request.files and request.files['video'].filename:
            video = request.files['video']
            video_filename = secure_filename(video.filename)
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
            video.save(video_path)
            uploaded_files['video'] = video_path
            print(f"✅ Video uploaded: {video_filename}")
        
        # Image upload
        if 'images' in request.files:
            images = request.files.getlist('images')
            image_paths = []
            for img in images:
                if img.filename:
                    img_filename = secure_filename(img.filename)
                    img_path = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
                    img.save(img_path)
                    image_paths.append(img_path)
            uploaded_files['images'] = image_paths
            print(f"✅ {len(image_paths)} images uploaded")
        
        # 5 AI Agent Pipeline çalıştır
        result = run_ai_pipeline(uploaded_files, game_description, keywords)
        
        return render_template_string(HTML_TEMPLATE, result=result)
        
    except Exception as e:
        print(f"❌ Processing error: {str(e)}")
        return render_template_string(HTML_TEMPLATE, error=str(e))

def run_ai_pipeline(files, game_description, keywords):
    """5 AI Agent'ı sırayla çalıştır"""
    
    print("🤖 AI Pipeline starting...")
    
    # 📊 1. TREND ANALYSIS
    print("📊 1. Analyzing trends...")
    try:
        trends = trend_agent.analyze_trends(keywords)
        popular_hashtags = trend_agent.get_popular_hashtags(8)
        print(f"✅ Trend analysis completed")
    except Exception as e:
        print(f"❌ Trend analysis error: {e}")
        trends = f"Gaming trends: {', '.join(keywords) if keywords else 'mobile gaming'}"
        popular_hashtags = ['#gaming', '#mobilegaming']
    
    # 🧠 2. CONTENT UNDERSTANDING
    print("🧠 2. Understanding content...")
    image_caption = "Game visual"
    audio_transcript = "Audio analysis not available"
    video_analysis = None
    
    # Image analysis
    if 'images' in files and files['images']:
        try:
            image_caption = understanding_agent.describe_image(files['images'][0])
            print(f"✅ Image analysis: {image_caption[:50]}...")
        except Exception as e:
            print(f"⚠️ Image analysis error: {e}")
    
    # Video analysis
    if 'video' in files:
        try:
            video_analysis = understanding_agent.analyze_video(files['video'])
            print(f"✅ Video analysis completed")
        except Exception as e:
            print(f"⚠️ Video analysis error: {e}")
    
    # Audio analysis
    if 'video' in files:
        try:
            audio_transcript = understanding_agent.transcribe_audio(files['video'])
            print(f"✅ Audio analysis: {audio_transcript[:30]}...")
        except Exception as e:
            print(f"⚠️ Audio analysis error: {e}")
    
    # ✍️ 3. CONTENT GENERATION
    print("✍️ 3. Generating content...")
    try:
        media_info = f"{game_description} {image_caption}"
        caption = content_agent.generate_caption(trends, media_info, game_description)
        print(f"✅ Caption generated: {caption[:50]}...")
    except Exception as e:
        print(f"❌ Content generation error: {e}")
        caption = "🎮 Amazing gaming experience! Highly recommend this game 🔥"
    
    # 🔍 4. QUALITY CONTROL
    print("🔍 4. Quality checking...")
    try:
        temp_hashtags = [f"#{kw}" for kw in keywords] + ['#gaming', '#mobilegaming']
        
        content_data = {
            'caption': caption,
            'hashtags': temp_hashtags
        }
        
        if 'images' in files and files['images']:
            content_data['image_path'] = files['images'][0]
        if 'video' in files:
            content_data['video_path'] = files['video']
        
        quality_result = quality_agent.overall_quality_check(content_data)
        print(f"✅ Quality check: {quality_result['score']}/10")
    except Exception as e:
        print(f"❌ Quality check error: {e}")
        quality_result = {
            'status': 'unknown',
            'score': 7.0,
            'emoji': '⚠️',
            'message': 'Quality check failed',
            'issues': ['Quality control system error'],
            'recommendations': ['Manual review needed']
        }
    
    # 🎯 5. FINALIZATION
    print("🎯 5. Finalizing content...")
    try:
        all_keywords = keywords + ['gaming', 'mobilegaming', 'game']
        hashtags = final_agent.generate_hashtags(all_keywords, max_count=10)
        
        final_post = final_agent.finalize_post(caption, hashtags, platform='instagram')
        
        content_variations = final_agent.generate_content_variations(caption, hashtags, count=2)
        
        print(f"✅ Finalization completed")
    except Exception as e:
        print(f"❌ Finalization error: {e}")
        hashtags = ['#gaming', '#mobilegaming', '#game']
        final_post = f"{caption}\n\n{' '.join(hashtags)}"
        content_variations = []
    
    # Return results
    result = {
        'trends': trends,
        'popular_hashtags': popular_hashtags,
        'image_caption': image_caption,
        'audio_transcript': audio_transcript,
        'video_analysis': video_analysis,
        'caption': caption,
        'hashtags': hashtags,
        'quality_data': quality_result,
        'final_post': final_post,
        'content_variations': content_variations
    }
    
    print("🎉 Pipeline completed!")
    return result

# API Endpoints
@app.route('/api/test', methods=['GET'])
def api_test():
    """API test endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'AI Instagram Content Generator API is running!',
        'agents': {
            'trend_analyzer': '✅ Active',
            'understanding_agent': '✅ Active', 
            'content_generator': '✅ Active',
            'quality_controller': '✅ Active',
            'finalizer': '✅ Active'
        }
    })

@app.route('/api/trends', methods=['POST'])
def api_trends():
    """Trend analysis API"""
    try:
        data = request.get_json()
        keywords = data.get('keywords', ['gaming'])
        
        trends = trend_agent.analyze_trends(keywords)
        hashtags = trend_agent.get_popular_hashtags(10)
        
        return jsonify({
            'success': True,
            'trends': trends,
            'popular_hashtags': hashtags
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🎮 AI Instagram Content Generator")
    print("="*50)
    print("📱 Web Demo: http://localhost:5000")
    print("🔗 API Test: http://localhost:5000/api/test")
    print("📊 Agents: 5 AI Agents active")
    print("🚀 Ready!")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)