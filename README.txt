Newegg Price Tracker

A Python script that tracks product prices on Newegg and sends email notifications when prices drop below your target price.

## Features:
- Automated price tracking for any Newegg product
- Email notifications when price drops below target
- Configurable checking intervals
- Headless browser operation (runs in background)
- Secure credential handling using environment variables

## Before Starting make sure to have:
- Python 3.x
- Google Chrome browser
- ChromeDriver (matching your Chrome version)
- Gmail account with App Password set up

## Installation:

1. Clone or download this repository
2. Create a virtual environment:

python -m venv venv

# For Windows (What I used):
venv\Scripts\activate

3. Install required packages:

pip install beautifulsoup4 selenium requests python-dotenv


4. Create a `.env` file in the project root with your email credentials:

SENDER_EMAIL=your_email@gmail.com
EMAIL_APP_PASSWORD=your_gmail_app_password
RECEIVER_EMAIL=your_email@gmail.com


## Usage

1. Open `newegg-tracker.py`
2. Modify the following variables:

   url = "your_newegg_product_url"
   target_price = your_desired_price  # e.g., 399.99


3. Run the script:

python newegg-tracker.py


4. The script will:
   - Check the price at regular intervals
   - Print the current price in the console
   - Send an email when the price drops below your target

## Customizing Check Intervals:

Modify the `check_interval` parameter to change how often the price is checked:

# Check every hour example: (3600 seconds)
tracker.track_price(check_interval=3600)


## Troubleshooting:

1. **ChromeDriver Issues**:
   - Make sure ChromeDriver matches your Chrome browser version
   - Verify ChromeDriver is in your system PATH

2. **Email Issues**:
   - Confirm your Gmail App Password is correct
   - Check if 2-Factor Authentication is enabled
   - Verify your `.env` file contains correct credentials


## Notes:
- The script uses a headless browser, so no window will pop up
- Price checks are done silently in the background
- Press Ctrl+C to stop the script
- The script will continue running until manually stopped

## Security:
- Never commit your `.env` file to version control
- Keep your email credentials secure
- Use the included `.gitignore` file to prevent sensitive data from being shared

## Contributing:
Feel free to fork this repository and make improvements!
This implementation currently tracks prices for the Ryzen 7 7800x3d CPU, change the values mentioned in this document to fit your needs!