from django.contrib import admin
from django import forms
from Authentication.models import Token
import secrets
# Register your models here.

# admin.py

class TokenForm(forms.ModelForm):
    class Meta:
        model = Token
        exclude = ['created_at']

    def clean_token(self):
        return secrets.token_hex()



class TokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'token')
    form = TokenForm


admin.site.register(Token, TokenAdmin)
