import streamlit as st
import random

st.set_page_config(page_title="Flashcard Study App", layout="centered")

# 1. ADD YOUR STUDY UNITS BELOW
# Add each written word once under "entries". List its key under "vocab" if
# it belongs in vocabulary practice. "kanji" lists focus characters; the app
# finds every entry containing one of those characters automatically.

unit_1 = {
    "entries": {
        "小学校": {"reading": ["しょうがっこう"], "meaning": "Elementary school"},
        "ようちえん": {"reading": ["ようちえん"], "meaning": "Kindergarten"},
        "〜年間": {"reading": ["~ねんかん, ねんかん"], "meaning": "For ~years"},
        "中学校": {"reading": ["ちゅうがっこう"], "meaning": "Middle school"},
        "高校": {"reading": ["こうこう"], "meaning": "High school"},
        "教いく": {"reading": ["きょういく"], "meaning": "Education"},
        "ぎむ教いく": {"reading": ["ぎむきょういく"], "meaning": "Compulsory education"},
        "しけん": {"reading": ["しけん"], "meaning": "Exam"},
        "外": {"reading": ["そと"], "meaning": "Outside"},
        "家事": {"reading": ["かじ"], "meaning": "Housework"},
        "ピアノ": {"reading": ["ピアノ, ぴあの"], "meaning": "Piano"},
        "よるおそく": {"reading": ["よるおそく"], "meaning": "Late night"},
        "まんが": {"reading": ["まんが"], "meaning": "Manga, Cartoon, Comic"},
        "インターネット": {"reading": ["インターネット, いんたーねっと"], "meaning": "Internet"},
        "先ぱい": {"reading": ["せんぱい"], "meaning": "One's senior"},
        "ゆう気": {"reading": ["ゆうき"], "meaning": "Courage"},
        "じょうねつ": {"reading": ["じょうねつ"], "meaning": "Passion"},
        "心": {"reading": ["こころ"], "meaning": "Heart"},
        "じゅぎょう": {"reading": ["じゅぎょう"], "meaning": "Class"},
        "ゆめ": {"reading": ["ゆめ"], "meaning": "Dream"},
        "外国": {"reading": ["がいこく"], "meaning": "Foreign country"},
        "しゅくだい": {"reading": ["しゅくだい"], "meaning": "Homework"},
        "心のやさしい人": {"reading": ["こころのやさしいひと"], "meaning": "Gentle-hearted person"},
        "おに": {"reading": ["おに"], "meaning": "Demon"},
        "赤おに": {"reading": ["あかおに"], "meaning": "Red demon"},
        "青おに": {"reading": ["あおおに"], "meaning": "Blue demon"},
        "人生": {"reading": ["じんせい"], "meaning": "One's life"},
        "むら": {"reading": ["むら"], "meaning": "Village"},
        "人間": {"reading": ["にんげん"], "meaning": "Human beings"},
        "かんばん": {"reading": ["かんばん"], "meaning": "Sign"},
        "アイデア": {"reading": ["アイデア, あいであ"], "meaning": "Idea"},
        "手紙": {"reading": ["てがみ"], "meaning": "Letter"},
        "とおく": {"reading": ["とおく"], "meaning": "Far"},
        "話": {"reading": ["はなし"], "meaning": "Story, Talk"},
        "問だい": {"reading": ["もんだい"], "meaning": "Problem"},
        "家": {"reading": ["いえ"], "meaning": "House"},
        "ギリギリス": {"reading": ["ギリギリス, ぎりぎりす"], "meaning": "Grasshopper"},
        "食べ物": {"reading": ["食べ物"], "meaning": "Food"},
        "飲み物": {"reading": ["飲み物"], "meaning": "Drink, Beverage"},
        "アリ": {"reading": ["アリ, あり"], "meaning": "Ant"},
        "明かり": {"reading": ["あかり"], "meaning": "Light"},
        "おりる": {"reading": ["おりる"], "meaning": "Get off"},
        "着く": {"reading": ["つく"], "meaning": "Arrive"},
        "出る": {"reading": ["でる"], "meaning": "Get out, Leave"},
        "決める": {"reading": ["きめる"], "meaning": "Decide"},
        "習う": {"reading": ["ならう"], "meaning": "Learn"},
        "世話をする": {"reading": ["せわをする"], "meaning": "Take care, Look after"},
        "ペットをかう": {"reading": ["ペットをかう, ぺっとをかう"], "meaning": "Have a pet"},
        "泊まる": {"reading": ["とまる"], "meaning": "Stay over (night)"},
        "くれる": {"reading": ["くれる"], "meaning": "Give (me)"},
        "おごる": {"reading": ["おごる"], "meaning": "Treat (someone)"},
        "連れて行く": {"reading": ["連れて行く"], "meaning": "Take (someone)"},
        "おしゃれをする": {"reading": ["おしゃれをする"], "meaning": "Dress up"},
        "サボる": {"reading": ["サボる, さぼる"], "meaning": "Skip (a class)"},
        "持つ": {"reading": ["もつ"], "meaning": "Hold, Have"},
        "あきらめる": {"reading": ["あきらめる"], "meaning": "Give up"},
        "困る": {"reading": ["こまる"], "meaning": "Be in need, In trouble"},
        "考える": {"reading": ["かんがえる"], "meaning": "Think, Consider"},
        "こわす": {"reading": ["こわす"], "meaning": "Break"},
        "オイオイ泣く": {"reading": ["オイオイなく, おいおいなく"], "meaning": "Cry one's heart out"},
        "笑う": {"reading": ["わらう"], "meaning": "Laugh"},
        "はたらく": {"reading": ["はたらく"], "meaning": "Work"},
        "バイオリンをひく": {"reading": ["バイオリンをひく, ばいおりんをひく"], "meaning": "Play a violin"},
        "答える": {"reading": ["こたえる"], "meaning": "Answer"},
        "始まる": {"reading": ["はじまる"], "meaning": "(It) starts, begins"},
        "さがす": {"reading": ["さがす"], "meaning": "Look for, Search"},
        "つく": {"reading": ["つく"], "meaning": "(Lights) turn on"},
        "シャイ": {"reading": ["シャイ"], "meaning": "Shy"},
        "いたずら": {"reading": ["いたずら"], "meaning": "Mischievous"},
        "とくい": {"reading": ["とくい"], "meaning": "Good at"},
        "悪い": {"reading": ["わるい"], "meaning": "Bad"},
        "かなしい": {"reading": ["かなしい"], "meaning": "Sad"},
        "正しい": {"reading": ["正しい"], "meaning": "Correct"},
        "自分で": {"reading": ["自分で"], "meaning": "By oneself"},
        "いっしょうけんめい": {"reading": ["いっしょうけんめい"], "meaning": "Very hard"},
        "しかし": {"reading": ["しかし"], "meaning": "However, But"},
        "ゆめを持つこと": {"reading": ["ゆめをもつこと"], "meaning": "Having one's dreams"},
        "あきらめないこと": {"reading": ["あきらめないこと"], "meaning": "Not giving up"},
        "ある山": {"reading": ["ある山"], "meaning": "A certain mountain"},
        "おなかがペコペコです": {"reading": ["おなかがペコペコです, おなかがぺこぺこです"], "meaning": "I'm starving"},
        "教える": {"reading": ["おしえる"], "meaning": "To teach, To tell"},
        "仕事": {"reading": ["しごと"], "meaning": "Job, Occupation"},
        "火事": {"reading": ["かじ"], "meaning": "Fire"},
        "事故": {"reading": ["じこ"], "meaning": "Accident"},
        "作る": {"reading": ["つくる"], "meaning": "To make"},
        "作り方": {"reading": ["つくりかた"], "meaning": "How to make"},
        "家族": {"reading": ["かぞく"], "meaning": "Family"},
        "使う": {"reading": ["つかう"], "meaning": "To use"},
        "大使館": {"reading": ["たいしかん"], "meaning": "Embassy"},
        "心配する": {"reading": ["しんぱいする"], "meaning": "To worry"},
        "中心": {"reading": ["ちゅうしん"], "meaning": "Center"},
        "安心する": {"reading": ["あんしんする"], "meaning": "To be relieved"},
        "食べ方": {"reading": ["たべかた"], "meaning": "How to eat"},
        "言い方": {"reading": ["いいかた"], "meaning": "How to say"},
        "手": {"reading": ["て"], "meaning": "Hand"},
        "手伝う": {"reading": ["てつだう"], "meaning": "To help"},
        "上手": {"reading": ["じょうず"], "meaning": "Good at"},
        "持ってくる": {"reading": ["もってくる"], "meaning": "To bring"},
        "気持ち": {"reading": ["きもち"], "meaning": "Feeling"},
        "お金持ち": {"reading": ["おかねもち"], "meaning": "Rich person"},
        "山": {"reading": ["やま"], "meaning": "Mountain"},
        "富士山": {"reading": ["ふじさん"], "meaning": "Mt. Fuji"},
        "明るい": {"reading": ["あかるい"], "meaning": "Bright, Cheerful"},
        "明日": {"reading": ["あした"], "meaning": "Tomorrow"},
        "発明する": {"reading": ["はつめいする"], "meaning": "To invent"},
        "明治時代": {"reading": ["めいじじだい"], "meaning": "Meiji Era"},

    },
    "vocab": [
        "小学校",
        "ようちえん",
        "〜年間",
        "中学校",
        "高校",
        "きょういく",
        "ぎむきょういく",
        "しけん",
        "外",
        "家事",
        "ピアノ",
        "よるおそく",
        "まんが",
        "インターネット",
        "先ぱい",
        "ゆう気",
        "じょうねつ",
        "心",
        "じゅぎょう",
        "ゆめ",
        "外国",
        "しゅくだい",
        "心のやさしい人",
        "おに",
        "赤おに",
        "青おに",
        "人生",
        "むら",
        "人間",
        "かんばん",
        "アイデア",
        "手紙",
        "とおく",
        "話",
        "問だい",
        "家",
        "ギリギリス",
        "食べ物",
        "飲み物",
        "アリ",
        "明かり",
        "おりる",
        "着く",
        "出る",
        "決める",
        "習う",
        "世話をする",
        "ペットをかう",
        "泊まる",
        "くれる",
        "おごる",
        "連れて行く",
        "おしゃれをする",
        "サボる",
        "持つ",
        "あきらめる",
        "困る",
        "考える",
        "こわす",
        "オイオイ泣く",
        "笑う",
        "はたらく",
        "バイオリンをひく",
        "答える",
        "始まる",
        "さがす",
        "つく",
        "シャイ",
        "いたずら",
        "とくい",
        "悪い",
        "かなしい",
        "正しい",
        "自分で",
        "いっしょうけんめい",
        "しかし",
        "ゆめを持つこと",
        "あきらめないこと",
        "ある山",
        "おなかがペコペコです",
    ],
    "kanji": ["教", "事", "作", "仕", "家", "使"],
}

