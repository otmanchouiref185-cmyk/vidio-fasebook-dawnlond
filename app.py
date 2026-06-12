from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

# الدالة الأصلية لجلب الفيديوهات
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
        
        <title>VRTX | تحميل فيديوهات فيسبوك برابط مباشر وبأعلى جودة</title>
        <meta name="description" content="أفضل أداة مجانية وسريعة لتنزيل فيديوهات الفيسبوك بجودة عالية. فقط ضع رابط الفيديو وحمل مباشرة بدون برامج.">
        <meta name="keywords" content="تنزيل فيديوهات فيسبوك, تحميل من الفيسبوك, facebook downloader, download fb video, تحميل فيديوهات fb, تنزيل فيديو فيسبوك">
        <meta name="author" content="Otman | VRTX">
        <meta name="robots" content="index, follow">
        
        <meta name="google-site-verification" content="47uiqRAN7VFxZEC8DheNAakZcyaPL-rIkUTnFUMnM-s" />

        <style>
            :root {
                --bg-color: #0f0c1b;
                --card-bg: #1a1631;
                --primary: #8a2be2;
                --accent: #bb86fc;
                --success: #00e676;
                --dark-pop: #151126;
            }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background-color: var(--bg-color); 
                color: white; 
                text-align: center; 
                padding: 140px 15px 20px 15px; 
                margin: 0;
                position: relative;
            }
            
            /* الهيدر العلوي */
            .navbar {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                padding: 25px 40px;
                box-sizing: border-box;
                z-index: 100;
                height: 90px;
            }
            
            /* تثبيت زر كيفية التحميل في أقصى اليسار دائماً */
            .nav-links {
                position: absolute !important;
                top: 25px;
                left: 40px;
                display: flex;
                align-items: center;
                gap: 12px;
                direction: ltr !important;
            }

            /* تثبيت مربع اختيار اللغة في أقصى اليمين دائماً */
            .lang-dropdown {
                position: absolute !important;
                top: 25px;
                right: 40px;
                z-index: 200;
                direction: ltr !important; 
            }

            @media (max-width: 768px) {
                .navbar { 
                    height: auto;
                    padding: 15px; 
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    gap: 15px;
                }
                .nav-links, .lang-dropdown {
                    position: static !important;
                    margin: 5px auto;
                }
                body { padding-top: 220px; }
            }

            .nav-btn {
                background: transparent;
                border: 1px solid rgba(138, 43, 226, 0.4);
                color: white;
                padding: 10px 18px;
                border-radius: 8px;
                cursor: pointer;
                font-weight: bold;
                font-size: 14px;
                transition: 0.3s;
                text-decoration: none;
                display: inline-flex;
                align-items: center;
                gap: 6px;
            }
            .nav-btn:hover {
                background: var(--primary);
                border-color: var(--accent);
                box-shadow: 0 0 12px rgba(138, 43, 226, 0.5);
            }
            
            .dropdown-btn {
                background: var(--card-bg);
                color: white;
                border: 1px solid rgba(138, 43, 226, 0.4);
                padding: 10px 18px;
                border-radius: 8px;
                font-weight: bold;
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 14px;
                user-select: none;
            }
            
            .arrow-svg {
                width: 12px;
                height: 12px;
                fill: none;
                stroke: var(--accent);
                stroke-width: 2.5;
                stroke-linecap: round;
                stroke-linejoin: round;
                transition: transform 0.3s ease;
            }
            
            .lang-dropdown.active .arrow-svg {
                transform: rotate(180deg);
            }
            
            .dropdown-content {
                display: block;
                opacity: 0;
                visibility: hidden;
                transform: translateY(-10px);
                position: absolute;
                top: 100%;
                right: 0;
                background-color: var(--card-bg);
                min-width: 160px;
                box-shadow: 0px 10px 30px rgba(0,0,0,0.7);
                border-radius: 8px;
                border: 1px solid rgba(138, 43, 226, 0.3);
                z-index: 250;
                overflow: hidden;
                margin-top: 5px;
                transition: opacity 0.3s ease, transform 0.3s ease, visibility 0.3s;
            }
            
            .lang-dropdown.active .dropdown-content {
                opacity: 1;
                visibility: visible;
                transform: translateY(0);
            }
            
            .dropdown-content a {
                color: white;
                padding: 12px 16px;
                text-decoration: none;
                display: block;
                font-size: 14px;
                text-align: left;
                transition: 0.2s;
            }
            .dropdown-content a:hover {
                background-color: var(--primary);
            }

            /* تصميم الحاوية الرئيسية ومربع التحميل */
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

            /* قسم الأسئلة الشائعة - ثابت ومستقر */
            .faq-section {
                max-width: 650px;
                margin: 40px auto 0 auto;
                text-align: right !important;
            }
            .faq-section h2 {
                font-size: 22px;
                color: white;
                margin-bottom: 20px;
                text-align: right !important;
            }
            .faq-item {
                background: var(--card-bg);
                border: 1px solid rgba(138, 43, 226, 0.2);
                border-radius: 10px;
                margin-bottom: 12px;
                overflow: hidden;
            }
            .faq-question {
                padding: 18px;
                font-weight: bold;
                font-size: 15px;
                cursor: pointer;
                display: flex;
                justify-content: space-between;
                align-items: center;
                user-select: none;
                transition: background 0.3s;
                direction: rtl !important;
            }
            .faq-question:hover {
                background: rgba(138, 43, 226, 0.1);
            }
            .faq-answer {
                padding: 0 18px;
                max-height: 0;
                overflow: hidden;
                transition: max-height 0.3s ease-out, padding 0.3s ease;
                color: #b3b0c2;
                font-size: 14px;
                line-height: 1.6;
                border-top: 1px solid transparent;
                text-align: right !important;
                direction: rtl !important;
            }

            .modal {
                display: none;
                position: fixed;
                z-index: 1000;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0,0,0,0.7);
                backdrop-filter: blur(5px);
                align-items: center;
                justify-content: center;
            }
            .modal-content {
                background-color: var(--dark-pop);
                border: 2px solid var(--primary);
                padding: 30px;
                border-radius: 20px;
                width: 90%;
                max-width: 500px;
                position: relative;
                box-shadow: 0 10px 40px rgba(138, 43, 226, 0.4);
                animation: fadeIn 0.4s ease;
                box-sizing: border-box;
            }
            @keyframes fadeIn {
                from { transform: scale(0.9); opacity: 0; }
                to { transform: scale(1); opacity: 1; }
            }
            .close-modal {
                position: absolute;
                top: 15px;
                left: 20px;
                color: #aaa;
                font-size: 28px;
                font-weight: bold;
                cursor: pointer;
                z-index: 10;
            }
            html[dir="rtl"] .close-modal { left: auto; right: 20px; }
            .close-modal:hover { color: white; }
            .modal h3 { color: var(--accent); margin-top: 0; font-size: 20px; text-align: center; margin-bottom: 25px; }
            
            .step-box {
                background: rgba(255,255,255,0.03);
                border: 1px solid rgba(138, 43, 226, 0.2);
                border-radius: 10px;
                padding: 12px 15px;
                margin-bottom: 12px;
                display: flex;
                align-items: center;
                gap: 12px;
            }
            .step-num {
                background: var(--primary);
                color: white;
                width: 28px;
                height: 28px;
                border-radius: 50%;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                flex-shrink: 0;
            }
            .step-text { font-size: 14px; line-height: 1.4; color: #e1def2; text-align: initial; }

            .footer { margin-top: 50px; font-size: 13px; color: #524e69; letter-spacing: 0.5px; }
        </style>
    </head>
    <body>

        <div class="navbar">
            <div class="nav-links">
                <button class="nav-btn" id="howToBtn" onclick="openModal()">💡 كيفية التحميل؟</button>
            </div>

            <div class="lang-dropdown" id="langDropdown">
                <button class="dropdown-btn" id="dropBtn" onclick="toggleDropdown(event)">
                    🌐 <span id="currentLang">العربية</span>
                    <svg class="arrow-svg" viewBox="0 0 24 24">
                        <path d="M6 9l6 6 6-6"></path>
                    </svg>
                </button>
                <div class="dropdown-content" id="dropContent">
                    <a href="#" onclick="changeLang(event, 'ar')">🇲🇦 العربية</a>
                    <a href="#" onclick="changeLang(event, 'en')">🇺🇸 English</a>
                    <a href="#" onclick="changeLang(event, 'fr')">🇫🇷 Français</a>
                    <a href="#" onclick="changeLang(event, 'es')">🇪🇸 Español</a>
                    <a href="#" onclick="changeLang(event, 'de')">🇩🇪 Deutsch</a>
                    <a href="#" onclick="changeLang(event, 'pt')">🇵🇹 Português</a>
                </div>
            </div>
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

        <div class="faq-section" id="faqSection">
            <h2 id="faqMainTitle">❓ الأسئلة الشائعة</h2>
            
            <div class="faq-item">
                <div class="faq-question" onclick="toggleFaq(this)"><span id="q1">أين يتم حفظ الفيديوهات بعد التحميل؟</span> <span>➕</span></div>
                <div class="faq-answer" id="a1">تُحفظ الفيديوهات تلقائياً في مجلد "Downloads" أو "التحميلات" الخاص بجهازك (الهاتف أو الكمبيوتر).</div>
            </div>
            
            <div class="faq-item">
                <div class="faq-question" onclick="toggleFaq(this)"><span id="q2">هل يمكنني تحميل الفيديوهات الخاصة (Private)؟</span> <span>➕</span></div>
                <div class="faq-answer" id="a2">لا، الأداة تدعم تحميل الفيديوهات العامة (Public) فقط لضمان سرعة وحماية جلب الروابط بشكل مباشر.</div>
            </div>
        </div>

        <div id="howToModal" class="modal">
            <div class="modal-content" id="modalContent" style="text-align: right;">
                <span class="close-modal" onclick="closeModal()">&times;</span>
                <h3 id="modalTitle">📖 خطوات تحميل الفيديو</h3>
                <div id="modalSteps"></div>
            </div>
        </div>

        <div class="footer">🔒 Developed by Otman | All Rights Reserved © VRTX 2026</div>

        <script>
            const translations = {
                ar: {
                    title: "VRTX <span>FB Downloader</span> 🎬", subtitle: "أداة ذكية وخفيفة لتحميل فيديوهات الفيسبوك برابط مباشر وبأعلى جودة",
                    btn: "تحميل الفيديو المباشر ✨", loading: "جاري الاتصال بالسيرفر واستخراج الرابط... ⏳", success_btn: "تحميل بجودة عالية MP4 📥",
                    fail: "فشل الجلب! تأكد من أن الفيديو عام (Public) وليس في مجموعة خاصة.", alert: "عافاك حط رابط فيديو الفيسبوك أولاً!",
                    f1_t: "🚀 سريع جداً", f1_d: "جلب فوري للروابط", f2_t: "🔒 آمن 100%", f2_d: "حماية كاملة لبياناتك", f3_t: "📱 متوافق بالكامل", f3_d: "للـ هواتف والكمبيوتر",
                    howToBtn: "💡 كيفية التحميل؟", currentLang: "العربية", faqMainTitle: "❓ الأسئلة الشائعة",
                    q1: "أين يتم حفظ الفيديوهات بعد التحميل؟", a1: "تُحفظ الفيديوهات تلقائياً في مجلد 'Downloads' أو 'التحميلات' الخاص بجهازك (الهاتف أو الكمبيوتر).",
                    q2: "هل يمكنني تحميل الفيديوهات الخاصة (Private)؟", a2: "لا، الأداة تدعم تحميل الفيديوهات العامة (Public) فقط لضمان سرعة وحماية جلب الروابط بشكل مباشر.",
                    modalTitle: "📖 خطوات تحميل الفيديو",
                    modalSteps: `<div class="step-box"><div class="step-num">1</div><div class="step-text">قم بنسخ رابط الفيديو من تطبيق الفيسبوك.</div></div>
                                 <div class="step-box"><div class="step-num">2</div><div class="step-text">ضع الرابط داخل صندوق الإدخال في الأعلى.</div></div>
                                 <div class="step-box"><div class="step-num">3</div><div class="step-text">اضغط على زر "تحميل" ثم انقر على الزر الأخضر لحفظ الفيديو مباشرة.</div></div>`,
                    dir: "rtl", align: "right"
                },
                en: {
                    title: "VRTX <span>FB Downloader</span> 🎬", subtitle: "Smart and lightweight tool to download Facebook videos directly in high quality",
                    btn: "Download Direct Video ✨", loading: "Connecting to server and extracting link... ⏳", success_btn: "Download High Quality MP4 📥",
                    fail: "Extraction failed! Make sure the video is Public, not Private.", alert: "Please paste a Facebook video link first!",
                    f1_t: "🚀 Ultra Fast", f1_d: "Instant links fetching", f2_t: "🔒 100% Secure", f2_d: "Your data is protected", f3_t: "📱 Fully Responsive", f3_d: "For mobile & desktop",
                    howToBtn: "💡 How to download?", currentLang: "English", faqMainTitle: "❓ FAQs",
                    q1: "Where are videos saved after download?", a1: "Videos are automatically saved in the 'Downloads' folder of your device.",
                    q2: "Can I download Private Facebook videos?", a2: "No, this tool only supports Public videos to ensure speed and direct secure link extraction.",
                    modalTitle: "📖 Video Download Steps",
                    modalSteps: `<div class="step-box"><div class="step-num">1</div><div class="step-text">Copy the video URL link from Facebook.</div></div>
                                 <div class="step-box"><div class="step-num">2</div><div class="step-text">Paste the link inside the input box above.</div></div>
                                 <div class="step-box"><div class="step-num">3</div><div class="step-text">Click 'Download' button, then click the green button to save.</div></div>`,
                    dir: "ltr", align: "left"
                },
                fr: {
                    title: "VRTX <span>FB Downloader</span> 🎬", subtitle: "Outil intelligent et léger pour télécharger des vidéos Facebook directement en haute qualité",
                    btn: "Télécharger la Vidéo ✨", loading: "Connexion au serveur et extraction du lien... ⏳", success_btn: "Télécharger en Haute Qualité MP4 📥",
                    fail: "Échec de l'extraction! Assurez-vous que la vidéo est publique.", alert: "Veuillez coller un lien de vidéo Facebook d'abord!",
                    f1_t: "🚀 Ultra Rapide", f1_d: "Récupération instantanée", f2_t: "🔒 100% Sécurisé", f2_d: "Vos données sont protégées", f3_t: "📱 Entièrement Responsive", f3_d: "Pour mobile et bureau",
                    howToBtn: "💡 Comment télécharger?", currentLang: "Français", faqMainTitle: "❓ FAQ",
                    q1: "Où sont enregistrées les vidéos après le téléchargement?", a1: "Les vidéos sont automatiquement enregistrées dans le dossier 'Téléchargements' de votre appareil.",
                    q2: "Puis-je télécharger des vidéos Facebook privées?", a2: "Non, cet outil ne prend en charge que les vidéos publiques pour garantir la rapidité.",
                    modalTitle: "📖 Étapes de téléchargement",
                    modalSteps: `<div class="step-box"><div class="step-num">1</div><div class="step-text">Copiez le lien de la vidéo depuis Facebook.</div></div>
                                 <div class="step-box"><div class="step-num">2</div><div class="step-text">Collez le lien dans la case ci-dessus.</div></div>
                                 <div class="step-box"><div class="step-num">3</div><div class="step-text">Cliquez sur 'Télécharger', puis sur le bouton vert pour enregistrer.</div></div>`,
                    dir: "ltr", align: "left"
                },
                es: {
                    title: "VRTX <span>FB Downloader</span> 🎬", subtitle: "Herramienta inteligente y ligera para descargar videos de Facebook directamente en alta calidad",
                    btn: "Descargar Video Directo ✨", loading: "Conectando al servidor y extrayendo enlace... ⏳", success_btn: "Descargar Alta Calidad MP4 📥",
                    fail: "¡Extracción fallida! Asegúrate de que el video sea público.", alert: "¡Por favor, pega un enlace de video de Facebook primero!",
                    f1_t: "🚀 Ultra Rápido", f1_d: "Obtención instantánea", f2_t: "🔒 100% Seguro", f2_d: "Tus datos están protegidos", f3_t: "📱 Totalmente Compatible", f3_d: "Para móvil y escritorio",
                    howToBtn: "💡 ¿Cómo descargar?", currentLang: "Español", faqMainTitle: "❓ Preguntas Frecuentes",
                    q1: "¿Dónde se guardan los videos después de la descarga?", a1: "Los videos se guardan automáticamente en la carpeta 'Descargas' de tu dispositivo.",
                    q2: "¿Puedo descargar videos privados de Facebook?", a2: "No, esta herramienta solo admite videos públicos para garantizar la velocidad.",
                    modalTitle: "📖 Pasos para descargar",
                    modalSteps: `<div class="step-box"><div class="step-num">1</div><div class="step-text">Copia el enlace del video desde Facebook.</div></div>
                                 <div class="step-box"><div class="step-num">2</div><div class="step-text">Pega el enlace en el cuadro de arriba.</div></div>
                                 <div class="step-box"><div class="step-num">3</div><div class="step-text">Haz clic en 'Descargar', luego en el botón verde para guardar.</div></div>`,
                    dir: "ltr", align: "left"
                },
                de: {
                    title: "VRTX <span>FB Downloader</span> 🎬", subtitle: "Intelligentes und leichtes Tool zum direkten Herunterladen von Facebook-Videos in hoher Qualität",
                    btn: "Video direkt herunterladen ✨", loading: "Verbindung zum Server wird hergestellt... ⏳", success_btn: "In hoher Qualität MP4 herunterladen 📥",
                    fail: "Extraktion fehlgeschlagen! Stellen Sie sicher, dass das Video öffentlich ist.", alert: "Bitte fügen Sie zuerst einen Facebook-Videolink ein!",
                    f1_t: "🚀 Ultra Schnell", f1_d: "Sofortige Link-Abfrage", f2_t: "🔒 100% Sicher", f2_d: "Ihre Daten sind geschützt", f3_t: "📱 Vollständig Anpassungsfähig", f3_d: "Für Mobilgeräte & Desktop",
                    howToBtn: "💡 Wie herunterladen?", currentLang: "Deutsch", faqMainTitle: "❓ Häufig gestelle Fragen",
                    q1: "Wo werden die Videos nach dem Download gespeichert?", a1: "Videos werden automatisch im Ordner 'Downloads' Ihres Geräts gespeichert.",
                    q2: "Kann ich private Facebook-Videos herunterladen?", a2: "Nein, dieses Tool unterstützt nur öffentliche Videos, um Schnelligkeit zu garantieren.",
                    modalTitle: "📖 Download-Schritte",
                    modalSteps: `<div class="step-box"><div class="step-num">1</div><div class="step-text">Kopieren Sie den Videolink von Facebook.</div></div>
                                 <div class="step-box"><div class="step-num">2</div><div class="step-text">Fügen Sie den Link in das Feld oben ein.</div></div>
                                 <div class="step-box"><div class="step-num">3</div><div class="step-text">Klicken Sie auf 'Herunterladen' und dann auf den grünen Button.</div></div>`,
                    dir: "ltr", align: "left"
                },
                pt: {
                    title: "VRTX <span>FB Downloader</span> 🎬", subtitle: "Ferramenta inteligente e leve para baixar vídeos do Facebook diretamente em alta qualidade",
                    btn: "Baixar Vídeo Direto ✨", loading: "Conectando ao servidor e extraindo o link... ⏳", success_btn: "Baixar em Alta Qualidade MP4 📥",
                    fail: "Falha na extração! Certifique-se de que o vídeo é público.", alert: "Por favor, cole um link de vídeo do Facebook primeiro!",
                    f1_t: "🚀 Ultra Rápido", f1_d: "Busca instantânea de links", f2_t: "🔒 100% Seguro", f2_d: "Seus dados estão protegidos", f3_t: "📱 Totalmente Responsivo", f3_d: "Para celular e desktop",
                    howToBtn: "💡 Como baixar?", currentLang: "Português", faqMainTitle: "❓ Perguntas Frecuentes",
                    q1: "Onde os vídeos são salvos após o download?", a1: "Os vídeos são salvos automaticamente na pasta 'Downloads' do seu dispositivo.",
                    q2: "Baixar vídeos privados do Facebook?", a2: "Não, esta ferramenta suporta apenas vídeos públicos para garantir velocidade.",
                    modalTitle: "📖 Passos para baixar",
                    modalSteps: `<div class="step-box"><div class="step-num">1</div><div class="step-text">Copie o link do vídeo do Facebook.</div></div>
                                 <div class="step-box"><div class="step-num">2</div><div class="step-text">Cole o link na caixa acima.</div></div>
                                 <div class="step-box"><div class="step-num">3</div><div class="step-text">Clique em 'Baixar' e depois no botão verde para salvar.</div></div>`,
                    dir: "ltr", align: "left"
                }
            };

            function toggleDropdown(event) {
                event.stopPropagation();
                const dropdown = document.getElementById('langDropdown');
                dropdown.classList.toggle('active');
            }

            function changeLang(event, lang) {
                event.preventDefault();
                setLanguage(lang);
                document.getElementById('langDropdown').classList.remove('active');
            }

            window.addEventListener('click', function(event) {
                const dropdown = document.getElementById('langDropdown');
                if (!dropdown.contains(event.target)) {
                    dropdown.classList.remove('active');
                }
            });

            function setLanguage(lang) {
                const t = translations[lang];
                document.getElementById('htmlTag').setAttribute('dir', t.dir);
                document.getElementById('mainTitle').innerHTML = t.title;
                document.getElementById('subTitle').innerText = t.subtitle;
                document.getElementById('actionBtn').innerText = t.btn;
                document.getElementById('downloadLink').innerText = t.success_btn;
                
                document.getElementById('f1_t').innerText = t.f1_t; document.getElementById('f1_d').innerText = t.f1_d;
                document.getElementById('f2_t').innerText = t.f2_t; document.getElementById('f2_d').innerText = t.f2_d;
                document.getElementById('f3_t').innerText = t.f3_t; document.getElementById('f3_d').innerText = t.f3_d;
                
                document.getElementById('howToBtn').innerText = t.howToBtn;
                document.getElementById('currentLang').innerText = t.currentLang;
                document.getElementById('faqMainTitle').innerText = t.faqMainTitle;
                document.getElementById('q1').innerText = t.q1; document.getElementById('a1').innerText = t.a1;
                document.getElementById('q2').innerText = t.q2; document.getElementById('a2').innerText = t.a2;
                document.getElementById('modalTitle').innerText = t.modalTitle;
                document.getElementById('modalSteps').innerHTML = t.modalSteps;
                
                document.getElementById('howToModal').style.direction = t.dir;
                document.getElementById('modalContent').style.textAlign = t.align;
            }

            document.getElementById('modalSteps').innerHTML = translations['ar'].modalSteps;

            function openModal() { document.getElementById('howToModal').style.display = "flex"; }
            function closeModal() { document.getElementById('howToModal').style.display = "none"; }
            
            window.addEventListener('click', function(event) {
                let modal = document.getElementById('howToModal');
                if (event.target == modal) { modal.style.display = "none"; }
            });

            function toggleFaq(element) {
                let answer = element.nextElementSibling;
                let icon = element.querySelector('span:last-child');
                if (answer.style.maxHeight && answer.style.maxHeight !== "0px") {
                    answer.style.maxHeight = "0px";
                    answer.style.padding = "0 18px";
                    answer.style.borderTopWidth = "0px";
                    icon.innerText = "➕";
                } else {
                    answer.style.maxHeight = answer.scrollHeight + "20px";
                    answer.style.padding = "14px 18px";
                    answer.style.borderTop = "1px solid rgba(138, 43, 226, 0.2)";
                    icon.innerText = "➖";
                }
            }

            async function getDownloadLink() {
                const url = document.getElementById('videoUrl').value;
                const resultBox = document.getElementById('resultBox');
                const downloadLink = document.getElementById('downloadLink');
                const videoTitle = document.getElementById('videoTitle');
                
                const currentLangText = document.getElementById('currentLang').innerText;
                let activeLang = 'en';
                if(currentLangText === "العربية") activeLang = 'ar';
                else if(currentLangText === "Français") activeLang = 'fr';
                else if(currentLangText === "Español") activeLang = 'es';
                else if(currentLangText === "Deutsch") activeLang = 'de';
                else if(currentLangText === "Português") activeLang = 'pt';
                
                const t = translations[activeLang];
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
                    videoTitle.innerText = (activeLang === 'ar') ? "حدث خطأ في الاتصال." : "Connection error.";
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
    if not video_url or not any(x in video_url for x in ["facebook.com", "fb.watch", "fb.gg"]):
        return jsonify({"success": False, "error": "رابط غير صحيح"})
        
    result = get_facebook_video_url(video_url)
    return jsonify(result)

@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    import datetime
    from flask import Response
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://vidio-fasebook-dawnlond-mrad.vercel.app/</loc>
        <lastmod>{today}</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
</urlset>"""
    return Response(xml_content, mimetype='application/xml')

if __name__ == '__main__':
    app.run(debug=True)