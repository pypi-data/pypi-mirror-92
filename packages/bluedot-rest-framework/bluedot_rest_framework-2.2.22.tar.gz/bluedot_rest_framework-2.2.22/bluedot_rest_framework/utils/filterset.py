from datetime import datetime


class FilterBackend:

    @classmethod
    def get_filterset(cls, request, queryset, filterset_fields):
        return cls().filter_queryset(request, queryset, filterset_fields)

    def filter_queryset(self, request, queryset, filterset_fields):
        if filterset_fields:
            for key in filterset_fields:
                field_value = request.query_params.get(key, None)
                if field_value:
                    if key == 'time_state':
                        queryset = self.get_time_state(
                            key, field_value, filterset_fields[key], queryset)
                    else:
                        _filter = filterset_fields[key]
                        if _filter['lookup_expr'] == 'in':
                            field_value = self.filter_in(_filter, field_value)
                        elif _filter['field_type'] == 'bool':
                            field_value = self.filter_bool(field_value)
                        lookup_type = key + _filter['lookup_expr']
                        queryset = queryset.filter(
                            **{lookup_type: field_value})
        return queryset

    def get_time_state(self, key, field_value, filterset_field, queryset):
        date_now = datetime.now()
        if field_value == '1':
            queryset = queryset.filter(
                **{f"{filterset_field['start_time']}__gt": date_now})
        elif field_value == '2':
            queryset = queryset.filter(
                **{f"{filterset_field['start_time']}__lte": date_now, f"{filterset_field['end_time']}__gte": date_now})
        elif field_value == '3':
            queryset = queryset.filter(
                **{f"{filterset_field['end_time']}__lt": date_now})
        return queryset

    def filter_in(self, _filter, field_value):
        field_value = field_value.split(',')
        if _filter['field_type'] == 'int':
            field_value = [int(i) for i in field_value]
        return field_value

    def filter_bool(self, field_value):
        if field_value == 'true':
            field_value = True
        elif field_value == 'false':
            field_value = False
        return field_value
