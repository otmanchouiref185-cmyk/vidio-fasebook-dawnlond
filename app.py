from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

# دالة السيرفر الموثوقة والسريعة لجلب الفيديو
def get_facebook_video_url(fb_url):
    ydl_opts = {
        'format': 'best', 
        'quiet': True,
        'no_warnings': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(fb_url, download=False)
            video_url = info_dict.get('url', None)
            title = info_dict.get('title', 'Facebook Video')
            return {"success": True, "video_url": video_url, "title": title}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="ar" id="htmlTag" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>VRTX | Facebook Video Downloader</title>
        <style>
            :root {
                --bg-color: #0f0c1b;
                --card-bg: #1a1631;
                --primary: #8a2be2;
                --accent: #bb86fc;
                --success: #00e676;
                --text-muted: #8a2be2; /* رجعنا اللون الأساسي الخافت هو البنفسجي الماركة ديالك */
            }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background-color: var(--bg-color); 
                color: white; 
                text-align: center; 
                padding: 80px 15px 20px 15px; 
                margin: 0;
                position: relative;
            }
            
            /* الحاوية ثابتة ف أعلى اليمين دائماً وبلا تغيير ف الاتجاه */
            .lang-container {
                position: absolute;
                top: 20px;
                right: 40px;
                display: flex;
                align-items: center;
                z-index: 100;
                direction: ltr !important; /* إجبار الحاوية تبقى ديما بنفس الترتيب وخا تتبدل dir د الصفحة */
            }
            @media (max-width: 600px) {
                .lang-container { right: 20px; }
            }

            .lang-link {
                color: var(--text-muted); /* البنفسجي العادي */
                text-decoration: none;
                font-weight: bold;
                font-size: 15px;
                cursor: pointer;
                transition: color 0.3s ease;
                display: inline-block;
            }
            
            /* الستايل السحري فاش كتشعل اللغة النشطة ترجع بيضاء تماماً */
            .lang-link.active {
                color: #ffffff !important;
                text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
            }
            
            .lang-divider {
                color: #444;
                margin: 0 12px;
                font-size: 15px;
                user-select: none;
            }

            .container { 
                max-width: 650px; 
                margin: auto; 
                background: var(--card-bg); 
                padding: 40px 25px; 
                border-radius: 20px; 
                box-shadow: 0px 10px 30px rgba(138, 43, 226, 0.25); 
                border: 1px solid rgba(138, 43, 226, 0.2);
                box-sizing: border-box;
            }
            h1 { color: white; font-size: 32px; margin-bottom: 10px; font-weight: 800; }
            h1 span { color: var(--accent); }
            .subtitle { color: #b3b0c2; font-size: 15px; margin-bottom: 30px; }
            
            .input-group {
                position: relative;
                margin-bottom: 20px;
            }
            input[type="text"] { 
                width: 100%; 
                padding: 16px 20px; 
                border: 2px solid rgba(138, 43, 226, 0.4); 
                border-radius: 12px; 
                background: #090614; 
                color: white; 
                font-size: 16px; 
                text-align: left; 
                transition: 0.3s;
                box-sizing: border-box;
            }
            input[type="text"]:focus { 
                border-color: var(--accent); 
                outline: none; 
                box-shadow: 0 0 15px rgba(187, 134, 252, 0.2);
            }
            
            button.main-btn { 
                background: linear-gradient(135deg, var(--primary), #6a1b9a); 
                color: white; 
                border: none; 
                width: 100%;
                padding: 16px; 
                font-size: 16px; 
                border-radius: 12px; 
                cursor: pointer; 
                font-weight: bold; 
                transition: 0.3s; 
                box-shadow: 0 5px 15px rgba(138, 43, 226, 0.3);
            }
            button.main-btn:hover { 
                background: linear-gradient(135deg, var(--accent), var(--primary)); 
                transform: translateY(-2px); 
            }
            
            .result { 
                margin-top: 30px; 
                display: none; 
                background: #090614; 
                padding: 25px; 
                border-radius: 14px; 
                border: 1px solid rgba(138, 43, 226, 0.3); 
            }
            .video-info {
                color: white;
                font-size: 15px;
                margin-bottom: 20px;
                line-height: 1.5;
                font-weight: 500;
            }
            .download-btn { 
                background: var(--success); 
                color: black; 
                text-decoration: none; 
                padding: 14px 30px; 
                border-radius: 10px; 
                font-weight: bold; 
                display: inline-block; 
                transition: 0.3s; 
                width: 90%;
                box-sizing: border-box;
                box-shadow: 0 4px 12px rgba(0, 230, 118, 0.2);
            }
            .download-btn:hover { 
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0, 230, 118, 0.4);
            }
            
            .features-grid {
                display: flex;
                justify-content: space-around;
                max-width: 650px;
                margin: 40px auto 0 auto;
                background: rgba(26, 22, 49, 0.5);
                padding: 20px;
                border-radius: 15px;
            }
            .feature-item { font-size: 13px; color: #b3b0c2; }
            .feature-item strong { color: var(--accent); display: block; margin-bottom: 4px; }

            .footer { margin-top: 50px; font-size: 13px; color: #524e69; letter-spacing: 0.5px; }
        </style>
    </head>
    <body>

        <div class="lang-container">
            <span class="lang-link" id="langEn" onclick="setLanguage('en')">English</span>
            <span class="lang-divider">|</span>
            <span class="lang-link active" id="langAr" onclick="setLanguage('ar')">العربية</span>
        </div>

        <div class="container">
            <h1 id="mainTitle">VRTX <span>FB Downloader</span> 🎬</h1>
            <p id="subTitle" class="subtitle">أداة ذكية وخفيفة لتحميل فيديوهات الفيسبوك برابط مباشر وبأعلى جودة</p>
            
            <div class="input-group">
                <input type="text" id="videoUrl" placeholder="https://www.facebook.com/..." dir="ltr">
            </div>
            <button onclick="getDownloadLink()" class="main-btn" id="actionBtn">تحميل الفيديو المباشر ✨</button>
            
            <div class="result" id="resultBox">
                <div class="video-info" id="videoTitle"></div>
                <a id="downloadLink" class="download-btn" target="_blank" download>تحميل بجودة عالية MP4 📥</a>
            </div>
        </div>

        <div class="features-grid">
            <div class="feature-item"><strong id="f1_t">🚀 سريع جداً</strong><span id="f1_d">جلب فوري للروابط</span></div>
            <div class="feature-item"><strong id="f2_t">🔒 آمن 100%</strong><span id="f2_d">حماية كاملة لبياناتك</span></div>
            <div class="feature-item"><strong id="f3_t">📱 متوافق بالكامل</strong><span id="f3_d">للـ هواتف والكمبيوتر</span></div>
        </div>

        <div class="footer">🔒 Developed by Otman | All Rights Reserved © VRTX 2026</div>

        <script>
            const translations = {
                ar: {
                    title: "VRTX <span>FB Downloader</span> 🎬",
                    subtitle: "أداة ذكية وخفيفة لتحميل فيديوهات الفيسبوك برابط مباشر وبأعلى جودة",
                    btn: "تحميل الفيديو المباشر ✨",
                    loading: "جاري الاتصال بالسيرفر واستخراج الرابط... ⏳",
                    success_btn: "تحميل بجودة عالية MP4 📥",
                    fail: "فشل الجلب! تأكد من أن الفيديو عام (Public) وليس في مجموعة خاصة.",
                    alert: "عافاك حط رابط فيديو الفيسبوك أولاً!",
                    f1_t: "🚀 سريع جداً", f1_d: "جلب فوري للروابط",
                    f2_t: "🔒 آمن 100%", f2_d: "حماية كاملة لبياناتك",
                    f3_t: "📱 متوافق بالكامل", f3_d: "للـ هواتف والكمبيوتر",
                    dir: "rtl"
                },
                en: {
                    title: "VRTX <span>FB Downloader</span> 🎬",
                    subtitle: "Smart and lightweight tool to download Facebook videos directly in high quality",
                    btn: "Download Direct Video ✨",
                    loading: "Connecting to server and extracting link... ⏳",
                    success_btn: "Download High Quality MP4 📥",
                    fail: "Extraction failed! Make sure the video is Public, not Private.",
                    alert: "Please paste a Facebook video link first!",
                    f1_t: "🚀 Ultra Fast", f1_d: "Instant links fetching",
                    f2_t: "🔒 100% Secure", f2_d: "Your data is protected",
                    f3_t: "📱 Fully Responsive", f3_d: "For mobile & desktop",
                    dir: "ltr"
                }
            };

            function setLanguage(lang) {
                // 1. تبديل كلاس الـ active لتغيير الألوان (الأبيض للنشط والبنفسجي للخافت)
                if (lang === 'ar') {
                    document.getElementById('langAr').classList.add('active');
                    document.getElementById('langEn').classList.remove('active');
                } else {
                    document.getElementById('langEn').classList.add('active');
                    document.getElementById('langAr').classList.remove('active');
                }
                
                // 2. تحديث نصوص الصفحة كاملة بنقاء
                const t = translations[lang];
                document.getElementById('htmlTag').setAttribute('dir', t.dir);
                document.getElementById('mainTitle').innerHTML = t.title;
                document.getElementById('subTitle').innerText = t.subtitle;
                document.getElementById('actionBtn').innerText = t.btn;
                document.getElementById('downloadLink').innerText = t.success_btn;
                
                document.getElementById('f1_t').innerText = t.f1_t; document.getElementById('f1_d').innerText = t.f1_d;
                document.getElementById('f2_t').innerText = t.f2_t; document.getElementById('f2_d').innerText = t.f2_d;
                document.getElementById('f3_t').innerText = t.f3_t; document.getElementById('f3_d').innerText = t.f3_d;
            }

            async function getDownloadLink() {
                const url = document.getElementById('videoUrl').value;
                const resultBox = document.getElementById('resultBox');
                const downloadLink = document.getElementById('downloadLink');
                const videoTitle = document.getElementById('videoTitle');
                
                // جلب اتجاه اللغة الحالية لمعرفة التنبيهات
                const isAr = document.getElementById('langAr').classList.contains('active');
                const t = isAr ? translations['ar'] : translations['en'];
                
                if(!url) { alert(t.alert); return; }
                
                videoTitle.innerText = t.loading;
                resultBox.style.display = "block";
                downloadLink.style.display = "none";

                try {
                    const response = await fetch('/download', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ url: url })
                    });
                    
                    const data = await response.json();
                    
                    if(data.success) {
                        videoTitle.innerText = data.title;
                        downloadLink.href = data.video_url;
                        downloadLink.style.display = "inline-block";
                    } else {
                        videoTitle.innerText = t.fail;
                    }
                } catch(err) {
                    videoTitle.innerText = isAr ? "حدث خطأ في الاتصال." : "Error connecting to server.";
                }
            }
        </script>
    </body>
    </html>
    '''

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    video_url = data.get('url')
    if not video_url or ("facebook.com" not in video_url and "fb.watch" not in video_url):
        return jsonify({"success": False, "error": "رابط غير صحيح"})
        
    result = get_facebook_video_url(video_url)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True) 