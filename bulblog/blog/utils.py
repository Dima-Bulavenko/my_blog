navigation = [
    {"title": "Главная страница", "url_name": "index"},
    {"title": "Категории", "url_name": "cat"},
    {"title": "Добавить пост", "url_name": "add_post"},
]


class DataMixin:
    paginate_by = 2

    def get_user_context(self, **kwargs):
        context = kwargs
        context["navigation"] = navigation
        return context
