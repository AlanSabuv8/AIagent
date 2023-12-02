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

# Streamlit UI
def main():
    st.title("Indoor air temperature control system")

    # Ask for the external temperature
    external_temperature = st.number_input("Enter the external temperature:")

    epsilon = 0.2  # Exploration-exploitation trade-off
    indoor_temperature = 24

    # Create a placeholder for the system-generated output
    output_placeholder = st.empty()

    # Simulate the environment
    action = choose_action(indoor_temperature, epsilon)

    # Update the placeholder with the system-generated output
    output_placeholder.write(f"Action: {action}")

    # Ask the user if manual changes are required
    manual_changes_required = st.radio("Do you want to make manual changes to the indoor temperature?", ("Yes", "No"))

    # If manual changes are required, ask the user for the desired indoor temperature
    if manual_changes_required == "Yes":
        new_indoor_temperature = st.number_input("Enter the desired indoor temperature:")
        indoor_temperature = new_indoor_temperature

    # Update Q-value and apply rewards/punishments
    next_indoor_temperature = indoor_temperature
    if action == "decrease":
        next_indoor_temperature -= 1
    elif action == "increase":
        next_indoor_temperature += 1
    update_Q_value(indoor_temperature, action, next_indoor_temperature, reward if manual_changes_required == "No" else punishment)

    # Display Q-values
    st.write("Q-values:")
    for key, value in Q_values.items():
        st.write(f"Q-value for state-action pair {key}: {value}")

if __name__ == "__main__":
    main()
