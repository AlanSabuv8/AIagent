import streamlit as st

def max_qvalue(a, b, c):
    max_val = max(a, b, c)
    if max_val == a:
        return 0
    elif max_val == b:
        return 1
    else:
        return 2
    


def airTemp(j,k):
    # print qvalue
    table_data = {
        "indoor": list(range(18, 30)),
        "decrease": [st.session_state.qvalue[i][0] for i in range(18, 30)],
        "nochange": [st.session_state.qvalue[i][1] for i in range(18, 30)],
        "increase": [st.session_state.qvalue[i][2] for i in range(18, 30)],
    }

# Display the table
    st.table(table_data)

    st.write("\n----------------------------------------------")
    st.write("present temperature===== ", st.session_state.temp)

    # choose action acc to qvalue
    act = max_qvalue(st.session_state.qvalue[st.session_state.temp][0], st.session_state.qvalue[st.session_state.temp][1], st.session_state.qvalue[st.session_state.temp][2])

    if act == 0:
        st.write("\nDECREASE temp.")
        ptemp = st.session_state.temp - 1
        st.write("new temp = ", st.session_state.temp - 1)
    elif act == 1:
        st.write("\nNO CHANGE.")
        ptemp = st.session_state.temp
        st.write("temp remains same = ", st.session_state.temp)
    elif act == 2:
        st.write("\nINCREASE temp.")
        ptemp = st.session_state.temp + 1
        st.write("new temp = ", st.session_state.temp + 1)
    else:
        st.write("\nERROR!")

    # ask user if changes required
    manual_changes_required_key = f"manual_changes_required_{j}"
    change_placeholder = st.empty()
    change = st.radio("Do you want to make manual changes to the indoor temperature?", ("Yes", "No"), key=manual_changes_required_key, index=None)


    if change == "Yes":
        indoor_temperature_key = f"outdoor_temperature_{j}"
        new_temp = int(st.number_input("Enter the required temperature between 18-29:", key=indoor_temperature_key))
        if new_temp is not None and not (18 <= new_temp <= 29):
        # Clear the input and radio button if the value is not in the specified range
            new_temp = None
            change = None
            #st.warning("Please enter a temperature between 18 and 29.")
        else:
            reward = -5
            k = True
    elif change == "No":
        new_temp = ptemp
        st.write("\nno changes needed. temp remains as ", new_temp)
        reward = 5
        k = True

    # find new qvalue using bellman equation
    next_button_key = f"next_button_{j}"
    if st.button(f"Next", key=next_button_key):
        if change is not None:
            if new_temp is not None or change == "No":
                maxQ = st.session_state.qvalue[new_temp][max_qvalue(st.session_state.qvalue[new_temp][0], st.session_state.qvalue[new_temp][1], st.session_state.qvalue[new_temp][2])]
                Q = reward + maxQ
                st.session_state.qvalue[st.session_state.temp][act] = Q
                st.session_state.temp = new_temp
                new_temp = None
                change = None
                j = j + 1
                st.rerun()

if __name__ == "__main__":
    st.title("Indoor Air Conditioner Control System")

    if 'qvalue' not in st.session_state:
        st.session_state.qvalue = [[0] * 3 for _ in range(40)]


    st.write("\ninitial temperature: 24")
    if 'temp' not in st.session_state:
            st.session_state.temp = 24

    j = 0
    k = False
    airTemp(j,k)
    
