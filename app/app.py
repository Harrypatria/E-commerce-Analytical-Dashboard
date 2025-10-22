import reflex as rx
from app.components.main_layout import main_layout
from app.state import DashboardState
from app.components.metric_card import metric_card
from app.components.advanced_charts import (
    sales_vs_profit_chart,
    category_stacked_area_chart,
    quantity_profit_scatter,
)
from app.components.top_products_table import top_products_table
from app.components.profit_by_category_chart import profit_by_category_chart
from app.pages.login import login_page
from app.pages.register import registration_page


@rx.page(route="/login")
def login() -> rx.Component:
    return login_page()


@rx.page(route="/register")
def register() -> rx.Component:
    return registration_page()


@rx.page(route="/", on_load=DashboardState.load_data)
def index() -> rx.Component:
    """The main dashboard page."""
    return main_layout(
        rx.el.div(
            rx.el.h1(
                "Welcome to your Dashboard",
                class_name="text-2xl font-bold text-gray-900 mb-6",
            ),
            rx.el.div(
                metric_card(
                    "Total Sales",
                    f"${DashboardState.total_sales.to_string()}",
                    "dollar-sign",
                    "text-green-600",
                ),
                metric_card(
                    "Total Profit",
                    f"${DashboardState.total_profit.to_string()}",
                    "trending-up",
                    "text-blue-600",
                ),
                metric_card(
                    "Total Orders",
                    DashboardState.total_orders.to_string(),
                    "shopping-cart",
                    "text-orange-600",
                ),
                metric_card(
                    "Profit Margin",
                    f"{DashboardState.profit_margin.to_string()}%",
                    "percent",
                    "text-violet-600",
                ),
                class_name="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4",
            ),
            rx.el.div(
                sales_vs_profit_chart(),
                category_stacked_area_chart(),
                quantity_profit_scatter(),
                profit_by_category_chart(),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6",
            ),
            rx.el.div(top_products_table(), class_name="mt-6"),
            class_name="w-full",
        )
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap",
            rel="stylesheet",
        ),
    ],
)