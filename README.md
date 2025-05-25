# Python CherryPy Application

## Description

This project is a Python application built with the CherryPy framework. It is a conversion from an original PHP MiniFramework project, aiming to replicate its core functionalities and structure in a Python environment.

## Project Structure

The main application code is located within the `python_app` directory:

```
python_app/
├── app.py                # Main application entry point (starts CherryPy server)
├── requirements.txt      # Python package dependencies
├── config/               # Configuration files
│   └── settings.py       # Application and CherryPy configurations
├── controllers/          # Handles incoming web requests and business logic
│   ├── __init__.py
│   ├── api_controller.py   # API specific controllers
│   ├── error_controller.py # Error handling controller
│   ├── example_controller.py # Example controller
│   ├── index_controller.py # Main index/root controller
│   └── root.py             # Initial root controller (can be merged or used for specific root paths)
├── models/               # Data models and database interaction logic
│   ├── __init__.py
│   └── info_model.py       # Example model
├── static/               # Static assets (CSS, JavaScript, images)
│   ├── css/
│   ├── js/
│   ├── img/
│   └── uploads/
├── tests/                # Unit and integration tests
│   ├── __init__.py
│   └── test_controllers.py # Example tests for controllers
├── utils.py              # Utility functions converted from PHP helper functions
└── views/                # Jinja2 templates for rendering HTML
    ├── __init__.py
    ├── error/
    ├── example/
    ├── index/
    └── layouts/          # Base layout templates (e.g., default.html, header.html)
```

## Setup and Installation

### Prerequisites
*   Python 3 (Python 3.8+ recommended)

### Steps

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    ```
    Activate the virtual environment:
    *   On Linux/macOS:
        ```bash
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        venv\Scripts\activate
        ```

3.  **Install dependencies:**
    Navigate to the project root directory (where this README is located) and run:
    ```bash
    pip install -r python_app/requirements.txt
    ```
    The `python_app/requirements.txt` file should contain `CherryPy` and any other necessary packages.

## Running the Application

1.  **Start the CherryPy server:**
    Ensure your virtual environment is activated. From the project root directory, run:
    ```bash
    python python_app/app.py
    ```

2.  **Access the application:**
    The application will typically be available at: `http://0.0.0.0:8080` (or `http://localhost:8080`).
    This is based on the default configuration in `python_app/config/settings.py` and `python_app/app.py`.

## Running Tests

1.  **Execute unit tests:**
    Ensure your virtual environment is activated. To run the example controller tests, from the project root directory:
    ```bash
    python -m unittest python_app/tests/test_controllers.py
    ```
    For a more general approach to discover and run all tests within the `python_app/tests` directory:
    ```bash
    python -m unittest discover python_app/tests
    ```

---
This README provides the basic setup and operational instructions for the converted Python CherryPy application.
