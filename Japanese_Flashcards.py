import streamlit as st
import random

st.set_page_config(page_title="Flashcard Study App", layout="centered")

# 1. ADD YOUR STUDY SETS BELOW
# Format: "Prompt": ["Accepted Answer 1", "Accepted Answer 2"]

set_1 = {
    "college": ["だいがく", "大学"],
    "student": ["がくせい", "学生"],
    "teacher; professor": ["せんせい", "先生"],
}

set_2 = {
    "water": ["みず", "水"],
    "to eat": ["たべる", "食べる"],
    "coffee": ["コーヒー"],
}

# 2. ORGANIZE SETS INTO CATEGORIES
# Add or rename categories and sets here.

STUDY_CATEGORIES = {
    "Vocabulary": {
        "Set 1": set_1,
        "Set 2": set_2,
    },
    "Kanji": {
        "Set 1": set_1,
    },
}

# APP LOGIC
if "stage" not in st.session_state:
    st.session_state.stage = "setup"

def build_deck(raw_dict, direction):
    deck = {}
    if direction == "ENG to JPN":
        for eng, jpn_list in raw_dict.items():
            deck[eng] = jpn_list
    else:
        for eng, jpn_list in raw_dict.items():
            prompt = jpn_list[-1]
            accepted = [eng.lower()] + [part.strip().lower() for part in eng.split(";")]
            deck[prompt] = list(dict.fromkeys(accepted))
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

    direction = st.radio(
        "Direction:",
        ["ENG to JPN", "JPN to ENG"],
        horizontal=True
    )

    available_sets = STUDY_CATEGORIES[category]
    study_all = st.checkbox("Study all sets")

    if study_all:
        selected_sets = list(available_sets.keys())
    else:
        selected_sets = st.multiselect(
            "Choose sets to study:",
            options=list(available_sets.keys()),
            default=list(available_sets.keys())[:1]
        )

    with st.expander("Notes"):
        st.write("- You have 3 attempts per card.")
        st.write("- In JPN to ENG mode, capitalization is ignored, and cards with multiple meanings separated by a semicolon accept any single meaning.")
        st.write("- Type 'done' (or 'どね') to end the session early.")

    if st.button("Start", type="primary", use_container_width=True):
        if not selected_sets:
            st.error("Invalid selection. Please select at least one set.")
        else:
            combined_raw = {}
            for s in selected_sets:
                combined_raw.update(available_sets[s])
            deck = build_deck(combined_raw, direction)
            start_quiz(deck, direction)
            st.rerun()

# QUIZ SCREEN
elif st.session_state.stage == "quiz":
    current = st.session_state.current
    correct_answers = st.session_state.deck[current]
    words_done = st.session_state.total_count - len(st.session_state.prompts)
    is_jpn_to_eng = st.session_state.direction == "JPN to ENG"

    st.progress(words_done / st.session_state.total_count)
    st.caption(f"{words_done}/{st.session_state.total_count} | Attempt {st.session_state.attempts + 1}/3")

    display_prompt = current if is_jpn_to_eng else current.capitalize()
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
                    st.session_state.feedback = f"Incorrect. Correct answer is: {' / '.join(correct_answers)}"
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
        st.success("All vocabulary studied. Nice work!")
    else:
        st.info("Session ended early.")

    if st.button("Study again", type="primary", use_container_width=True):
        st.session_state.stage = "setup"
        st.rerun()
