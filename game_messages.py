import textwrap


class Message:
    def __init__(self, text, color=(255, 255, 255)):
        self.text = text
        self.color = color


class MessageLog:
    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height

    def add_message(self, message):
        # splits messages over multiple lines if needed
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in new_msg_lines:
            # remove the top line if necessary to make room for new ones
            if len(self.messages) == self.height:
                del self.messages[0]

            # add new line as a message object
            self.messages.append(Message(line, message.color))