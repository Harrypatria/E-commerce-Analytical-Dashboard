import reflex as rx
from app.state import DashboardState
from app.components.chart_utils import TOOLTIP_PROPS, chart_container


def regional_sales_chart() -> rx.Component:
    return chart_container(
        "Sales by Region",
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(horizontal=True, stroke_dasharray="3 3"),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.x_axis(
                data_key="Region", type_="category", tick_line=False, axis_line=False
            ),
            rx.recharts.y_axis(tick_line=False, axis_line=False),
            rx.recharts.bar(data_key="Sales", fill="#A5B4FC", radius=[4, 4, 0, 0]),
            data=DashboardState.regional_sales,
            height=300,
            margin={"top": 5, "right": 20, "left": 20, "bottom": 5},
            class_name="[&_.recharts-tooltip-cursor]:fill-gray-100",
        ),
    )