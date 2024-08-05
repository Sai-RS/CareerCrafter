from rest_framework import serializers
from .models import CandidatesApplied, Job

class JobSerializer(serializers.ModelSerializer):
    posted_by = serializers.SerializerMethodField()

    def get_posted_by(self, obj):
        return obj.user.username if obj.user else None
    
    class Meta:
        model = Job
        fields ='__all__'


class CandidatesAppliedSerializer(serializers.ModelSerializer):

    job = JobSerializer()

    class Meta:
        model = CandidatesApplied
        fields = ('user', 'resume', 'appliedAt', 'job')