from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (
    UserLearningProgress, DailyActivity, SavedVocabulary, UserCertificate, 
    LevelAssessment, AssessmentQuestion, UserAssessmentAttempt, UserFeedback,
    LearningDayAnalytics, LearnerAnalyticsSummary, LevelTransitionAnalytics
)

@admin.register(DailyActivity)
class DailyActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'level', 'day_number', 'activity_type', 'completed', 'completed_at']
    list_filter = ['level', 'activity_type', 'completed', 'completed_at']
    search_fields = ['user__username']

@admin.register(SavedVocabulary)
class SavedVocabularyAdmin(admin.ModelAdmin):
    list_display = ['user', 'word', 'saved_at']
    list_filter = ['saved_at']
    search_fields = ['user__username', 'word']

@admin.register(UserCertificate)
class UserCertificateAdmin(admin.ModelAdmin):
    list_display = ['user', 'level', 'certificate_code', 'issued_at', 'downloaded', 'shared']
    list_filter = ['level', 'issued_at', 'downloaded', 'shared']
    search_fields = ['user__username', 'certificate_code']

class AssessmentQuestionInline(admin.TabularInline):
    """Inline editor for assessment questions"""
    model = AssessmentQuestion
    extra = 1
    fields = ['order', 'text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'explanation', 'is_active']
    show_change_link = True
    
    def get_extra(self, request, obj=None, **kwargs):
        """Set extra to 0 when editing existing assessment"""
        if obj:
            return 0
        return 1

@admin.register(LevelAssessment)
class LevelAssessmentAdmin(admin.ModelAdmin):
    list_display = ['level', 'title', 'question_count', 'passing_score', 'time_limit_minutes', 'is_active', 'assessment_status']
    list_filter = ['level', 'is_active', 'created_at']
    search_fields = ['level', 'title', 'description']
    readonly_fields = ['total_questions', 'created_at', 'updated_at', 'question_preview']
    fieldsets = (
        ('Assessment Information', {
            'fields': ('level', 'title', 'description', 'is_active')
        }),
        ('Grading Settings', {
            'fields': ('passing_score', 'time_limit_minutes', 'total_questions'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('question_preview', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [AssessmentQuestionInline]
    
    def question_count(self, obj):
        count = obj.get_question_count()
        if count == 0:
            return mark_safe('<span style="color: red;">⚠ 0 Questions</span>')
        return f"{count} questions"
    question_count.short_description = 'Questions'
    
    def assessment_status(self, obj):
        if not obj.is_active:
            return mark_safe('<span style="color: gray;">🔒 Inactive</span>')
        if obj.get_question_count() == 0:
            return mark_safe('<span style="color: orange;">⚠ No Questions</span>')
        return mark_safe('<span style="color: green;">✓ Ready</span>')
    assessment_status.short_description = 'Status'
    
    def question_preview(self, obj):
        questions = obj.get_questions()[:3]
        if not questions:
            return "No questions added yet."
        
        preview_html = "<div style='background: #f8f9fa; padding: 10px; border-radius: 5px;'>"
        for q in questions:
            preview_html += f"<p><strong>Q{q.order}:</strong> {q.text[:100]}...</p>"
        if obj.get_question_count() > 3:
            preview_html += f"<p><em>... and {obj.get_question_count() - 3} more questions</em></p>"
        preview_html += "</div>"
        return mark_safe(preview_html)
    question_preview.short_description = 'Question Preview'
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Update total_questions after saving
        obj.total_questions = obj.get_question_count()
        obj.save()

@admin.register(AssessmentQuestion)
class AssessmentQuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'assessment_level', 'order', 'question_preview', 'correct_answer', 'is_active']
    list_filter = ['assessment__level', 'is_active', 'created_at']
    search_fields = ['text', 'assessment__level']
    list_editable = ['order', 'is_active']
    fieldsets = (
        ('Question Information', {
            'fields': ('assessment', 'order', 'text', 'is_active')
        }),
        ('Options', {
            'fields': ('option_a', 'option_b', 'option_c', 'option_d')
        }),
        ('Answer & Explanation', {
            'fields': ('correct_answer', 'explanation'),
            'classes': ('collapse',)
        }),
    )
    
    def assessment_level(self, obj):
        return obj.assessment.get_level_display()
    assessment_level.short_description = 'Level'
    assessment_level.admin_order_field = 'assessment__level'
    
    def question_preview(self, obj):
        return obj.text[:75] + ('...' if len(obj.text) > 75 else '')
    question_preview.short_description = 'Question'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('assessment')

@admin.register(UserAssessmentAttempt)
class UserAssessmentAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'assessment_level', 'score', 'total', 'percentage_display', 'passed', 'completed_at']
    list_filter = ['assessment__level', 'passed', 'completed_at', 'started_at']
    search_fields = ['user__username', 'user__email', 'assessment__level']
    readonly_fields = ['started_at', 'completed_at', 'answers_preview']
    fieldsets = (
        ('User & Assessment', {
            'fields': ('user', 'assessment', 'level')
        }),
        ('Results', {
            'fields': ('score', 'total_questions', 'percentage', 'passed', 'time_taken_seconds')
        }),
        ('Timestamps', {
            'fields': ('started_at', 'completed_at'),
            'classes': ('collapse',)
        }),
        ('Answers Data', {
            'fields': ('answers_preview',),
            'classes': ('collapse',)
        }),
    )
    
    def assessment_level(self, obj):
        return obj.get_level_display()
    assessment_level.short_description = 'Level'
    assessment_level.admin_order_field = 'level'
    
    def total(self, obj):
        return obj.total_questions
    total.short_description = 'Total'
    
    def percentage_display(self, obj):
        color = 'green' if obj.passed else 'red'
        return mark_safe(f'<span style="color: {color}; font-weight: bold;">{obj.percentage:.1f}%</span>')
    percentage_display.short_description = 'Percentage'
    
    def answers_preview(self, obj):
        if not obj.answers:
            return "No answers recorded"
        
        preview = "<div style='max-height: 400px; overflow-y: auto;'>"
        for key, value in obj.answers.items():
            if key.startswith('q_'):
                preview += f"<p><strong>{key}:</strong> {value}</p>"
        preview += "</div>"
        return mark_safe(preview)
    answers_preview.short_description = 'User Answers'
    
    def has_add_permission(self, request):
        return False  # Prevent manual creation, only through assessment submission
    
    def has_change_permission(self, request, obj=None):
        return False  # Prevent changes to attempts
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Only superusers can delete attempts

# Enhanced UserLearningProgress admin (without the inline that was causing issues)
@admin.register(UserLearningProgress)
class UserLearningProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'level', 'current_day', 'completed_days_count', 'streak_days', 'completion_percentage', 'toolkit_status', 'certificate_status', 'assessment_status', 'updated_at']
    list_filter = ['level', 'toolkit_completed', 'certificate_issued', 'started_at', 'current_day']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['completed_days_count', 'completion_percentage', 'assessment_attempts_info', 'advanced_toolkit_data_preview', 'updated_at']
    
    def toolkit_status(self, obj):
        if obj.toolkit_completed:
            return mark_safe(f'<span style="color: green;">✓ Done ({obj.toolkit_score}%)</span>')
        if obj.toolkit_total_tools_completed > 0:
            return mark_safe(f'<span style="color: orange;">In Progress ({obj.toolkit_total_tools_completed}/8)</span>')
        return mark_safe('<span style="color: gray;">Not Started</span>')
    toolkit_status.short_description = 'Adv. Toolkit'

    def advanced_toolkit_data_preview(self, obj):
        import json
        return mark_safe(f'<pre>{json.dumps(obj.advanced_toolkit_data, indent=2)}</pre>')
    advanced_toolkit_data_preview.short_description = 'Toolkit Data (JSON)'
    
    def completed_days_count(self, obj):
        return len(obj.completed_days)
    completed_days_count.short_description = 'Days Completed'
    
    def completion_percentage(self, obj):
        return f"{obj.completion_percentage():.1f}%"
    completion_percentage.short_description = 'Progress'
    
    def certificate_status(self, obj):
        if obj.certificate_issued:
            return mark_safe('<span style="color: green;">✓ Issued</span>')
        elif obj.is_completed():
            return mark_safe('<span style="color: orange;">⚠ Ready to Issue</span>')
        return mark_safe('<span style="color: gray;">Not Available</span>')
    certificate_status.short_description = 'Certificate'
    
    def assessment_status(self, obj):
        """Show assessment attempt status"""
        latest_attempt = UserAssessmentAttempt.objects.filter(
            user=obj.user, 
            level=obj.level
        ).order_by('-completed_at').first()
        
        if latest_attempt:
            if latest_attempt.passed:
                return mark_safe(f'<span style="color: green;">✓ Passed ({latest_attempt.score}/{latest_attempt.total_questions})</span>')
            else:
                return mark_safe(f'<span style="color: red;">✗ Failed ({latest_attempt.score}/{latest_attempt.total_questions})</span>')
        return mark_safe('<span style="color: gray;">Not Taken</span>')
    assessment_status.short_description = 'Assessment'
    
    def assessment_attempts_info(self, obj):
        """Show all assessment attempts"""
        attempts = UserAssessmentAttempt.objects.filter(
            user=obj.user, 
            level=obj.level
        ).order_by('-completed_at')
        
        if not attempts:
            return "No assessment attempts yet."
        
        html = "<div style='max-height: 300px; overflow-y: auto;'>"
        html += "<table style='width: 100%; border-collapse: collapse;'>"
        html += "<tr style='background: #f0f0f0;'><th style='text-align: left; padding: 8px;'>Date</th><th style='text-align: left; padding: 8px;'>Score</th><th style='text-align: left; padding: 8px;'>Result</th></tr>"
        
        for attempt in attempts[:10]:  # Show last 10 attempts
            result_color = 'green' if attempt.passed else 'red'
            html += f"""
            <tr style='border-bottom: 1px solid #eee;'>
                <td style='padding: 8px;'>{attempt.completed_at.strftime('%Y-%m-%d %H:%M') if attempt.completed_at else 'N/A'}</td>
                <td style='padding: 8px;'><strong>{attempt.score}/{attempt.total_questions}</strong> ({attempt.percentage:.1f}%)</td>
                <td style='padding: 8px; color: {result_color}; font-weight: bold;'>{'✓ PASSED' if attempt.passed else '✗ FAILED'}</td>
            </tr>
            """
        html += "</table></div>"
        
        if attempts.count() > 10:
            html += f"<p style='margin-top: 10px;'><em>... and {attempts.count() - 10} more attempts</em></p>"
        
        return mark_safe(html)
    assessment_attempts_info.short_description = 'Assessment History'

@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'level', 'rating', 'created_at']
    list_filter = ['level', 'rating', 'created_at']
    search_fields = ['user__username', 'comment']

@admin.register(LearningDayAnalytics)
class LearningDayAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['user', 'level', 'day_number', 'stage', 'formatted_time', 'sections_completed', 'total_attempts', 'accuracy_badge', 'completed_at']
    list_filter = ['level', 'stage', 'day_number', 'completed_at']
    search_fields = ['user__username']
    readonly_fields = ['activity_data_preview', 'formatted_time', 'accuracy_badge']

    def formatted_time(self, obj):
        minutes = obj.total_time_spent_seconds // 60
        seconds = obj.total_time_spent_seconds % 60
        return f"{minutes}m {seconds}s"
    formatted_time.short_description = 'Time Spent'

    def accuracy_badge(self, obj):
        acc = obj.overall_accuracy
        color = 'green' if acc >= 80 else ('orange' if acc >= 60 else 'red')
        return mark_safe(f'<span style="background: {color}; color: white; padding: 2px 8px; border-radius: 10px; font-weight: bold;">{acc:.1f}%</span>')
    accuracy_badge.short_description = 'Accuracy'

    def activity_data_preview(self, obj):
        import json
        return mark_safe(f'<pre style="max-height: 300px; overflow-y: auto; background: #f8f9fa; padding: 10px; border: 1px solid #ddd;">{json.dumps(obj.activity_data, indent=2)}</pre>')
    activity_data_preview.short_description = 'Activity Data (JSON)'

@admin.register(LearnerAnalyticsSummary)
class LearnerAnalyticsSummaryAdmin(admin.ModelAdmin):
    list_display = ['user', 'improvement_category', 'behavior_type', 'completion_rate_display', 'overall_accuracy_display', 'speaking_confidence_score', 'dropout_risk_badge', 'strongest_section', 'weakest_section', 'last_updated']
    list_filter = ['improvement_category', 'behavior_type', 'strongest_section', 'weakest_section', 'certificate_issued']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['last_updated', 'completion_rate_display', 'overall_accuracy_display', 'dropout_risk_badge']

    def completion_rate_display(self, obj):
        return f"{obj.completion_rate:.1f}%"
    completion_rate_display.short_description = 'Completion %'

    def overall_accuracy_display(self, obj):
        return f"{obj.overall_accuracy:.1f}%"
    overall_accuracy_display.short_description = 'Accuracy %'

    def dropout_risk_badge(self, obj):
        risk = obj.dropout_risk_score
        color = 'red' if risk >= 70 else ('orange' if risk >= 40 else 'green')
        return mark_safe(f'<span style="color: {color}; font-weight: bold;">{risk:.1f}%</span>')
    dropout_risk_badge.short_description = 'Dropout Risk'

    def get_urls(self):
        from django.urls import path
        from .views import admin_analytics_dashboard
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(admin_analytics_dashboard), name='analytics-dashboard'),
        ]
        return custom_urls + urls
    
    fieldsets = (
        ('Overview', {
            'fields': ('user', 'total_learning_time_seconds', 'completed_days', 'completion_rate', 'overall_accuracy')
        }),
        ('Skill Scores', {
            'fields': ('listening_score', 'speaking_confidence_score', 'reading_accuracy_score', 'writing_improvement_score', 'grammar_score', 'vocabulary_engagement_score', 'game_performance_score'),
            'classes': ('collapse',)
        }),
        ('Assessment Results', {
            'fields': ('beginner_assessment_score', 'intermediate_assessment_score', 'advanced_toolkit_score', 'pretest_score', 'posttest_score', 'overall_improvement_percentage'),
            'classes': ('collapse',)
        }),
        ('Behavior Analytics', {
            'fields': ('engagement_score', 'consistency_score', 'retention_score', 'dropout_risk_score', 'total_retry_count'),
            'classes': ('collapse',)
        }),
        ('Insights', {
            'fields': ('strongest_section', 'weakest_section', 'improvement_category', 'behavior_type')
        }),
        ('Status', {
            'fields': ('certificate_issued', 'last_updated')
        }),
    )

@admin.register(LevelTransitionAnalytics)
class LevelTransitionAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['user', 'initial_level', 'final_level', 'improvement_type', 'improvement_percentage', 'transition_speed', 'certificate_issued']
    list_filter = ['initial_level', 'final_level', 'improvement_type', 'transition_speed', 'certificate_issued']
    search_fields = ['user__username']