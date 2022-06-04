from django.urls import path

from .views import PendingResults, AssignedUsers, CounselingRequestsView, PendingResultsSection, CounselingRequestsSection

urlpatterns = [
    path('', CounselingRequestsView.as_view(), name='counseling-requests'),
    path('pending-results/', PendingResults.as_view(), name='pending-results'),
    path('pending-results-section/', PendingResultsSection.as_view(), name='pending-results-section'),
    path('counseling-requests-section/', CounselingRequestsSection.as_view(), name='counseling-requests-section'),
    path('assigned-users/', AssignedUsers.as_view(), name='assigned-users'),
]