unit_2 = {
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

unit_3 = {
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

unit_4 = {
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

unit_5 = {
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
    "Unit 1": unit_1,
    "Unit 2": unit_2,
    "Unit 3": unit_3,
    "Unit 4": unit_4,
    "Unit 5": unit_5,
    "Index": index,
}

# Units can be included in either category, or both, through their internal lists.
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

# APP LOGIC
if "stage" not in st.session_state:
    st.session_state.stage = "setup"

def build_vocabulary_deck(entries, entry_keys, direction):
    deck = {}
    if direction == "ENG to JPN":
        for written in entry_keys:
            entry = entries[written]
            accepted = entry["reading"] + [written]
            deck[entry["meaning"]] = list(dict.fromkeys(accepted))
    else:
        for written in entry_keys:
            meanings = [
                part.strip().lower()
                for part in entries[written]["meaning"].split(";")
            ]
            deck[written] = list(dict.fromkeys(meanings))
    return deck

def build_kanji_deck(entries, focus_kanji, mode):
    deck = {}
    for written, entry in entries.items():
        if not any(kanji in written for kanji in focus_kanji):
            continue
        if mode == "Reading":
            accepted = entry["reading"]
        else:
            accepted = [
                part.strip().lower()
                for part in entry["meaning"].split(";")
            ]
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

    if category == "Kanji":
        kanji_mode = st.radio(
            "Kanji mode:",
            ["Reading", "Meaning"],
            horizontal=True
        )
        direction = f"Kanji {kanji_mode}"
    else:
        direction = st.radio(
            "Direction:",
            ["ENG to JPN", "JPN to ENG"],
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
                    deck = build_kanji_deck(combined_entries, focus_kanji, kanji_mode)
                    start_quiz(deck, direction)
                    st.rerun()
        else:
            combined_entries = {}
            entry_keys = []
            for unit_name in selected_sets:
                unit = available_sets[unit_name]
                combined_entries.update(unit["entries"])
                entry_keys.extend(unit["vocab"])

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
                deck = build_vocabulary_deck(combined_entries, entry_keys, direction)
                start_quiz(deck, direction)
                st.rerun()

# QUIZ SCREEN
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

        if st.button("Next", type="primary", use_container_width=True):
            next_word()
            st.rerun()

# FINISHED SCREEN
elif st.session_state.stage == "finished":
    st.title("Session complete")
    if st.session_state.completed_all:
        st.success("All cards studied. Nice work!")
    else:
        st.info("Session ended early.")

    if st.button("Study again", type="primary", use_container_width=True):
        st.session_state.stage = "setup"
        st.rerun()
