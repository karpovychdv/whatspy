import json
import os
from typing import Optional

from playwright.sync_api import sync_playwright, Page, Browser


class ChatMessage:
    def __init__(self, uid: str, text: str, sender: str, timestamp: str):
        self.uid = uid
        self.text = text
        self.sender = sender
        self.timestamp = timestamp

    def __repr__(self):
        return f"ChatMessage({self.uid}, {self.sender}, {self.timestamp}, {self.text})"

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "text": self.text,
            "sender": self.sender,
            "uid": self.uid,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data["uid"], data["text"], data["sender"], data["timestamp"])

    def __eq__(self, other):
        return self.uid == other.uid

    def __hash__(self):
        return hash(self.uid)


def find_whatsapp_page(browser: Browser) -> Optional[Page]:
    for context in browser.contexts:
        for page in context.pages:
            if "web.whatsapp.com" in page.url:
                return page
    return None


def check_page(page: Page):
    # check if the page has `#main` element
    main_element = page.query_selector("#main")
    if main_element is None:
        print("Main element not found")
        return False

    # check if the page has at least one `[role="row"]` elements
    rows = page.query_selector_all('[role="row"]')
    if len(rows) == 0:
        return False

    return True


def get_messages(page: Page) -> list[ChatMessage]:
    message_els = page.query_selector_all('[role="row"]')
    messages = []
    for message in message_els:
        # get `.copyable-text` element
        copyable_text = message.query_selector('.copyable-text')
        if copyable_text is None:
            continue
        # get the text of the message
        text = copyable_text.inner_text()

        # get data-pre-plain-text attribute with value like `[6:34 pm, 01/03/2024] Dmytro Karpovych: `
        pre_plain_text = copyable_text.get_attribute('data-pre-plain-text')
        if pre_plain_text is None:
            continue
        # split the string by `]` and get the last part
        sender = pre_plain_text.split(']')[-1].strip(': ')

        # get the date from the attribute
        date = pre_plain_text.split(']')[0].split(', ')[-1]

        # get the time from the attribute
        time = pre_plain_text.split(']')[0].split(', ')[0].strip('[')

        timestamp = f"{date} {time}"

        # get the uid of the message
        uid = message.query_selector('[data-id]').get_attribute('data-id')

        messages.append(ChatMessage(uid, text, sender, timestamp))

    return messages


def read_from_log(log_file_path):
    if not os.path.exists(log_file_path):
        return []

    with open(log_file_path, 'r') as file:
        lines = file.readlines()
    messages = []
    for line in lines:
        if not line.strip():
            continue
        data = json.loads(line)
        messages.append(ChatMessage.from_dict(data))
    return messages


def on_new_message(message: ChatMessage):
    print("New message:", message)
    print('@TODO: doing something useful with the message')


def track_whatsapp(browser: Browser, check_timeout=1000, log_file_path='last_messages_log.jsonl'):
    page = find_whatsapp_page(browser)
    if page is None:
        print("WhatsApp page not found")
        return

    # Select page as active
    # page.bring_to_front()

    # Print the title of the page.
    print('title:', page.title())
    # Print the URL of the page.
    print('url:', page.url)

    if not check_page(page):
        print("Chat is not open.")
        return

    existing_messages = read_from_log(log_file_path)

    while True:
        chat_messages = get_messages(page)

        new_messages = [message for message in chat_messages if message not in existing_messages]

        if new_messages:
            with open(log_file_path, 'a') as file:
                for message in new_messages:
                    file.write(json.dumps(message.to_dict(), ensure_ascii=False) + '\n')
                    existing_messages.append(message)
                    on_new_message(message)

        # Wait for new messages
        page.wait_for_timeout(check_timeout)


def main():
    # Start a new session with Playwright using the sync_playwright function.
    with sync_playwright() as playwright:
        cdp_endpoint = "http://localhost:21220"
        # Connect to an existing instance of Chrome using the connect_over_cdp method.
        browser = playwright.chromium.connect_over_cdp(endpoint_url=cdp_endpoint)

        track_whatsapp(browser)


if __name__ == "__main__":
    main()
