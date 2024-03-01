# WhatSpy (WhatsApp Message Logger)

This project is a Python application that logs WhatsApp messages from a web browser session.
It uses the Playwright library to interact with the browser and extract message data.

## Features

- Connects to an existing browser session
- Finds the WhatsApp web page
- Extracts and logs new messages
- Handles new messages with a customizable function

## Requirements

- Python 3.8 or higher
- Playwright Python library
- An active WhatsApp Web session

## Setup

1. Clone the repository
2. Install the required Python libraries using pip:

```bash
pip install -r requirements.txt
```

3. Install the browser (if needed):

```bash
playwright install
````

4. Customize the `on_new_message` function in the `main.py` file to handle new messages

5. Run the script:

```bash
python main.py
```

## Usage

The script will connect to an existing browser session and start logging new WhatsApp messages.
The messages are logged in the `last_messages_log.jsonl` file.

You can customize the `on_new_message` function in the `main.py` file to handle new messages in a way that suits your
needs.

## Limitations

- The script can only connect to an existing browser session.
- The script can only log messages from the currently active chat.
- The script does not handle media messages.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
