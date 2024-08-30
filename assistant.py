import os
import google.generativeai as genai
import gradio as gr


genai.configure(api_key="API_KEY") #insert you api key here


generation_config = {
    "temperature": 0.7, 
    "top_p": 0.9,  
    "top_k": 40,  
    "max_output_tokens": 8192,  
    "response_mime_type": "text/plain",
}


model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-exp-0801",
    generation_config=generation_config,
)


chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "You are a legal chatbot specializing in the Indian Penal Code. "
                "You will answer legal questions in a concise and accurate manner. "
                "Provide your responses in a bullet-point format, and make sure each point "
                "is clear, relevant, and directly addresses the user's query. "
                "Ensure your responses are based on the provisions of the Indian Penal Code, "
                "avoiding assumptions not provided in the query."
            ],
        },
        {
            "role": "model",
            "parts": [
                "Understood! I am ready to provide legal information based on the Indian Penal Code. "
                "Please ask your legal question."
            ],
        },
    ]
)


def ask_question(user_input):
    response = chat_session.send_message(user_input)
    return response.text

# Create the Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# Indian Penal Code Legal Chatbot ")
    gr.Markdown(
        """
        **Description:** 
        This chatbot is designed to assist with questions related to the Indian Penal Code (IPC). 
        You can ask questions about specific sections, legal definitions, or consequences of various IPC provisions. 
        The chatbot will provide concise, accurate, and contextually appropriate responses.
        """
    )
    query_input = gr.Textbox(label="Enter your query", placeholder="Type your query here...")
    generate_button = gr.Button("Generate")
    response_output = gr.Markdown(label="Response")

    gr.Examples(
        examples=[
            ["What is IPC 42?"],
            ["What are the consequences of IPC 302?"],
            ["Explain the term 'good faith' as per IPC."],
        ],
        inputs=query_input
    )

    generate_button.click(ask_question, inputs=query_input, outputs=response_output)

demo.launch()
