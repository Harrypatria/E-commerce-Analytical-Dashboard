import reflex as rx


def footer() -> rx.Component:
    """The footer component."""
    return rx.el.footer(
        rx.el.p("Made by Patria & Co. 2025", class_name="text-sm text-gray-500"),
        rx.el.a(
            "www.patriaco.id",
            href="http://www.patriaco.id",
            target="_blank",
            class_name="text-sm text-violet-600 hover:underline",
        ),
        class_name="flex items-center justify-between border-t bg-white px-6 py-4 mt-auto",
    )