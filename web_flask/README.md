# Flask Web Application

This is a Flask web application that implements various routes to display different messages and HTML pages. It serves as an example project to demonstrate the usage of Flask and its route handling capabilities.

## Requirements

- Python 3.4.3 or later
- Flask

## Getting Started

To run the web application, follow these steps:

1. Clone the repository or download the project files.
2. Install Flask if it's not already installed. You can use the following command: $ pip install flask
3. Make the main script executable: $ chmod +x <script_name>.py
4. Run the Flask web application: $ ./<script_name>.py

The web application will start and be accessible at `http://0.0.0.0:5000/`.

## Routes

The following routes are available in the web application:

- `/`: Displays "Hello HBNB!"
- `/hbnb`: Displays "HBNB"
- `/c/<text>`: Displays "C ", followed by the value of the text variable (replace underscores (_) with spaces)
- `/python/(<text>)`: Displays "Python ", followed by the value of the text variable (replace underscores (_) with spaces). The default value of text is "is cool".
- `/number/<n>`: Displays "n is a number" only if n is an integer.
- `/number_template/<n>`: Displays an HTML page only if n is an integer. The page contains an H1 tag with the text "Number: n".
- `/number_odd_or_even/<n>`: Displays an HTML page indicating if n is even or odd. The page contains an H1 tag with the text "Number: n is even" for even values of n, or "Number: n is odd" for odd values of n.

## Project Structure

The project structure is as follows:

- `<script_name>.py`: The main Python script that starts the Flask web application and defines the routes.
- `templates/`: A directory containing HTML templates used by the Flask application.
- `5-number.html`: HTML template for the `/number_template/<n>` route.
- `6-number_odd_or_even.html`: HTML template for the `/number_odd_or_even/<n>` route.

## Notes

- This project adheres to the PEP 8 style guide.
- The Flask web application listens on `0.0.0.0` and port `5000`.
- The option `strict_slashes=False` is used in route definitions to allow routes with or without trailing slashes.

Feel free to explore the routes and experiment with different inputs to see the corresponding outputs.

Enjoy!
