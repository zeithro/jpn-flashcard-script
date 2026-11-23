import streamlit as st
import random

st.set_page_config(page_title="Flashcard Study App", layout="centered")

# 1. ADD YOUR STUDY UNITS BELOW
# Add each written word once under "entries". List its key under "vocab" if
# it belongs in vocabulary practice. "kanji" lists focus characters; the app
# finds every entry containing one of those characters automatically.

unit_1 = {
    "entries": {
        "大学": {"reading": ["だいがく"], "meaning": "college"},
        "学生": {"reading": ["がくせい"], "meaning": "student"},
        "先生": {"reading": ["せんせい"], "meaning": "teacher; professor"},
        "小雨": {"reading": ["こさめ"], "meaning": "drizzle; light rain"}
    },
    "vocab": ["大学", "学生", "先生"],
    "kanji": ["大", "学", "生", "先", "小"],
}

unit_2 = {
    "entries": {
        "水": {"reading": ["みず"], "meaning": "water"},
        "食べる": {"reading": ["たべる"], "meaning": "to eat"},
        "コーヒー": {"reading": ["コーヒー"], "meaning": "coffee"},
    },
    "vocab": ["水", "食べる", "コーヒー"],
    "kanji": ["水", "食"],
}

STUDY_UNITS = {
    "Unit 1": unit_1,
    "Unit 2": unit_2,
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

    with st.expander("Notes"):
        st.write("- The correct answer will be shown after three incorrect guesses.")
        st.write("- Capitalization is ignored in JPN to ENG and Kanji Meaning modes. Use the exact spelling/phrasing used in the book.")
        st.write("- Kanji Reading shows a full written word containing a selected kanji and expects its full kana reading.")
        st.write("- Add a word once under a unit's \"entries\". Add it to \"vocab\" for vocabulary practice; kanji entries are found automatically from the unit's focus kanji.")
        st.write("- Type 'done' (or 'どね' if you'd rather not switch off JPN keyboard) to end the session early.")

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
