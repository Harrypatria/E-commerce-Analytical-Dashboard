import reflex as rx
from app.components.auth_components import input_1, button_1
from app.states.auth_state import AuthState


def registration_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Create an Account", class_name="text-3xl font-bold text-gray-900"
                ),
                rx.el.p(
                    "Join us and start analyzing your data.", class_name="text-gray-500"
                ),
                class_name="text-center",
            ),
            rx.el.form(
                rx.el.div(
                    input_1(label="Username", type="text", field_name="username"),
                    input_1(label="Password", type="password", field_name="password"),
                    input_1(
                        label="Confirm Password",
                        type="password",
                        field_name="confirm_password",
                    ),
                    class_name="flex flex-col gap-4",
                ),
                button_1(
                    text="Create Account",
                    is_loading=AuthState.is_loading,
                    type_="submit",
                ),
                on_submit=AuthState.register,
                class_name="flex flex-col gap-6",
            ),
            rx.el.p(
                "Already have an account? ",
                rx.el.a(
                    "Log In",
                    href="/login",
                    class_name="font-semibold text-violet-600 hover:underline",
                ),
                class_name="text-center text-sm text-gray-600",
            ),
            class_name="flex flex-col gap-8 bg-white p-8 rounded-xl shadow-lg w-full max-w-md",
        ),
        class_name="flex min-h-screen items-center justify-center bg-gray-50 font-['Lato'] p-4",
    )