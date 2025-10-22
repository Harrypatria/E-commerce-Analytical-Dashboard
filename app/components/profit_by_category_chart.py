import reflex as rx
from app.state import DashboardState
from app.components.chart_utils import TOOLTIP_PROPS, chart_container


def profit_by_category_chart() -> rx.Component:
    return chart_container(
        "Profit by Category",
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(vertical=True, stroke_dasharray="3 3"),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.x_axis(
                data_key="Category",
                type_="category",
                tick_line=False,
                axis_line=False,
                tick_margin=8,
            ),
            rx.recharts.y_axis(tick_line=False, axis_line=False),
            rx.recharts.bar(data_key="Profit", fill="#34D399", radius=[4, 4, 0, 0]),
            data=DashboardState.profit_by_category,
            height=300,
            margin={"top": 5, "right": 20, "left": 20, "bottom": 5},
            class_name="[&_.recharts-tooltip-cursor]:fill-gray-100",
        ),
    )