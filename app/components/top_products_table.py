import reflex as rx
from app.state import DashboardState
from app.components.chart_utils import chart_container


def top_products_table() -> rx.Component:
    def render_row(product: dict):
        formatted_sales = f"${product['Sales']:,.2f}"
        return rx.el.tr(
            rx.el.td(
                product["Product Name"],
                class_name="py-2 px-4 border-b text-sm text-gray-700 truncate max-w-xs",
            ),
            rx.el.td(
                formatted_sales,
                class_name="py-2 px-4 border-b text-sm text-gray-900 font-medium text-right",
            ),
            class_name="hover:bg-gray-50",
        )

    return chart_container(
        "Top 10 Products by Sales",
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Product Name",
                            class_name="py-2 px-4 bg-gray-50 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Total Sales",
                            class_name="py-2 px-4 bg-gray-50 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider",
                        ),
                    )
                ),
                rx.el.tbody(rx.foreach(DashboardState.top_products, render_row)),
                class_name="w-full",
            ),
            class_name="overflow-x-auto rounded-lg border",
        ),
    )