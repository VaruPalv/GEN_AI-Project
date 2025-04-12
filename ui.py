import streamlit as st
import requests

st.set_page_config(page_title="Langgraph Agent",layout="centered", page_icon="icon.png")
API_URL="http://127.0.0.1:8000/chat"

MODEL_NAMES= [
    "llama-guard-3-8b",
    "gemma2-9b-it",
    "llama3-8b-8192",
    "llama3-70b-8192"
]
st.title("Let's Chat")
st.write("Interact with the Langgraph agent using this interface")

given_system_prompt=st.text_area("Define your AI Agent:",height=100,placeholder="Say act as researcher/analyst...")
selected_model=st.selectbox("Select Model",MODEL_NAMES)
user_input = st.text_area("Enter your message(s):", height=150, placeholder="Type your message here...")
if st.button("Submit"):
    if user_input.strip():
        try:
            payload={"messages":[user_input],"model_name":selected_model,'system_prompt':given_system_prompt}
            response=requests.post(API_URL,json=payload)
            if response.status_code==200:
                response_data=response.json()
                if "error" in response_data:
                    st.error(response_data["error"])
                else:
                    ai_responses=[
                        message.get("content","")
                        for message in response_data.get("messages",[])
                          if message.get("type")=="ai"
                    ]

                    if ai_responses:
                        st.subheader("Agent Response:")
                        st.markdown(f"**Final Response:**{ai_responses[-1]}")
                    else:
                        st.warning("No AI response found in the agent output.")
            else:
                st.error(f"Request failed with status code {response.status_code}.")

        

            
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a message before clicking 'Submit'.")
    

