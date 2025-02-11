import streamlit as st
import random
import time

# --- Define the Chapter class to structure each adventure branch ---
class Chapter:
    def __init__(self, id, title, text, choices, endpoint=False):
        self.id = id
        self.title = title
        self.text = text
        self.choices = choices  # List of dicts: {"label": <str>, "destination": <str>}
        self.endpoint = endpoint

# --- Define the AdventureGame class to hold our chapters ---
class AdventureGame:
    def __init__(self, chapters):
        self.chapters = chapters

    def get_chapter(self, chapter_id):
        return self.chapters.get(chapter_id, None)

# --- Define all chapters for our adventure ---
chapters = {
    "start": Chapter(
        "start",
        "The Overengineered Quest Begins",
        "Welcome, brave adventurer, to the land of absurdity. You stand at a crossroads made of glittering code and caffeinated dreams. Where will you go?",
        [
            {"label": "Venture to the Donut Village", "destination": "donut_village"},
            {"label": "Enter the Coffee Forest", "destination": "coffee_forest"}
        ]
    ),
    "donut_village": Chapter(
        "donut_village",
        "Donut Village",
        "You arrive in the whimsical Donut Village, where every street smells of sugary delight and there's a secret bakery in the center.",
        [
            {"label": "Enter the mysterious bakery", "destination": "bakery"},
            {"label": "Talk to the eccentric donut mayor", "destination": "mayor"}
        ]
    ),
    "coffee_forest": Chapter(
        "coffee_forest",
        "Coffee Forest",
        "You wander into the Coffee Forest. Trees drip steaming espresso and the aroma jolts your senses into hyperdrive. A chatty squirrel offers you a sample of her special brew.",
        [
            {"label": "Accept the sample (Risky caffeine boost!)", "destination": "coffee_accept"},
            {"label": "Politely decline the sample", "destination": "decline_coffee"}
        ]
    ),
    "bakery": Chapter(
        "bakery",
        "The Enchanted Bakery",
        "Inside the bakery, you witness a marvel: a magical, self-refilling donut machine that sings show tunes. The air is thick with mystery and frosting.",
        [
            {"label": "Devour a magical donut", "destination": "donut_delight"},
            {"label": "Investigate the secret ingredient", "destination": "ingredient_mystery"}
        ]
    ),
    "mayor": Chapter(
        "mayor",
        "The Donut Mayor",
        "The donut mayor, a round man with sprinkles of wisdom, engages you in a heated debate about the existential meaning of glazed existence.",
        [
            {"label": "Join the debate", "destination": "debate"},
            {"label": "Escape to a quiet corner", "destination": "quiet_corner"}
        ]
    ),
    "decline_coffee": Chapter(
        "decline_coffee",
        "Abstaining from Caffeine",
        "You quietly avoid the sample and continue pondering what life in the Coffee Forest is like without a jolt of java. Perhaps caution is golden?",
        [
            {"label": "Return to the crossroads", "destination": "start"}
        ]
    ),
    # "coffee_accept" is a pseudo-chapter handled dynamically to simulate randomness
    "espresso_explosion": Chapter(
        "espresso_explosion",
        "Espresso Explosion",
        "The caffeinated sample triggers an unintended explosion, propelling you into a parallel universe where espresso and foam art govern reality.",
        [
            {"label": "Navigate through the nebula of nerves", "destination": "cosmic_caffeine"},
            {"label": "Wade through the creamy aftermath", "destination": "aftermath"}
        ]
    ),
    "caffeine_craze": Chapter(
        "caffeine_craze",
        "Caffeine Craze",
        "The sample sends you spiraling into a jittery frenzy of hilariously erratic behavior. The world becomes a blur of hyperactive hijinks.",
        [
            {"label": "Embrace the madness", "destination": "madness"},
            {"label": "Seek refuge in a quiet monastery", "destination": "monastery"}
        ]
    ),
    "donut_delight": Chapter(
        "donut_delight",
        "Donut Delight",
        "You devour the magical donut and are transformed into a being of pure sugary radiance. The universe now makes a bit more sense.",
        [],
        endpoint=True
    ),
    "ingredient_mystery": Chapter(
        "ingredient_mystery",
        "Ingredient Mystery",
        "Your investigation reveals the secret ingredient to be the laughter of a thousand clowns. Absurdity overwhelms you and your quest ends in delicious bewilderment.",
        [],
        endpoint=True
    ),
    "debate": Chapter(
        "debate",
        "Intellectual Butter",
        "The debate about sprinkles and existential meaning rages on until you're drenched in the butter of intellectual insight. Victory is bittersweet.",
        [],
        endpoint=True
    ),
    "quiet_corner": Chapter(
        "quiet_corner",
        "Quiet Contemplation",
        "In a quiet corner, you find solace and ponder the cosmic insignificance of sprinkles. A peaceful, if underwhelming, end.",
        [],
        endpoint=True
    ),
    "cosmic_caffeine": Chapter(
        "cosmic_caffeine",
        "Cosmic Caffeine",
        "Through a nebula of nerves you navigate an odyssey of celestial latte art, emerging as the unsung hero of a caffeinated cosmos.",
        [],
        endpoint=True
    ),
    "aftermath": Chapter(
        "aftermath",
        "Creamy Aftermath",
        "After the espresso explosion, you find tranquility in a slow drip of life. Adventure, it seems, always turns unexpectedly mellow.",
        [],
        endpoint=True
    ),
    "madness": Chapter(
        "madness",
        "Madness Maven",
        "In a state of blissful madness, logic dissolves and you become a legend of irreverent genius.",
        [],
        endpoint=True
    ),
    "monastery": Chapter(
        "monastery",
        "Monastic Mellow",
        "In a secluded monastery, you seek inner peace and leave behind the hyperactive escapades. Enlightenment becomes your true adventure.",
        [],
        endpoint=True
    )
}

