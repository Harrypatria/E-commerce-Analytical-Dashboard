import reflex as rx

TOOLTIP_PROPS = {
    "content_style": {
        "background": "white",
        "border_color": "#E8E8E8",
        "border_radius": "0.75rem",
        "box_shadow": "0px 1px 3px rgba(0,0,0,0.12)",
        "font_size": "0.875rem",
        "line_height": "1.25rem",
        "font_weight": "500",
        "padding": "0.5rem 0.75rem",
    },
    "item_style": {},
    "label_style": {"color": "#333", "font_weight": "600", "margin_bottom": "0.25rem"},
    "separator": ": ",
}


def chart_container(title: str, chart: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.h3(title, class_name="text-lg font-semibold text-gray-800 mb-4"),
        chart,
        class_name="rounded-lg border bg-white p-6 transition-all hover:shadow-lg",
        style={"box-shadow": "0px 1px 3px rgba(0,0,0,0.12)"},
    )