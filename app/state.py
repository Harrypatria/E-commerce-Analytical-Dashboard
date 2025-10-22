import reflex as rx
import pandas as pd
from typing import TypedDict, Any
import logging
import datetime


class NavItem(TypedDict):
    icon: str
    label: str
    href: str


class ChatMessage(TypedDict):
    role: str
    content: str
    timestamp: str


class DashboardState(rx.State):
    """The state for the main dashboard with advanced analytics."""

    is_sidebar_collapsed: bool = False
    superstore_data: pd.DataFrame = pd.DataFrame()
    is_loading: bool = True
    nav_items: list[NavItem] = [
        {"icon": "layout-dashboard", "label": "Dashboard", "href": "/"},
        {"icon": "bar-chart-3", "label": "Analytics", "href": "#"},
        {"icon": "shopping-cart", "label": "Orders", "href": "#"},
        {"icon": "package", "label": "Products", "href": "#"},
        {"icon": "users", "label": "Customers", "href": "#"},
        {"icon": "settings", "label": "Settings", "href": "#"},
    ]
    selected_date_range: dict[str, str] = {"start": "", "end": ""}
    selected_categories: list[str] = []
    selected_regions: list[str] = []
    comparison_mode: str = "none"
    search_query: str = ""
    sort_column: str = "Sales"
    sort_direction: str = "desc"
    current_page: int = 1
    items_per_page: int = 50
    available_categories: list[str] = []
    available_regions: list[str] = []
    date_range_options: list[dict[str, str]] = [
        {"label": "Last 30 Days", "value": "30d"},
        {"label": "Last 90 Days", "value": "90d"},
        {"label": "This Year", "value": "year"},
        {"label": "Last Year", "value": "last_year"},
        {"label": "All Time", "value": "all"},
    ]

    @rx.var
    def filtered_data(self) -> pd.DataFrame:
        """Returns filtered dataset based on current filters."""
        if self.superstore_data.empty:
            return pd.DataFrame()
        df = self.superstore_data.copy()
        if self.selected_date_range.get("start") and self.selected_date_range.get(
            "end"
        ):
            df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
            start_date = pd.to_datetime(self.selected_date_range["start"])
            end_date = pd.to_datetime(self.selected_date_range["end"])
            df = df[(df["Order Date"] >= start_date) & (df["Order Date"] <= end_date)]
        if self.selected_categories:
            df = df[df["Category"].isin(self.selected_categories)]
        if self.selected_regions:
            df = df[df["Region"].isin(self.selected_regions)]
        return df

    @rx.var
    def total_sales(self) -> float:
        """Calculates the total sales from filtered data."""
        filtered = self.filtered_data
        if not filtered.empty:
            return float(filtered["Sales"].sum())
        return 0.0

    @rx.var
    def total_orders(self) -> int:
        """Calculates the total number of orders from filtered data."""
        filtered = self.filtered_data
        if not filtered.empty:
            return int(filtered["Order ID"].nunique())
        return 0

    @rx.var
    def total_profit(self) -> float:
        """Calculates the total profit from filtered data."""
        filtered = self.filtered_data
        if not filtered.empty:
            return float(filtered["Profit"].sum())
        return 0.0

    @rx.var
    def profit_margin(self) -> float:
        """Calculates the profit margin in percentage."""
        if self.total_sales > 0:
            return round(self.total_profit / self.total_sales * 100, 2)
        return 0.0

    @rx.var
    def sales_vs_profit_trend(self) -> list[dict[str, str | float | int]]:
        """Multi-line chart with Sales and Profit trends over time."""
        filtered = self.filtered_data
        if filtered.empty:
            return []
        try:
            df = filtered.copy()
            df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
            monthly_data = (
                df.groupby(df["Order Date"].dt.to_period("M"))
                .agg({"Sales": "sum", "Profit": "sum", "Order ID": "nunique"})
                .reset_index()
            )
            monthly_data["Order Date"] = monthly_data["Order Date"].dt.strftime("%b %y")
            monthly_data["Profit Margin"] = (
                monthly_data["Profit"] / monthly_data["Sales"] * 100
            ).round(2)
            return monthly_data.to_dict("records")
        except Exception as e:
            logging.exception(f"Error processing sales vs profit trend: {e}")
            return []

    @rx.var
    def category_sales_overtime(self) -> list[dict[str, str | float | int]]:
        """Stacked area chart showing category contribution over time."""
        filtered = self.filtered_data
        if filtered.empty:
            return []
        try:
            df = filtered.copy()
            df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
            monthly_category = (
                df.groupby([df["Order Date"].dt.to_period("M"), "Category"])["Sales"]
                .sum()
                .reset_index()
            )
            monthly_category["Order Date"] = monthly_category["Order Date"].dt.strftime(
                "%b %y"
            )
            pivot_data = (
                monthly_category.pivot(
                    index="Order Date", columns="Category", values="Sales"
                )
                .fillna(0)
                .reset_index()
            )
            return pivot_data.to_dict("records")
        except Exception as e:
            logging.exception(f"Error processing category sales over time: {e}")
            return []

    @rx.var
    def quantity_profit_scatter(self) -> list[dict[str, str | float | int]]:
        """Scatter plot with Quantity vs Profit, sized by Sales."""
        filtered = self.filtered_data
        if filtered.empty:
            return []
        try:
            df = filtered.copy()
            scatter_data = (
                df.groupby("Product Name")
                .agg({"Quantity": "sum", "Profit": "sum", "Sales": "sum"})
                .reset_index()
            )
            max_sales = scatter_data["Sales"].max()
            min_sales = scatter_data["Sales"].min()
            if max_sales > min_sales:
                scatter_data["Bubble Size"] = (
                    5
                    + 45 * (scatter_data["Sales"] - min_sales) / (max_sales - min_sales)
                ).round(0)
            else:
                scatter_data["Bubble Size"] = 25
            scatter_data = scatter_data.nlargest(100, "Sales")
            return scatter_data.to_dict("records")
        except Exception as e:
            logging.exception(f"Error processing quantity profit scatter: {e}")
            return []

    @rx.var
    def regional_category_heatmap(self) -> list[dict[str, str | float | int]]:
        """Heatmap data for Region vs Category performance."""
        filtered = self.filtered_data
        if filtered.empty:
            return []
        try:
            df = filtered.copy()
            heatmap_data = (
                df.groupby(["Region", "Category"])["Sales"].sum().reset_index()
            )
            for region in heatmap_data["Region"].unique():
                region_data = heatmap_data[heatmap_data["Region"] == region]
                max_sales = region_data["Sales"].max()
                min_sales = region_data["Sales"].min()
                if max_sales > min_sales:
                    heatmap_data.loc[
                        heatmap_data["Region"] == region, "Performance Score"
                    ] = (
                        (region_data["Sales"] - min_sales)
                        / (max_sales - min_sales)
                        * 100
                    ).round(1)
                else:
                    heatmap_data.loc[
                        heatmap_data["Region"] == region, "Performance Score"
                    ] = 50
            return heatmap_data.to_dict("records")
        except Exception as e:
            logging.exception(f"Error processing regional category heatmap: {e}")
            return []

    @rx.var
    def order_volume_metrics(self) -> list[dict[str, str | float | int]]:
        """Combined chart with Order Volume (bars) and Average Order Value (line)."""
        filtered = self.filtered_data
        if filtered.empty:
            return []
        try:
            df = filtered.copy()
            df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
            monthly_orders = (
                df.groupby(df["Order Date"].dt.to_period("M"))
                .agg({"Order ID": "nunique", "Sales": "sum"})
                .reset_index()
            )
            monthly_orders["Order Date"] = monthly_orders["Order Date"].dt.strftime(
                "%b %y"
            )
            monthly_orders["Average Order Value"] = (
                monthly_orders["Sales"] / monthly_orders["Order ID"]
            ).round(2)
            monthly_orders.rename(columns={"Order ID": "Order Count"}, inplace=True)
            return monthly_orders.to_dict("records")
        except Exception as e:
            logging.exception(f"Error processing order volume metrics: {e}")
            return []

    @rx.var
    def sales_trend_data(self) -> list[dict[str, str | float]]:
        """Legacy sales trend for backward compatibility."""
        return [
            {"Order Date": item["Order Date"], "Sales": item["Sales"]}
            for item in self.sales_vs_profit_trend
        ]

    @rx.var
    def category_performance(self) -> list[dict[str, str | float]]:
        """Calculates sales for each product category from filtered data."""
        filtered = self.filtered_data
        if filtered.empty:
            return []
        try:
            category_sales = (
                filtered.groupby("Category")["Sales"]
                .sum()
                .reset_index()
                .sort_values(by="Sales", ascending=False)
            )
            return category_sales.to_dict("records")
        except Exception as e:
            logging.exception(f"Error processing category performance data: {e}")
            return []

    @rx.var
    def regional_sales(self) -> list[dict[str, str | float]]:
        """Calculates total sales per region from filtered data."""
        filtered = self.filtered_data
        if filtered.empty:
            return []
        try:
            regional_data = (
                filtered.groupby("Region")["Sales"]
                .sum()
                .reset_index()
                .sort_values(by="Sales", ascending=False)
            )
            return regional_data.to_dict("records")
        except Exception as e:
            logging.exception(f"Error processing regional sales data: {e}")
            return []

    @rx.var
    def top_products(self) -> list[dict[str, str | float]]:
        """Finds the top 10 products by sales from filtered data."""
        filtered = self.filtered_data
        if filtered.empty:
            return []
        try:
            top_prods = (
                filtered.groupby("Product Name")["Sales"]
                .sum()
                .nlargest(10)
                .reset_index()
            )
            return top_prods.to_dict("records")
        except Exception as e:
            logging.exception(f"Error processing top products data: {e}")
            return []

    @rx.var
    def profit_by_category(self) -> list[dict[str, str | float]]:
        """Calculates total profit for each product category from filtered data."""
        filtered = self.filtered_data
        if filtered.empty:
            return []
        try:
            profit_data = (
                filtered.groupby("Category")["Profit"]
                .sum()
                .reset_index()
                .sort_values(by="Profit", ascending=False)
            )
            return profit_data.to_dict("records")
        except Exception as e:
            logging.exception(f"Error processing profit by category data: {e}")
            return []

    @rx.var
    def filtered_table_data(self) -> list[dict[str, str | float | int]]:
        """Returns paginated and sorted table data with search."""
        filtered = self.filtered_data
        if filtered.empty:
            return []
        try:
            df = filtered.copy()
            if self.search_query.strip():
                search_lower = self.search_query.lower()
                mask = (
                    df["Product Name"].str.lower().str.contains(search_lower, na=False)
                    | df["Category"].str.lower().str.contains(search_lower, na=False)
                    | df["Customer Name"]
                    .str.lower()
                    .str.contains(search_lower, na=False)
                    | df["Region"].str.lower().str.contains(search_lower, na=False)
                )
                df = df[mask]
            ascending = self.sort_direction == "asc"
            df = df.sort_values(by=self.sort_column, ascending=ascending)
            start_idx = (self.current_page - 1) * self.items_per_page
            end_idx = start_idx + self.items_per_page
            df = df.iloc[start_idx:end_idx]
            display_columns = [
                "Order Date",
                "Product Name",
                "Category",
                "Sales",
                "Quantity",
                "Profit",
                "Customer Name",
                "Region",
            ]
            df = df[display_columns]
            return df.to_dict("records")
        except Exception as e:
            logging.exception(f"Error processing filtered table data: {e}")
            return []

    @rx.var
    def total_filtered_rows(self) -> int:
        """Total number of rows after filtering (for pagination)."""
        filtered = self.filtered_data
        if filtered.empty:
            return 0
        if self.search_query.strip():
            search_lower = self.search_query.lower()
            mask = (
                filtered["Product Name"]
                .str.lower()
                .str.contains(search_lower, na=False)
                | filtered["Category"].str.lower().str.contains(search_lower, na=False)
                | filtered["Customer Name"]
                .str.lower()
                .str.contains(search_lower, na=False)
                | filtered["Region"].str.lower().str.contains(search_lower, na=False)
            )
            return int(mask.sum())
        return len(filtered)

    @rx.var
    def total_pages(self) -> int:
        """Calculate total pages for pagination."""
        return max(1, -(-self.total_filtered_rows // self.items_per_page))

    @rx.var
    def export_data(self) -> str:
        """Export filtered data as CSV string."""
        filtered = self.filtered_data
        if filtered.empty:
            return ""
        return filtered.to_csv(index=False)

    @rx.event
    def apply_date_filter(self, form_data: dict[str, str]):
        """Apply date range filter."""
        self.selected_date_range = {
            "start": form_data.get("start_date", ""),
            "end": form_data.get("end_date", ""),
        }

    @rx.event
    def apply_category_filter(self, category: str):
        """Toggle category filter."""
        if category in self.selected_categories:
            self.selected_categories.remove(category)
        else:
            self.selected_categories.append(category)

    @rx.event
    def apply_region_filter(self, region: str):
        """Toggle region filter."""
        if region in self.selected_regions:
            self.selected_regions.remove(region)
        else:
            self.selected_regions.append(region)

    @rx.event
    def clear_filters(self):
        """Clear all filters."""
        self.selected_date_range = {"start": "", "end": ""}
        self.selected_categories = []
        self.selected_regions = []
        self.search_query = ""

    @rx.event
    def set_comparison_mode(self, mode: str):
        """Set comparison mode (YoY, MoM, etc)."""
        self.comparison_mode = mode

    @rx.event
    def set_search_query(self, query: str):
        """Set search query for table filtering."""
        self.search_query = query
        self.current_page = 1

    @rx.event
    def sort_table(self, column: str):
        """Sort table by column."""
        if self.sort_column == column:
            self.sort_direction = "desc" if self.sort_direction == "asc" else "asc"
        else:
            self.sort_column = column
            self.sort_direction = "desc"
        self.current_page = 1

    @rx.event
    def set_page(self, page: int):
        """Set current page for table pagination."""
        self.current_page = max(1, min(page, self.total_pages))

    @rx.event
    def previous_page(self):
        """Go to previous page."""
        self.set_page(self.current_page - 1)

    @rx.event
    def next_page(self):
        """Go to next page."""
        self.set_page(self.current_page + 1)

    @rx.event
    def toggle_sidebar(self):
        """Toggles the sidebar collapse state."""
        self.is_sidebar_collapsed = not self.is_sidebar_collapsed

    @rx.event(background=True)
    async def load_data(self):
        """Loads the superstore dataset and initializes filter options."""
        try:
            url = "https://raw.githubusercontent.com/atharvayeola/superstore-analytics-pipeline/main/superstore.csv"
            df = pd.read_csv(url, encoding="latin1")
            async with self:
                self.superstore_data = df
                self.available_categories = df["Category"].unique().tolist()
                self.available_regions = df["Region"].unique().tolist()
                self.is_loading = False
        except Exception as e:
            logging.exception(f"Error loading data: {e}")
            async with self:
                self.is_loading = False


class ChatState(rx.State):
    """Enhanced state for the AI chatbot with advanced analytics."""

    is_chat_open: bool = False
    messages: list[ChatMessage] = []
    current_input: str = ""
    is_processing: bool = False
    query_suggestions: list[str] = [
        "What are the top selling products?",
        "Show me sales vs profit trends",
        "Which region-category combo performs best?",
        "Analyze quantity vs profit relationship",
        "What's the order volume trend?",
    ]

    @rx.event
    def toggle_chat(self):
        self.is_chat_open = not self.is_chat_open
        if self.is_chat_open and (not self.messages):
            self._add_bot_message(
                "Hello! I'm your advanced analytics assistant. I can help you analyze trends, correlations, and generate insights from your data. Try asking about sales trends, product performance, or regional analysis!"
            )

    def _add_bot_message(self, text: str):
        self.messages.append(
            {
                "role": "bot",
                "content": text,
                "timestamp": datetime.datetime.now().strftime("%H:%M"),
            }
        )

    @rx.event
    async def process_query(self, query: str):
        """Enhanced query processing with advanced analytics."""
        dashboard_state = await self.get_state(DashboardState)
        if dashboard_state.superstore_data.empty:
            self._add_bot_message("The data is not loaded yet. Please wait a moment.")
            return
        try:
            df = (
                dashboard_state.filtered_data
                if not dashboard_state.filtered_data.empty
                else dashboard_state.superstore_data
            )
            query = query.lower()
            response = "I'm sorry, I could not understand your query. Try one of the suggestions."
            if "sales vs profit" in query or "sales profit trend" in query:
                trend_data = dashboard_state.sales_vs_profit_trend
                if trend_data:
                    latest = trend_data[-1]
                    response = f"📈 **Sales vs Profit Trend Analysis:**\n\nLatest month ({latest['Order Date']}):\n- Sales: ${latest['Sales']:,.2f}\n- Profit: ${latest['Profit']:,.2f}\n- Profit Margin: {latest['Profit Margin']:.1f}%\n\nThe trend shows {('strong' if latest['Profit Margin'] > 15 else 'moderate' if latest['Profit Margin'] > 10 else 'weak')} profitability with a {latest['Profit Margin']:.1f}% margin."
            elif "top selling products" in query or "best products" in query:
                top_prods = (
                    df.groupby("Product Name")["Sales"].sum().nlargest(5).reset_index()
                )
                response = """🏆 **Top 5 Selling Products:**
"""
                for idx, row in top_prods.iterrows():
                    response += (
                        f"{idx + 1}. {row['Product Name']}: ${row['Sales']:,.2f}\n"
                    )
            elif (
                "region" in query
                and "category" in query
                and ("perform" in query or "best" in query)
            ):
                heatmap_data = dashboard_state.regional_category_heatmap
                if heatmap_data:
                    best = max(heatmap_data, key=lambda x: x["Sales"])
                    response = f"🎯 **Regional-Category Performance:**\n\nBest performing combination:\n- Region: **{best['Region']}**\n- Category: **{best['Category']}**\n- Sales: ${best['Sales']:,.2f}\n- Performance Score: {best['Performance Score']:.1f}/100\n\nThis combination generates the highest sales volume in our dataset."
            elif "quantity" in query and "profit" in query:
                scatter_data = dashboard_state.quantity_profit_scatter
                if scatter_data:
                    high_profit = max(scatter_data, key=lambda x: x["Profit"])
                    high_quantity = max(scatter_data, key=lambda x: x["Quantity"])
                    response = f"""📊 **Quantity vs Profit Analysis:**\n\nHighest Profit Product:\n- {high_profit["Product Name"]}: ${high_profit["Profit"]:,.2f} profit from {high_profit["Quantity"]} units\n\nHighest Quantity Product:\n- {high_quantity["Product Name"]}: {high_quantity["Quantity"]} units sold, ${high_quantity["Profit"]:,.2f} profit\n\n**Insight:** {("High quantity doesn't always mean high profit" if high_profit["Product Name"] != high_quantity["Product Name"] else "This product excels in both volume and profitability")}."""
            elif "order volume" in query or "order trend" in query:
                order_data = dashboard_state.order_volume_metrics
                if order_data:
                    latest = order_data[-1]
                    response = f"📦 **Order Volume Analysis:**\n\nLatest month ({latest['Order Date']}):\n- Order Count: {latest['Order Count']} orders\n- Average Order Value: ${latest['Average Order Value']:.2f}\n- Total Sales: ${latest['Sales']:,.2f}\n\nThe average customer spends ${latest['Average Order Value']:.2f} per order."
            elif "profit margin" in query:
                margin = dashboard_state.profit_margin
                response = f"💰 **Profit Margin Analysis:**\n\nCurrent overall profit margin: **{margin:.2f}%**\n\nThis is {('excellent (>20%)' if margin > 20 else 'good (15-20%)' if margin > 15 else 'average (10-15%)' if margin > 10 else 'below average (<10%)')} for retail operations."
            elif "category" in query and ("best" in query or "perform" in query):
                categories = (
                    df.groupby("Category")
                    .agg({"Sales": "sum", "Profit": "sum"})
                    .reset_index()
                )
                categories["Profit Margin"] = (
                    categories["Profit"] / categories["Sales"] * 100
                ).round(2)
                best_sales = categories.loc[categories["Sales"].idxmax()]
                best_margin = categories.loc[categories["Profit Margin"].idxmax()]
                response = f"📈 **Category Performance Analysis:**\n\nBest by Sales Volume:\n- **{best_sales['Category']}**: ${best_sales['Sales']:,.2f} ({best_sales['Profit Margin']:.1f}% margin)\n\nBest by Profit Margin:\n- **{best_margin['Category']}**: {best_margin['Profit Margin']:.1f}% margin (${best_margin['Sales']:,.2f} sales)\n\n**Recommendation:** Focus on {best_sales['Category']} for volume growth and {best_margin['Category']} for profitability."
            self._add_bot_message(response)
        except Exception as e:
            logging.exception(f"Error processing query: {e}")
            self._add_bot_message(
                "Sorry, I encountered an error processing your query. Please try a different question."
            )

    @rx.event
    async def handle_submit(self, form_data: dict[str, str]):
        query = form_data.get("query", "").strip()
        if not query:
            return
        self.current_input = ""
        self.messages.append(
            {
                "role": "user",
                "content": query,
                "timestamp": datetime.datetime.now().strftime("%H:%M"),
            }
        )
        self.is_processing = True
        yield
        await self.process_query(query)
        self.is_processing = False

    @rx.event
    async def handle_suggestion_click(self, suggestion: str):
        self.current_input = suggestion
        return await ChatState.handle_submit({"query": suggestion})