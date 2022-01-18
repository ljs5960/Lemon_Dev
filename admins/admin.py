from django.contrib import admin
from admins.models import Qna, Notice


# 문의하기
@admin.register(Qna)
class QnaAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'category',
        'qna_date',
        'user',
        'status',
    ]
    list_filter = ['status', 'category']
    search_fields = ['title']
    fieldsets = [
        ('문의내용', {'fields': ['qna_date', 'category', 'title', 'content', 'file']}),
        ('답변내용', {'fields': ['reply', 'status']}),
    ]


# 공지사항
@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'date',
    )