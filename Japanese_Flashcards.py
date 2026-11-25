import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="Flashcard Study App", layout="centered")

#add ALL terms in entries, then copy all vocab terms into vocab. don't copy terms that only appear in the kanji study section there
#only add the kanji to kanji list, the thing will auto search for entries that contain them
#only use kanji if it has been learned before or is being learned in the current unit, unless it's for the kanji section or simple enough that it won't be a problem (like 困る)
#additional allowance: if the book itself uses kanji on the vocab page, it is allowed, even if it hasn't been learned yet

#kanji by unit and book:
ND2_KANJI_BY_UNIT = {
    "はじめに": list("月火水木金土日一二三四五六七八九十百千万円"),
    "13": list("子好本人大休"),
    "14": list("私住女男何年"),
    "15": list("行読聞見来言"),
    "16": list("会社週今先雨"),
    "17": list("東西南北国小"),
    "18": list("話食買飲電車"),
    "19": list("上下中入毎町"),
    "20": list("開閉語気学生"),
    "21": list("思出高校外駅"),
    "22": list("多少左右時間"),
    "23": list("母父安書名天"),
    "24": list("午後前半友元"),
}

DD_KANJI_BY_UNIT = {
    "1": list("教仕事家手使心持方山作明"),
    "2": list("質問起正分犬有帰待知白足"),
    "3": list("物魚肉料理長口京体着朝夜"),
    "4": list("便利新古切目始意春夏秋冬"),
    "5": list("川海場所世界変道歩走花病"),
}

ALL_ND2_KANJI = [k for chars in ND2_KANJI_BY_UNIT.values() for k in chars]

