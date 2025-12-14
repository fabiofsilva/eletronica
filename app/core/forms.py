from captcha.fields import CaptchaField
from django import forms
from django.utils.translation import gettext_lazy as _


class SugestaoSolucaoForm(forms.Form):
    email = forms.EmailField(label=_('E-mail'), widget=forms.TextInput(attrs={'placeholder': 'seu.email@exemplo.com'}))
    sugestao = forms.CharField(
        label=_('Sugestão'),
        widget=forms.Textarea(
            attrs={
                'rows': 6,
                'cols': 40,
                'placeholder': 'Ex: Modelo, Defeito, Componentes Substituídos, Passos da Solução.',
            }
        ),
    )
    captcha = CaptchaField(label=_('Validação de Segurança (CAPTCHA)'))
