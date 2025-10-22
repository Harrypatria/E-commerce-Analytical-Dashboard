import reflex as rx
from app.state import DashboardState, NavItem


def nav_item(item: NavItem) -> rx.Component:
    """Renders a navigation item for the sidebar."""
    return rx.el.a(
        rx.icon(item["icon"], class_name="h-5 w-5 shrink-0"),
        rx.cond(
            DashboardState.is_sidebar_collapsed,
            None,
            rx.el.span(item["label"], class_name="truncate"),
        ),
        href=item["href"],
        class_name=rx.cond(
            DashboardState.is_sidebar_collapsed,
            "flex h-9 w-9 items-center justify-center rounded-lg text-gray-500 transition-colors hover:text-gray-900",
            "flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900 hover:bg-gray-100",
        ),
        title=item["label"],
    )


def sidebar() -> rx.Component:
    """The sidebar component for navigation."""
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("store", class_name="h-7 w-7 text-violet-600"),
                rx.cond(
                    DashboardState.is_sidebar_collapsed,
                    None,
                    rx.el.span(
                        "Patria & Co.", class_name="text-lg font-bold text-gray-800"
                    ),
                ),
                class_name="flex items-center gap-2",
            ),
            rx.el.button(
                rx.icon("chevrons-left", class_name="h-5 w-5"),
                on_click=DashboardState.toggle_sidebar,
                class_name="rounded-lg p-2 hover:bg-gray-100",
                title="Collapse Sidebar",
            ),
            class_name="flex h-16 items-center justify-between border-b px-4",
        ),
        rx.el.nav(
            rx.foreach(DashboardState.nav_items, nav_item),
            class_name="flex flex-col gap-1 p-2",
        ),
        class_name=rx.cond(
            DashboardState.is_sidebar_collapsed,
            "hidden md:flex flex-col border-r bg-white transition-all duration-300 w-20",
            "hidden md:flex flex-col border-r bg-white transition-all duration-300 w-64",
        ),
    )