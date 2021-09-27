from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, ArticleScope, Scope


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass

# Relationship - ArticleScope
# Object - Scope


class ArticleScopeInline(admin.TabularInline):
    model = ArticleScope


@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    inlines = [ArticleScopeInline]


class ArticleScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        for tag in ArticleScopeInlineFormset:
            tags_counter = 0
            if tag.is_main is True:
                tags_counter += 1
        for form in self.forms:
            if form.cleaned_data == "0":
                raise ValidationError('Укажите основной раздел')
            if form.cleaned_data >= 2:
                raise ValidationError('Основным может быть только один раздел')
        return super(ArticleScopeInlineFormset, self).clean()


class ArticleScopeInline(admin.TabularInline):
    model = ArticleScope
    formset = ArticleScopeInlineFormset