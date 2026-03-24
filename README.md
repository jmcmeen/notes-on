# notes-on

A personal collection of introductory notes on programming languages, tools, frameworks, and concepts I use in my work. Each note covers fundamentals with code examples, practical patterns, and exercises.

The notes are plain Markdown files in the `notes/` directory — browse them directly on GitHub or read them locally.

## Web View

The repo includes a self-hosted documentation site powered by [MkDocs Material](https://squidfunnel.github.io/mkdocs-material/) with full-text search, dark mode, syntax highlighting, and download options (MD/HTML/PDF per note or as a bundle).

```bash
docker compose up --build
# Open http://localhost:8080
```

---

## Notes

### Programming Languages

- [C Intro](notes/c_intro_notes.md) - Low-level, general-purpose procedural language used for systems programming, operating systems, and embedded systems
- [C# Intro](notes/csharp_intro_notes.md) - Modern, object-oriented language by Microsoft, used for Windows apps, game development (Unity), and web services
- [C++ Intro](notes/cpp_intro_notes.md) - Extension of C with object-oriented features, used for game engines, systems software, and high-performance applications
- [Java Intro](notes/java_intro_notes.md) - Platform-independent, object-oriented language used for enterprise backends, Android apps, and large-scale systems
- [JavaScript Intro](notes/javascript_intro_notes.md) - Dynamic scripting language for web browsers and server-side (Node.js), powering interactive web applications
- [PHP Intro](notes/php_intro_notes.md) - Server-side scripting language widely used for web development and content management systems like WordPress
- [Python Intro](notes/python_intro_notes.md) - High-level, general-purpose language popular for data science, scripting, web development, and automation
- [Ruby Intro](notes/ruby_intro_notes.md) - Dynamic, object-oriented language focused on simplicity and productivity, known for the Ruby on Rails web framework
- [VB.NET Intro](notes/vbnet_intro_notes.md) - Object-oriented language on the .NET platform, used for Windows desktop applications and enterprise tooling
- [x64 Assembly Intro](notes/x64_assembly_intro_notes.md) - Low-level programming language for x86-64 processors, used for performance-critical code and systems programming

### Agentic Programming

- [Claude Code and Skills](notes/claude_code.md) - Anthropic's CLI tool for AI-assisted software development with skills, hooks, and MCP integration
- [LLM Application Engineering](notes/llm_application_engineering.md) - Patterns and practices for building production applications powered by large language models
- [Prompt Engineering](notes/prompt_engineering.md) - Techniques for designing effective prompts to guide LLM behavior and output quality
- [RAG](notes/rag.md) - Retrieval-Augmented Generation — architecture pattern combining search/retrieval with LLM generation

### Data Science & Analysis

- [HDBSCAN](notes/hdbscan.md) - Hierarchical density-based clustering algorithm that finds clusters of varying densities in high-dimensional data
- [Jupyter](notes/jupyter.md) - Interactive computing environment for creating notebooks combining live code, equations, visualizations, and text
- [Matplotlib](notes/matplotlib.md) - Comprehensive Python plotting library for creating static, animated, and interactive visualizations
- [NumPy](notes/numpy.md) - Fundamental Python library for numerical computing with support for large multi-dimensional arrays and matrices
- [Pandas](notes/pandas.md) - Python library for data manipulation and analysis, providing DataFrames for structured data operations
- [SciPy](notes/scipy.md) - Scientific computing library building on NumPy, providing optimization, integration, interpolation, and statistics
- [scikit-learn](notes/scikit_learn.md) - Machine learning library providing classification, regression, clustering, and preprocessing tools
- [UMAP](notes/umap.md) - Uniform Manifold Approximation and Projection — dimensionality reduction technique for visualization and clustering

### Geospatial

- [Folium](notes/folium.md) - Python library for creating interactive Leaflet.js maps with markers, choropleths, and GeoJSON layers
- [GeoPandas](notes/geopandas.md) - Python library extending Pandas with geospatial data types and operations for geographic analysis
- [PostGIS](notes/postgis.md) - Spatial database extension for PostgreSQL, enabling geographic queries, spatial indexing, and GIS operations
- [pyinaturalist](notes/pyinaturalist.md) - Python client for the iNaturalist API, enabling access to biodiversity observations and species data

### Frameworks & APIs

- [Airflow](notes/airflow.md) - Platform for programmatically authoring, scheduling, and monitoring data pipeline workflows
- [CUDA](notes/cuda.md) - NVIDIA's parallel computing platform for GPU-accelerated computing in scientific and ML workloads
- [FastAPI](notes/fastapi.md) - Modern, high-performance Python web framework for building APIs with automatic OpenAPI documentation
- [Flask](notes/flask.md) - Lightweight Python web framework for building web applications and REST APIs with minimal boilerplate
- [Gradio](notes/gradio.md) - Python library for quickly building interactive web demos and UIs for ML models
- [HuggingFace](notes/huggingface.md) - Open-source ML platform providing pre-trained models, datasets, and tools for NLP, computer vision, and more
- [HuggingFace Datasets](notes/huggingface_datasets.md) - Library for efficiently loading, processing, and sharing datasets for ML model training and evaluation
- [HuggingFace Transformers](notes/huggingface_transformers.md) - Python library providing thousands of pre-trained transformer models for NLP, vision, and audio tasks
- [Keras](notes/keras.md) - High-level neural network API providing a simple interface for building and training deep learning models
- [ML.NET](notes/mlnet.md) - Cross-platform ML framework for .NET, enabling model training and deployment in C# applications
- [MLflow](notes/mlflow.md) - Open-source platform for managing the ML lifecycle including experiment tracking, model registry, and deployment
- [OpenCLIP](notes/openclip.md) - Open-source implementation of OpenAI's CLIP model for connecting images and text through contrastive learning
- [OpenCV](notes/opencv.md) - Open-source computer vision library with tools for image processing, object detection, and video analysis
- [Pydantic](notes/pydantic.md) - Python data validation library using type annotations for parsing, serialization, and schema enforcement
- [PyTorch](notes/pytorch.md) - Open-source deep learning framework by Meta with dynamic computation graphs, popular in research
- [Streamlit](notes/streamlit.md) - Python framework for rapidly creating data apps and dashboards with minimal frontend code
- [TensorFlow](notes/tensorflow.md) - Google's open-source ML framework for building and deploying models at scale across platforms

### Databases

- [MySQL and MariaDB](notes/mysql_mariadb.md) - Popular open-source relational databases — MySQL and its community fork MariaDB — widely used in web applications
- [Oracle Database](notes/oracle.md) - Enterprise-grade relational database known for scalability, reliability, and advanced features for large organizations
- [PostgreSQL](notes/postgresql.md) - Advanced open-source relational database with strong standards compliance, extensibility, and geospatial support
- [SQL Server](notes/sql_server.md) - Microsoft's enterprise relational database system with integrated analytics, reporting, and BI tools
- [SQLite](notes/sqlite.md) - Lightweight, serverless, file-based relational database engine embedded directly into applications

### DevOps & Infrastructure

- [Bash and Shell Scripting](notes/bash_shell.md) - Unix command-line shell and scripting language for automating tasks and system administration
- [Docker](notes/docker.md) - Containerization platform for packaging applications and dependencies into portable, isolated containers
- [Git](notes/git.md) - Distributed version control system for tracking changes in source code during software development
- [GitHub](notes/github.md) - Cloud-based platform for Git repository hosting, collaboration, code review, and project management
- [GitHub Actions](notes/github_actions.md) - CI/CD and workflow automation platform integrated into GitHub for building, testing, and deploying code
- [GitLab](notes/gitlab.md) - DevOps platform providing Git repository management, CI/CD pipelines, and project planning tools
- [Grafana](notes/grafana.md) - Open-source observability platform for monitoring, visualizing metrics, and alerting on system data
- [Linux and Unix](notes/linux_unix.md) - Open-source operating system family — fundamentals of the command line, file system, and administration
- [Windows Administration](notes/windows.md) - Microsoft operating system — developer-focused administration, PowerShell, WSL, and environment setup

### Audio & Signal Processing

- [audiomentations](notes/audiomentations.md) - Audio data augmentation library for applying transformations to training data in ML pipelines
- [librosa](notes/librosa.md) - Python library for audio and music analysis including feature extraction, spectrograms, and beat tracking
- [OpenSoundscape](notes/opensoundscape.md) - Python library for bioacoustics analysis — automated classification and detection of wildlife sounds
- [pydub](notes/pydub.md) - Simple Python library for audio manipulation — slicing, concatenating, exporting, and applying effects
- [sounddevice](notes/sounddevice.md) - Python library for recording and playing audio using PortAudio, providing real-time audio I/O
- [SoundFile](notes/soundfile.md) - Python library for reading and writing sound files (WAV, FLAC, OGG) based on libsndfile
- [torchaudio](notes/torchaudio.md) - PyTorch-based library for audio processing, transformations, and pre-trained models for audio tasks
