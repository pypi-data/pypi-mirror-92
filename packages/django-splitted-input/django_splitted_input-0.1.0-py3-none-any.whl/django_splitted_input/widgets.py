from typing import Optional, Tuple, Type

from django.forms.widgets import Widget, MultiWidget, TextInput


class SplittedInput(MultiWidget):
    template_name = 'django_splitted_input/widget.html'

    def __init__(self, sizes: Tuple[int, ...], attrs: Optional[dict] = None,
                 input_widget: Optional[Type[Widget]] = None):
        """
        A widget that renders any type of input into multiple HTML input elements.
        :param sizes: A tuple containing the max allowed chars for each input tag
        :param attrs: attrs to the django widget superclass and all subwidgets
        :param input_widget: A subclass of django's widget class, used for all inputs. Defaults to TextInput
        """
        if attrs is None:
            attrs = {}
        self.input_widget = input_widget if input_widget else TextInput
        self.sizes = sizes
        self.indexed_sizes = [sum(self.sizes[:i]) for i in range(len(self.sizes) + 1)]
        self.attrs = dict(attrs, **{"class": "splitted_input"})
        self.widgets = [
            self.input_widget(attrs=dict(
                self.attrs,
                **{
                    "size": size,
                    "maxlength": size,
                },
            )
            )
            for size in self.sizes
        ]

        super().__init__(self.widgets, self.attrs)

    def value_from_datadict(self, data, files, name):
        values = super().value_from_datadict(data, files, name)

        return "".join(values)

    def decompress(self, value):
        if isinstance(value, str):
            values = [value[i:j] for i, j in zip(self.indexed_sizes[:-1], self.indexed_sizes[1:])]
            return values
        else:
            return [None for x in self.sizes]

    class Media:
        css = {
            "all": ("django_splitted_input/css/input.css",)
        }
        js = ("django_splitted_input/js/input.js",)
