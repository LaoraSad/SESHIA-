def __init__(
    self,
    *args,
    user=None,
    category_type=CategoryType.EXPENSE,
    **kwargs,
):
    super().__init__(*args, **kwargs)

    if user:
        self.fields["category"].queryset = Category.objects.filter(
            category_type=category_type,
        ).filter(
            Q(user=user) | Q(user__isnull=True)
        )