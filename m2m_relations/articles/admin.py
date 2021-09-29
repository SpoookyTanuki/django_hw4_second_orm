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
        for form in self.forms:
            tags_counter = 0
            if form.cleaned_data is True:
                tags_counter += 1
            if tags_counter == 0:
                raise ValidationError('Укажите основной раздел')
            if tags_counter >= 2:
                raise ValidationError('Основным может быть только один раздел')
        return super(ArticleScopeInlineFormset, self).clean()


class ArticleScopeInline(admin.TabularInline):
    model = ArticleScope
    formset = ArticleScopeInlineFormset


