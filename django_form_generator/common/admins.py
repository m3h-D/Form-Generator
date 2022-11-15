import urllib
from django.contrib import admin


class FormFilter(admin.FieldListFilter):

    initial = {}
    form_class = None

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.request = request
        expected = self.expected_parameters()
        others = {k: v for k, v in request.GET.items() if k not in expected}
        self.other_query_string = urllib.parse.urlencode(others)
        self.form = self.get_form(request)
        if self.form:
            self.form.is_valid()

    def form_lookups(self):
        raise NotImplementedError(
            "subclasses of FormFieldFilter must provide a form_lookups() method"
        )

    def expected_parameters(self):
        return [item[0] for item in self.form_lookups()]

    def get_initial(self):
        return self.initial.copy()

    def get_form_kwargs(self, request):
        return {
            "prefix": self.field.name,
            "initial": self.get_initial(),
            "data": request.GET or None,
        }

    def get_form(self, request):
        return self.form_class(**self.get_form_kwargs(request))

    def get_lookups(self):
        lookups = {k.split("_")[1]: v for k, v in self.form_lookups()}
        data = self.form.cleaned_data if self.form.is_bound else {}
        return {v: data[k] for k, v in lookups.items() if data.get(k)}

    def queryset(self, request, queryset):
        lookup = self.get_lookups()
        if isinstance(lookup, dict):
            return queryset.filter(**lookup)
        return queryset.filter(lookup)

    def choices(self, changelist):
        return ()