jlpt_n5 = {
    "allowed_kanji": set(),
    "entries": {
        # 人
        "人": {"reading": ["ひと; じん"], "meaning": "Person"},
        "人生": {"reading": ["じんせい"], "meaning": "One's life"},
        "大人": {"reading": ["おとな"], "meaning": "Adult"},
        "人口": {"reading": ["じんこう"], "meaning": "Population"},
        # 一
        "一": {"reading": ["いち; ひと"], "meaning": "One"},
        "一人": {"reading": ["ひとり"], "meaning": "One person; Alone"},
        "一日": {"reading": ["ついたち; いちにち"], "meaning": "First day of the month; One day"},
        "一番": {"reading": ["いちばん"], "meaning": "Number one; Best; Most"},
        # 日
        "日": {"reading": ["ひ; か"], "meaning": "Day; Sun"},
        "日本": {"reading": ["にほん; にっぽん"], "meaning": "Japan"},
        "日曜日": {"reading": ["にちようび"], "meaning": "Sunday"},
        "毎日": {"reading": ["まいにち"], "meaning": "Every day"},
        # 大
        "大きい": {"reading": ["おおきい"], "meaning": "Big; Large"},
        "大学": {"reading": ["だいがく"], "meaning": "University; College"},
        "大切": {"reading": ["たいせつ"], "meaning": "Important; Precious"},
        "大好き": {"reading": ["だいすき"], "meaning": "Love; Very fond of"},
        # 年
        "年": {"reading": ["とし; ねん"], "meaning": "Year"},
        "今年": {"reading": ["ことし"], "meaning": "This year"},
        "来年": {"reading": ["らいねん"], "meaning": "Next year"},
        "去年": {"reading": ["きょねん"], "meaning": "Last year"},
        # 出
        "出る": {"reading": ["でる"], "meaning": "Go out; Leave; Appear"},
        "出す": {"reading": ["だす"], "meaning": "Take out; Put out; Send"},
        "出口": {"reading": ["でぐち"], "meaning": "Exit"},
        "外出": {"reading": ["がいしゅつ"], "meaning": "Going out"},
        # 本
        "本": {"reading": ["ほん"], "meaning": "Book; Origin"},
        "日本語": {"reading": ["にほんご"], "meaning": "Japanese language"},
        "本当": {"reading": ["ほんとう"], "meaning": "Truth; Reality"},
        "一本": {"reading": ["いっぽん"], "meaning": "One long object; One bottle"},
        # 中
        "中": {"reading": ["なか; ちゅう"], "meaning": "Inside; Middle"},
        "中学校": {"reading": ["ちゅうがっこう"], "meaning": "Middle school; Junior high school"},
        "一日中": {"reading": ["いちにちじゅう"], "meaning": "All day long"},
        "水中": {"reading": ["すいちゅう"], "meaning": "Underwater"},
        # 子
        "子": {"reading": ["こ"], "meaning": "Child"},
        "子供": {"reading": ["こども"], "meaning": "Child; Children"},
        "女の子": {"reading": ["おんなのこ"], "meaning": "Girl"},
        "男の子": {"reading": ["おとこのこ"], "meaning": "Boy"},
        # 見
        "見る": {"reading": ["みる"], "meaning": "See; Look; Watch"},
        "見せる": {"reading": ["みせる"], "meaning": "Show"},
        "見える": {"reading": ["みえる"], "meaning": "Be visible; Can see"},
        "見物": {"reading": ["けんぶつ"], "meaning": "Sightseeing; Watching"},
        # 国
        "国": {"reading": ["くに"], "meaning": "Country"},
        "外国": {"reading": ["がいこく"], "meaning": "Foreign country"},
        "外国人": {"reading": ["がいこくじん"], "meaning": "Foreigner"},
        "天国": {"reading": ["てんごく"], "meaning": "Heaven"},
        # 上
        "上": {"reading": ["うえ; じょう"], "meaning": "Above; Up; Top"},
        "上がる": {"reading": ["あがる"], "meaning": "Rise; Go up"},
        "上げる": {"reading": ["あげる"], "meaning": "Raise; Give"},
        "上手": {"reading": ["じょうず"], "meaning": "Skillful; Good at"},
        # 分
        "分かる": {"reading": ["わかる"], "meaning": "Understand"},
        "十分": {"reading": ["じゅうぶん; じっぷん"], "meaning": "Enough; Ten minutes"},
        "半分": {"reading": ["はんぶん"], "meaning": "Half"},
        "自分": {"reading": ["じぶん"], "meaning": "Oneself"},
        # 生
        "生きる": {"reading": ["いきる"], "meaning": "Live"},
        "生まれる": {"reading": ["うまれる"], "meaning": "Be born"},
        "先生": {"reading": ["せんせい"], "meaning": "Teacher"},
        "学生": {"reading": ["がくせい"], "meaning": "Student"},
        # 行
        "行く": {"reading": ["いく"], "meaning": "Go"},
        "行う": {"reading": ["おこなう"], "meaning": "Carry out; Conduct; Perform"},
        "銀行": {"reading": ["ぎんこう"], "meaning": "Bank"},
        "旅行": {"reading": ["りょこう"], "meaning": "Travel; Trip"},
        # 二
        "二": {"reading": ["に; ふた"], "meaning": "Two"},
        "二人": {"reading": ["ふたり"], "meaning": "Two people"},
        "二日": {"reading": ["ふつか"], "meaning": "Second day of the month; Two days"},
        "二十歳": {"reading": ["はたち"], "meaning": "Twenty years old"},
        # 間
        "間": {"reading": ["あいだ; かん"], "meaning": "Interval; Between; While"},
        "時間": {"reading": ["じかん"], "meaning": "Time; Hour"},
        "人間": {"reading": ["にんげん"], "meaning": "Human beings; People; Humans"},
        "年間": {"reading": ["ねんかん"], "meaning": "Per year; Annual; A year; (Duration of) a year; (For) a year"},
        # 時
        "時": {"reading": ["とき; じ"], "meaning": "Time; Hour"},
        "時計": {"reading": ["とけい"], "meaning": "Clock; Watch"},
        "時々": {"reading": ["ときどき"], "meaning": "Sometimes"},
        "一時": {"reading": ["いちじ"], "meaning": "One o'clock; For a while"},
        # 気
        "気": {"reading": ["き"], "meaning": "Spirit; Mind; Mood"},
        "天気": {"reading": ["てんき"], "meaning": "Weather"},
        "元気": {"reading": ["げんき"], "meaning": "Healthy; Energetic"},
        "人気": {"reading": ["にんき"], "meaning": "Popularity"},
        # 十
        "十": {"reading": ["じゅう; とお"], "meaning": "Ten"},
        "十日": {"reading": ["とおか"], "meaning": "Tenth day of the month; Ten days"},
        "二十": {"reading": ["にじゅう"], "meaning": "Twenty"},
        # 女
        "女": {"reading": ["おんな"], "meaning": "Woman; Female"},
        "女性": {"reading": ["じょせい"], "meaning": "Woman; Female"},
        "彼女": {"reading": ["かのじょ"], "meaning": "She; Girlfriend"},
        "女の人": {"reading": ["おんなのひと"], "meaning": "Woman"},
        # 三
        "三": {"reading": ["さん; み"], "meaning": "Three"},
        "三人": {"reading": ["さんにん"], "meaning": "Three people"},
        "三日": {"reading": ["みっか"], "meaning": "Third day of the month; Three days"},
        "三月": {"reading": ["さんがつ"], "meaning": "March"},
        # 前
        "前": {"reading": ["まえ"], "meaning": "Front; Before"},
        "名前": {"reading": ["なまえ"], "meaning": "Name"},
        "午前": {"reading": ["ごぜん"], "meaning": "Morning; A.M."},
        "前回": {"reading": ["ぜんかい"], "meaning": "Last time"},
        # 入
        "入る": {"reading": ["はいる; いる"], "meaning": "Enter; Go in"},
        "入れる": {"reading": ["いれる"], "meaning": "Put in; Insert"},
        "入口": {"reading": ["いりぐち"], "meaning": "Entrance"},
        "入学": {"reading": ["にゅうがく"], "meaning": "School admission; Enrollment"},
        # 小
        "小さい": {"reading": ["ちいさい"], "meaning": "Small; Little"},
        "小学校": {"reading": ["しょうがっこう"], "meaning": "Elementary school"},
        "小川": {"reading": ["おがわ"], "meaning": "Stream; Brook"},
        # 後
        "後": {"reading": ["あと; うしろ; ご"], "meaning": "After; Behind; Later"},
        "後ろ": {"reading": ["うしろ"], "meaning": "Back; Behind"},
        "午後": {"reading": ["ごご"], "meaning": "Afternoon; P.M."},
        "最後": {"reading": ["さいご"], "meaning": "Last; End"},
        # 長
        "長い": {"reading": ["ながい"], "meaning": "Long"},
        "校長": {"reading": ["こうちょう"], "meaning": "Principal"},
        "長男": {"reading": ["ちょうなん"], "meaning": "Eldest son"},
        "長女": {"reading": ["ちょうじょ"], "meaning": "Eldest daughter"},
        # 下
        "下": {"reading": ["した; もと; か"], "meaning": "Below; Down; Under"},
        "下がる": {"reading": ["さがる"], "meaning": "Go down; Drop"},
        "下げる": {"reading": ["さげる"], "meaning": "Lower; Hang down"},
        "地下鉄": {"reading": ["ちかてつ"], "meaning": "Subway"},
        # 学
        "学ぶ": {"reading": ["まなぶ"], "meaning": "Learn; Study"},
        "学校": {"reading": ["がっこう"], "meaning": "School"},
        "文学": {"reading": ["ぶんがく"], "meaning": "Literature"},
        # 月
        "月": {"reading": ["つき; がつ"], "meaning": "Moon; Month"},
        "月曜日": {"reading": ["げつようび"], "meaning": "Monday"},
        "今月": {"reading": ["こんげつ"], "meaning": "This month"},
        "来月": {"reading": ["らいげつ"], "meaning": "Next month"},
        # 何
        "何": {"reading": ["なに; なん"], "meaning": "What"},
        "何時": {"reading": ["なんじ"], "meaning": "What time"},
        "何人": {"reading": ["なんにん; なんじん"], "meaning": "How many people; What nationality"},
        "何か": {"reading": ["なにか"], "meaning": "Something"},
        # 来
        "来る": {"reading": ["くる"], "meaning": "Come"},
        "来年": {"reading": ["らいねん"], "meaning": "Next year"},
        "未来": {"reading": ["みらい"], "meaning": "Future"},
        # 話
        "話す": {"reading": ["はなす"], "meaning": "Speak; Talk"},
        "話": {"reading": ["はなし"], "meaning": "Talk; Story"},
        "電話": {"reading": ["でんわ"], "meaning": "Telephone"},
        "会話": {"reading": ["かいわ"], "meaning": "Conversation"},
        # 山
        "山": {"reading": ["やま"], "meaning": "Mountain"},
        "富士山": {"reading": ["ふじさん"], "meaning": "Mt. Fuji"},
        "火山": {"reading": ["かざん"], "meaning": "Volcano"},
        "登山": {"reading": ["とざん"], "meaning": "Mountain climbing"},
        # 高
        "高い": {"reading": ["たかい"], "meaning": "High; Expensive"},
        "高校": {"reading": ["こうこう"], "meaning": "High school"},
        "高校生": {"reading": ["こうこうせい"], "meaning": "High school student"},
        # 今
        "今": {"reading": ["いま"], "meaning": "Now"},
        "今日": {"reading": ["きょう"], "meaning": "Today"},
        "今年": {"reading": ["ことし"], "meaning": "This year"},
        # 書
        "書く": {"reading": ["かく"], "meaning": "Write"},
        "辞書": {"reading": ["じしょ"], "meaning": "Dictionary"},
        "教科書": {"reading": ["きょうかしょ"], "meaning": "Textbook"},
        "図書館": {"reading": ["としょかん"], "meaning": "Library"},
        # 五
        "五": {"reading": ["ご; いつ"], "meaning": "Five"},
        "五日": {"reading": ["いつか"], "meaning": "Fifth day of the month; Five days"},
        "五月": {"reading": ["ごがつ"], "meaning": "May"},
        "五人": {"reading": ["ごにん"], "meaning": "Five people"},
        # 名
        "有名": {"reading": ["ゆうめい"], "meaning": "Famous"},
        "名字": {"reading": ["みょうじ"], "meaning": "Surname; Family name"},
        # 金
        "お金": {"reading": ["おかね"], "meaning": "Money"},
        "金曜日": {"reading": ["きんようび"], "meaning": "Friday"},
        "金": {"reading": ["きん"], "meaning": "Gold; Money"},
        "料金": {"reading": ["りょうきん"], "meaning": "Fee; Charge"},
        # 男
        "男": {"reading": ["おとこ"], "meaning": "Man; Male"},
        "男性": {"reading": ["だんせい"], "meaning": "Man; Male"},
        "男の人": {"reading": ["おとこのひと"], "meaning": "Man"},
        # 外
        "外": {"reading": ["そと; がい"], "meaning": "Outside"},
        "外国人": {"reading": ["がいこくじん"], "meaning": "Foreigner"},
        "以外": {"reading": ["いがい"], "meaning": "Except; Other than"},
        # 四
        "四": {"reading": ["よん; し; よ"], "meaning": "Four"},
        "四日": {"reading": ["よっか"], "meaning": "Fourth day of the month; Four days"},
        "四月": {"reading": ["しがつ"], "meaning": "April"},
        "四人": {"reading": ["よにん"], "meaning": "Four people"},
        # 先
        "先": {"reading": ["さき"], "meaning": "Ahead; First; Previous"},
        "先週": {"reading": ["せんしゅう"], "meaning": "Last week"},
        "先月": {"reading": ["せんげつ"], "meaning": "Last month"},
        # 川
        "川": {"reading": ["かわ"], "meaning": "River"},
        "川上": {"reading": ["かわかみ"], "meaning": "Upstream"},
        "天の川": {"reading": ["あまのかわ"], "meaning": "Milky Way"},
        # 東
        "東": {"reading": ["ひがし"], "meaning": "East"},
        "東京": {"reading": ["とうきょう"], "meaning": "Tokyo"},
        "東口": {"reading": ["ひがしぐち"], "meaning": "East exit"},
        "東方": {"reading": ["とうほう"], "meaning": "East; Orient"},
        # 聞
        "聞く": {"reading": ["きく"], "meaning": "Listen; Hear; Ask"},
        "聞こえる": {"reading": ["きこえる"], "meaning": "Be audible; Can hear"},
        "新聞": {"reading": ["しんぶん"], "meaning": "Newspaper"},
        "見聞": {"reading": ["けんぶん"], "meaning": "Information; Experience"},
        # 語
        "英語": {"reading": ["えいご"], "meaning": "English language"},
        "言語": {"reading": ["げんご"], "meaning": "Language"},
        "単語": {"reading": ["たんご"], "meaning": "Word; Vocabulary"},
        # 九
        "九": {"reading": ["きゅう; く; ここの"], "meaning": "Nine"},
        "九日": {"reading": ["ここのか"], "meaning": "Ninth day of the month; Nine days"},
        "九月": {"reading": ["くがつ"], "meaning": "September"},
        "九人": {"reading": ["きゅうにん"], "meaning": "Nine people"},
        # 食
        "食べる": {"reading": ["たべる"], "meaning": "Eat"},
        "食べ物": {"reading": ["たべもの"], "meaning": "Food"},
        "食堂": {"reading": ["しょくどう"], "meaning": "Dining hall; Cafeteria"},
        "食事": {"reading": ["しょくじ"], "meaning": "Meal"},
        # 八
        "八": {"reading": ["はち; や"], "meaning": "Eight"},
        "八日": {"reading": ["ようか"], "meaning": "Eighth day of the month; Eight days"},
        "八月": {"reading": ["はちがつ"], "meaning": "August"},
        "八人": {"reading": ["はちにん"], "meaning": "Eight people"},
        # 水
        "水": {"reading": ["みず"], "meaning": "Water"},
        "水曜日": {"reading": ["すいようび"], "meaning": "Wednesday"},
        "水道": {"reading": ["すいどう"], "meaning": "Water supply; Tap water"},
        "水泳": {"reading": ["すいえい"], "meaning": "Swimming"},
        # 天
        "天気": {"reading": ["てんき"], "meaning": "Weather"},
        "天ぷら": {"reading": ["てんぷら"], "meaning": "Tempura"},
        "天国": {"reading": ["てんごく"], "meaning": "Heaven; Paradise"},
        "天才": {"reading": ["てんさい"], "meaning": "Genius; Talent"},
        # 木
        "木": {"reading": ["き"], "meaning": "Tree; Wood"},
        "木曜日": {"reading": ["もくようび"], "meaning": "Thursday"},
        "木工": {"reading": ["もっこう"], "meaning": "Woodworking; Carpentry"},
        "大木": {"reading": ["たいぼく"], "meaning": "Large tree"},
        # 六
        "六": {"reading": ["ろく; む"], "meaning": "Six"},
        "六日": {"reading": ["むいか"], "meaning": "Sixth day of the month; Six days"},
        "六月": {"reading": ["ろくがつ"], "meaning": "June"},
        "六人": {"reading": ["ろくにん"], "meaning": "Six people"},
        # 万
        "一万": {"reading": ["いちまん"], "meaning": "Ten thousand"},
        "万円": {"reading": ["まんえん"], "meaning": "Ten thousand yen"},
        "百万": {"reading": ["ひゃくまん"], "meaning": "One million"},
        # 白
        "白い": {"reading": ["しろい"], "meaning": "White"},
        "白": {"reading": ["しろ"], "meaning": "White"},
        "白黒": {"reading": ["しろくろ"], "meaning": "Black and white"},
        "白紙": {"reading": ["はくし"], "meaning": "Blank paper"},
        # 七
        "七": {"reading": ["なな; しち"], "meaning": "Seven"},
        "七日": {"reading": ["なのか"], "meaning": "Seventh day of the month; Seven days"},
        "七月": {"reading": ["しちがつ"], "meaning": "July"},
        "七人": {"reading": ["しちにん"], "meaning": "Seven people"},
        # 円
        "円": {"reading": ["えん"], "meaning": "Yen; Circle"},
        "百円": {"reading": ["ひゃくえん"], "meaning": "One hundred yen"},
        "千円": {"reading": ["せんえん"], "meaning": "One thousand yen"},
        # 電
        "電車": {"reading": ["でんしゃ"], "meaning": "Train"},
        "電気": {"reading": ["でんき"], "meaning": "Electricity; Electric light"},
        "電話": {"reading": ["でんわ"], "meaning": "Telephone"},
        # 父
        "父": {"reading": ["ちち"], "meaning": "Father"},
        "お父さん": {"reading": ["おとうさん"], "meaning": "Father; Dad"},
        "父母": {"reading": ["ふぼ"], "meaning": "Parents"},
        # 北
        "北": {"reading": ["きた"], "meaning": "North"},
        "北海道": {"reading": ["ほっかいどう"], "meaning": "Hokkaido"},
        "北口": {"reading": ["きたぐち"], "meaning": "North exit"},
        "北米": {"reading": ["ほくべい"], "meaning": "North America"},
        # 車
        "車": {"reading": ["くるま"], "meaning": "Car; Vehicle"},
        "自転車": {"reading": ["じてんしゃ"], "meaning": "Bicycle"},
        "自動車": {"reading": ["じどうしゃ"], "meaning": "Automobile; Car"},
        # 母
        "母": {"reading": ["はは"], "meaning": "Mother"},
        "お母さん": {"reading": ["おかあさん"], "meaning": "Mother; Mom"},
        "母国": {"reading": ["ぼこく"], "meaning": "Home country; Mother country"},
        # 半
        "半日": {"reading": ["はんにち"], "meaning": "Half a day"},
        "後半": {"reading": ["こうはん"], "meaning": "Second half"},
        "前半": {"reading": ["ぜんはん"], "meaning": "First half"},
        # 百
        "百": {"reading": ["ひゃく"], "meaning": "Hundred"},
        "百貨店": {"reading": ["ひゃっかてん"], "meaning": "Department store"},
        "八百屋": {"reading": ["やおや"], "meaning": "Greengrocer; Vegetable shop"},
        # 土
        "土": {"reading": ["つち; ど"], "meaning": "Soil; Earth"},
        "土曜日": {"reading": ["どようび"], "meaning": "Saturday"},
        "土地": {"reading": ["とち"], "meaning": "Land; Plot"},
        "お土産": {"reading": ["みやげ"], "meaning": "Souvenir"},
        # 西
        "西": {"reading": ["にし"], "meaning": "West"},
        "西口": {"reading": ["にしぐち"], "meaning": "West exit"},
        "関西": {"reading": ["かんさい"], "meaning": "Kansai region"},
        "東西": {"reading": ["とうざい"], "meaning": "East and west"},
        # 読
        "読む": {"reading": ["よむ"], "meaning": "Read"},
        "読み方": {"reading": ["よみかた"], "meaning": "How to read; Reading"},
        "音読み": {"reading": ["おんよみ"], "meaning": "On'yomi; Chinese reading; Onyomi"},
        # 千
        "千": {"reading": ["せん"], "meaning": "Thousand"},
        "千葉": {"reading": ["ちば"], "meaning": "Chiba"},
        "一千年": {"reading": ["いっせんねん"], "meaning": "One thousand years"},
        # 校 most use cases already covered
        # 右
        "右": {"reading": ["みぎ"], "meaning": "Right"},
        "右側": {"reading": ["みぎがわ"], "meaning": "Right side"},
        "右手": {"reading": ["みぎて"], "meaning": "Right hand"},
        # 南
        "南": {"reading": ["みなみ"], "meaning": "South"},
        "南口": {"reading": ["みなみぐち"], "meaning": "South exit"},
        "南米": {"reading": ["なんべい"], "meaning": "South America"},
        "東南": {"reading": ["とうなん"], "meaning": "Southeast"},
        # 左
        "左": {"reading": ["ひだり"], "meaning": "Left"},
        "左側": {"reading": ["ひだりがわ"], "meaning": "Left side"},
        "左手": {"reading": ["ひだりて"], "meaning": "Left hand"},
        # 友
        "友達": {"reading": ["ともだち"], "meaning": "Friend"},
        "友人": {"reading": ["ゆうじん"], "meaning": "Friend"},
        "親友": {"reading": ["しんゆう"], "meaning": "Close friend; Best friend"},
        "友好": {"reading": ["ゆうこう"], "meaning": "Friendship"},
        # 火
        "火": {"reading": ["ひ"], "meaning": "Fire; Flame"},
        "火曜日": {"reading": ["かようび"], "meaning": "Tuesday"},
        "花火": {"reading": ["はなび"], "meaning": "Fireworks"},
        # 毎
        "毎週": {"reading": ["まいしゅう"], "meaning": "Every week"},
        "毎月": {"reading": ["まいつき; まいげつ"], "meaning": "Every month"},
        "毎年": {"reading": ["まいとし; まいねん"], "meaning": "Every year"},
        # 雨
        "雨": {"reading": ["あめ"], "meaning": "Rain"},
        "大雨": {"reading": ["おおあめ"], "meaning": "Heavy rain"},
        "小雨": {"reading": ["こさめ"], "meaning": "Light rain; Drizzle"},
        # 休
        "休む": {"reading": ["やすむ"], "meaning": "Rest; Take a day off; Be absent"},
        "休み": {"reading": ["やすみ"], "meaning": "Rest; Holiday; Vacation"},
        "夏休み": {"reading": ["なつやすみ"], "meaning": "Summer vacation"},
        "冬休み": {"reading": ["ふゆやすみ"], "meaning": "Winter vacation"},
        # 午
        "正午": {"reading": ["しょうご"], "meaning": "Noon; Midday"},
        "少年": {"reading": ["しょうねん"], "meaning": "Young man; Boy"},
    },
    "vocab": [],
    "kanji": [
        "人", "一", "日", "大", "年", "出", "本", "中", "子", "見",
        "国", "上", "分", "生", "行", "二", "間", "時", "気", "十",
        "女", "三", "前", "入", "小", "後", "長", "下", "学", "月",
        "何", "来", "話", "山", "高", "今", "書", "五", "名", "金",
        "男", "外", "四", "先", "川", "東", "聞", "語", "九", "食",
        "八", "水", "天", "木", "六", "万", "白", "七", "円", "電",
        "父", "北", "車", "母", "半", "百", "土", "西", "読", "千",
        "校", "右", "南", "左", "友", "火", "毎", "雨", "休", "午",
    ],
}

