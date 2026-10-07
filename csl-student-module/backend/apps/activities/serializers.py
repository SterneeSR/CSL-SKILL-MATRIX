from rest_framework import serializers
from .models import Activity, Task, Assessment, Project, Submission


class StudentActivityListSerializer(serializers.ModelSerializer):
    course = serializers.CharField(source="course.name", read_only=True)
    batch = serializers.SerializerMethodField()
    type = serializers.CharField(source="activity_type", read_only=True)
    due_date = serializers.DateTimeField(source="deadline", read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = [
            "id",
            "title",
            "type",
            "description",
            "course",
            "batch",
            "due_date",
            "max_marks",
            "status",
        ]

    def get_batch(self, obj):
        return obj.batch.name if obj.batch else None

    def get_status(self, obj):
        student_profile = self.context.get("student_profile")
        if not student_profile:
            return "PENDING"
        # Check if the student has a submission for this activity
        submission = Submission.objects.filter(
            activity=obj,
            student=student_profile,
        ).first()

        if submission:
            if hasattr(submission, "evaluation") and submission.evaluation:
                if submission.evaluation.status == "COMPLETED":
                    return "EVALUATED"
            if submission.status == Submission.Status.SUBMITTED:
                return "SUBMITTED"
            elif submission.status == Submission.Status.WITHDRAWN:
                return "WITHDRAWN"
            elif submission.status == Submission.Status.DRAFT:
                return "DRAFT"
        return "PENDING"


class StudentActivityDetailSerializer(serializers.ModelSerializer):
    course = serializers.CharField(source="course.name", read_only=True)
    course_code = serializers.CharField(source="course.code", read_only=True)
    batch = serializers.SerializerMethodField()
    type = serializers.CharField(source="activity_type", read_only=True)
    due_date = serializers.DateTimeField(source="deadline", read_only=True)
    status = serializers.SerializerMethodField()
    skills_covered = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = [
            "id",
            "title",
            "type",
            "description",
            "course",
            "course_code",
            "batch",
            "due_date",
            "max_marks",
            "status",
            "skills_covered",
            "created_at",
        ]

    def get_batch(self, obj):
        return obj.batch.name if obj.batch else None

    def get_status(self, obj):
        student_profile = self.context.get("student_profile")
        if not student_profile:
            return "PENDING"
        submission = Submission.objects.filter(
            activity=obj,
            student=student_profile,
        ).first()
        if submission:
            if hasattr(submission, "evaluation") and submission.evaluation:
                if submission.evaluation.status == "COMPLETED":
                    return "EVALUATED"
            if submission.status == Submission.Status.SUBMITTED:
                return "SUBMITTED"
            elif submission.status == Submission.Status.WITHDRAWN:
                return "WITHDRAWN"
            elif submission.status == Submission.Status.DRAFT:
                return "DRAFT"
        return "PENDING"

    def get_skills_covered(self, obj):
        skills_dict = {}
        # 1. If TASK
        if obj.activity_type == Activity.ActivityType.TASK:
            try:
                task = obj.task
                for mapping in task.skill_mappings.select_related("skill", "sub_skill").all():
                    sk = mapping.skill
                    if sk.id not in skills_dict:
                        skills_dict[sk.id] = {
                            "id": sk.id,
                            "name": sk.name,
                            "subskills": [],
                        }
                    if mapping.sub_skill:
                        skills_dict[sk.id]["subskills"].append({
                            "id": mapping.sub_skill.id,
                            "name": mapping.sub_skill.name,
                        })
            except Exception:
                pass

        # 2. If PROJECT
        elif obj.activity_type == Activity.ActivityType.PROJECT:
            try:
                project = obj.project
                for mapping in project.skill_mappings.select_related("skill", "sub_skill").all():
                    sk = mapping.skill
                    if sk.id not in skills_dict:
                        skills_dict[sk.id] = {
                            "id": sk.id,
                            "name": sk.name,
                            "subskills": [],
                        }
                    if mapping.sub_skill:
                        skills_dict[sk.id]["subskills"].append({
                            "id": mapping.sub_skill.id,
                            "name": mapping.sub_skill.name,
                        })
            except Exception:
                pass

        # 3. If ASSESSMENT
        elif obj.activity_type == Activity.ActivityType.ASSESSMENT:
            try:
                assessment = obj.assessment
                for section in assessment.sections.all():
                    for q in section.questions.select_related("skill", "sub_skill").all():
                        sk = q.skill
                        if sk.id not in skills_dict:
                            skills_dict[sk.id] = {
                                "id": sk.id,
                                "name": sk.name,
                                "subskills": [],
                            }
                        if q.sub_skill and not any(sub["id"] == q.sub_skill.id for sub in skills_dict[sk.id]["subskills"]):
                            skills_dict[sk.id]["subskills"].append({
                                "id": q.sub_skill.id,
                                "name": q.sub_skill.name,
                            })
            except Exception:
                pass

        return list(skills_dict.values())
