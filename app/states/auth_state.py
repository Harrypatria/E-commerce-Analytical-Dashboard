import reflex as rx


class AuthState(rx.State):
    is_authenticated: bool = False
    is_user_menu_open: bool = False
    is_loading: bool = False
    username: str = ""
    authenticated_user: dict[str, str] = {}

    @rx.var
    def user_avatar(self) -> str:
        if self.is_authenticated and self.username:
            return f"https://api.dicebear.com/9.x/initials/svg?seed={self.username}"
        return "https://api.dicebear.com/9.x/initials/svg?seed=Guest"

    @rx.event
    def toggle_user_menu(self):
        self.is_user_menu_open = not self.is_user_menu_open

    @rx.event
    async def login(self, form_data: dict[str, str]):
        self.is_loading = True
        yield
        username = form_data.get("username", "")
        password = form_data.get("password", "")
        if username and password:
            self.is_authenticated = True
            self.username = username
            self.authenticated_user = {"username": username}
            self.is_loading = False
            self.is_user_menu_open = False
            yield rx.redirect("/")
            return
        self.is_loading = False

    @rx.event
    async def register(self, form_data: dict[str, str]):
        self.is_loading = True
        yield
        username = form_data.get("username", "")
        password = form_data.get("password", "")
        confirm_password = form_data.get("confirm_password", "")
        if username and password and (password == confirm_password):
            self.is_authenticated = True
            self.username = username
            self.authenticated_user = {"username": username}
            self.is_loading = False
            self.is_user_menu_open = False
            yield rx.redirect("/")
            return
        self.is_loading = False

    @rx.event
    def logout(self):
        self.is_authenticated = False
        self.username = ""
        self.authenticated_user = {}
        self.is_user_menu_open = False
        return rx.redirect("/login")