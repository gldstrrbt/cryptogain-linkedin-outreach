import csv

TARGET_KEYWORDS = [
    # --- English Keywords (Focused) ---
    "reporter", "journalist", "correspondent", "staff writer", "news writer",
    "editor", "news editor", "features editor", # Editorial roles focused on content
    "content writer", "copywriter", "freelance writer", "contributor", "columnist",
    "technical writer", "blogger", "author", "writer",
    "anchor", "producer", "media producer", "multimedia journalist", # Roles involved in presenting/creating media content
    "analyst", "market analyst", "research analyst", "crypto analyst", "financial analyst",
    "data analyst", "quant", "quantitative analyst", "chartist", "technical analyst",
    "strategist", # (Assuming this relates to research/analysis for content/trading)
    "researcher",
    "trader", "crypto trader", "investment analyst", # (If they also write/share insights)
    "product reviewer", "tech reviewer", "app reviewer", # Produce review content

    # --- Spanish (es) Translations (Focused) ---
    "reportero", "reportera",
    "periodista",
    "corresponsal", # Correspondent
    "redactor de plantilla", # Staff writer (approx.)
    "redactor de noticias", # News writer
    "editor", "editora", # Editor
    "editor de noticias", "editora de noticias", # News editor
    "editor de reportajes", "editora de reportajes", # Features editor (approx.)
    "escritor de contenido", "escritora de contenido", # Content writer
    "redactor publicitario", "redactora publicitaria", # Copywriter
    "escritor freelance", "escritora freelance", # Freelance writer
    "colaborador", "colaboradora", # Contributor
    "columnista",
    "redactor técnico", "redactora técnica", # Technical writer
    "bloguero", "bloguera",
    "autor", "autora",
    "presentador", "presentadora", # Anchor
    "productor", "productora", # Producer (content-focused)
    "productor de medios", "productora de medios", # Media producer
    "periodista multimedia", # Multimedia journalist
    "analista",
    "analista de mercado",
    "analista de investigación", # Research analyst
    "criptoanalista", "analista de criptomonedas", # Crypto analyst
    "analista financiero", "analista financiera",
    "analista de datos",
    "cuantitativo", "analista cuantitativo", # Quant, Quantitative analyst
    "cartista", "analista técnico", # Chartist, Technical analyst
    "estratega", # Strategist
    "investigador", "investigadora",
    "trader", "comerciante", # (Trader)
    "cripto trader", "trader de criptomonedas", # Crypto trader
    "analista de inversiones", # Investment analyst
    "revisor de productos", "revisora de productos", # Product reviewer
    "revisor de tecnología", "revisora de tecnología", # Tech reviewer
    "revisor de aplicaciones", "revisora de aplicaciones", # App reviewer

    # --- French (fr) Translations (Focused) ---
    "reporter", "reporteure",
    "journaliste",
    "correspondant", "correspondante",
    "rédacteur permanent", "rédactrice permanente", # Staff writer (approx.)
    "rédacteur d'actualités", "rédactrice d'actualités", # News writer
    "éditeur", "éditrice", "rédacteur", "rédactrice", # Editor
    "chef des informations", # News editor (can also be Rédacteur en chef informations)
    "rédacteur de fond", "rédactrice de fond", # Features editor (approx)
    "rédacteur de contenu", "rédactrice de contenu",
    "concepteur-rédacteur", "concepteur-rédactrice", # Copywriter
    "rédacteur freelance", "rédactrice freelance", "pigiste", # Freelance writer
    "contributeur", "contributrice",
    "chroniqueur", "chroniqueuse", # Columnist
    "rédacteur technique", "rédactrice technique",
    "blogueur", "blogueuse",
    "auteur", "auteure",
    "présentateur", "présentatrice", # Anchor
    "producteur", "productrice", # Producer (content-focused)
    "producteur multimédia", "productrice multimédia", # Media producer
    "journaliste multimédia",
    "analyste",
    "analyste de marché",
    "analyste de recherche",
    "analyste crypto",
    "analyste financier", "analyste financière",
    "analyste de données",
    "quant", "analyste quantitatif", # (Quant is often used)
    "chartiste", "analyste technique",
    "stratège",
    "chercheur", "chercheuse",
    "trader", "négociant", "négociante",
    "trader crypto",
    "analyste en investissements",
    "testeur de produits", "testeuse de produits", # Product reviewer
    "critique technique", # Tech reviewer
    "testeur d'applications", "testeuse d'applications", # App reviewer

    # --- German (de) Translations (Focused) ---
    "Reporter", "Reporterin",
    "Journalist", "Journalistin",
    "Korrespondent", "Korrespondentin",
    "Redakteur", "Redakteurin", # (Can mean staff writer/editor)
    "Nachrichtenredakteur", "Nachrichtenredakteurin", # News writer/editor
    "Feature-Redakteur", "Feature-Redakteurin", # Features editor
    "Content Writer", "Texter für Inhalte", # Content writer
    "Texter", "Texterin", "Werbetexter", "Werbetexterin", # Copywriter
    "freiberuflicher Autor", "freiberufliche Autorin", "freier Texter", "freie Texterin", # Freelance writer
    "Mitarbeiter", "Mitarbeiterin", "(freier) Beiträger", # Contributor
    "Kolumnist", "Kolumnistin",
    "Technischer Redakteur", "Technische Redakteurin", # Technical writer
    "Blogger", "Bloggerin",
    "Autor", "Autorin",
    "Moderator", "Moderatorin", "(Nachrichten-)Sprecher", "(Nachrichten-)Sprecherin", # Anchor
    "Produzent", "Produzentin", # Producer (content-focused)
    "Medienproduzent", "Medienproduzentin", # Media producer
    "Multimedia-Journalist", "Multimedia-Journalistin",
    "Analyst", "Analystin",
    "Marktanalyst", "Marktanalystin",
    "Research-Analyst", "Forschungsanalyst", "Forschungsanalystin", # Research analyst
    "Krypto-Analyst", "Krypto-Analystin",
    "Finanzanalyst", "Finanzanalystin",
    "Datenanalyst", "Datenanalystin",
    "Quant", "Quantitativer Analyst", "Quantitative Analystin", # Quant is common
    "Charttechniker", "Charttechnikerin", "Technischer Analyst", "Technische Analystin", # Chartist, Technical Analyst
    "Stratege", "Strategin",
    "Forscher", "Forscherin",
    "Händler", "Händlerin", "Trader", # (Trader is common)
    "Krypto-Händler", "Krypto-Trader",
    "Investmentanalyst", "Investmentanalystin",
    "Produktbewerter", "Produktbewerterin", "Produkttester", "Produkttesterin", # Product reviewer
    "Technik-Rezensent", "Technik-Rezensentin", # Tech reviewer
    "App-Tester", "App-Testerin", # App reviewer

    # --- Italian (it) Translations (Focused) ---
    "reporter",
    "giornalista",
    "corrispondente",
    "redattore", # Staff writer/editor
    "redattore di notizie", # News writer
    "caporedattore (per rubriche/features)", # Features editor (approx)
    "scrittore di contenuti", "redattore di contenuti", # Content writer
    "copywriter", # (often used directly)
    "scrittore freelance", "redattore freelance",
    "collaboratore", "collaboratrice", # Contributor
    "editorialista", "opinionista", # Columnist
    "redattore tecnico", # Technical writer
    "blogger",
    "autore", "autrice",
    "conduttore", "conduttrice", # Anchor
    "produttore", "produttrice", # Producer (content-focused)
    "produttore multimediale", # Media producer
    "giornalista multimediale",
    "analista",
    "analista di mercato",
    "analista ricercatore", # Research analyst
    "analista crypto",
    "analista finanziario",
    "analista dati",
    "quant", "analista quantitativo", # (Quant is common)
    "chartista", "analista tecnico",
    "stratega",
    "ricercatore", "ricercatrice",
    "trader", "commerciante",
    "crypto trader",
    "analista degli investimenti",
    "recensore di prodotti", # Product reviewer
    "recensore tecnologico", # Tech reviewer
    "recensore di app", # App reviewer

    # --- Portuguese (pt) Translations (Focused) ---
    "repórter",
    "jornalista",
    "correspondente",
    "redator", "redatora", # Staff writer/editor
    "redator de notícias", "redatora de notícias",
    "editor de pautas especiais", "editora de pautas especiais", # Features editor (approx)
    "escritor de conteúdo", "escritora de conteúdo",
    "redator publicitário", "redatora publicitária", # Copywriter
    "escritor freelancer", "escritora freelancer",
    "colaborador", "colaboradora",
    "colunista",
    "redator técnico", "redatora técnica",
    "blogueiro", "blogueira",
    "autor", "autora",
    "âncora", "apresentador", "apresentadora", # Anchor
    "produtor", "produtora", # Producer (content-focused)
    "produtor de mídia", "produtora de mídia", # Media producer
    "jornalista multimídia",
    "analista",
    "analista de mercado",
    "analista de pesquisa",
    "analista de cripto",
    "analista financeiro", "analista financeira",
    "analista de dados",
    "quant", "analista quantitativo", # (Quant is common)
    "grafista", "analista técnico", # Chartist, Technical analyst
    "estrategista",
    "pesquisador", "pesquisadora",
    "trader", "negociador", "negociadora",
    "trader de cripto",
    "analista de investimentos",
    "revisor de produtos", # Product reviewer
    "revisor de tecnologia", # Tech reviewer
    "revisor de aplicativos", # App reviewer

    # --- Russian (ru) Translations (Focused) ---
    "репортер",
    "журналист",
    "корреспондент",
    "штатный автор", "штатный писатель", # Staff writer
    "новостной автор", "новостной редактор", # News writer/editor
    "редактор", # Editor
    "редактор специальных репортажей", # Features editor (approx.)
    "автор контента", "контент-райтер", # Content writer
    "копирайтер",
    "писатель-фрилансер", "автор-фрилансер", # Freelance writer
    "контрибьютор", "автор (статей)", # Contributor
    "колумнист", "обозреватель", # Columnist
    "технический писатель",
    "блогер",
    "автор",
    "ведущий", "ведущая", # Anchor
    "продюсер", # Producer (content-focused)
    "медиа-продюсер", # Media producer
    "мультимедийный журналист",
    "аналитик",
    "рыночный аналитик", "аналитик рынка",
    "аналитик-исследователь", # Research analyst
    "криптоаналитик",
    "финансовый аналитик",
    "аналитик данных",
    "квант", "количественный аналитик", # Quant, Quantitative analyst
    "чартист", "технический аналитик",
    "стратег",
    "исследователь",
    "трейдер",
    "криптотрейдер",
    "инвестиционный аналитик",
    "обзорщик продуктов", # Product reviewer
    "технологический обозреватель", # Tech reviewer
    "обзорщик приложений", # App reviewer

    # --- Chinese (Simplified, zh-CN) Translations (Focused) ---
    "记者", # jìzhě (reporter/journalist)
    "新闻工作者", # xīnwén gōngzuòzhě (journalist)
    "通讯员", # tōngxùnyuán (correspondent)
    "专职作者", "专职撰稿人", # zhuānzhí zuòzhě / zhuāngǎo rén (staff writer)
    "新闻撰稿人", # xīnwén zhuāngǎo rén (news writer)
    "编辑", # biānjí (editor)
    "新闻编辑", # xīnwén biānjí (news editor)
    "特稿编辑", # tègǎo biānjí (features editor)
    "内容写手", "内容撰稿人", # nèiróng xiěshǒu / zhuāngǎo rén (content writer)
    "文案", # wén'àn (copywriter)
    "自由撰稿人", # zìyóu zhuāngǎo rén (freelance writer)
    "撰稿人", "投稿人", # zhuāngǎo rén, tóugǎo rén (contributor)
    "专栏作家", # zhuānlán zuòjiā (columnist)
    "技术文档工程师", "技术写手", # jìshù wéndàng gōngchéngshī / xiěshǒu (technical writer)
    "博主", # bózhǔ (blogger)
    "作者", # zuòzhě (author)
    "主播", # zhǔbō (anchor)
    "制作人", # zhìzuòrén (producer, content-focused)
    "媒体制作人", # méitǐ zhìzuòrén (media producer)
    "多媒体记者", # duōméitǐ jìzhě (multimedia journalist)
    "分析师", "分析员", # fēnxīshī, fēnxīyuán (analyst)
    "市场分析师", # shìchǎng fēnxīshī (market analyst)
    "研究分析师", # yánjiū fēnxīshī (research analyst)
    "加密分析师", # jiāmì fēnxīshī (crypto analyst)
    "金融分析师", # jīnróng fēnxīshī (financial analyst)
    "数据分析师", # shùjù fēnxīshī (data analyst)
    "量化分析师", # liànghuà fēnxīshī (quant/quantitative analyst)
    "图表分析师", "技术分析师", # túbiǎo fēnxīshī, jìshù fēnxīshī (chartist, technical analyst)
    "策略师", # cèlüèshī (strategist)
    "研究员", # yánjiūyuán (researcher)
    "交易员", # jiāoyìyuán (trader)
    "加密货币交易员", # jiāmì huòbì jiāoyìyuán (crypto trader)
    "投资分析师", # tóuzī fēnxīshī (investment analyst)
    "产品评论员", # chǎnpǐn pínglùnyuán (product reviewer)
    "科技评论员", # kējì pínglùnyuán (tech reviewer)
    "应用评论员", # yìngyòng pínglùnyuán (app reviewer)

    # --- Japanese (ja) Translations (Focused) ---
    "レポーター", # repōtā
    "ジャーナリスト", # jānarīsuto
    "特派員", # tokuhain (correspondent)
    "スタッフライター", # sutaffu raitā
    "ニュースライター", # nyūsu raitā
    "編集者", # henshūsha (editor)
    "ニュース編集者", # nyūsu henshūsha (news editor)
    "特集編集者", # tokushū henshūsha (features editor)
    "コンテンツライター", # kontentsu raitā
    "コピーライター", # kopīraitā
    "フリーランスライター", # furīransu raitā
    "寄稿者", "コントリビューター", # kikōsha, kontoribyūtā (contributor)
    "コラムニスト", # koramunisuto
    "テクニカルライター", # tekunikaru raitā
    "ブロガー", # burogā
    "著者", "作家", # chosha, sakka (author)
    "アンカー", "キャスター", # ankā, kyasutā (anchor)
    "プロデューサー", # purodyūsā (producer, content-focused)
    "メディアプロデューサー", # media purodyūsā (media producer)
    "マルチメディアジャーナリスト", # maruchimedia jānarīsuto
    "アナリスト", # anarisuto
    "市場アナリスト", "マーケットアナリスト", # shijō anarisuto, māketto anarisuto
    "リサーチアナリスト", # risāchi anarisuto
    "暗号アナリスト", "仮想通貨アナリスト", # angō anarisuto, kasō tsūka anarisuto (crypto analyst)
    "金融アナリスト", # kin'yū anarisuto
    "データアナリスト", # dēta anarisuto
    "クオンツ", "定量アナリスト", # kuontsu, teiryō anarisuto (quant, quantitative analyst)
    "チャーティスト", "テクニカルアナリスト", # chātisuto, tekunikaru anarisuto
    "ストラテジスト", # sutoratejisuto
    "研究者", # kenkyūsha
    "トレーダー", # torēdā
    "暗号トレーダー", "仮想通貨トレーダー", # angō torēdā, kasō tsūka torēdā (crypto trader)
    "投資アナリスト", # tōshi anarisuto
    "製品レビュアー", # seihin rebyuā (product reviewer)
    "技術レビュアー", # gijutsu rebyuā (tech reviewer)
    "アプリレビュアー", # apuri rebyuā (app reviewer)

    # --- Korean (ko) Translations (Focused) ---
    "리포터", # ripoteo
    "저널리스트", "기자", # jeoneolliseuteu, gija (journalist)
    "특파원", # teukpawon (correspondent)
    "전속 작가", # jeonsok jakga (staff writer, approx.)
    "뉴스 작가", # nyuseu jakga (news writer)
    "편집자", # pyeonjipja (editor)
    "뉴스 편집자", # nyuseu pyeonjipja (news editor)
    "특집 편집자", # teukjip pyeonjipja (features editor)
    "콘텐츠 작가", # kontencheu jakga (content writer)
    "카피라이터", # kapiraiteo
    "프리랜서 작가", # peuriraenseo jakga (freelance writer)
    "기고가", "컨트리뷰터", # gigoga, keonteuribyuteo (contributor)
    "칼럼니스트", # kalleomniseuteu
    "기술 작가", # gisul jakga (technical writer)
    "블로거", # beullogeo
    "작가", "저자", # jakga, jeoja (author)
    "앵커", # aengkeo
    "프로듀서", # peurodyuseo (producer, content-focused)
    "미디어 프로듀サー", # midieo peurodyuseo (media producer)
    "멀티미디어 기자", # meoltimidieo gija (multimedia journalist)
    "분석가", # bunseokga (analyst)
    "시장 분석가", # sijang bunseokga (market analyst)
    "연구 분석가", # yeongu bunseokga (research analyst)
    "암호화폐 분석가", "크립토 분석가", # amhohwapye bunseokga, keuripto bunseokga (crypto analyst)
    "금융 분석가", # geumyung bunseokga (financial analyst)
    "데이터 분석가", # deiteo bunseokga (data analyst)
    "퀀트", "계량 분석가", # kwonteu, gyeryang bunseokga (quant, quantitative analyst)
    "차트 분석가", "기술적 분석가", # chateu bunseokga, gisuljeok bunseokga (chartist, technical analyst)
    "전략가", # jeollyakga (strategist)
    "연구원", # yeonguwon (researcher)
    "트레이더", # teureideo
    "암호화폐 트레이더", "크립토 트레이더", # amhohwapye teureideo, keuripto teureideo (crypto trader)
    "투자 분석가", # tuja bunseokga (investment analyst)
    "제품 리뷰어", # jepum ribyueo (product reviewer)
    "기술 리뷰어", # gisul ribyueo (tech reviewer)
    "앱 리뷰어", # aep ribyueo (app reviewer)

    # --- Arabic (ar) Translations (Focused) ---
    "مراسل", # murāsil (reporter)
    "صحفي", # ṣaḥafī (journalist)
    "مراسل صحفي", # murāsil ṣaḥafī (correspondent)
    "كاتب دائم", # kātib dāʾim (staff writer approx)
    "كاتب أخبار", # kātib ʾakhbār (news writer)
    "محرر", # muḥarrir (editor)
    "محرر أخبار", # muḥarrir ʾakhbār (news editor)
    "محرر تحقيقات", # muḥarrir taḥqīqāt (features editor approx)
    "كاتب محتوى", # kātib muḥtawá (content writer)
    "ناسخ إعلانات", "كاتب إعلانات", # nāsikh ʾiʿlānāt, kātib ʾiʿlānāt (copywriter)
    "كاتب مستقل", # kātib mustaqill (freelance writer)
    "مساهم", # musāhim (contributor)
    "كاتب عمود", # kātib ʿamūd (columnist)
    "كاتب تقني", # kātib tiqnī (technical writer)
    "مدون", # mudawwin (blogger)
    "مؤلف", # muʾallif (author)
    "مذيع", # mudhīʿ (anchor)
    "منتج", # muntij (producer, content-focused)
    "منتج إعلامي", # muntij ʾiʿlāmī (media producer)
    "صحفي وسائط متعددة", # ṣaḥafī wasāʾiṭ mutaʿaddida (multimedia journalist)
    "محلل", # muḥallil (analyst)
    "محلل سوق", # muḥallil sūq (market analyst)
    "محلل أبحاث", # muḥallil ʾabḥāth (research analyst)
    "محلل تشفير", "محلل عملات مشفرة", # muḥallil tashfīr, muḥallil ʿumalāt mushaffara (crypto analyst)
    "محلل مالي", # muḥallil mālī (financial analyst)
    "محلل بيانات", # muḥallil bayānāt (data analyst)
    "محلل كمي", # muḥallil kammī (quant/quantitative analyst)
    "محلل فني", "محلل رسوم بيانية", # muḥallil fannī, muḥallil rusūm bayāniyya (technical analyst/chartist)
    "استراتيجي", # ʾistrātījī (strategist)
    "باحث", # bāḥith (researcher)
    "متداول", # mutadāwil (trader)
    "متداول عملات مشفرة", # mutadāwil ʿumalāt mushaffara (crypto trader)
    "محلل استثمار", # muḥallil ʾistithmār (investment analyst)
    "مراجع منتجات", # murājiʿ muntajāt (product reviewer)
    "مراجع تقني", # murājiʿ tiqnī (tech reviewer)
    "مراجع تطبيقات", # murājiʿ taṭbīqāt (app reviewer)

    # --- Hindi (hi) Translations (Focused) ---
    "रिपोर्टर", # riporṭar
    "पत्रकार", # patrakār (journalist)
    "संवाददाता", # saṃvāddātā (correspondent)
    "स्टाफ लेखक", # sṭāph lekhak (staff writer)
    "समाचार लेखक", # samāchār lekhak (news writer)
    "संपादक", # sampādak (editor)
    "समाचार संपादक", # samāchār sampādak (news editor)
    "फीचर संपादक", # phīchar sampādak (features editor)
    "कंटेंट लेखक", # kaṇṭeṇṭ lekhak (content writer)
    "कॉपीराइटर", # kŏpīrāiṭar
    "फ्रीलांस लेखक", # phrīlāns lekhak (freelance writer)
    "योगदानकर्ता", # yogadānakartā (contributor)
    "स्तंभकार", # staṃbhakār (columnist)
    "तकनीकी लेखक", # takanīkī lekhak (technical writer)
    "ब्लॉगर", # blŏgar
    "लेखक", # lekhak (author)
    "एंकर", # aiṅkar
    "निर्माता", # nirmātā (producer, content-focused)
    "मीडिया निर्माता", # mīḍiyā nirmātā (media producer)
    "मल्टीमीडिया पत्रकार", # malṭīmīḍiyā patrakār (multimedia journalist)
    "विश्लेषक", # viśleṣak (analyst)
    "बाजार विश्लेषक", # bājār viśleṣak (market analyst)
    "अनुसंधान विश्लेषक", # anusandhān viśleṣak (research analyst)
    "क्रिप्टो विश्लेषक", # kripṭo viśleṣak (crypto analyst)
    "वित्तीय विश्लेषक", # vittīya viśleṣak (financial analyst)
    "डेटा विश्लेषक", # ḍeṭā viśleṣak (data analyst)
    "क्वांट विश्लेषक", # kvāṇṭ viśleṣak (quant/quantitative analyst)
    "चार्टिस्ट", "तकनीकी विश्लेषक", # chārṭisṭ, takanīkī viśleṣak (chartist, technical analyst)
    " रणनीतिकार", # raṇanītikār (strategist)
    "शोधकर्ता", # śodhakartā (researcher)
    "ट्रेडर", # ṭreḍar
    "क्रिप्टो ट्रेडर", # kripṭo ṭreḍar
    "निवेश विश्लेषक", # niveś viśleṣak (investment analyst)
    "उत्पाद समीक्षक", # utpād samīkṣak (product reviewer)
    "तकनीकी समीक्षक", # takanīkī samīkṣak (tech reviewer)
    "ऐप समीक्षक", # aip samīkṣak (app reviewer)

    # --- Turkish (tr) Translations (Focused) ---
    "muhabir",
    "gazeteci",
    "muhabir", "yurt dışı muhabiri", # (Correspondent can overlap with reporter)
    "kadrolu yazar", # Staff writer
    "haber yazarı", # News writer
    "editör",
    "haber editörü", # News editor
    "özellikli yazılar editörü", # Features editor (approx)
    "içerik yazarı", # Content writer
    "reklam yazarı", # Copywriter
    "serbest yazar", # Freelance writer
    "katkıda bulunan", # Contributor
    "köşe yazarı", # Columnist
    "teknik yazar",
    "blogger", # (often used directly)
    "yazar",
    "spiker", "sunucu", # Anchor
    "yapımcı", # Producer (content-focused)
    "medya yapımcısı", # Media producer
    "multimedya gazetecisi", # Multimedia journalist
    "analist",
    "piyasa analisti",
    "araştırma analisti",
    "kripto analisti",
    "finans analisti",
    "veri analisti",
    "kantitatif analist", "quant", # (Quant is often used)
    "teknik analist", "grafik analisti", # Technical analyst, chartist
    "stratejist",
    "araştırmacı",
    "tüccar", "trader",
    "kripto trader",
    "yatırım analisti",
    "ürün inceleme yazarı", # Product reviewer
    "teknoloji inceleme yazarı", # Tech reviewer
    "uygulama inceleme yazarı" # App reviewer
]