jlpt_n4 = {
    "allowed_kanji": set(),
    "entries": {},
    "vocab": [],
    "kanji": [
        # N4 1-100
        "言", "手", "自", "者", "事", "思", "会", "家", "的", "方",
        "地", "目", "場", "代", "私", "立", "物", "田", "体", "動",
        "社", "知", "理", "同", "心", "発", "作", "新", "世", "度",
        "明", "力", "意", "用", "主", "通", "文", "屋", "業", "持",
        "道", "身", "不", "口", "多", "野", "考", "開", "教", "近",
        "以", "問", "正", "真", "味", "界", "無", "少", "海", "切",
        "重", "集", "員", "公", "画", "死", "安", "親", "強", "使",
        "朝", "題", "仕", "京", "足", "品", "着", "別", "音", "元",
        "特", "風", "夜", "空", "有", "起", "運", "料", "楽", "色",
        "帰", "歩", "悪", "広", "店", "町", "住", "売", "待", "古",
        # N4 101-170
        "始", "終", "計", "院", "送", "族", "映", "買", "病", "早",
        "質", "台", "室", "可", "建", "転", "医", "止", "字", "工",
        "急", "図", "黒", "花", "英", "走", "青", "答", "紙", "歌",
        "注", "赤", "春", "館", "旅", "験", "写", "去", "研", "飲",
        "肉", "服", "銀", "茶", "究", "洋", "兄", "秋", "堂", "週",
        "習", "試", "夏", "弟", "鳥", "犬", "夕", "魚", "借", "飯",
        "駅", "昼", "冬", "姉", "曜", "漢", "牛", "妹", "貸", "勉",
    ],
}

jlpt_n3 = {
    "allowed_kanji": set(),
    "entries": {},
    "vocab": [],
    "kanji": [],
}

jlpt_n2 = {
    "allowed_kanji": set(),
    "entries": {},
    "vocab": [],
    "kanji": [],
}

jlpt_n1 = {
    "allowed_kanji": set(),
    "entries": {},
    "vocab": [],
    "kanji": [],
}

nd_hajimeni = {
    "allowed_kanji": set(ND2_KANJI_BY_UNIT["はじめに"]),
    "entries": {},
    "vocab": [],
    "kanji": list(ND2_KANJI_BY_UNIT["はじめに"]),
}

