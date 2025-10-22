import reflex as rx
from app.state import ChatState, ChatMessage


def message_bubble(message: ChatMessage) -> rx.Component:
    is_user = message["role"] == "user"
    return rx.el.div(
        rx.el.div(
            rx.el.p(message["content"], class_name="text-sm"),
            rx.el.span(
                message["timestamp"], class_name="text-xs text-gray-400 mt-1 self-end"
            ),
            class_name=rx.cond(
                is_user,
                "bg-violet-600 text-white rounded-t-lg rounded-bl-lg p-3 max-w-sm",
                "bg-gray-200 text-gray-800 rounded-t-lg rounded-br-lg p-3 max-w-sm",
            ),
        ),
        class_name=rx.cond(
            is_user, "flex justify-end w-full", "flex justify-start w-full"
        ),
    )


def query_suggestion_button(suggestion: str) -> rx.Component:
    return rx.el.button(
        suggestion,
        on_click=lambda: ChatState.handle_suggestion_click(suggestion),
        class_name="px-3 py-1.5 text-xs text-violet-700 bg-violet-100 rounded-full hover:bg-violet-200 transition-colors",
    )


def chatbot() -> rx.Component:
    """The AI chatbot component."""
    return rx.el.div(
        rx.cond(
            ChatState.is_chat_open,
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Analytics Assistant",
                            class_name="font-semibold text-gray-800",
                        ),
                        rx.el.p(
                            "Ask me about your data", class_name="text-xs text-gray-500"
                        ),
                        class_name="flex-1",
                    ),
                    rx.el.button(
                        rx.icon("x", class_name="h-5 w-5"),
                        on_click=ChatState.toggle_chat,
                        class_name="p-2 rounded-full hover:bg-gray-100",
                    ),
                    class_name="flex items-center justify-between border-b p-4",
                ),
                rx.el.div(
                    rx.foreach(ChatState.messages, message_bubble),
                    rx.cond(
                        ChatState.is_processing,
                        rx.el.div(
                            rx.spinner(class_name="h-5 w-5 text-violet-600"),
                            class_name="flex justify-center p-4",
                        ),
                        None,
                    ),
                    class_name="flex-1 flex flex-col gap-4 p-4 overflow-y-auto",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.foreach(
                            ChatState.query_suggestions, query_suggestion_button
                        ),
                        class_name="flex flex-wrap gap-2 mb-2",
                    ),
                    rx.el.form(
                        rx.el.input(
                            placeholder="Type your question...",
                            name="query",
                            class_name="flex-1 bg-transparent focus:outline-none text-sm",
                            default_value=ChatState.current_input,
                        ),
                        rx.el.button(
                            rx.icon("send", class_name="h-5 w-5 text-white"),
                            type_="submit",
                            class_name="p-2 bg-violet-600 rounded-full hover:bg-violet-700 disabled:opacity-50",
                            disabled=ChatState.is_processing
                            | (ChatState.current_input.strip() == ""),
                        ),
                        on_submit=ChatState.handle_submit,
                        reset_on_submit=True,
                        class_name="flex items-center border rounded-lg p-2",
                    ),
                    class_name="border-t p-4 bg-white",
                ),
                class_name="flex flex-col bg-white rounded-lg shadow-2xl w-96 h-[600px]",
            ),
            rx.el.button(
                rx.icon("message-circle", class_name="h-6 w-6 text-white"),
                on_click=ChatState.toggle_chat,
                class_name="p-4 bg-violet-600 rounded-full shadow-lg hover:bg-violet-700 transition-transform hover:scale-110",
            ),
        ),
        class_name="fixed bottom-8 right-8 z-50",
    )