# --- Initialize the game ---
game = AdventureGame(chapters)

# --- Utility functions for state management ---

def init_state():
    if 'current_chapter' not in st.session_state:
        st.session_state.current_chapter = 'start'
    if 'path_taken' not in st.session_state:
        st.session_state.path_taken = ['start']
    # This flag is used for the coffee branch random decision
    if 'coffee_computed' not in st.session_state:
        st.session_state.coffee_computed = False


def reset_game():
    st.session_state.current_chapter = 'start'
    st.session_state.path_taken = ['start']
    st.session_state.coffee_computed = False
    if 'coffee_result' in st.session_state:
        del st.session_state.coffee_result
    st.experimental_rerun()

# --- Main function to display the adventure ---

def main():
    st.title('Choose Your Own Adventure: The Overengineered Quest for the Holy Cupcake')
    init_state()

    # Sidebar info and reset button
    st.sidebar.header('Adventure Control Panel')
    if st.sidebar.button('Restart Adventure'):
        reset_game()
    st.sidebar.markdown('### Debug Info')
    st.sidebar.write('Current Path:', ' -> '.join(st.session_state.path_taken))
    if 'coffee_result' in st.session_state:
        st.sidebar.write('Coffee Random Value:', st.session_state.coffee_result)

    current_id = st.session_state.current_chapter

    # Special handling for the coffee branch
    if current_id == 'coffee_accept':
        with st.spinner('Brewing suspense...'):
            time.sleep(1)  
            # Compute random outcome once
            if not st.session_state.coffee_computed:
                outcome = random.random()
                st.session_state.coffee_result = outcome
                if outcome < 0.5:
                    st.session_state.current_chapter = 'espresso_explosion'
                else:
                    st.session_state.current_chapter = 'caffeine_craze'
                st.session_state.coffee_computed = True
                st.session_state.path_taken.append(st.session_state.current_chapter)
                st.experimental_rerun()

    chapter = game.get_chapter(st.session_state.current_chapter)
    if chapter is None:
        st.error('Chapter not found!')
        return

    # Display the current chapter
    st.header(chapter.title)
    st.write(chapter.text)

    # Check if we reached an endpoint
    if chapter.endpoint or len(chapter.choices) == 0:
        st.success('The End!')
        if st.button('Restart Adventure'):
            reset_game()
        return

    st.write('---')
    st.subheader('What will you do next?')

    # Display each choice as a button
    for choice in chapter.choices:
        if st.button(choice['label']):
            dest = choice['destination']
            # Reset coffee branch flag if leaving that branch
            if dest != 'coffee_accept':
                st.session_state.coffee_computed = False
            st.session_state.current_chapter = dest
            st.session_state.path_taken.append(dest)
            st.experimental_rerun()

if __name__ == '__main__':
    main() 