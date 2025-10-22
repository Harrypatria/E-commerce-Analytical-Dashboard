import reflex as rx
from app.components.sidebar import sidebar
from app.components.header import header
from app.components.footer import footer
from app.state import DashboardState
from app.components.chatbot import chatbot


def main_layout(child: rx.Component) -> rx.Component:
    """The main layout for the dashboard, including sidebar, header, and footer."""
    return rx.el.div(
        sidebar(),
        rx.el.div(
            header(),
            rx.el.main(
                rx.cond(
                    DashboardState.is_loading,
                    rx.el.div(
                        rx.spinner(class_name="h-12 w-12 text-violet-600"),
                        rx.el.p(
                            "Loading Superstore Data...",
                            class_name="mt-4 text-gray-600 font-medium",
                        ),
                        class_name="flex flex-col items-center justify-center h-full",
                    ),
                    child,
                ),
                class_name="flex-1 overflow-y-auto p-6 bg-gray-50",
            ),
            footer(),
            class_name="flex flex-col flex-1 min-h-screen",
        ),
        chatbot(),
        class_name="flex min-h-screen w-full bg-white font-['Lato']",
    )