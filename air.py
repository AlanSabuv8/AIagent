import streamlit as st
import numpy as np

# Define the possible actions
actions = ["decrease", "no_change", "increase"]

# Initialize Q-values to 0 for all state-action pairs
Q_values = {
    (24, "decrease"): 0,
    (24, "no_change"): 0,
    (24, "increase"): 0,
}

# Set initial parameters
alpha = 1  # Learning rate
gamma = 0.9  # Discount factor
reward = 5
punishment = -5

# Function to choose an action based on Q-values and epsilon-greedy policy
def choose_action(state, epsilon):
    if np.random.rand() < epsilon:
        # Explore: choose a random action
        return np.random.choice(actions)
    else:
        # Exploit: choose the action with the highest Q-value
        return max(Q_values.keys(), key=lambda a: Q_values[a] + np.random.randn() * 0.1)[1]

# Function to update Q-values based on the Bellman equation
def update_Q_value(state, action, next_state, reward):
    current_Q = Q_values.get((state, action), 0)
    best_next_Q = max(Q_values.get((next_state, a), 0) for a in actions)
    new_Q = (1 - alpha) * current_Q + alpha * (reward + gamma * best_next_Q)
    Q_values[(state, action)] = new_Q


# Function to simulate the air conditioner agent
def air_conditioner_agent():
    epsilon = 0.2  # Exploration-exploitation trade-off
    episodes = 10  # Reduced number of training episodes for simplicity

    # Initialize session state
    if 'indoor_temperature' not in st.session_state:
        st.session_state.indoor_temperature = 24
        st.session_state.episode_number = 1

        
    episode = st.session_state.episode_number

    for episode in range(episodes):
        # Display inputs for the current episode only when the "Next Episode" button is clicked
        #episode_container = st.empty()

        # Display the initial indoor temperature
        st.write(f"Initial Indoor Temperature = {st.session_state.indoor_temperature}")

        # User inputs external temperature
        outdoor_temperature_key = f"outdoor_temperature_{episode}"
        outdoor_temperature = st.number_input("Enter the external temperature:", key=outdoor_temperature_key)

        # Limiting the number of actions for simplicity
        # Choose action using epsilon-greedy policy
        action = choose_action(st.session_state.indoor_temperature, epsilon)
        #print(st.session_state.indoor_temperature)
        next_indoor_temperature = st.session_state.indoor_temperature
        #print(next_indoor_temperature)
        if action == "decrease":
            next_indoor_temperature -= 1
        elif action == "increase":
            next_indoor_temperature += 1

        # Display indoor temperature after each action, only if outdoor temperature is provided
        st.write(f"Action: {action}, New Indoor Temperature: {next_indoor_temperature}")

        # Ask the user if manual changes are required
        manual_changes_required_key = f"manual_changes_required_{episode}"
        manual_changes_required = st.radio("Do you want to make manual changes to the indoor temperature?", ("Yes", "No"), key=manual_changes_required_key, index=None)

        # If manual changes are required, ask the user for the desired indoor temperature
        if manual_changes_required == "Yes":
            new_indoor_temperature_key = f"new_indoor_temperature_{episode}"
            new_indoor_temperature = st.number_input("Enter the desired indoor temperature:", key=new_indoor_temperature_key)
            next_indoor_temperature = new_indoor_temperature

        # Update Q-value and apply rewards/punishments
        if manual_changes_required == "No":
            update_Q_value(st.session_state.indoor_temperature, action, next_indoor_temperature, reward)
        else:
            update_Q_value(st.session_state.indoor_temperature, action, next_indoor_temperature, punishment)

        # Move to the next state
        

        next_button_key = f"next_button_{episode}"
        if st.button(f"Next", key=next_button_key):
            st.session_state.indoor_temperature = next_indoor_temperature  
            st.session_state.episode_number += 1
            st.rerun()
        else:
            break

if __name__ == "__main__":
    st.title("Indoor Air Conditioner Control System")
    air_conditioner_agent()

    # Print the learned Q-values
    st.write("Learned Q-values:")
    for key, value in Q_values.items():
        st.write(f"Q-value for state-action pair {key}: {value}")
