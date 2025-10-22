import reflex as rx
from typing import Literal


def input_1(
    label: str, type: Literal["text", "password", "email"], field_name: str
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label, class_name="text-sm font-medium text-gray-700", html_for=field_name
        ),
        rx.el.input(
            type=type,
            id=field_name,
            name=field_name,
            class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-violet-500 focus:border-violet-500 sm:text-sm",
            required=True,
        ),
        class_name="w-full",
    )


def button_1(text: str, is_loading: rx.Var[bool], type_: str) -> rx.Component:
    return rx.el.button(
        rx.cond(
            is_loading, rx.spinner(class_name="h-5 w-5 text-white"), rx.el.span(text)
        ),
        type=type_,
        disabled=is_loading,
        class_name="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-violet-600 hover:bg-violet-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500 disabled:opacity-50",
    )