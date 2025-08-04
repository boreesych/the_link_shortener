This is a simple web-based URL shortener built using Python and the Flask web framework. Users can input long URLs and receive short, shareable links that redirect to the original address.

This project is an example of a final assignment for students learning the basics of Python and web development.
It introduces key backend concepts such as routing, form handling, HTTP methods, and data storage using Flask.

### How to Run the Project

1. **Clone the repository and navigate to the project directory:**
    ```
    git clone <repository_url>
    cd the_link_shortener
    ```

2. **Create and activate a virtual environment:**
    ```
    python3 -m venv venv
    ```
    - On Linux/macOS:
        ```
        source venv/bin/activate
        ```
    - On Windows:
        ```
        source venv/scripts/activate
        ```

3. **Upgrade pip and install dependencies:**
    ```
    python3 -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

4. **Create a `.env` file in the project directory with the following content:**
    ```
    FLASK_APP=yacut
    FLASK_ENV=development
    SECRET_KEY=your_secret_key
    DB=sqlite:///db.sqlite3
    ```

5. **Initialize the database and apply migrations:**
    ```
    flask db upgrade
    ```

6. **Run the project:**
    ```
    flask run
    ```
