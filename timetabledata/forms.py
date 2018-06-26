from django import forms
from timetabledata.models import ConexionType


class ConexionTypeForm(forms.Form):
    """
    Form for individual ConexionType
    """
    CONEXION_CHOICES = (
        ('ME', 'Meeting'),
        ('OP', 'Option'),
        ('NO', 'Nothing'),
        ('IN', 'Indepednent'),
    )
    name = forms.CharField(
                    max_length=50,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Original file name',
                        'class': "form-control"

                    }),
                    required=True)
    ctype = forms.ChoiceField(
                    widget=forms.Select(attrs={
                         'class': "form-control"
                        }),
                    choices=CONEXION_CHOICES,
                    required=False)

    class Meta:
        model = ConexionType