import reflex as rx
from app.state import DashboardState
from app.components.chart_utils import TOOLTIP_PROPS, chart_container


def category_performance_chart() -> rx.Component:
    return chart_container(
        "Sales by Category",
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(horizontal=True, stroke_dasharray="3 3"),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.x_axis(
                type_="number", hide=True, tick_line=False, axis_line=False
            ),
            rx.recharts.y_axis(
                data_key="Category",
                type_="category",
                tick_line=False,
                axis_line=False,
                width=80,
                tick_margin=5,
            ),
            rx.recharts.bar(data_key="Sales", fill="#818CF8", radius=[0, 4, 4, 0]),
            data=DashboardState.category_performance,
            height=300,
            layout="vertical",
            margin={"top": 5, "right": 20, "left": 20, "bottom": 5},
            class_name="[&_.recharts-tooltip-cursor]:fill-gray-100",
        ),
    )