nd_unit_13 = {
    #allowed kanji: nd2 はじめに + unit 13
    "allowed_kanji": set(ND2_KANJI_BY_UNIT["はじめに"] + ND2_KANJI_BY_UNIT["13"]),
    "entries": {
        # Verbs
        "怠け者": {"reading": ["なまけもの"], "meaning": "Lazy; idle person", "kana_pieces": ["なま", "け", "もの"]},
        "泳ぐ": {"reading": ["およぐ"], "meaning": "Swim", "kana_pieces": ["およ", "ぐ"]},
        "遊ぶ": {"reading": ["あそぶ"], "meaning": "Play", "kana_pieces": ["あそ", "ぶ"]},
        "待つ": {"reading": ["まつ"], "meaning": "Wait", "kana_pieces": ["ま", "つ"]},
        "貰う": {"reading": ["もらう"], "meaning": "Get; receive", "kana_pieces": ["もら", "う"]},
        "話す": {"reading": ["はなす"], "meaning": "Speak", "kana_pieces": ["はな", "す"]},
        "上げる": {"reading": ["あげる"], "meaning": "Give", "kana_pieces": ["あ", "げ", "る"]},
        # Adjectives
        "大好き": {"reading": ["だいすき"], "meaning": "Love", "kana_pieces": ["だい", "すき"]},
        "好き": {"reading": ["すき"], "meaning": "Like", "kana_pieces": ["すき"]},
        "まあまあ": {"reading": ["まあまあ"], "meaning": "Fairly; so-so"},
        "駄目": {"reading": ["だめ"], "meaning": "Cannot stand; no way", "kana_pieces": ["だ", "め"]},
        "上手": {"reading": ["じょうず"], "meaning": "Be good at; skillful", "kana_pieces": ["じょう", "ず"]},
        "明るい": {"reading": ["あかるい"], "meaning": "Cheerful", "kana_pieces": ["あか", "る", "い"]},
        "面白い": {"reading": ["おもしろい"], "meaning": "Humorous; funny", "kana_pieces": ["おも", "しろ", "い"]},
        "頭がいい": {"reading": ["あたまがいい"], "meaning": "Smart; clever", "kana_pieces": ["あたま", "が", "い", "い"]},
        "厳しい": {"reading": ["きびしい"], "meaning": "Strict", "kana_pieces": ["きび", "し", "い"]},
        "真面目": {"reading": ["まじめ"], "meaning": "Serious; earnest", "kana_pieces": ["ま", "じ", "め"]},
        "親切": {"reading": ["しんせつ"], "meaning": "Kind; helpful", "kana_pieces": ["しん", "せつ"]},
        "フレンドリー": {"reading": ["フレンドリー; ふれんどりー"], "meaning": "Friendly"},
        "冷静": {"reading": ["れいせい"], "meaning": "Calm; cool-headed", "kana_pieces": ["れい", "せい"]},
        "ハンサム": {"reading": ["ハンサム; はんさむ"], "meaning": "Handsome"},
        # Nouns
        "相撲": {"reading": ["すもう"], "meaning": "Sumo", "kana_pieces": ["す", "もう"]},
        "プール": {"reading": ["プール; ぷーる"], "meaning": "Swimming pool"},
        "ピンポン": {"reading": ["ピンポン; ぴんぽん"], "meaning": "Table tennis"},
        "旅行": {"reading": ["りょこう"], "meaning": "Travel; trip [-suru]", "kana_pieces": ["りょ", "こう"]},
        "温泉": {"reading": ["おんせん"], "meaning": "Hot spring", "kana_pieces": ["おん", "せん"]},
        "アクション": {"reading": ["アクション; あくしょん"], "meaning": "Action"},
        "コメディー": {"reading": ["コメディー; こめでぃー"], "meaning": "Comedy"},
        "ホラー": {"reading": ["ホラー; ほらー"], "meaning": "Horror"},
        "SF": {"reading": ["SF; えすえふ"], "meaning": "Science fiction"},
        "アニメ": {"reading": ["アニメ; あにめ"], "meaning": "Animation"},
        "ラブストーリー": {"reading": ["ラブストーリー; らぶすとーりー"], "meaning": "Love story"},
        "スポーツ": {"reading": ["スポーツ; すぽーつ"], "meaning": "Sport"},
        "サッカー": {"reading": ["サッカー; さっかー"], "meaning": "Soccer"},
        "絵": {"reading": ["え"], "meaning": "Painting; drawing; picture", "kana_pieces": ["え"]},
        "恋人": {"reading": ["こいびと"], "meaning": "Lover", "kana_pieces": ["こい", "びと"]},
        "子ども": {"reading": ["こども"], "meaning": "Child", "kana_pieces": ["こ", "ども"]},
        "料理": {"reading": ["りょうり"], "meaning": "Food; dishes; cooking [-suru]", "kana_pieces": ["りょう", "り"]},
        "カフェ": {"reading": ["カフェ; かふぇ"], "meaning": "Café"},
        # Adverbs
        "結構": {"reading": ["けっこう"], "meaning": "Quite", "kana_pieces": ["けっ", "こう"]},
        "何時でも": {"reading": ["いつも"], "meaning": "Always", "kana_pieces": ["いつ", "で", "も"]},
        #expressions excluded because they often contain symbols that are difficult to match during testing
    },
    "vocab": [
        "怠け者",
        "泳ぐ",
        "遊ぶ",
        "待つ",
        "貰う",
        "話す",
        "上げる",
        "大好き",
        "好き",
        "まあまあ",
        "駄目",
        "上手",
        "明るい",
        "面白い",
        "頭がいい",
        "厳しい",
        "真面目",
        "親切",
        "フレンドリー",
        "冷静",
        "ハンサム",
        "相撲",
        "プール",
        "ピンポン",
        "旅行",
        "温泉",
        "アクション",
        "コメディー",
        "ホラー",
        "SF",
        "アニメ",
        "ラブストーリー",
        "スポーツ",
        "サッカー",
        "絵",
        "恋人",
        "子ども",
        "料理",
        "カフェ",
        "結構",
        "何時でも",
    ],
    "kanji": ["子", "好", "本", "人", "大", "休"],
}