EXCLUDED_KEYWORDS = [
    "visual", "automotive", "video", "transportation", "photo", "litigation", 
    "graphic", "audio", "multimedia", "health", "legal", "investigative", 
    "sport", "environment", "climate", "immigration", "multi media", "film", 
	"attorney", "lawyer", " law", " law ", " ux ", "design", "customer"
]

# Optional: Remove duplicates if any (though less likely with multiple languages and now focused)
# TARGET_KEYWORDS_FOCUSED = sorted(list(set(TARGET_KEYWORDS_FOCUSED)))

# print(f"Total focused keywords: {len(TARGET_KEYWORDS_FOCUSED)}")
# for keyword in TARGET_KEYWORDS_FOCUSED:
# print(keyword)

def read_csv(filepath):
	a = open(filepath, "r", encoding="utf8", errors="ignore", newline="")
	b = csv.reader(a)
	return [c for c in b]


def write_csv(filepath):
	a = open(filepath, "w", encoding="utf8", errors="ignore", newline="")
	b = csv.writer(a)
	return b


def main():
	filepath = "writers_only.csv"
	a = read_csv(filepath)
	write_path = "writers_only_updated.csv"
	b = write_csv(write_path)
	print(a[0])
	print(len(a[0]))
	print(a[1])
	print(len(a[1]))
	print(a[1][0])
	print(a[1][1])
	print(a[1][2])
	print(a[1][3])
	print(a[1][4])
	print(a[1][5])
	for c in a:
		matched_keyword = next(
			(kw for kw in TARGET_KEYWORDS 
			if kw.lower() in c[2].lower() and 
			not any(excluded.lower() in c[2].lower() for excluded in EXCLUDED_KEYWORDS)),
			None
		)
		if matched_keyword:
			b.writerow(c)

main()