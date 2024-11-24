from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from app.models.meeting import Meeting, SavedMeeting
from app.models.user import UserProfile
from app.serializers.meeting_serializer import MeetingSerializer, MeetingListSerializer, SavedMeetingSerializer, \
    InviteMeetingSerializer


class MeetingCreateView(generics.CreateAPIView):
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        meeting = Meeting.objects.create(icon=serializer.data["icon"], title=serializer.data["title"],
                                         owner=self.request.user.userprofile)

        res_serializer = MeetingListSerializer(meeting)
        return JsonResponse(res_serializer.data, status=status.HTTP_200_OK)


class MeetingSaveView(generics.CreateAPIView):
    serializer_class = SavedMeetingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        saved_meetings = SavedMeeting.objects.filter(meeting_id=serializer.data["id"],
                                                     user=self.request.user.userprofile)
        if saved_meetings.exists():
            return JsonResponse({"detail": "Can't save saved meeting!"}, status=status.HTTP_400_BAD_REQUEST)

        meeting = Meeting.objects.filter(id=serializer.data["id"]).first()
        if not meeting:
            return JsonResponse({"detail": "Meeting not found!"}, status=status.HTTP_404_NOT_FOUND)

        saved_meeting = SavedMeeting.objects.create(meeting=meeting, user=self.request.user.userprofile)

        res_serializer = MeetingListSerializer(meeting)
        return JsonResponse(res_serializer.data, status=status.HTTP_200_OK)


class MeetingInviteView(generics.CreateAPIView):
    serializer_class = InviteMeetingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = UserProfile.objects.filter(user__username=serializer.data["email"]).first()

        if not user:
            return JsonResponse({"detail": "User does not exist!"}, status=status.HTTP_404_NOT_FOUND)

        saved_meetings = SavedMeeting.objects.filter(meeting_id=serializer.data["id"], user=user)
        if saved_meetings.exists():
            return JsonResponse({"detail": "User already added!"}, status=status.HTTP_400_BAD_REQUEST)

        meeting = Meeting.objects.filter(id=serializer.data["id"]).first()
        if not meeting:
            return JsonResponse({"detail": "Meeting not found!"}, status=status.HTTP_404_NOT_FOUND)

        saved_meeting = SavedMeeting.objects.create(meeting=meeting, user=user)

        res_serializer = MeetingListSerializer(meeting)
        return JsonResponse(res_serializer.data, status=status.HTTP_200_OK)

class MeetingListView(generics.ListAPIView):
    serializer_class = MeetingListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_profile = self.request.user.userprofile
        return Meeting.objects.filter(owner=user_profile)


class SavedMeetingListView(generics.ListAPIView):
    serializer_class = MeetingListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_profile = self.request.user.userprofile
        saves = SavedMeeting.objects.filter(user=user_profile)
        return [save.meeting for save in saves]


class SaveMeetingRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    serializer_class = SavedMeetingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        meeting_id = self.kwargs.get("meeting_id")
        return SavedMeeting.objects.filter(meeting_id=meeting_id, user=self.request.user.userprofile)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return JsonResponse({"detail": "Meeting not found"}, status=status.HTTP_404_NOT_FOUND)

        instance = queryset.first()
        serializer = self.get_serializer(instance)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return JsonResponse({"detail": "Meeting not found"}, status=status.HTTP_404_NOT_FOUND)

        instance = queryset.first()
        instance.delete()
        return JsonResponse({"detail": "Deleted successfully"}, status=status.HTTP_200_OK)

class MeetingDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        meeting_id = self.kwargs.get("meeting_id")
        return Meeting.objects.filter(id=meeting_id, owner=self.request.user.userprofile)

    def destroy(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return JsonResponse({"detail": "Meeting not found"}, status=status.HTTP_404_NOT_FOUND)

        instance = queryset.first()
        instance.delete()
        return JsonResponse({"detail": "Deleted successfully"}, status=status.HTTP_200_OK)