dd_unit_1 = {
    # allowed kanji: all of nd2 + dd unit 1
    "allowed_kanji": set(ALL_ND2_KANJI + DD_KANJI_BY_UNIT["1"]),
    "entries": {
        #Nouns
        "小学校": {"reading": ["しょうがっこう"], "meaning": "Elementary school", "kana_pieces": ["しょう", "がっ", "こう"]},
        "幼稚園": {"reading": ["ようちえん"], "meaning": "Kindergarten", "kana_pieces": ["よう", "ち", "えん"]},
        "〜年間": {"reading": ["~ねんかん; ねんかん"], "meaning": "For ~years", "kana_pieces": ["〜", "ねん", "かん"]},
        "中学校": {"reading": ["ちゅうがっこう"], "meaning": "Middle school", "kana_pieces": ["ちゅう", "がっ", "こう"]},
        "高校": {"reading": ["こうこう"], "meaning": "High school", "kana_pieces": ["こう", "こう"]},
        "教育": {"reading": ["きょういく"], "meaning": "Education", "kana_pieces": ["きょう", "いく"]},
        "義務教育": {"reading": ["ぎむきょういく"], "meaning": "Compulsory education", "kana_pieces": ["ぎ", "む", "きょう", "いく"]},
        "試験": {"reading": ["しけん"], "meaning": "Exam", "kana_pieces": ["し", "けん"]},
        "外": {"reading": ["そと"], "meaning": "Outside", "kana_pieces": ["そと"]},
        "家事": {"reading": ["かじ"], "meaning": "Housework", "kana_pieces": ["か", "じ"]},
        "ピアノ": {"reading": ["ピアノ; ぴあの"], "meaning": "Piano"},
        "夜遅く": {"reading": ["よるおそく"], "meaning": "Late night", "kana_pieces": ["よる", "おそ", "く"]},
        "漫画": {"reading": ["まんが"], "meaning": "Manga; Cartoon; Comic", "kana_pieces": ["まん", "が"]},
        "インターネット": {"reading": ["インターネット; いんたーねっと"], "meaning": "Internet"},
        "先輩": {"reading": ["せんぱい"], "meaning": "One's senior", "kana_pieces": ["せん", "ぱい"]},
        "勇気": {"reading": ["ゆうき"], "meaning": "Courage", "kana_pieces": ["ゆう", "き"]},
        "情熱": {"reading": ["じょうねつ"], "meaning": "Passion", "kana_pieces": ["じょう", "ねつ"]},
        "心": {"reading": ["こころ"], "meaning": "Heart", "kana_pieces": ["こころ"]},
        "授業": {"reading": ["じゅぎょう"], "meaning": "Class", "kana_pieces": ["じゅ", "ぎょう"]},
        "夢": {"reading": ["ゆめ"], "meaning": "Dream", "kana_pieces": ["ゆめ"]},
        "外国": {"reading": ["がいこく"], "meaning": "Foreign country", "kana_pieces": ["がい", "こく"]},
        "宿題": {"reading": ["しゅくだい"], "meaning": "Homework", "kana_pieces": ["しゅく", "だい"]},
        "心の優しい人": {"reading": ["こころのやさしいひと"], "meaning": "Gentle-hearted person", "kana_pieces": ["こころ", "の", "やさ", "し", "い", "ひと"]},
        "鬼": {"reading": ["おに"], "meaning": "Demon", "kana_pieces": ["おに"]},
        "赤鬼": {"reading": ["あかおに"], "meaning": "Red demon", "kana_pieces": ["あか", "おに"]},
        "青鬼": {"reading": ["あおおに"], "meaning": "Blue demon", "kana_pieces": ["あお", "おに"]},
        "人生": {"reading": ["じんせい"], "meaning": "One's life", "kana_pieces": ["じん", "せい"]},
        "村": {"reading": ["むら"], "meaning": "Village", "kana_pieces": ["むら"]},
        "人間": {"reading": ["にんげん"], "meaning": "Human beings", "kana_pieces": ["にん", "げん"]},
        "看板": {"reading": ["かんばん"], "meaning": "Sign", "kana_pieces": ["かん", "ばん"]},
        "アイデア": {"reading": ["アイデア; あいであ"], "meaning": "Idea"},
        "手紙": {"reading": ["てがみ"], "meaning": "Letter", "kana_pieces": ["て", "がみ"]},
        "遠く": {"reading": ["とおく"], "meaning": "Far", "kana_pieces": ["とお", "く"]},
        "話": {"reading": ["はなし"], "meaning": "Story; Talk", "kana_pieces": ["はなし"]},
        "問題": {"reading": ["もんだい"], "meaning": "Problem", "kana_pieces": ["もん", "だい"]},
        "家": {"reading": ["いえ"], "meaning": "House", "kana_pieces": ["いえ"]},
        "ギリギリス": {"reading": ["ギリギリス; ぎりぎりす"], "meaning": "Grasshopper"},
        "食べ物": {"reading": ["たべもの"], "meaning": "Food", "kana_pieces": ["た", "べ", "もの"]},
        "飲み物": {"reading": ["のみもの"], "meaning": "Drink; Beverage", "kana_pieces": ["の", "み", "もの"]},
        "アリ": {"reading": ["アリ; あり"], "meaning": "Ant"},
        "明かり": {"reading": ["あかり"], "meaning": "Light", "kana_pieces": ["あ", "か", "り"]},
        #Verbs
        "降りる": {"reading": ["おりる"], "meaning": "Get off", "kana_pieces": ["お", "り", "る"]},
        "着く": {"reading": ["つく"], "meaning": "Arrive", "kana_pieces": ["つ", "く"]},
        "出る": {"reading": ["でる"], "meaning": "Get out; Leave", "kana_pieces": ["で", "る"]},
        "決める": {"reading": ["きめる"], "meaning": "Decide", "kana_pieces": ["き", "め", "る"]},
        "習う": {"reading": ["ならう"], "meaning": "Learn", "kana_pieces": ["なら", "う"]},
        "世話をする": {"reading": ["せわをする"], "meaning": "Take care; Look after", "kana_pieces": ["せ", "わ", "を", "す", "る"]},
        "ペットを飼う": {"reading": ["ペットをかう; ぺっとをかう"], "meaning": "Have a pet", "kana_pieces": ["ペ", "ッ", "ト", "を", "か", "う"]},
        "泊まる": {"reading": ["とまる"], "meaning": "Stay over (night)", "kana_pieces": ["と", "ま", "る"]},
        "呉れる": {"reading": ["くれる"], "meaning": "Give (me)", "kana_pieces": ["く", "れ", "る"]},
        "奢る": {"reading": ["おごる"], "meaning": "Treat (someone)", "kana_pieces": ["おご", "る"]},
        "連れて行く": {"reading": ["つれていく"], "meaning": "Take (someone)", "kana_pieces": ["つ", "れ", "て", "い", "く"]},
        "おしゃれをする": {"reading": ["おしゃれをする"], "meaning": "Dress up"},
        "サボる": {"reading": ["サボる; さぼる"], "meaning": "Skip (a class)"},
        "持つ": {"reading": ["もつ"], "meaning": "Hold; Have", "kana_pieces": ["も", "つ"]},
        "諦める": {"reading": ["あきらめる"], "meaning": "Give up", "kana_pieces": ["あきら", "め", "る"]},
        "困る": {"reading": ["こまる"], "meaning": "Be in need; In trouble", "kana_pieces": ["こま", "る"]},
        "考える": {"reading": ["かんがえる"], "meaning": "Think; Consider", "kana_pieces": ["かんが", "え", "る"]},
        "壊す": {"reading": ["こわす"], "meaning": "Break", "kana_pieces": ["こわ", "す"]},
        "オイオイ泣く": {"reading": ["オイオイなく; おいおいなく"], "meaning": "Cry one's heart out", "kana_pieces": ["オ", "イ", "オ", "イ", "な", "く"]},
        "笑う": {"reading": ["わらう"], "meaning": "Laugh", "kana_pieces": ["わら", "う"]},
        "働く": {"reading": ["はたらく"], "meaning": "Work", "kana_pieces": ["はたら", "く"]},
        "バイオリンを弾く": {"reading": ["バイオリンをひく; ばいおりんをひく"], "meaning": "Play a violin", "kana_pieces": ["バ", "イ", "オ", "リ", "ン", "を", "ひ", "く"]},
        "答える": {"reading": ["こたえる"], "meaning": "Answer", "kana_pieces": ["こた", "え", "る"]},
        "始まる": {"reading": ["はじまる"], "meaning": "(It) starts; begins", "kana_pieces": ["はじ", "ま", "る"]},
        "探す": {"reading": ["さがす"], "meaning": "Look for; Search", "kana_pieces": ["さが", "す"]},
        "点く": {"reading": ["つく"], "meaning": "(Lights) turn on", "kana_pieces": ["つ", "く"]},
        #Adjectives
        "シャイ": {"reading": ["シャイ"], "meaning": "Shy"},
        "悪戯": {"reading": ["いたずら"], "meaning": "Mischievous", "kana_pieces": ["いた", "ずら"]},
        "得意": {"reading": ["とくい"], "meaning": "Good at", "kana_pieces": ["とく", "い"]},
        "悪い": {"reading": ["わるい"], "meaning": "Bad", "kana_pieces": ["わる", "い"]},
        "悲しい": {"reading": ["かなしい"], "meaning": "Sad", "kana_pieces": ["かな", "し", "い"]},
        "正しい": {"reading": ["ただしい"], "meaning": "Correct", "kana_pieces": ["ただ", "し", "い"]},
        "自分で": {"reading": ["じぶんで"], "meaning": "By oneself", "kana_pieces": ["じ", "ぶん", "で"]},
        "一生懸命": {"reading": ["いっしょうけんめい"], "meaning": "Very hard", "kana_pieces": ["いっ", "しょう", "けん", "めい"]},
        #Conjunctions
        "然し": {"reading": ["しかし"], "meaning": "However; But", "kana_pieces": ["しか", "し"]},
        #Expressions
        "夢を持つこと": {"reading": ["ゆめをもつこと"], "meaning": "Having one's dreams", "kana_pieces": ["ゆめ", "を", "も", "つ", "こ", "と"]},
        "諦めないこと": {"reading": ["あきらめないこと"], "meaning": "Not giving up", "kana_pieces": ["あきら", "め", "な", "い", "こ", "と"]},
        "ある山": {"reading": ["あるやま"], "meaning": "A certain mountain", "kana_pieces": ["あ", "る", "やま"]},
        "お腹がペコペコです": {"reading": ["おなかがペコペコです; おなかがぺこぺこです"], "meaning": "I'm starving", "kana_pieces": ["お", "なか", "が", "ペ", "コ", "ペ", "コ", "で", "す"]},
        #Kanji terms
        "教える": {"reading": ["おしえる"], "meaning": "To teach; To tell", "kana_pieces": ["おし", "え", "る"]},
        "仕事": {"reading": ["しごと"], "meaning": "Job; Occupation", "kana_pieces": ["し", "ごと"]},
        "火事": {"reading": ["かじ"], "meaning": "Fire", "kana_pieces": ["か", "じ"]},
        "事故": {"reading": ["じこ"], "meaning": "Accident", "kana_pieces": ["じ", "こ"]},
        "作る": {"reading": ["つくる"], "meaning": "To make", "kana_pieces": ["つく", "る"]},
        "作り方": {"reading": ["つくりかた"], "meaning": "How to make", "kana_pieces": ["つく", "り", "かた"]},
        "家族": {"reading": ["かぞく"], "meaning": "Family", "kana_pieces": ["か", "ぞく"]},
        "使う": {"reading": ["つかう"], "meaning": "To use", "kana_pieces": ["つか", "う"]},
        "大使館": {"reading": ["たいしかん"], "meaning": "Embassy", "kana_pieces": ["たい", "し", "かん"]},
        "心配する": {"reading": ["しんぱいする"], "meaning": "To worry", "kana_pieces": ["しん", "ぱい", "す", "る"]},
        "中心": {"reading": ["ちゅうしん"], "meaning": "Center", "kana_pieces": ["ちゅう", "しん"]},
        "安心する": {"reading": ["あんしんする"], "meaning": "To be relieved", "kana_pieces": ["あん", "しん", "す", "る"]},
        "食べ方": {"reading": ["たべかた"], "meaning": "How to eat", "kana_pieces": ["た", "べ", "かた"]},
        "言い方": {"reading": ["いいかた"], "meaning": "How to say", "kana_pieces": ["い", "い", "かた"]},
        "手": {"reading": ["て"], "meaning": "Hand", "kana_pieces": ["て"]},
        "手伝う": {"reading": ["てつだう"], "meaning": "To help", "kana_pieces": ["て", "つだ", "う"]},
        "上手": {"reading": ["じょうず"], "meaning": "Good at", "kana_pieces": ["じょう", "ず"]},
        "持ってくる": {"reading": ["もってくる"], "meaning": "To bring", "kana_pieces": ["も", "っ", "て", "く", "る"]},
        "気持ち": {"reading": ["きもち"], "meaning": "Feeling", "kana_pieces": ["き", "も", "ち"]},
        "お金持ち": {"reading": ["おかねもち"], "meaning": "Rich person", "kana_pieces": ["お", "かね", "もち"]},
        "山": {"reading": ["やま"], "meaning": "Mountain", "kana_pieces": ["やま"]},
        "富士山": {"reading": ["ふじさん"], "meaning": "Mt. Fuji", "kana_pieces": ["ふ", "じ", "さん"]},
        "明るい": {"reading": ["あかるい"], "meaning": "Bright; Cheerful", "kana_pieces": ["あか", "る", "い"]},
        "明日": {"reading": ["あした"], "meaning": "Tomorrow", "kana_pieces": ["あ", "した"]},
        "発明する": {"reading": ["はつめいする"], "meaning": "To invent", "kana_pieces": ["はつ", "めい", "す", "る"]},
        "明治時代": {"reading": ["めいじじだい"], "meaning": "Meiji Era", "kana_pieces": ["めい", "じ", "じ", "だい"]},
    },
    "vocab": [
        "小学校",
        "幼稚園",
        "〜年間",
        "中学校",
        "高校",
        "教育",
        "義務教育",
        "試験",
        "外",
        "家事",
        "ピアノ",
        "夜遅く",
        "漫画",
        "インターネット",
        "先輩",
        "勇気",
        "情熱",
        "心",
        "授業",
        "夢",
        "外国",
        "宿題",
        "心の優しい人",
        "鬼",
        "赤鬼",
        "青鬼",
        "人生",
        "村",
        "人間",
        "看板",
        "アイデア",
        "手紙",
        "遠く",
        "話",
        "問題",
        "家",
        "ギリギリス",
        "食べ物",
        "飲み物",
        "アリ",
        "明かり",
        "降りる",
        "着く",
        "出る",
        "決める",
        "習う",
        "世話をする",
        "ペットを飼う",
        "泊まる",
        "呉れる",
        "奢る",
        "連れて行く",
        "おしゃれをする",
        "サボる",
        "持つ",
        "諦める",
        "困る",
        "考える",
        "壊す",
        "オイオイ泣く",
        "笑う",
        "働く",
        "バイオリンを弾く",
        "答える",
        "始まる",
        "探す",
        "点く",
        "シャイ",
        "悪戯",
        "得意",
        "悪い",
        "悲しい",
        "正しい",
        "自分で",
        "一生懸命",
        "然し",
        "夢を持つこと",
        "諦めないこと",
        "ある山",
        "お腹がペコペコです",
    ],
    "kanji": ["教", "事", "作", "仕", "家", "使"],
}

