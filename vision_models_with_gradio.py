import io

import gradio as gr
import base64
import json
import requests
from PIL import Image

def get_base64(image):
    """Convert image file to base64 encoding."""
    try:
        # Check if the input is a PIL image or bytes
        if isinstance(image, Image.Image):
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            image_bytes = buffer.getvalue()
        elif isinstance(image, bytes):
            image_bytes = image
        else:
            raise ValueError("Invalid image type. Must be PIL.Image or bytes.")

        # Encode bytes to base64
        encoded_string = base64.b64encode(image_bytes).decode('utf-8')
        return encoded_string
    except Exception as e:
        return f"Error encoding image to base64: {str(e)}"


def generate_response(base_url, model_name, user_input, image_64):
    """Send the image and user input to the vision model and stream the response."""
    print("inside generate_response")
    url = f'{base_url}/api/chat'
    headers = {'Content-Type': 'application/json'}
    data = {
        "model": model_name,
        "messages": [{
            "role": "user",
            "content": user_input,
            "images": [image_64]
        }],
        "stream": True  # Enable streaming
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)
        if response.status_code == 200:
            full_response = ""
            for chunk in response.iter_lines():
                if chunk:
                    # Decode JSON chunk
                    chunk_data = json.loads(chunk.decode('utf-8'))
                    partial_msg = chunk_data.get('message', {}).get('content', '')

                    full_response += partial_msg
            return full_response
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

def process_image_and_query(image, model_name, user_input):
    """Process the image and query, send it to the model, and return the response."""
    try:
        print("inside process_image_and_query")
        # Convert the image to bytes
        # image_bytes = image.tobytes()

        image_base64 = get_base64(image)
        print("image_base64", image_base64)
        base_url = "http://localhost:11434"
        response = generate_response(base_url, model_name, user_input, image_base64)
        return response
    except Exception as e:
        return f"Error processing the request: {str(e)}"

# Gradio Interface
def main():
    with gr.Blocks() as demo:
        gr.Markdown("## Vision Model Interaction App")

        with gr.Row():
            model_name = gr.Textbox(label="Vision Model Name", value="llava:latest", placeholder="Enter model name")
            user_input = gr.Textbox(label="Query", value="Describe this image", placeholder="Enter your query")

        with gr.Row():
            image_input = gr.Image(type="pil", label="Upload Image")

        output_response = gr.Textbox(label="Model Response", lines=10, interactive=False)

        submit_button = gr.Button("Send to Model")

        submit_button.click(
            fn=process_image_and_query,
            inputs=[image_input, model_name, user_input],
            outputs=[output_response]
        )

    demo.launch()

if __name__ == "__main__":
    main()
