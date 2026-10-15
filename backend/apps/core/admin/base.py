from django.contrib.admin import ModelAdmin


class BaseAdmin(ModelAdmin):
    ordering = ('-created_at',)

    def get_list_display(self, request):
        list_display = list(super().get_list_display(request))
        if self.__can_append_is_active(list_display):
            list_display.append("is_active")
        return list_display

    def get_list_filter(self, request):
        list_field = list(super().get_list_filter(request))
        if self.__can_append_is_active(list_field):
            list_field.append("is_active")
        return list_field

    def __can_append_is_active(self, list_type):
        return (
            hasattr(self.model, 'is_active')
            and "__all__" not in list_type
        )