dd_unit_2 = {
    "allowed_kanji": set(ALL_ND2_KANJI + DD_KANJI_BY_UNIT["1"] + DD_KANJI_BY_UNIT["2"]),
    "entries": {
        "ENTRY_01": {"reading": [""], "meaning": ""},
        "ENTRY_02": {"reading": [""], "meaning": ""},
        "ENTRY_03": {"reading": [""], "meaning": ""},
        "ENTRY_04": {"reading": [""], "meaning": ""},
        "ENTRY_05": {"reading": [""], "meaning": ""},
        "ENTRY_06": {"reading": [""], "meaning": ""},
        "ENTRY_07": {"reading": [""], "meaning": ""},
        "ENTRY_08": {"reading": [""], "meaning": ""},
        "ENTRY_09": {"reading": [""], "meaning": ""},
        "ENTRY_10": {"reading": [""], "meaning": ""},
        "ENTRY_11": {"reading": [""], "meaning": ""},
        "ENTRY_12": {"reading": [""], "meaning": ""},
        "ENTRY_13": {"reading": [""], "meaning": ""},
        "ENTRY_14": {"reading": [""], "meaning": ""},
        "ENTRY_15": {"reading": [""], "meaning": ""},
        "ENTRY_16": {"reading": [""], "meaning": ""},
        "ENTRY_17": {"reading": [""], "meaning": ""},
        "ENTRY_18": {"reading": [""], "meaning": ""},
        "ENTRY_19": {"reading": [""], "meaning": ""},
        "ENTRY_20": {"reading": [""], "meaning": ""},
    },
    "vocab": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    "kanji": ["", "", "", "", "", ""],
}

dd_unit_3 = {
    "allowed_kanji": set(ALL_ND2_KANJI + DD_KANJI_BY_UNIT["1"] + DD_KANJI_BY_UNIT["2"] + DD_KANJI_BY_UNIT["3"]),
    "entries": {
        "ENTRY_01": {"reading": [""], "meaning": ""},
        "ENTRY_02": {"reading": [""], "meaning": ""},
        "ENTRY_03": {"reading": [""], "meaning": ""},
        "ENTRY_04": {"reading": [""], "meaning": ""},
        "ENTRY_05": {"reading": [""], "meaning": ""},
        "ENTRY_06": {"reading": [""], "meaning": ""},
        "ENTRY_07": {"reading": [""], "meaning": ""},
        "ENTRY_08": {"reading": [""], "meaning": ""},
        "ENTRY_09": {"reading": [""], "meaning": ""},
        "ENTRY_10": {"reading": [""], "meaning": ""},
        "ENTRY_11": {"reading": [""], "meaning": ""},
        "ENTRY_12": {"reading": [""], "meaning": ""},
        "ENTRY_13": {"reading": [""], "meaning": ""},
        "ENTRY_14": {"reading": [""], "meaning": ""},
        "ENTRY_15": {"reading": [""], "meaning": ""},
        "ENTRY_16": {"reading": [""], "meaning": ""},
        "ENTRY_17": {"reading": [""], "meaning": ""},
        "ENTRY_18": {"reading": [""], "meaning": ""},
        "ENTRY_19": {"reading": [""], "meaning": ""},
        "ENTRY_20": {"reading": [""], "meaning": ""},
    },
    "vocab": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    "kanji": ["", "", "", "", "", ""],
}

dd_unit_4 = {
    "allowed_kanji": set(ALL_ND2_KANJI + DD_KANJI_BY_UNIT["1"] + DD_KANJI_BY_UNIT["2"] + DD_KANJI_BY_UNIT["3"] + DD_KANJI_BY_UNIT["4"]),
    "entries": {
        "ENTRY_01": {"reading": [""], "meaning": ""},
        "ENTRY_02": {"reading": [""], "meaning": ""},
        "ENTRY_03": {"reading": [""], "meaning": ""},
        "ENTRY_04": {"reading": [""], "meaning": ""},
        "ENTRY_05": {"reading": [""], "meaning": ""},
        "ENTRY_06": {"reading": [""], "meaning": ""},
        "ENTRY_07": {"reading": [""], "meaning": ""},
        "ENTRY_08": {"reading": [""], "meaning": ""},
        "ENTRY_09": {"reading": [""], "meaning": ""},
        "ENTRY_10": {"reading": [""], "meaning": ""},
        "ENTRY_11": {"reading": [""], "meaning": ""},
        "ENTRY_12": {"reading": [""], "meaning": ""},
        "ENTRY_13": {"reading": [""], "meaning": ""},
        "ENTRY_14": {"reading": [""], "meaning": ""},
        "ENTRY_15": {"reading": [""], "meaning": ""},
        "ENTRY_16": {"reading": [""], "meaning": ""},
        "ENTRY_17": {"reading": [""], "meaning": ""},
        "ENTRY_18": {"reading": [""], "meaning": ""},
        "ENTRY_19": {"reading": [""], "meaning": ""},
        "ENTRY_20": {"reading": [""], "meaning": ""},
    },
    "vocab": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    "kanji": ["", "", "", "", "", ""],
}

dd_unit_5 = {
    "allowed_kanji": set(ALL_ND2_KANJI + [k for chars in DD_KANJI_BY_UNIT.values() for k in chars]),
    "entries": {
        "ENTRY_01": {"reading": [""], "meaning": ""},
        "ENTRY_02": {"reading": [""], "meaning": ""},
        "ENTRY_03": {"reading": [""], "meaning": ""},
        "ENTRY_04": {"reading": [""], "meaning": ""},
        "ENTRY_05": {"reading": [""], "meaning": ""},
        "ENTRY_06": {"reading": [""], "meaning": ""},
        "ENTRY_07": {"reading": [""], "meaning": ""},
        "ENTRY_08": {"reading": [""], "meaning": ""},
        "ENTRY_09": {"reading": [""], "meaning": ""},
        "ENTRY_10": {"reading": [""], "meaning": ""},
        "ENTRY_11": {"reading": [""], "meaning": ""},
        "ENTRY_12": {"reading": [""], "meaning": ""},
        "ENTRY_13": {"reading": [""], "meaning": ""},
        "ENTRY_14": {"reading": [""], "meaning": ""},
        "ENTRY_15": {"reading": [""], "meaning": ""},
        "ENTRY_16": {"reading": [""], "meaning": ""},
        "ENTRY_17": {"reading": [""], "meaning": ""},
        "ENTRY_18": {"reading": [""], "meaning": ""},
        "ENTRY_19": {"reading": [""], "meaning": ""},
        "ENTRY_20": {"reading": [""], "meaning": ""},
    },
    "vocab": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    "kanji": ["", "", "", "", "", ""],
}

