from django.contrib import admin

from materials.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    fields = ("name", "preview", "description")
    search_fields = ("name", "description")
    ordering = ("name",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    fields = ("name", "preview", "description", "link_to_the_video")
    search_fields = ("name", "description", "course")
    ordering = ("name", "course")
