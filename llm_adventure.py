import streamlit as st
from openai import OpenAI
import os
from typing import List, Tuple, Dict, Any
from player import Player  # new import for player class
from game_mechanics import update_player_stats  # new game mechanics
import random
from environment import initialize_environment, update_environment  # new import for environment mechanics

import sentry_sdk

sentry_sdk.init(
    dsn="https://c807fe7f9016ee8501884d838068e63f@o87286.ingest.us.sentry.io/4508799482003456",
    send_default_pii=True,
    traces_sample_rate=1.0,
)


class AdventureEngine:
    def __init__(self, temperature: float = 0.7):
        self.client = OpenAI(api_key=os.environ["OPENAI_KEY"])
        self.temperature = temperature
        self.starting_prompt = (
            "You are a narrative generator for a choose-your-own-adventure debugging game. "
            "Set up the initial scenario for a software engineer facing a critical production issue. "
            "Describe the initial alert or problem that starts their debugging journey in 2-3 sentences. "
            "Include realistic technical details like error messages or monitoring alerts.\n\n"
            "Provide exactly 3 initial debugging approaches as options, formatted as:\n"
            "1. [Action verb] [specific technical approach]\n"
            "2. [Action verb] [specific technical approach]\n"
            "3. [Action verb] [specific technical approach]\n\n"
            "Each option MUST:\n"
            "- Start with an action verb (e.g., Check, Deploy, Monitor)\n"
            "- Describe a specific technical action\n"
            "- Be relevant to investigating the initial problem"
        )
        self.iteration_prompt = (
            "You are continuing a debugging adventure narrative. "
            "Based on the engineer's previous actions, describe the next development in 2-3 sentences. "
            "Keep the narrative focused and technical.\n\n"
            "Previous actions and results:\n"
        )

    def generate_prompt(self, history: List[Dict[str, Any]], chosen_option: str = None) -> str:
        if not history:
            return self.starting_prompt
            
        prompt = self.iteration_prompt
        for entry in history:
            prompt += f"[Action: {entry.get('choice')}, Result: {entry.get('narrative')}]\n"
        if chosen_option:
            prompt += f"\nThe engineer chose to: {chosen_option}. "
        
        num_options = random.randint(2, 3)
        prompt += "\nNow describe what happens next, maintaining technical accuracy and suspense. "
        prompt += f"End with EXACTLY {num_options} clearly formatted action options (no more, no less):\n"
        
        for i in range(num_options):
            prompt += f"{i+1}. [Action verb] [specific technical approach]\n"
        return prompt.rstrip()

    def call_openai(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": "You are a technical storyteller familiar with software engineering, DevOps, and debugging production issues. Always format action options as 'Action verb + specific technical approach'."},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=self.temperature,
                        )
            narrative = response.choices[0].message.content.strip()
            return narrative
        except Exception as e:
            return f"Error calling OpenAI API: {e}"

    def parse_response(self, response: str) -> Tuple[str, List[str]]:
        # Parses the response to separate narrative text from options.
        # We expect exactly 3 numbered options after the narrative.
        lines = response.splitlines()
        narrative_lines = []
        option_lines = []
        
        # Find where options start (numbered lines)
        in_options = False
        for line in lines:
            stripped_line = line.strip()
            if stripped_line and stripped_line[0].isdigit() and '.' in stripped_line[:2]:
                in_options = True
                option_lines.append(stripped_line)
            elif not in_options:
                narrative_lines.append(line)
                
        narrative_text = "\n".join(narrative_lines).strip()
        
        # Clean options: remove numbers and ensure action verb format
        options = []
        for opt in option_lines:
            # Remove numbering and clean whitespace
            cleaned = opt.split('.', 1)[1].strip()
            # Ensure option starts with action verb
            if cleaned and not any(cleaned.lower().startswith(verb) for verb in ['check', 'deploy', 'run', 'monitor', 'debug', 'analyze', 'restart', 'test']):
                cleaned = f"Debug {cleaned}"
            options.append(cleaned)
            
        return narrative_text, [options[0], options[1], options[2]]


def initialize_state():
    if 'adventure_history' not in st.session_state:
        st.session_state['adventure_history'] = []
    if 'current_narrative' not in st.session_state:
        st.session_state['current_narrative'] = ""
    if 'current_options' not in st.session_state:
        st.session_state['current_options'] = []
    if 'game_started' not in st.session_state:
        st.session_state['game_started'] = False
    if 'engine' not in st.session_state:
        st.session_state['engine'] = AdventureEngine()
    # Initialize the player if not already present
    if 'player' not in st.session_state:
        st.session_state['player'] = Player()
    # Initialize the system environment if not already present
    if 'environment' not in st.session_state:
        st.session_state['environment'] = initialize_environment()


