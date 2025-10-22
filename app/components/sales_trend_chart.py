import reflex as rx
from app.state import DashboardState
from app.components.chart_utils import TOOLTIP_PROPS, chart_container


def sales_trend_chart() -> rx.Component:
    return chart_container(
        "Sales Trend",
        rx.recharts.line_chart(
            rx.recharts.cartesian_grid(horizontal=True, stroke_dasharray="3 3"),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.x_axis(
                data_key="Order Date", tick_line=False, axis_line=False, tick_margin=8
            ),
            rx.recharts.y_axis(tick_line=False, axis_line=False, tick_margin=8),
            rx.recharts.line(
                data_key="Sales",
                stroke="#6366F1",
                stroke_width=2,
                type_="natural",
                dot=False,
            ),
            data=DashboardState.sales_trend_data,
            height=300,
            margin={"top": 5, "right": 20, "left": 20, "bottom": 5},
            class_name="[&_.recharts-tooltip-cursor]:stroke-gray-300",
        ),
    )