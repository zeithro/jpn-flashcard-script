import streamlit as st
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

KANJI_UNIT_SETS = {
    **{f"ND2: {unit}": set(chars) for unit, chars in ND2_KANJI_BY_UNIT.items()},
    **{f"DD: {unit}": set(chars) for unit, chars in DD_KANJI_BY_UNIT.items()},
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
    "DD Unit 1": dd_unit_1,
    "DD Unit 2": dd_unit_2,
    "DD Unit 3": dd_unit_3,
    "DD Unit 4": dd_unit_4,
    "DD Unit 5": dd_unit_5,
    "ND Unit 13": nd_unit_13,
    "Index": index,
}

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
    use_filtered_kanji = (kanji_mode in ("Progress-based", "Custom")) and (allowed_kanji is not None)

    if direction == "ENG to JPN":
        for written in entry_keys:
            entry = entries[written]
            readings = [
                answer
                for reading in entry["reading"]
                for answer in split_answers(reading)
            ]
            if use_filtered_kanji:
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
                if use_filtered_kanji
                else written
            )
            meanings = [part.lower() for part in split_answers(entry["meaning"])]
            deck[prompt_text] = list(dict.fromkeys(meanings))
    return deck

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

    custom_allowed_kanji = None

    if category == "Kanji":
        kanji_mode = st.radio(
            "Kanji mode:",
            ["Reading", "Meaning"],
            horizontal=True
        )
        direction = f"Kanji {kanji_mode}"
        vocab_kanji_mode = "All Kanji"
    else:
        direction = st.radio(
            "Direction:",
            ["ENG to JPN", "JPN to ENG"],
            horizontal=True
        )
        vocab_kanji_mode = st.radio(
            "Vocabulary kanji:",
            ["Progress-based", "All Kanji", "Custom"],
            horizontal=True
        )

        if vocab_kanji_mode == "Custom":
            all_kanji_unit_labels = list(KANJI_UNIT_SETS.keys())

            if "custom_kanji_units" not in st.session_state:
                st.session_state.custom_kanji_units = [
                    "ND2: はじめに",
                    "ND2: 13"
                ]

            preset_col1, preset_col2, preset_col3 = st.columns([2, 1, 1])

            with preset_col1:
                preset_cutoff = st.selectbox(
                    "Quick preset (select all through unit):",
                    options=all_kanji_unit_labels,
                    index=(
                        all_kanji_unit_labels.index("ND2: 20")
                        if "ND2: 20" in all_kanji_unit_labels
                        else 0
                    ),
                    label_visibility="collapsed",
                )

            with preset_col2:
                if st.button("Select up to unit", use_container_width=True):
                    cutoff_idx = all_kanji_unit_labels.index(preset_cutoff)
                    st.session_state.custom_kanji_units = (
                        all_kanji_unit_labels[:cutoff_idx + 1]
                    )
                    st.rerun()

            with preset_col3:
                if st.button("Clear all", use_container_width=True):
                    st.session_state.custom_kanji_units = []
                    st.rerun()

            selected_kanji_units = st.multiselect(
                "Select kanji units to allow (kanji from chosen units will be kept; others become kana):",
                options=all_kanji_unit_labels,
                key="custom_kanji_units",
            )

            extra_kanji_raw = st.text_input(
                "Optional extra allowed kanji (type characters directly):",
                value="",
                placeholder="e.g., 困思",
            )

            extra_kanji = {
                ch for ch in extra_kanji_raw if is_kanji_char(ch)
            }

            custom_allowed_kanji = set().union(
                *(KANJI_UNIT_SETS[u] for u in selected_kanji_units),
                extra_kanji,
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
        st.write("- Vocabulary kanji: 'Progress-based' uses each unit's allowed kanji; 'All Kanji' shows full kanji spellings; 'Custom' lets you pick any combination of kanji units (plus optional extra characters) while substituting unchosen kanji with kana.")
        st.write("- Kanji Reading shows a kanji word and expects the full kana spelling, INCLUDING any hiragana/katakana in the word. E.g., answer「夏休み」 with 「なつやすみ」.")
        st.write("- If you have any problems or ideas for things I could add, message me on LINE or something and I'll see what I can do.")

    if st.button("Start", type="primary", use_container_width=True):
        if not selected_sets:
            st.error("Invalid selection. Please select at least one unit.")

        elif category == "Kanji":
            combined_entries = {}
            focus_kanji = []

            for unit_name in selected_sets:
                unit = available_sets[unit_name]
                combined_entries.update(unit["entries"])
                focus_kanji.extend(unit["kanji"])

            focus_kanji = list(dict.fromkeys(focus_kanji))

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
                    st.error("No entries in the selected units contain their focus kanji.")

                elif kanji_mode == "Reading" and missing_readings:
                    st.error(f"Add a reading for: {', '.join(missing_readings)}.")

                elif kanji_mode == "Meaning" and missing_meanings:
                    st.error(f"Add a meaning for: {', '.join(missing_meanings)}.")

                else:
                    deck = build_kanji_deck(
                        combined_entries,
                        focus_kanji,
                        kanji_mode
                    )
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
                combined_allowed_kanji.update(
                    unit.get("allowed_kanji", set())
                )

            entry_keys = list(dict.fromkeys(entry_keys))

            missing_entries = [
                written for written in entry_keys
                if written not in combined_entries
            ]

            if missing_entries:
                st.error(
                    f"Vocabulary lists refer to missing entries: "
                    f"{', '.join(missing_entries)}."
                )

            elif not entry_keys:
                st.error("The selected units don't contain any vocabulary.")

            else:
                active_allowed_kanji = (
                    custom_allowed_kanji
                    if vocab_kanji_mode == "Custom"
                    else combined_allowed_kanji
                )

                deck = build_vocabulary_deck(
                    combined_entries,
                    entry_keys,
                    direction,
                    kanji_mode=vocab_kanji_mode,
                    allowed_kanji=active_allowed_kanji,
                )

                start_quiz(deck, direction)
                st.rerun()


# QUIZ SCREEN
elif st.session_state.stage == "quiz":

    current = st.session_state.current
    correct_answers = st.session_state.deck[current]

    words_done = (
        st.session_state.total_count
        - len(st.session_state.prompts)
    )

    is_jpn_to_eng = st.session_state.direction in (
        "JPN to ENG",
        "Kanji Meaning"
    )

    is_kanji_mode = st.session_state.direction in (
        "Kanji Reading",
        "Kanji Meaning"
    )

    st.progress(words_done / st.session_state.total_count)

    st.caption(
        f"{words_done}/{st.session_state.total_count} | "
        f"Attempt {st.session_state.attempts + 1}/3"
    )

    display_prompt = (
        current
        if is_jpn_to_eng or is_kanji_mode
        else current.capitalize()
    )

    st.subheader(
        f"{st.session_state.direction}: {display_prompt}"
    )

    # ANSWER INPUT
    if not st.session_state.waiting_next:

        with st.form(
            key=f"form_{words_done}_{st.session_state.attempts}",
            clear_on_submit=True
        ):

            guess = st.text_input(
                "Your answer:",
                key=f"input_{words_done}_{st.session_state.attempts}"
            ).strip()

            col1, col2 = st.columns(2)

            with col1:
                submitted = st.form_submit_button(
                    "Submit",
                    type="primary",
                    use_container_width=True
                )

            with col2:
                quit_early = st.form_submit_button(
                    "End session",
                    use_container_width=True
                )

        if quit_early or (
            submitted and (guess.lower() == "done" or guess == "どね")
        ):
            st.session_state.completed_all = False
            st.session_state.stage = "finished"
            st.rerun()

        if submitted and guess:

            cleaned_guess = (
                guess.lower()
                if is_jpn_to_eng
                else guess
            )

            normalized_answers = [
                answer.lower() if is_jpn_to_eng else answer
                for answer in correct_answers
            ]

            if cleaned_guess in normalized_answers:

                st.session_state.feedback = (
                    f"Correct. Answer was: {' / '.join(correct_answers)}"
                )

                st.session_state.feedback_type = "success"
                st.session_state.waiting_next = True
                st.rerun()

            else:

                st.session_state.attempts += 1

                if st.session_state.attempts >= 3:

                    st.session_state.feedback = (
                        f"Incorrect. Correct answer was: "
                        f"{' / '.join(correct_answers)}"
                    )

                    st.session_state.feedback_type = "error"
                    st.session_state.waiting_next = True
                    st.rerun()

                else:

                    st.session_state.feedback = "Incorrect."
                    st.session_state.feedback_type = "warning"
                    st.rerun()

        if st.session_state.feedback_type == "warning":
            st.warning(st.session_state.feedback)


    # NEXT CARD SCREEN
    else:

        if st.session_state.feedback_type == "success":
            st.success(st.session_state.feedback)

        elif st.session_state.feedback_type == "error":
            st.error(st.session_state.feedback)

        import streamlit.components.v1 as components

        next_button_key = (
            f"next_button_{words_done}_{st.session_state.attempts}"
        )

        st.button(
            "Next",
            key=next_button_key,
            type="primary",
            use_container_width=True,
            on_click=next_word,
        )

        components.html(
            """
            <script>
            const doc = window.parent.document;

            if (!doc._flashcardEnterHandler) {

                doc._flashcardEnterHandler = function(event) {

                    if (event.key !== "Enter") return;

                    const buttons = Array.from(
                        doc.querySelectorAll('button')
                    );

                    const nextButton = buttons.find(button =>
                        button.innerText.trim() === "Next"
                    );

                    if (!nextButton) return;

                    event.preventDefault();
                    event.stopImmediatePropagation();
                    nextButton.click();
                };

                doc.addEventListener(
                    "keydown",
                    doc._flashcardEnterHandler,
                    true
                );
            }
            </script>
            """,
            height=0,
        )



# FINISHED SCREEN
elif st.session_state.stage == "finished":

    st.title("Session complete")

    if st.session_state.completed_all:
        st.success("All cards studied. Nice work!")
    else:
        st.info("Session ended early.")

    if st.button(
        "Study again",
        type="primary",
        use_container_width=True
    ):
        st.session_state.stage = "setup"
        st.rerun()