index = {
    "allowed_kanji": set(ALL_ND2_KANJI + [k for chars in DD_KANJI_BY_UNIT.values() for k in chars]),
    "entries": {
        "ENTRY_01": {"reading": [""], "meaning": ""},
        "ENTRY_02": {"reading": [""], "meaning": ""},
        "ENTRY_03": {"reading": [""], "meaning": ""},
        "ENTRY_04": {"reading": [""], "meaning": ""},
        "ENTRY_05": {"reading": [""], "meaning": ""},
        "ENTRY_06": {"reading": [""], "meaning": ""},
        "ENTRY_07": {"reading": [""], "meaning": ""},
        "ENTRY_08": {"reading": [""], "meaning": ""},
        "ENTRY_09": {"reading": [""], "meaning": ""},
        "ENTRY_10": {"reading": [""], "meaning": ""},
        "ENTRY_11": {"reading": [""], "meaning": ""},
        "ENTRY_12": {"reading": [""], "meaning": ""},
        "ENTRY_13": {"reading": [""], "meaning": ""},
        "ENTRY_14": {"reading": [""], "meaning": ""},
        "ENTRY_15": {"reading": [""], "meaning": ""},
        "ENTRY_16": {"reading": [""], "meaning": ""},
        "ENTRY_17": {"reading": [""], "meaning": ""},
        "ENTRY_18": {"reading": [""], "meaning": ""},
        "ENTRY_19": {"reading": [""], "meaning": ""},
        "ENTRY_20": {"reading": [""], "meaning": ""},
    },
    "vocab": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    "kanji": ["", "", "", "", "", ""],
}

STUDY_UNITS = {
    "JLPT N5": jlpt_n5,
    "JLPT N4": jlpt_n4,
    "JLPT N3": jlpt_n3,
    "JLPT N2": jlpt_n2,
    "JLPT N1": jlpt_n1,
    "ND はじめに": nd_hajimeni,
    "ND Unit 13": nd_unit_13,
    "DD Unit 1": dd_unit_1,
    "DD Unit 2": dd_unit_2,
    "DD Unit 3": dd_unit_3,
    "DD Unit 4": dd_unit_4,
    "DD Unit 5": dd_unit_5,
    "Index": index,
}

# Ascending order of JLPT levels (N5 lowest -> N1 highest)
JLPT_HIERARCHY = [
    "JLPT N5",
    "JLPT N4",
    "JLPT N3",
    "JLPT N2",
    "JLPT N1",
]

# Ascending order of ND / DD levels (ND はじめに lowest -> DD Unit 5 highest)
ND_DD_HIERARCHY = [
    "ND はじめに",
    "ND Unit 13",
    "ND Unit 14",
    "ND Unit 15",
    "ND Unit 16",
    "ND Unit 17",
    "ND Unit 18",
    "ND Unit 19",
    "ND Unit 20",
    "ND Unit 21",
    "ND Unit 22",
    "ND Unit 23",
    "ND Unit 24",
    "DD Unit 1",
    "DD Unit 2",
    "DD Unit 3",
    "DD Unit 4",
    "DD Unit 5",
]

# really shouldn't need to touch this, just establishes what's vocab and what's kanji
STUDY_CATEGORIES = {
    "Vocabulary": {
        name: unit
        for name, unit in STUDY_UNITS.items()
        if unit["vocab"]
    },
    "Kanji": {
        name: unit
        for name, unit in STUDY_UNITS.items()
        if unit["kanji"]
    },
}

#boring stuff i honestly don't super understand; makes the thing do the thing
if "stage" not in st.session_state:
    st.session_state.stage = "setup"

def is_kanji_char(ch):
    code = ord(ch)
    return (0x4E00 <= code <= 0x9FFF) or (0x3400 <= code <= 0x4DBF)

def split_answers(text):
    return [
        part.strip()
        for part in text.replace(",", ";").split(";")
        if part.strip()
    ]

def _extract_kana_reading(entry):
    readings = [
        ans
        for r in entry.get("reading", [])
        for ans in split_answers(r)
    ]
    for ans in readings:
        if not any(is_kanji_char(ch) for ch in ans):
            return ans
    return readings[0] if readings else ""

def _align_mixed_kana(written, kana, allowed_kanji):
    """
    Best-effort alignment for mixed kanji/kana words when 'kana_pieces' isn't specified.
    Keeps kanji in `allowed_kanji` and converts unlearned kanji spans to kana if unambiguous;
    otherwise returns None so the caller can fall back cleanly.
    """
    kanji_positions = [i for i, ch in enumerate(written) if is_kanji_char(ch)]
    if not kanji_positions:
        return kana

    first_k = kanji_positions[0]
    last_k = kanji_positions[-1]
    prefix = written[:first_k]
    suffix = written[last_k + 1:]
    core = written[first_k:last_k + 1]

    if prefix and not kana.startswith(prefix):
        return None
    if suffix and not kana.endswith(suffix):
        return None

    kana_start = len(prefix)
    kana_end = len(kana) - len(suffix) if suffix else len(kana)
    if kana_end < kana_start:
        return None
    core_kana = kana[kana_start:kana_end]

    if len(core) == 1:
        k = core[0]
        if k in allowed_kanji:
            return f"{prefix}{k}{suffix}"
        return f"{prefix}{core_kana}{suffix}"

    core_kanji = [ch for ch in core if is_kanji_char(ch)]
    if all(ch in allowed_kanji for ch in core_kanji):
        return f"{prefix}{core}{suffix}"
    if all(ch not in allowed_kanji for ch in core_kanji):
        return f"{prefix}{core_kana}{suffix}"

    return None

def render_progress_term(written, entry, allowed_kanji):
    word_kanji = [ch for ch in written if is_kanji_char(ch)]
    if not word_kanji:
        return written
    if all(ch in allowed_kanji for ch in word_kanji):
        return written

    kana = _extract_kana_reading(entry)
    if not any(ch in allowed_kanji for ch in word_kanji):
        return kana or written

    kana_pieces = entry.get("kana_pieces")
    if kana_pieces and len(kana_pieces) == len(written):
        out = []
        for ch, piece in zip(written, kana_pieces):
            if is_kanji_char(ch):
                out.append(ch if ch in allowed_kanji else piece)
            else:
                out.append(ch)
        return "".join(out)

    aligned = _align_mixed_kana(written, kana, allowed_kanji) if kana else None
    return aligned if aligned is not None else (kana or written)

def build_vocabulary_deck(entries, entry_keys, direction, kanji_mode="All Kanji", allowed_kanji=None):
    deck = {}
    use_progress = (kanji_mode == "Progress-based") and (allowed_kanji is not None)

    if direction == "ENG to JPN":
        for written in entry_keys:
            entry = entries[written]
            readings = [
                answer
                for reading in entry["reading"]
                for answer in split_answers(reading)
            ]
            if use_progress:
                display_form = render_progress_term(written, entry, allowed_kanji)
                accepted = readings + [display_form, written]
            else:
                accepted = readings + [written]
            deck[entry["meaning"]] = list(dict.fromkeys(accepted))
    else:
        for written in entry_keys:
            entry = entries[written]
            prompt_text = (
                render_progress_term(written, entry, allowed_kanji)
                if use_progress
                else written
            )
            meanings = [part.lower() for part in split_answers(entry["meaning"])]
            deck[prompt_text] = list(dict.fromkeys(meanings))
    return deck

def get_kanji_source_entries(selected_unit_names, all_units, pull_from_eligible=False):
    """
    Collects source entry dicts for kanji quiz generation.
    - When `pull_from_eligible` is False: only uses entries from `selected_unit_names`.
    - When `pull_from_eligible` is True:
      * JLPT units draw from themselves + strictly lower JLPT levels (never higher JLPT levels),
        plus any ND/DD unit where at least one of the JLPT unit's focus kanji appears in that unit's "kanji" list.
      * ND/DD units draw from themselves + ND/DD units at or below them in `ND_DD_HIERARCHY`
        (never higher ND/DD levels), plus any JLPT unit where at least one of the ND/DD unit's focus kanji
        appears in that JLPT unit's "kanji" list.
    """
    combined_entries = {}
    if not pull_from_eligible:
        for unit_name in selected_unit_names:
            unit = all_units.get(unit_name)
            if unit:
                combined_entries.update(unit.get("entries", {}))
        return combined_entries

    for unit_name in selected_unit_names:
        unit = all_units.get(unit_name)
        if not unit:
            continue

        combined_entries.update(unit.get("entries", {}))
        unit_focus_set = {k for k in unit.get("kanji", []) if k}

        if unit_name in JLPT_HIERARCHY:
            rank = JLPT_HIERARCHY.index(unit_name)
            # Lower JLPT units only (strictly below rank)
            for lower_name in JLPT_HIERARCHY[:rank]:
                lower_unit = all_units.get(lower_name)
                if lower_unit:
                    combined_entries.update(lower_unit.get("entries", {}))
            # Any ND/DD unit where this JLPT unit's focus kanji is listed in "kanji"
            if unit_focus_set:
                for candidate_name, candidate_unit in all_units.items():
                    if candidate_name in ND_DD_HIERARCHY:
                        cand_focus = {k for k in candidate_unit.get("kanji", []) if k}
                        if cand_focus & unit_focus_set:
                            combined_entries.update(candidate_unit.get("entries", {}))

        elif unit_name in ND_DD_HIERARCHY:
            rank = ND_DD_HIERARCHY.index(unit_name)
            # ND/DD units at or below rank only (never above rank)
            for eligible_name in ND_DD_HIERARCHY[: rank + 1]:
                eligible_unit = all_units.get(eligible_name)
                if eligible_unit:
                    combined_entries.update(eligible_unit.get("entries", {}))
            # Any JLPT unit where this ND/DD unit's focus kanji is listed in "kanji"
            if unit_focus_set:
                for candidate_name, candidate_unit in all_units.items():
                    if candidate_name in JLPT_HIERARCHY:
                        cand_focus = {k for k in candidate_unit.get("kanji", []) if k}
                        if cand_focus & unit_focus_set:
                            combined_entries.update(candidate_unit.get("entries", {}))

    return combined_entries

