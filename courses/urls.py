from django.urls import path
from . import views

urlpatterns = [
    # ---------------- PUBLIC ----------------
    path('', views.home, name='home'),
    path('home/', views.home_view, name='home'),

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # ---------------- DASHBOARD ----------------
    path('dashboard/', views.dashboard_user, name='dashboard_user'),  # <-- ce nom doit exister
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),

    # ---------------- USERS ----------------
    path('dashboard/users/', views.manage_users, name='manage_users'),
    path('dashboard/users/add/', views.add_user, name='add_user'),
    path('dashboard/users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('dashboard/users/delete/<int:user_id>/', views.delete_user, name='delete_user'),

    # ---------------- COURSES ----------------
    path('courses/', views.course_list, name='courses'),
    path('course/add/', views.add_course, name='add_course'),
    path('update-course/<int:id>/', views.update_course, name='update_course'),
    path('delete-course/<int:id>/', views.delete_course, name='delete_course'),
    path('enroll/<int:id>/', views.enroll_course, name='enroll_course'),

    # ---------------- LESSONS ----------------
    path('lessons/add/', views.add_lesson, name='add_lesson'),
    path('lessons/<int:id>/update/', views.update_lesson, name='update_lesson'),
    path('lessons/<int:id>/delete/', views.delete_lesson, name='delete_lesson'),
    path('course/<int:course_id>/lessons/', views.lesson_list, name='lesson_list'),
    path('lesson/<int:id>/', views.lesson_detail, name='lesson_detail'),
    path('complete/<int:id>/', views.complete_lesson, name='complete_lesson'),

    # ---------------- CERTIFICATES / PROGRESS / ACTIVITY ----------------
    path('dashboard/certificates/', views.certificates, name='certificates'),
    path('dashboard/progress/', views.progress, name='progress'),
    path('dashboard/activity/', views.recent_activity, name='recent_activity'),
    path('dashboard/notifications/', views.notifications, name='notifications'),

    # ---------------- ADMIN EXTRA ----------------
    path('dashboard/manage-categories/', views.manage_categories, name='manage_categories'),
    path('dashboard/upload-resources/', views.upload_resources, name='upload_resources'),
    path('dashboard/review-feedback/', views.review_feedback, name='review_feedback'),
    path('dashboard/system-settings/', views.system_settings, name='system_settings'),

    # ---------------- SEARCH ----------------
    path('search/', views.search_courses, name='search_courses'),




    # ---------------- DASHBOARD ACTIONS ----------------
    path('dashboard/continue-learning/', views.continue_learning, name='continue_learning'),
    path('dashboard/my-certificates/', views.my_certificates, name='my_certificates'),
    path('dashboard/my-progress/', views.my_progress, name='my_progress'),
    path('dashboard/browse-courses/', views.browse_courses, name='browse_courses'),

    # ---------------- RESOURCE CENTER ----------------
    path('resources/download-pdfs/', views.download_pdfs, name='download_pdfs'),
    path('resources/watch-tutorials/', views.watch_tutorials, name='watch_tutorials'),
    path('resources/practice-exercises/', views.practice_exercises, name='practice_exercises'),
    path('resources/study-guides/', views.study_guides, name='study_guides'),

    # ---------------- COMMUNITY ----------------
    path('community/forum/', views.discussion_forum, name='discussion_forum'),
    path('community/study-groups/', views.study_groups, name='study_groups'),
    path('community/challenges/', views.learning_challenges, name='learning_challenges'),

    path('profile/', views.profile_view, name='profile'),


    # ---------------- SUPPORT ----------------
    path('support/help-center/', views.help_center, name='help_center'),
    path('support/report-issue/', views.report_issue, name='report_issue'),
    path('support/contact-support/', views.contact_support, name='contact_support'),
    path('support/faq/', views.faq, name='faq'),

    # ---------------- ACCOUNT ----------------
    path('account/edit-profile/', views.edit_profile, name='edit_profile'),
    path('account/change-password/', views.change_password, name='change_password'),

    path('forum/', views.discussion_forum, name='forum'),  # <- ici on nomme la route 'forum'
    path('forum/<int:post_id>/', views.forum_post_detail, name='forum_post_detail'),
    

    path('challenges/', views.learning_challenges, name='learning_challenges'),
    path('challenges/active/', views.active_challenge, name='active_challenge'),  # <-- IMPORTANT
    path('community/challenges/', views.learning_challenges, name='learning_challenges'),
    path('community/challenges/active/', views.active_challenge, name='active_challenge'),
]
