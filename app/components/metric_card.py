import reflex as rx


def metric_card(
    title: str, value: rx.Var[str | int | float], icon_name: str, color: str
) -> rx.Component:
    """A card component to display a key metric."""
    return rx.el.div(
        rx.el.div(
            rx.icon(icon_name, class_name=f"h-6 w-6 {color}"),
            class_name="p-3 bg-gray-100 rounded-lg",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
            rx.el.p(value, class_name="text-2xl font-bold text-gray-900"),
            class_name="flex-1",
        ),
        class_name="flex items-center gap-4 rounded-lg border bg-white p-4 transition-all hover:shadow-lg",
        style={"box-shadow": "0px 1px 3px rgba(0,0,0,0.12)"},
    )