def restart_game():
    st.session_state['adventure_history'] = []
    st.session_state['current_narrative'] = ""
    st.session_state['current_options'] = []
    st.session_state['game_started'] = False
    # Reset player stats by creating a new Player instance
    st.session_state['player'] = Player()
    st.rerun()


def render_game(engine: AdventureEngine):
    st.title("Sentry's Revenge: A Stack Trace Through Time")
    
    # Sidebar with dynamic player stats and additional info
    player = st.session_state['player']
    st.sidebar.header(f"{player.name}'s Stats")
    st.sidebar.write(f"Level: {player.level}")
    st.sidebar.write(f"HP: {player.hp}")
    st.sidebar.write(f"MP: {player.mp}")
    st.sidebar.write(f"XP: {player.xp}")
    st.sidebar.write("Inventory:", player.inventory)
    
    # Display system environment information in the sidebar
    env = st.session_state.get('environment', {})
    st.sidebar.subheader("System Environment")
    st.sidebar.write(f"Server Load: {env.get('server_load')}")
    st.sidebar.write(f"Network Latency: {env.get('network_latency')} ms")
    if env.get('error_rate') is not None:
        st.sidebar.write(f"Error Rate: {env.get('error_rate'):.2%}")
    else:
        st.sidebar.write("Error Rate: N/A")

    # Optional debug info
    if st.sidebar.checkbox("Show Debug Info", value=False):
        st.sidebar.write("Adventure History:", st.session_state['adventure_history'])

    # Display effect of the last action if any
    if "last_effect" in st.session_state:
         st.info(f"Effect from last action: {st.session_state['last_effect']}")
         del st.session_state['last_effect']

    # Main narrative display
    if st.session_state['current_narrative']:
        st.write(st.session_state['current_narrative'])
        if st.session_state['current_options']:
            # st.write("\nWhat will you do next?\n")
            for option in st.session_state['current_options']:
                if st.button(option, key=option):
                    # Append the chosen option and previous narrative to history
                    history = st.session_state['adventure_history']
                    history.append({"choice": option, "narrative": st.session_state['current_narrative']})
                    st.session_state['adventure_history'] = history

                    # Update player's stats based on the chosen option and store the effect message
                    effect_msg = update_player_stats(player, option)
                    st.session_state['last_effect'] = effect_msg

                    # Update system environment after each action
                    st.session_state['environment'] = update_environment(st.session_state['environment'])

                    # Check for game over condition
                    if player.hp <= 0:
                        st.error("Game Over - Your production system has crashed under the stress!")
                        st.stop()

                    # Generate next narration using the chosen option
                    prompt = engine.generate_prompt(st.session_state['adventure_history'], chosen_option=option)
                    response = engine.call_openai(prompt)
                    narrative, options = engine.parse_response(response)
                    st.session_state['current_narrative'] = narrative
                    st.session_state['current_options'] = options
                    st.rerun()
    else:
        st.write("Welcome to the overengineered adventure game! Click 'Start Adventure' to begin.")


def start_adventure(engine: AdventureEngine):
    prompt = engine.generate_prompt(st.session_state['adventure_history'])
    response = engine.call_openai(prompt)
    narrative, options = engine.parse_response(response)
    st.session_state['current_narrative'] = narrative
    st.session_state['current_options'] = options
    st.session_state['game_started'] = True


def main():
    initialize_state()
    engine = st.session_state.get('engine')
    
    st.sidebar.button("Restart Adventure", on_click=restart_game)
    
    if engine:
        if st.button("Start Adventure") or st.session_state.get('game_started'):
            if not st.session_state.get('game_started'):
                start_adventure(engine)
            render_game(engine)
        else:
            st.write("Press 'Start Adventure' to begin your journey.")
    else:
        st.error("No engine found in session state. Please check your configuration.")
        st.write("Debug info:")
        st.write({
            "Session state keys": list(st.session_state.keys()),
            "Game started": st.session_state.get('game_started', False),
            "Current narrative": st.session_state.get('current_narrative', None),
            "Options": st.session_state.get('current_options', [])
        })


if __name__ == "__main__":
    main()
