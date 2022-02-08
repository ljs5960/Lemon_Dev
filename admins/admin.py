from django.contrib import admin
from .models import Notice, Faq

# 공지사항
@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'date',
    ]
    list_per_page = 10

# FAQ
@admin.action(description = "카테고리 변경 - '운영정책'")
def edit_category_to_1(self, request, queryset):
    updated_count = queryset.update(category = 1)
    self.message_user(request, '{}개 FAQ를 변경'.format(updated_count))
    
@admin.action(description = "카테고리 변경 - '계정/인증'")
def edit_category_to_2(self, request, queryset):
    updated_count = queryset.update(category = 2)
    self.message_user(request, '{}개 FAQ를 변경'.format(updated_count))
    
@admin.action(description = "카테고리 변경 - '이벤트'")
def edit_category_to_3(self, request, queryset):
    updated_count = queryset.update(category = 3)
    self.message_user(request, '{}개 FAQ를 변경'.format(updated_count))
    
@admin.action(description = "카테고리 변경 - '이용 제재'")
def edit_category_to_4(self, request, queryset):
    updated_count = queryset.update(category = 4)
    self.message_user(request, '{}개 FAQ를 변경'.format(updated_count))
    
@admin.action(description = "카테고리 변경 - '기타'")
def edit_category_to_5(self, request, queryset):
    updated_count = queryset.update(category = 5)
    self.message_user(request, '{}개 FAQ를 변경'.format(updated_count))

@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = [
        'category',
        'title',
    ]
    list_display_links = ['title']
    list_editable = ['category']
    list_filter = ['category']
    list_per_page = 10
    actions = [
        edit_category_to_1,
        edit_category_to_2,
        edit_category_to_3,
        edit_category_to_4,
        edit_category_to_5,
    ]