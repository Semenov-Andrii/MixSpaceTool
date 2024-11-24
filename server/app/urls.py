from django.urls import path

from app.views.meeting_views import MeetingCreateView, MeetingListView, MeetingSaveView, SavedMeetingListView, \
    SaveMeetingRetrieveDestroyView, MeetingDestroyView, MeetingInviteView
from app.views.project_views import ProjectCreateView, OwnProjectListView, ProjectRetrieveDestroyView, \
    TaskListCreateView, \
    TaskCreateView, TaskListDestroyView, TaskDestroyView, TaskLabelListView, ProjectMemberCreateView, \
    ProjectMemberListView, ProjectMemberDestroyView, ProjectListView, TaskUpdateView, ProjectTimerCreateView, \
    ProjectTimerEndView, ProjectTimerListView, MemberProjectTimerListView, ProjectTimerCommentView
from app.views.repository_views import FileUploadAPIView, RepositoryCreateView, OwnRepositoryListView, \
    RepositoryRetrieveDestroyView, FileCreateAPIView, VersionCreateAPIView, FileUpdateAPIView, \
    VersionListAPIView, RepositoryMemberCreateView, RepositoryMemberListView, RepositoryMemberDestroyView, \
    RepositoryListView, VersionDestroyAPIView, FileRetrieveAPIView, FileDestroyAPIView
from app.views.user_views import UserRegistrationView, UserLoginView

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user-registration"),
    path("login/", UserLoginView.as_view(), name="user-login"),

    path("meeting/", MeetingCreateView.as_view(), name="create-meeting"),
    path("meetings/", MeetingListView.as_view(), name="list-meeting"),
    path("save/meeting/", MeetingSaveView.as_view(), name="save-meeting"),
    path("save/meeting/<str:meeting_id>", SaveMeetingRetrieveDestroyView.as_view(), name="get-unsave-meeting"),
    path("invite/meeting/", MeetingInviteView.as_view(), name="invite-meeting"),
    path("meeting/<str:meeting_id>", MeetingDestroyView.as_view(), name="delete-meeting"),
    path("save/meetings/", SavedMeetingListView.as_view(), name="saved-list-meeting"),

    path("project/timer/create/<str:project_id>", ProjectTimerCreateView.as_view(), name="create-timer"),
    path("project/timer/end/<int:timer_id>", ProjectTimerEndView.as_view(), name="end-timer"),
    path("project/timer/comment/<int:timer_id>", ProjectTimerCommentView.as_view(), name="comment-timer"),
    path("project/timers/<str:project_id>", ProjectTimerListView.as_view(), name="list-timers"),
    path("project/timers/member/<str:project_id>", MemberProjectTimerListView.as_view(), name="member-list-timers"),
    path("project/<str:project_id>", ProjectRetrieveDestroyView.as_view(), name="get-delete-project"),
    path("task-label/<str:project_id>", TaskLabelListView.as_view(), name="get-labels"),
    path("task-list/project/<str:project_id>", TaskListCreateView.as_view(), name="create-task-list"),
    path("task-list/<int:task_list_id>", TaskListDestroyView.as_view(), name="remove-task-list"),

    path("task/project/<str:task_list_id>", TaskCreateView.as_view(), name="create-task"),
    path("task/<int:task_id>", TaskDestroyView.as_view(), name="remove-task"),
    path("task/<int:pk>/", TaskUpdateView.as_view(), name="update-task"),
    path("project/", ProjectCreateView.as_view(), name="create-project"),
    path("projects/", OwnProjectListView.as_view(), name="list-project"),
    path("member/projects/", ProjectListView.as_view(), name="list-member-project"),

    path("member/project/", ProjectMemberCreateView.as_view(), name="create-member"),
    path("members/project/<str:project_id>", ProjectMemberListView.as_view(), name="list-member"),
    path("member/project/<str:project_id>/<str:member_id>", ProjectMemberDestroyView.as_view(), name="remove-member"),
    path("member/repositories/", RepositoryListView.as_view(), name="list-member-repo"),
    path("member/repository/", RepositoryMemberCreateView.as_view(), name="r-create-member"),
    path("members/repository/<str:repository_id>", RepositoryMemberListView.as_view(), name="r-list-member"),
    path("member/repository/<str:repository_id>/<str:member_id>", RepositoryMemberDestroyView.as_view(),
         name="r-remove-member"),
    path("repository/file/upload", FileUploadAPIView.as_view(), name="file-upload"),
    path("repository/file/download/<str:file_id>", FileRetrieveAPIView.as_view(), name="file-download"),
    path("repository/file/new", FileCreateAPIView.as_view(), name="file-create"),
    path("repository/file/<str:file_id>", FileUpdateAPIView.as_view(), name="file-update"),
    path("repository/file/delete/<str:file_id>", FileDestroyAPIView.as_view(), name="file-delete"),
    path("repository/commit/<str:repository_id>", VersionCreateAPIView.as_view(), name="repository-commit"),
    path("repository/commit/goto/<str:version_id>/<str:repository_id>", VersionDestroyAPIView.as_view(),
         name="repository-commit-goto"),
    path("repository/commits/<str:repository_id>", VersionListAPIView.as_view(), name="repository-commit-list"),

    path("repository/", RepositoryCreateView.as_view(), name="create-repository"),
    path("repository/<str:repository_id>", RepositoryRetrieveDestroyView.as_view(), name="get-delete-repository"),
    path("repositories/", OwnRepositoryListView.as_view(), name="list-repository"),
]
