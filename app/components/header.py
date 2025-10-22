import reflex as rx
from app.states.auth_state import AuthState


def user_menu() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.image(src=AuthState.user_avatar, class_name="h-8 w-8 rounded-full"),
            on_click=AuthState.toggle_user_menu,
            class_name="rounded-full",
        ),
        rx.cond(
            AuthState.is_user_menu_open,
            rx.el.div(
                rx.cond(
                    AuthState.is_authenticated,
                    rx.el.div(
                        rx.el.a(
                            "My Account",
                            href="#",
                            class_name="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100",
                        ),
                        rx.el.button(
                            "Logout",
                            on_click=AuthState.logout,
                            class_name="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100",
                        ),
                    ),
                    rx.el.div(
                        rx.el.a(
                            "Login",
                            href="/login",
                            class_name="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100",
                        ),
                        rx.el.a(
                            "Register",
                            href="/register",
                            class_name="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100",
                        ),
                    ),
                ),
                class_name="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-20",
            ),
        ),
        class_name="relative",
    )


def header() -> rx.Component:
    """The header component for the dashboard."""
    return rx.el.header(
        rx.el.div(),
        rx.el.div(class_name="flex-1"),
        rx.el.div(
            rx.el.button(
                rx.icon("bell", class_name="h-5 w-5"),
                class_name="rounded-full p-2 hover:bg-gray-100",
            ),
            user_menu(),
            class_name="flex items-center gap-4",
        ),
        class_name="sticky top-0 z-10 flex h-16 items-center justify-between border-b bg-white/50 px-6 backdrop-blur-sm",
    )