# Introduction to Gradio

## Table of Contents

- [What is Gradio](#what-is-gradio)
- [Installation](#installation)
- [Interface Basics](#interface-basics)
- [Input and Output Components](#input-and-output-components)
- [Blocks API](#blocks-api)
- [Event Handling](#event-handling)
- [Stateful Demos](#stateful-demos)
- [Sharing and Deployment](#sharing-and-deployment)
- [Integration with ML Models](#integration-with-ml-models)
- [Chatbot Interface](#chatbot-interface)
- [Flagging](#flagging)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## What is Gradio

Gradio is an open-source Python library for building interactive web-based demos and interfaces for machine learning models. It allows you to create a UI in just a few lines of code and share it with anyone via a public link.

Key features:
- Build ML demos quickly with minimal code
- Supports a wide range of input/output types (text, images, audio, video, files)
- Share demos via public links or deploy on Hugging Face Spaces
- Built-in support for common ML frameworks
- Flexible layout system with the Blocks API

---

## Installation

```python
# Install Gradio using pip
# pip install gradio

# Verify the installation
import gradio as gr
print(gr.__version__)  # prints the installed version
```

---

## Interface Basics

```python
import gradio as gr

# The simplest Gradio app: a function wrapped in an Interface
def greet(name):
    return f"Hello, {name}!"

demo = gr.Interface(
    fn=greet,               # the function to wrap
    inputs="text",          # input component type (shorthand)
    outputs="text",         # output component type (shorthand)
    title="Greeting App",   # title displayed at the top
    description="Enter your name to get a greeting."
)

demo.launch()  # opens in browser at http://127.0.0.1:7860
```

```python
import gradio as gr

# Multiple inputs and outputs
def calculate(num1, num2, operation):
    if operation == "Add":
        result = num1 + num2
    elif operation == "Subtract":
        result = num1 - num2
    elif operation == "Multiply":
        result = num1 * num2
    else:
        result = num1 / num2 if num2 != 0 else "Error: division by zero"
    return result, f"Computed {num1} {operation} {num2}"

demo = gr.Interface(
    fn=calculate,
    inputs=[
        gr.Number(label="First Number"),
        gr.Number(label="Second Number"),
        gr.Dropdown(choices=["Add", "Subtract", "Multiply", "Divide"],
                    label="Operation")
    ],
    outputs=[
        gr.Number(label="Result"),
        gr.Textbox(label="Description")
    ],
    title="Calculator"
)

demo.launch()
```

---

## Input and Output Components

```python
import gradio as gr
import numpy as np

# Textbox - for text input/output
def reverse_text(text):
    return text[::-1]

gr.Interface(fn=reverse_text, inputs=gr.Textbox(lines=3, placeholder="Enter text..."),
             outputs=gr.Textbox(label="Reversed")).launch()
```

```python
import gradio as gr

# Image component
def process_image(img):
    # img is a numpy array (H, W, C) when type="numpy" (default)
    gray = np.mean(img, axis=2).astype(np.uint8)  # convert to grayscale
    return gray

demo = gr.Interface(
    fn=process_image,
    inputs=gr.Image(type="numpy", label="Upload Image"),
    outputs=gr.Image(type="numpy", label="Grayscale")
)
demo.launch()
```

```python
import gradio as gr

# Audio component
def echo_audio(audio):
    sr, data = audio  # audio is a tuple of (sample_rate, numpy_array)
    return (sr, data)

demo = gr.Interface(
    fn=echo_audio,
    inputs=gr.Audio(type="numpy", label="Record or Upload Audio"),
    outputs=gr.Audio(type="numpy", label="Playback")
)
demo.launch()
```

```python
import gradio as gr

# Slider, Dropdown, and Checkbox components
def configure(temperature, model, verbose):
    return f"Model: {model}, Temp: {temperature}, Verbose: {verbose}"

demo = gr.Interface(
    fn=configure,
    inputs=[
        gr.Slider(minimum=0.0, maximum=2.0, value=0.7, step=0.1,
                  label="Temperature"),
        gr.Dropdown(choices=["gpt-4", "gpt-3.5", "llama-2"], value="gpt-4",
                    label="Model"),
        gr.Checkbox(value=False, label="Verbose Output")
    ],
    outputs=gr.Textbox(label="Configuration")
)
demo.launch()
```

```python
import gradio as gr

# File, Radio, and CheckboxGroup components
def demo_components(file, radio_val, check_group):
    info = f"File: {file.name if file else 'None'}"
    return f"{info}, Radio: {radio_val}, Checks: {check_group}"

demo = gr.Interface(
    fn=demo_components,
    inputs=[
        gr.File(label="Upload a File"),
        gr.Radio(choices=["Small", "Medium", "Large"], label="Size", value="Medium"),
        gr.CheckboxGroup(choices=["Bold", "Italic", "Underline"], label="Formatting")
    ],
    outputs="text"
)
demo.launch()
```

---

## Blocks API

```python
import gradio as gr

# Blocks API provides more flexible layouts than Interface
with gr.Blocks(title="My App") as demo:
    gr.Markdown("# My Custom Application")

    # Row layout - components side by side
    with gr.Row():
        input_text = gr.Textbox(label="Input", scale=2)
        output_text = gr.Textbox(label="Output", scale=1)

    submit_btn = gr.Button("Submit", variant="primary")

    def process(text):
        return text.upper()

    submit_btn.click(fn=process, inputs=input_text, outputs=output_text)

demo.launch()
```

```python
import gradio as gr

# Tabs, Columns, and Accordion
with gr.Blocks() as demo:
    gr.Markdown("# Multi-Tab Application")

    with gr.Tabs():
        with gr.TabItem("Text Processing"):
            text_input = gr.Textbox(label="Enter Text")
            text_output = gr.Textbox(label="Result")
            text_btn = gr.Button("Process")
            text_btn.click(fn=lambda t: t.upper(), inputs=text_input,
                          outputs=text_output)

        with gr.TabItem("Image Processing"):
            with gr.Row():
                with gr.Column(scale=1):
                    img_input = gr.Image(label="Upload Image")
                    img_btn = gr.Button("Flip")
                with gr.Column(scale=1):
                    img_output = gr.Image(label="Result")
            img_btn.click(fn=lambda img: img[::-1], inputs=img_input,
                         outputs=img_output)

        with gr.TabItem("Settings"):
            with gr.Accordion("Advanced Settings", open=False):
                gr.Slider(0, 100, value=50, label="Quality")
                gr.Checkbox(label="Enable feature")

demo.launch()
```

```python
import gradio as gr

# Visibility toggling
with gr.Blocks() as demo:
    with gr.Row():
        show_btn = gr.Button("Show Details")
        hide_btn = gr.Button("Hide Details")

    details = gr.Textbox(label="Details", value="Hidden content", visible=False)

    show_btn.click(fn=lambda: gr.update(visible=True), outputs=details)
    hide_btn.click(fn=lambda: gr.update(visible=False), outputs=details)

demo.launch()
```

---

## Event Handling

```python
import gradio as gr

# Events connect user actions to Python functions
with gr.Blocks() as demo:
    name = gr.Textbox(label="Name")
    greeting = gr.Textbox(label="Greeting")

    def greet(name_val):
        return f"Hello, {name_val}!" if name_val else ""

    # change event fires whenever the input value changes
    name.change(fn=greet, inputs=name, outputs=greeting)
```

```python
import gradio as gr

# Chaining events: output of one triggers another
with gr.Blocks() as demo:
    text = gr.Textbox(label="Text")
    word_count = gr.Number(label="Word Count")
    status = gr.Textbox(label="Status")

    def count_words(text):
        return len(text.split()) if text else 0

    def check_length(count):
        if count > 100:
            return "Long text"
        elif count > 20:
            return "Medium text"
        return "Short text"

    # Chain: text change -> count words -> check length
    text.change(fn=count_words, inputs=text, outputs=word_count).then(
        fn=check_length, inputs=word_count, outputs=status
    )

demo.launch()
```

---

## Stateful Demos

```python
import gradio as gr

# Session state persists data across interactions for each user
with gr.Blocks() as demo:
    history = gr.State(value=[])  # per-session state initialized with empty list

    msg = gr.Textbox(label="Enter message")
    output = gr.Textbox(label="History", lines=5)
    btn = gr.Button("Add")
    clear_btn = gr.Button("Clear")

    def add_message(message, state):
        state.append(message)
        return "", "\n".join(state), state  # clear input, update display, return state

    def clear_history(state):
        state.clear()
        return "", [], ""

    btn.click(fn=add_message, inputs=[msg, history], outputs=[msg, output, history])
    clear_btn.click(fn=clear_history, inputs=[history], outputs=[msg, history, output])

demo.launch()
```

---

## Sharing and Deployment

```python
import gradio as gr

# Share publicly with a temporary link (valid for 72 hours)
demo = gr.Interface(fn=lambda x: x, inputs="text", outputs="text")
demo.launch(share=True)
# Prints a public URL like: https://xxxxx.gradio.live
```

```python
# Deploying to Hugging Face Spaces
# 1. Create a repository on huggingface.co/spaces
# 2. Add an app.py file with your Gradio code
# 3. Add a requirements.txt with dependencies
# 4. Push to the repository - app deploys automatically

# Authentication for shared demos
import gradio as gr

demo = gr.Interface(fn=lambda x: x, inputs="text", outputs="text")
demo.launch(auth=("admin", "password123"),
            auth_message="Please log in to access this demo.")
```

```python
# Mounting Gradio inside a FastAPI application
from fastapi import FastAPI
import gradio as gr

app = FastAPI()

@app.get("/api/health")
def health():
    return {"status": "ok"}

demo = gr.Interface(fn=lambda t: t.upper(), inputs="text", outputs="text")
app = gr.mount_gradio_app(app, demo, path="/gradio")
# Gradio at /gradio, FastAPI routes at /api/health
```

---

## Integration with ML Models

```python
import gradio as gr
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris

# Train a scikit-learn model
iris = load_iris()
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(iris.data, iris.target)

def classify_iris(sepal_length, sepal_width, petal_length, petal_width):
    features = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
    probabilities = clf.predict_proba(features)[0]
    class_names = iris.target_names
    return {class_names[i]: float(probabilities[i]) for i in range(3)}

demo = gr.Interface(
    fn=classify_iris,
    inputs=[
        gr.Slider(4.0, 8.0, value=5.8, label="Sepal Length"),
        gr.Slider(2.0, 4.5, value=3.0, label="Sepal Width"),
        gr.Slider(1.0, 7.0, value=4.0, label="Petal Length"),
        gr.Slider(0.1, 2.5, value=1.2, label="Petal Width"),
    ],
    outputs=gr.Label(num_top_classes=3),
    title="Iris Classifier"
)
demo.launch()
```

```python
import gradio as gr
from transformers import pipeline

# Integration with Hugging Face Transformers
sentiment = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    result = sentiment(text)[0]
    return f"{result['label']}: {result['score']:.4f}"

demo = gr.Interface(
    fn=analyze_sentiment,
    inputs=gr.Textbox(lines=3, label="Enter text for sentiment analysis"),
    outputs=gr.Textbox(label="Sentiment"),
    title="Sentiment Analyzer",
    examples=[  # pre-filled example inputs
        ["I love this product! It's amazing."],
        ["This was terrible and disappointing."],
    ]
)
demo.launch()
```

---

## Chatbot Interface

```python
import gradio as gr

# Simple chatbot using the ChatInterface
def respond(message, history):
    # message: current user message, history: list of [user, bot] pairs
    return f"You said: {message}"

demo = gr.ChatInterface(
    fn=respond,
    title="Simple Chatbot",
    examples=["Hello", "How are you?", "Tell me a joke"],
    retry_btn="Retry",
    undo_btn="Undo",
    clear_btn="Clear"
)
demo.launch()
```

```python
import gradio as gr

# Custom chatbot with Blocks layout
with gr.Blocks() as demo:
    chatbot = gr.Chatbot(label="Chat")
    msg = gr.Textbox(label="Message", placeholder="Type your message...")
    clear = gr.Button("Clear")

    def user_message(message, history):
        history = history + [[message, None]]  # None = bot hasn't responded yet
        return "", history

    def bot_response(history):
        user_msg = history[-1][0]
        history[-1][1] = f"I received: {user_msg}"
        return history

    msg.submit(user_message, [msg, chatbot], [msg, chatbot]).then(
        bot_response, chatbot, chatbot
    )
    clear.click(lambda: [], outputs=chatbot)

demo.launch()
```

---

## Flagging

```python
import gradio as gr

# Flagging allows users to mark problematic outputs for review
def classify(text):
    if "happy" in text.lower():
        return "Positive"
    elif "sad" in text.lower():
        return "Negative"
    return "Neutral"

demo = gr.Interface(
    fn=classify,
    inputs="text",
    outputs="text",
    flagging_mode="manual",                      # users click a button to flag
    flagging_dir="flagged_data",                 # directory to save flagged data
    flagging_options=["Incorrect", "Offensive", "Other"]
)
# Flagged data is saved as a CSV file in the flagging_dir
demo.launch()
```

---

## Practice Exercises

1. **Text Analyzer**: Build a Gradio interface that accepts text and displays word count, character count, and the most common words.

2. **Image Filter App**: Create an app with tabs for different image filters (grayscale, blur, edge detection) using the Blocks API.

3. **ML Model Demo**: Train a scikit-learn classifier and create a Gradio interface with sliders for features and a label output showing probabilities.

4. **Chatbot**: Build a chatbot interface that maintains conversation history and responds based on keyword matching.

5. **Dashboard**: Use the Blocks API with tabs, rows, and columns to create a multi-page dashboard.

---

## Summary

Gradio is a Python library for rapidly building interactive web interfaces for machine learning models and data processing functions. Key takeaways:

- `gr.Interface` provides a quick way to wrap any Python function with a web UI
- Components like Textbox, Image, Audio, Slider, and Dropdown handle diverse input/output types
- The Blocks API enables flexible layouts with rows, columns, tabs, and accordions
- Event handling connects user interactions to Python functions with chaining support
- Session state with `gr.State` enables persistent data across interactions
- Demos can be shared with `share=True` or deployed to Hugging Face Spaces
- Gradio integrates smoothly with scikit-learn, PyTorch, and Hugging Face models

---

## Next Steps

- Explore advanced Blocks patterns for complex applications
- Learn about custom components and themes
- Study Gradio's API for programmatic access to deployed demos
- Investigate Gradio Clients for calling APIs from other languages
- Look into queuing and concurrency for production deployments

---

## Additional Resources

- [Gradio Official Documentation](https://www.gradio.app/docs/)
- [Gradio GitHub Repository](https://github.com/gradio-app/gradio)
- [Gradio Guides](https://www.gradio.app/guides/)
- [Hugging Face Spaces](https://huggingface.co/spaces)
- [Gradio Component Gallery](https://www.gradio.app/docs/components)
