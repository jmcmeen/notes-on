# Introduction to Streamlit

## Table of Contents

- [What is Streamlit](#what-is-streamlit)
- [Installation](#installation)
- [Your First Streamlit App](#your-first-streamlit-app)
- [Display Elements](#display-elements)
- [Input Widgets](#input-widgets)
- [Layout](#layout)
- [State Management](#state-management)
- [Caching](#caching)
- [Data Visualization](#data-visualization)
- [Forms](#forms)
- [Deployment](#deployment)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## What is Streamlit

Streamlit is an open-source Python framework for building data-centric web applications. It turns Python scripts into interactive web apps with minimal code, requiring no front-end development experience.

Key features:
- Write apps entirely in Python with no HTML, CSS, or JavaScript
- Automatic re-run on code or input changes
- Built-in support for data visualization, tables, and charts
- Simple caching mechanisms for performance
- Easy deployment via Streamlit Community Cloud

---

## Installation

```python
# Install Streamlit using pip
# pip install streamlit

# Run the built-in hello demo
# streamlit hello

# Common additional packages
# pip install pandas numpy matplotlib plotly
```

---

## Your First Streamlit App

```python
# app.py - A minimal Streamlit application
import streamlit as st

# Page configuration (must be the first Streamlit command)
st.set_page_config(
    page_title="My App",
    layout="wide",                 # "centered" or "wide"
    initial_sidebar_state="auto"
)

st.title("My First Streamlit App")

# st.write is the Swiss Army knife - handles many data types
st.write("Hello, World!")
st.write("This is **bold** and this is *italic*.")

# Run with: streamlit run app.py
# Options: --server.port 8080, --theme.base dark
# App opens at http://localhost:8501
```

---

## Display Elements

```python
import streamlit as st
import pandas as pd
import numpy as np

# Text elements
st.title("Title Text")
st.header("Header Text")
st.subheader("Subheader Text")
st.text("Fixed-width text")
st.markdown("**Markdown** supported")
st.latex(r"e^{i\pi} + 1 = 0")       # renders LaTeX math
st.caption("Small caption text")
st.code("print('hello')", language="python")
st.divider()                          # horizontal line
```

```python
import streamlit as st
import pandas as pd

# Data display
df = pd.DataFrame({"Name": ["Alice", "Bob"], "Age": [25, 30], "Score": [88.5, 92.3]})

st.dataframe(df, use_container_width=True)   # scrollable, sortable table
st.table(df)                                  # static table

# Metrics with delta indicators
st.metric(label="Revenue", value="$12,345", delta="$1,234")

# JSON display
st.json({"name": "Alice", "scores": [90, 85, 92]})
```

```python
import streamlit as st

# Status and progress elements
st.success("Operation completed successfully!")
st.info("This is an informational message.")
st.warning("Be careful with this action.")
st.error("An error occurred!")

# Progress bar
import time
progress = st.progress(0, text="Processing...")
for i in range(100):
    time.sleep(0.01)
    progress.progress(i + 1, text=f"Processing {i+1}%")

# Spinner for long operations
with st.spinner("Loading data..."):
    time.sleep(2)
st.write("Data loaded!")
```

---

## Input Widgets

```python
import streamlit as st

# Button
if st.button("Click Me"):
    st.write("Button was clicked!")

# Text input
name = st.text_input("Enter your name", placeholder="John Doe")
bio = st.text_area("Tell us about yourself", height=150)

# Number and slider
age = st.number_input("Age", min_value=0, max_value=120, value=25)
temperature = st.slider("Temperature", 0.0, 2.0, 0.7, step=0.1)

# Range slider (returns a tuple)
values = st.slider("Select a range", 0, 100, (25, 75))

# Selectbox and multiselect
option = st.selectbox("Framework", ["PyTorch", "TensorFlow", "JAX"])
colors = st.multiselect("Colors", ["Red", "Green", "Blue"], default=["Blue"])

# Radio and checkbox
size = st.radio("Size", ["Small", "Medium", "Large"], horizontal=True)
agree = st.checkbox("I agree to the terms")
dark_mode = st.toggle("Dark Mode")
```

```python
import streamlit as st
from datetime import date

# Date, time, and color inputs
selected_date = st.date_input("Pick a date", value=date.today())
color = st.color_picker("Pick a color", value="#00ff00")

# File uploader
uploaded_file = st.file_uploader("Upload a file", type=["csv", "txt", "json"])

if uploaded_file is not None:
    import pandas as pd
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)

# Download button
st.download_button(
    label="Download data",
    data="column1,column2\nval1,val2\n",
    file_name="data.csv",
    mime="text/csv"
)
```

---

## Layout

```python
import streamlit as st

# Columns - arrange elements side by side
col1, col2, col3 = st.columns(3)
with col1:
    st.header("Column 1")
with col2:
    st.header("Column 2")
with col3:
    st.header("Column 3")

# Columns with different widths
left, right = st.columns([2, 1])  # left is twice as wide
```

```python
import streamlit as st

# Sidebar - persistent navigation panel
with st.sidebar:
    st.title("Navigation")
    page = st.radio("Go to", ["Home", "Analysis", "Settings"])

if page == "Home":
    st.title("Home Page")
elif page == "Analysis":
    st.title("Analysis Page")
else:
    st.title("Settings Page")
```

```python
import streamlit as st

# Tabs
tab1, tab2, tab3 = st.tabs(["Data", "Visualization", "Settings"])
with tab1:
    st.header("Data Tab")
with tab2:
    st.header("Visualization Tab")
with tab3:
    st.header("Settings Tab")

# Expander - collapsible section
with st.expander("Click to expand"):
    st.write("Hidden content revealed.")

# Container and empty placeholder
with st.container():
    st.write("Grouped content inside a container")

placeholder = st.empty()
placeholder.text("Initial text")
# Later: placeholder.text("Updated text") or placeholder.empty()
```

---

## State Management

```python
import streamlit as st

# Streamlit re-runs the entire script on every interaction
# session_state persists data across re-runs

if "counter" not in st.session_state:
    st.session_state.counter = 0  # initialize on first load

st.title(f"Counter: {st.session_state.counter}")

if st.button("Increment"):
    st.session_state.counter += 1
    st.rerun()

if st.button("Reset"):
    st.session_state.counter = 0
    st.rerun()
```

```python
import streamlit as st

# Using session state with widgets via the key parameter
st.text_input("Your name", key="user_name")
# Access: st.session_state.user_name

# Callback functions with session state
def on_change():
    st.session_state.processed = st.session_state.raw_input.upper()

st.text_input("Enter text", key="raw_input", on_change=on_change)

if "processed" in st.session_state:
    st.write(f"Processed: {st.session_state.processed}")
```

---

## Caching

```python
import streamlit as st
import pandas as pd
import time

# @st.cache_data caches return values (for data transformations, API calls)
@st.cache_data
def load_data(url):
    time.sleep(3)  # simulate slow data loading
    df = pd.read_csv(url)
    return df

# First call takes 3 seconds; subsequent calls are instant
df = load_data("https://example.com/data.csv")

# Cache with TTL (time-to-live)
@st.cache_data(ttl=3600)  # expires after 1 hour
def fetch_live_data():
    return pd.DataFrame({"value": [42]})
```

```python
import streamlit as st

# @st.cache_resource caches shared objects (ML models, DB connections)
@st.cache_resource
def load_model():
    # Load a heavy ML model only once, shared across all users
    return {"model": "loaded"}

model = load_model()

# cache_data: serializes return value, each caller gets a copy
# cache_resource: stores object directly, all callers share the same instance

# Clear caches manually:
# st.cache_data.clear()
# st.cache_resource.clear()
```

---

## Data Visualization

```python
import streamlit as st
import pandas as pd
import numpy as np

# Built-in charts
data = pd.DataFrame(np.random.randn(50, 3), columns=["A", "B", "C"])
st.line_chart(data)
st.area_chart(data)
st.bar_chart(data.head(10))

# Map visualization
map_data = pd.DataFrame({
    "lat": np.random.uniform(37.7, 37.8, 100),
    "lon": np.random.uniform(-122.5, -122.4, 100)
})
st.map(map_data)
```

```python
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Matplotlib integration
fig, ax = plt.subplots(figsize=(10, 5))
x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x), label="sin(x)")
ax.plot(x, np.cos(x), label="cos(x)")
ax.set_title("Trigonometric Functions")
ax.legend()
st.pyplot(fig)
```

```python
import streamlit as st
import plotly.express as px

# Plotly integration for interactive charts
df = px.data.gapminder()
fig = px.scatter(
    df.query("year == 2007"), x="gdpPercap", y="lifeExp",
    size="pop", color="continent", hover_name="country",
    log_x=True, title="GDP vs Life Expectancy (2007)"
)
st.plotly_chart(fig, use_container_width=True)
```

---

## Forms

```python
import streamlit as st

# Forms batch widget values and submit them all at once
with st.form("my_form"):
    st.header("Registration Form")
    name = st.text_input("Name")
    email = st.text_input("Email")
    age = st.slider("Age", 18, 100, 25)
    agree = st.checkbox("I agree to the terms")

    submitted = st.form_submit_button("Submit")
    if submitted:
        if not agree:
            st.error("You must agree to the terms!")
        else:
            st.success(f"Welcome, {name}!")

# Form with clear_on_submit
with st.form("search_form", clear_on_submit=True):
    query = st.text_input("Search query")
    submitted = st.form_submit_button("Search")
    if submitted and query:
        st.write(f"Searching for '{query}'")
```

---

## Deployment

```python
# Deploying to Streamlit Community Cloud (free hosting)
# 1. Push code to a public GitHub repository
# Required files: app.py, requirements.txt
# 2. Go to share.streamlit.io, connect GitHub
# 3. Select repository, branch, and main file
# 4. Click "Deploy"
# App available at: https://<your-app-name>.streamlit.app
```

```python
# Secrets management
# Create .streamlit/secrets.toml (add to .gitignore!)
# [database]
# host = "localhost"
# password = "mysecret"

# Access in your app:
import streamlit as st
# db_host = st.secrets["database"]["host"]

# On Streamlit Community Cloud, set secrets in the app settings UI
```

---

## Practice Exercises

1. **Data Explorer**: Build an app that lets users upload a CSV file, displays the data, shows summary statistics, and provides interactive filters.

2. **Dashboard**: Create a dashboard with sidebar navigation, multiple tabs, and visualizations using Streamlit charts and Plotly.

3. **ML Predictor**: Build an app that loads a pre-trained model (cached), accepts user input via widgets, and displays predictions.

4. **Form Application**: Create a multi-step form using session state to track progress across pages.

---

## Summary

Streamlit is a Python framework for building interactive data applications with minimal code. Key takeaways:

- `st.write()` is the universal display function for text, data, and charts
- Input widgets (buttons, sliders, selectboxes, file uploaders) provide user interactivity
- Layout components (columns, sidebar, tabs, expanders) organize content effectively
- `st.session_state` persists data across script re-runs for stateful applications
- `@st.cache_data` caches data transformations; `@st.cache_resource` caches shared objects
- Built-in chart support plus Matplotlib and Plotly integration cover visualization needs
- Forms batch widget interactions to prevent unnecessary re-runs
- Deployment to Streamlit Community Cloud is free and straightforward

---

## Next Steps

- Explore Streamlit's multi-page app architecture
- Learn about custom components for extending Streamlit
- Study Streamlit's connection API for databases
- Investigate st.experimental features for advanced use cases
- Explore integration with LangChain for LLM-powered applications

---

## Additional Resources

- [Streamlit Official Documentation](https://docs.streamlit.io/)
- [Streamlit GitHub Repository](https://github.com/streamlit/streamlit)
- [Streamlit Gallery](https://streamlit.io/gallery)
- [Streamlit Community Cloud](https://share.streamlit.io/)
- [Streamlit Cheat Sheet](https://docs.streamlit.io/library/cheatsheet)