def build_kanji_deck(entries, focus_kanji, mode):
    deck = {}
    for written, entry in entries.items():
        if not any(kanji in written for kanji in focus_kanji):
            continue
        if mode == "Reading":
            accepted = [
                answer
                for reading in entry["reading"]
                for answer in split_answers(reading)
            ]
        else:
            accepted = [part.lower() for part in split_answers(entry["meaning"])]
        deck[written] = list(dict.fromkeys(accepted))
    return deck

def start_quiz(deck_dict, direction):
    prompts = list(deck_dict.keys())
    random.shuffle(prompts)
    st.session_state.deck = deck_dict
    st.session_state.direction = direction
    st.session_state.prompts = prompts
    st.session_state.total_count = len(prompts)
    st.session_state.current = st.session_state.prompts.pop()
    st.session_state.attempts = 0
    st.session_state.feedback = None
    st.session_state.feedback_type = None
    st.session_state.waiting_next = False
    st.session_state.completed_all = True
    st.session_state.stage = "quiz"

def next_word():
    if st.session_state.prompts:
        st.session_state.current = st.session_state.prompts.pop()
        st.session_state.attempts = 0
        st.session_state.feedback = None
        st.session_state.feedback_type = None
        st.session_state.waiting_next = False
    else:
        st.session_state.stage = "finished"

# SETUP SCREEN
if st.session_state.stage == "setup":
    st.title("Flashcard Study App")

    category = st.radio(
        "What would you like to study?",
        list(STUDY_CATEGORIES.keys()),
        horizontal=True
    )

    pull_from_eligible = False

    if category == "Kanji":
        kanji_mode = st.radio(
            "Kanji mode:",
            ["Reading", "Meaning"],
            horizontal=True
        )
        direction = f"Kanji {kanji_mode}"
        vocab_kanji_mode = "All Kanji"
        kanji_pool_mode = st.radio(
            "Kanji term pool:",
            ["Only selected unit(s)", "Pull from eligible units"],
            horizontal=True,
        )
        pull_from_eligible = (kanji_pool_mode == "Pull from eligible units")
    else:
        direction = st.radio(
            "Direction:",
            ["ENG to JPN", "JPN to ENG"],
            horizontal=True
        )
        vocab_kanji_mode = st.radio(
            "Vocabulary kanji:",
            ["Progress-based", "All Kanji"],
            horizontal=True
        )

    available_sets = STUDY_CATEGORIES[category]
    study_all = st.checkbox("Study all units")

    if study_all:
        selected_sets = list(available_sets.keys())
    else:
        selected_sets = st.multiselect(
            "Choose units to study:",
            options=list(available_sets.keys()),
            default=list(available_sets.keys())[:1]
        )

    with st.expander("Btw"):
        st.write("- The correct answer will be shown after three incorrect guesses.")
        st.write("- Use the exact spelling/phrasing used in the book; capitalization doesn't matter, but if there is a ~, 〜, parentheses, or other grammar element, it should be included. SPACES MATTER. If two meanings are separated by a comma, both are correct; you do not need to enter both.")
        st.write("- Do not include the (な) in な-adjectives.")
        st.write("- Vocabulary kanji: 'Progress-based' keeps learned kanji and renders unlearned kanji as kana; 'All Kanji' shows full kanji spellings.")
        st.write("- Kanji term pool: 'Only selected unit(s)' uses entries from the chosen unit(s); 'Pull from eligible units' draws from lower JLPT levels (never higher) for JLPT units, at-or-below ND/DD levels (from ND はじめに up to DD Unit 5, never higher) for ND/DD units, and cross-pulls between JLPT and ND/DD units when a focus kanji matches.")
        st.write("- Kanji Reading shows a kanji word and expects the full kana spelling, INCLUDING any hiragana/katakana in the word. E.g., answer「夏休み」 with 「なつやすみ」.")
        st.write("- If you have any problems or ideas for things I could add, message me on LINE or something and I'll see what I can do.")

    if st.button("Start", type="primary", use_container_width=True):
        if not selected_sets:
            st.error("Invalid selection. Please select at least one unit.")
        elif category == "Kanji":
            focus_kanji = []
            for unit_name in selected_sets:
                unit = available_sets[unit_name]
                focus_kanji.extend(unit["kanji"])

            focus_kanji = [k for k in dict.fromkeys(focus_kanji) if k]
            combined_entries = get_kanji_source_entries(
                selected_sets,
                STUDY_UNITS,
                pull_from_eligible=pull_from_eligible,
            )

            if not focus_kanji:
                st.error("The selected units don't have any focus kanji.")
            else:
                matching_words = [
                    written for written in combined_entries
                    if any(kanji in written for kanji in focus_kanji)
                ]
                missing_readings = [
                    written for written in matching_words
                    if not combined_entries[written]["reading"]
                ]
                missing_meanings = [
                    written for written in matching_words
                    if not combined_entries[written]["meaning"].strip()
                ]

                if not matching_words:
                    st.error("No entries in the eligible units contain their focus kanji.")
                elif kanji_mode == "Reading" and missing_readings:
                    st.error(f"Add a reading for: {', '.join(missing_readings)}.")
                elif kanji_mode == "Meaning" and missing_meanings:
                    st.error(f"Add a meaning for: {', '.join(missing_meanings)}.")
                else:
                    deck = build_kanji_deck(combined_entries, focus_kanji, kanji_mode)
                    start_quiz(deck, direction)
                    st.rerun()
        else:
            combined_entries = {}
            entry_keys = []
            combined_allowed_kanji = set()
            for unit_name in selected_sets:
                unit = available_sets[unit_name]
                combined_entries.update(unit["entries"])
                entry_keys.extend(unit["vocab"])
                combined_allowed_kanji.update(unit.get("allowed_kanji", set()))

            entry_keys = list(dict.fromkeys(entry_keys))
            missing_entries = [
                written for written in entry_keys
                if written not in combined_entries
            ]
            if missing_entries:
                st.error(f"Vocabulary lists refer to missing entries: {', '.join(missing_entries)}.")
            elif not entry_keys:
                st.error("The selected units don't contain any vocabulary.")
            else:
                deck = build_vocabulary_deck(
                    combined_entries,
                    entry_keys,
                    direction,
                    kanji_mode=vocab_kanji_mode,
                    allowed_kanji=combined_allowed_kanji,
                )
                start_quiz(deck, direction)
                st.rerun()

elif st.session_state.stage == "quiz":
    current = st.session_state.current
    correct_answers = st.session_state.deck[current]
    words_done = st.session_state.total_count - len(st.session_state.prompts)
    is_jpn_to_eng = st.session_state.direction in ("JPN to ENG", "Kanji Meaning")
    is_kanji_mode = st.session_state.direction in ("Kanji Reading", "Kanji Meaning")

    st.progress(words_done / st.session_state.total_count)
    st.caption(f"{words_done}/{st.session_state.total_count} | Attempt {st.session_state.attempts + 1}/3")

    display_prompt = current if is_jpn_to_eng or is_kanji_mode else current.capitalize()
    st.subheader(f"{st.session_state.direction}: {display_prompt}")

    if not st.session_state.waiting_next:
        with st.form(key=f"form_{words_done}_{st.session_state.attempts}", clear_on_submit=True):
            guess = st.text_input("Your answer:", key=f"input_{words_done}_{st.session_state.attempts}").strip()
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Submit", type="primary", use_container_width=True)
            with col2:
                quit_early = st.form_submit_button("End session", use_container_width=True)

        if quit_early or (submitted and (guess.lower() == "done" or guess == "どね")):
            st.session_state.completed_all = False
            st.session_state.stage = "finished"
            st.rerun()

        if submitted and guess:
            cleaned_guess = guess.lower() if is_jpn_to_eng else guess
            if cleaned_guess in correct_answers:
                st.session_state.feedback = f"Correct. Answer was: {' / '.join(correct_answers)}"
                st.session_state.feedback_type = "success"
                st.session_state.waiting_next = True
                st.rerun()
            else:
                st.session_state.attempts += 1
                if st.session_state.attempts >= 3:
                    st.session_state.feedback = f"Incorrect. Correct answer was: {' / '.join(correct_answers)}"
                    st.session_state.feedback_type = "error"
                    st.session_state.waiting_next = True
                    st.rerun()
                else:
                    st.session_state.feedback = "Incorrect."
                    st.session_state.feedback_type = "warning"
                    st.rerun()

        if st.session_state.feedback_type == "warning":
            st.warning(st.session_state.feedback)

    else:
        if st.session_state.feedback_type == "success":
            st.success(st.session_state.feedback)
        elif st.session_state.feedback_type == "error":
            st.error(st.session_state.feedback)

        st.caption("Press Enter to continue, or click Next.")
        if st.button("Next", type="primary", use_container_width=True):
            next_word()
            st.rerun()

        components.html(
            """
            <script>
            const parentWindow = window.parent;
            const parentDocument = parentWindow.document;

            if (!parentWindow.__flashcardEnterNextHandlerInstalled) {
                parentDocument.addEventListener("keydown", (event) => {
                    if (event.key !== "Enter" || event.repeat) return;

                    const nextButton = Array.from(
                        parentDocument.querySelectorAll("button")
                    ).find((button) => button.innerText.trim() === "Next");

                    if (!nextButton) return;

                    event.preventDefault();
                    event.stopImmediatePropagation();
                    nextButton.click();
                }, true);
                parentWindow.__flashcardEnterNextHandlerInstalled = true;
            }
            </script>
            """,
            height=0
        )

elif st.session_state.stage == "finished":
    st.title("Session complete")
    if st.session_state.completed_all:
        st.success("All cards studied. Nice work!")
    else:
        st.info("Session ended early.")

    if st.button("Study again", type="primary", use_container_width=True):
        st.session_state.stage = "setup"
        st.rerun()
