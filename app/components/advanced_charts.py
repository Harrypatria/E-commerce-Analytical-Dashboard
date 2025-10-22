import reflex as rx
from app.state import DashboardState
from app.components.chart_utils import TOOLTIP_PROPS, chart_container


def sales_vs_profit_chart() -> rx.Component:
    """Multi-line comparison chart with dual Y-axis showing Sales and Profit trends."""
    return chart_container(
        "Sales vs Profit Trend (Dual Y-Axis)",
        rx.recharts.composed_chart(
            rx.recharts.cartesian_grid(
                horizontal=True, stroke_dasharray="3 3", class_name="opacity-30"
            ),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.x_axis(
                data_key="Order Date",
                tick_line=False,
                axis_line=False,
                tick_margin=8,
                class_name="text-xs",
            ),
            rx.recharts.y_axis(
                y_axis_id="left",
                tick_line=False,
                axis_line=False,
                tick_margin=8,
                class_name="text-xs",
            ),
            rx.recharts.y_axis(
                y_axis_id="right",
                orientation="right",
                tick_line=False,
                axis_line=False,
                tick_margin=8,
                class_name="text-xs",
            ),
            rx.recharts.bar(
                data_key="Sales",
                y_axis_id="left",
                fill="#3B82F6",
                fill_opacity=0.7,
                name="Sales ($)",
            ),
            rx.recharts.line(
                data_key="Profit",
                y_axis_id="right",
                stroke="#10B981",
                stroke_width=3,
                type_="monotone",
                dot={"fill": "#10B981", "r": 4},
                name="Profit ($)",
            ),
            data=DashboardState.sales_vs_profit_trend,
            height=350,
            margin={"top": 5, "right": 30, "left": 20, "bottom": 5},
            class_name="[&_.recharts-tooltip-cursor]:fill-blue-50",
        ),
    )


def category_stacked_area_chart() -> rx.Component:
    """Stacked area chart showing category contribution over time."""
    return chart_container(
        "Category Sales Contribution Over Time",
        rx.recharts.area_chart(
            rx.recharts.cartesian_grid(
                horizontal=True, stroke_dasharray="3 3", class_name="opacity-30"
            ),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.x_axis(
                data_key="Order Date",
                tick_line=False,
                axis_line=False,
                tick_margin=8,
                class_name="text-xs",
            ),
            rx.recharts.y_axis(
                tick_line=False, axis_line=False, tick_margin=8, class_name="text-xs"
            ),
            rx.recharts.area(
                data_key="Technology",
                stack_id="1",
                stroke="#8B5CF6",
                fill="#8B5CF6",
                fill_opacity=0.8,
                type_="monotone",
            ),
            rx.recharts.area(
                data_key="Furniture",
                stack_id="1",
                stroke="#F59E0B",
                fill="#F59E0B",
                fill_opacity=0.8,
                type_="monotone",
            ),
            rx.recharts.area(
                data_key="Office Supplies",
                stack_id="1",
                stroke="#EF4444",
                fill="#EF4444",
                fill_opacity=0.8,
                type_="monotone",
            ),
            data=DashboardState.category_sales_overtime,
            height=300,
            margin={"top": 5, "right": 20, "left": 20, "bottom": 5},
            class_name="[&_.recharts-tooltip-cursor]:fill-gray-100",
        ),
    )


def quantity_profit_scatter() -> rx.Component:
    """Scatter plot showing Quantity vs Profit relationship with bubble sizing by Sales."""
    return chart_container(
        "Quantity vs Profit Analysis (Bubble Size = Sales)",
        rx.recharts.scatter_chart(
            rx.recharts.cartesian_grid(
                horizontal=True,
                vertical=True,
                stroke_dasharray="3 3",
                class_name="opacity-30",
            ),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.x_axis(
                data_key="Quantity",
                type_="number",
                name="Quantity",
                domain=["auto", "auto"],
                tick_line=False,
                axis_line=False,
                tick_margin=8,
                class_name="text-xs",
            ),
            rx.recharts.y_axis(
                data_key="Profit",
                type_="number",
                name="Profit ($)",
                domain=["auto", "auto"],
                tick_line=False,
                axis_line=False,
                tick_margin=8,
                class_name="text-xs",
            ),
            rx.recharts.z_axis(data_key="Bubble Size", range_=[50, 800]),
            rx.recharts.scatter(
                name="Product Performance",
                data=DashboardState.quantity_profit_scatter,
                fill="#FDBA74",
                shape="circle",
            ),
            height=300,
            margin={"top": 5, "right": 20, "left": 20, "bottom": 20},
            class_name="[&_.recharts-tooltip-cursor]:fill-gray-100",
        ),
    )