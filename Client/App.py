import customtkinter
import os
from PIL import Image
import asyncio

from Client.app_requests import get_token

user = "lev"


async def parallel_print():
    while True:
        await asyncio.sleep(1)
        print("rprprppr")


class ScrollableChatsFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.label_list = []
        self.button_list = []

    def add_item(self, item, image=None):
        button = customtkinter.CTkButton(self, text="Command", width=300, height=50)
        if self.command is not None:
            button.configure(command=lambda: self.command(item))
        button.grid(row=len(self.button_list), column=0, pady=(0, 10), padx=5)
        self.button_list.append(button)

    def remove_item(self, item):
        for label, button in zip(self.label_list, self.button_list):
            if item == label.cget("text"):
                label.destroy()
                button.destroy()
                self.label_list.remove(label)
                self.button_list.remove(button)
                return


class ScrollableMessagesFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.messages_list = []

    def add_message(self, item, image=None):
        label = customtkinter.CTkLabel(self, text=item, image=image, compound="left", padx=5, anchor="w", bg_color="blue")
        label.grid(row=len(self.messages_list), column=0, pady=(0, 10), sticky="w")
        self.messages_list.append(label)

    def remove_message(self, item):
        for message in self.messages_list:
            if item == message.cget("text"):
                message.destroy()
                self.messages_list.remove(message)
                return


class App(customtkinter.CTk):
    def __init__(self, loop):
        super().__init__()

        self.loop = loop

        self.title("CTkScrollableFrame example")
        self.grid_rowconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.resizable(width=False, height=True)

        # create scrollable label and button frame
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.scrollable_label_button_frame = ScrollableChatsFrame(master=self, width=300, command=self.label_button_frame_event, corner_radius=0)
        self.scrollable_label_button_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        for i in range(20):  # add items with images
            self.scrollable_label_button_frame.add_item(f"image and item {i}", image=customtkinter.CTkImage(Image.open(os.path.join(current_dir, "images", "chat_light.png"))))

        self.scrollable_label_button_frame2 = ScrollableMessagesFrame(master=self, width=1000, command=self.label_button_frame_event, corner_radius=0)
        self.scrollable_label_button_frame2.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
        for i in range(20):
            self.scrollable_label_button_frame2.add_message("message")

    def label_button_frame_event(self, item):
        pass


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    customtkinter.set_appearance_mode("dark")
    app = App(loop)
    loop.run_until_complete(get_token("lev", "lev"))
    loop.run_until_complete(app.mainloop())