"""Base test class with shared test data and visit helpers."""
from cryptography.fernet import Fernet
from django.test import TestCase, override_settings
from django.utils import timezone

import konote.encryption as enc_module

from .checker import Severity, UxChecker
from .conftest import get_report

TEST_KEY = Fernet.generate_key().decode()


@override_settings(FIELD_ENCRYPTION_KEY=TEST_KEY)
class UxWalkthroughBase(TestCase):
    """Base class for all UX walkthrough tests.

    Provides shared test data, visit helpers, and report collection.
    """

    databases = {"default", "audit"}

    @classmethod
    def setUpTestData(cls):
        """Create all test data once for the entire test class."""
        enc_module._fernet = None

        from apps.admin_settings.models import FeatureToggle
        from apps.auth_app.models import User
        from apps.clients.models import (
            ClientDetailValue,
            ClientFile,
            ClientProgramEnrolment,
            CustomFieldDefinition,
            CustomFieldGroup,
        )
        from apps.events.models import Alert, Event, EventType
        from apps.notes.models import (
            ProgressNote,
            ProgressNoteTemplate,
            ProgressNoteTemplateSection,
        )
        from apps.plans.models import (
            MetricDefinition,
            PlanSection,
            PlanTarget,
            PlanTargetMetric,
        )
        from apps.programs.models import Program, UserProgramRole

        # --- Programs ---
        cls.program_a = Program.objects.create(
            name="Housing Support", colour_hex="#10B981"
        )
        cls.program_b = Program.objects.create(
            name="Youth Services", colour_hex="#3B82F6"
        )

        # --- Users ---
        cls.receptionist_user = User.objects.create_user(
            username="frontdesk",
            password="testpass123",
            display_name="Dana Front Desk",
        )
        cls.staff_user = User.objects.create_user(
            username="staff",
            password="testpass123",
            display_name="Casey Worker",
        )
        cls.manager_user = User.objects.create_user(
            username="manager",
            password="testpass123",
            display_name="Morgan Manager",
        )
        cls.executive_user = User.objects.create_user(
            username="executive",
            password="testpass123",
            display_name="Eva Executive",
        )
        cls.admin_user = User.objects.create_user(
            username="admin",
            password="testpass123",
            display_name="Alex Admin",
        )
        cls.admin_user.is_admin = True
        cls.admin_user.save()

        cls.admin_pm_user = User.objects.create_user(
            username="adminpm",
            password="testpass123",
            display_name="Admin PM",
        )
        cls.admin_pm_user.is_admin = True
        cls.admin_pm_user.save()

        # --- Role assignments ---
        UserProgramRole.objects.create(
            user=cls.receptionist_user,
            program=cls.program_a,
            role="receptionist",
        )
        UserProgramRole.objects.create(
            user=cls.staff_user,
            program=cls.program_a,
            role="staff",
        )
        UserProgramRole.objects.create(
            user=cls.manager_user,
            program=cls.program_a,
            role="program_manager",
        )
        UserProgramRole.objects.create(
            user=cls.executive_user,
            program=cls.program_a,
            role="executive",
        )
        UserProgramRole.objects.create(
            user=cls.admin_pm_user,
            program=cls.program_a,
            role="program_manager",
        )
        UserProgramRole.objects.create(
            user=cls.admin_pm_user,
            program=cls.program_b,
            role="program_manager",
        )

        # --- Clients ---
        cls.client_a = ClientFile.objects.create(is_demo=False)
        cls.client_a.first_name = "Jane"
        cls.client_a.last_name = "Doe"
        cls.client_a.status = "active"
        cls.client_a.consent_given_at = timezone.now()
        cls.client_a.consent_type = "written"
        cls.client_a.save()

        cls.client_b = ClientFile.objects.create(is_demo=False)
        cls.client_b.first_name = "Bob"
        cls.client_b.last_name = "Smith"
        cls.client_b.status = "active"
        cls.client_b.save()

        ClientProgramEnrolment.objects.create(
            client_file=cls.client_a, program=cls.program_a
        )
        ClientProgramEnrolment.objects.create(
            client_file=cls.client_b, program=cls.program_b
        )

        # --- Custom fields ---
        cls.field_group = CustomFieldGroup.objects.create(
            title="Contact Info", sort_order=1
        )
        cls.phone_field = CustomFieldDefinition.objects.create(
            group=cls.field_group,
            name="Phone Number",
            input_type="text",
            receptionist_access="edit",
            sort_order=1,
        )
        cls.case_notes_field = CustomFieldDefinition.objects.create(
            group=cls.field_group,
            name="Case Notes",
            input_type="textarea",
            receptionist_access="none",
            sort_order=2,
        )
        ClientDetailValue.objects.create(
            client_file=cls.client_a,
            field_def=cls.phone_field,
            value="555-1234",
        )

        # --- Metrics ---
        cls.metric_a = MetricDefinition.objects.create(
            name="PHQ-9 Score",
            definition="Depression screening (0-27)",
            category="mental_health",
            min_value=0,
            max_value=27,
            unit="score",
            is_enabled=True,
            is_library=True,
        )

        # --- Plan ---
        cls.plan_section = PlanSection.objects.create(
            client_file=cls.client_a,
            name="Mental Health Goals",
            program=cls.program_a,
        )
        cls.plan_target = PlanTarget.objects.create(
            plan_section=cls.plan_section,
            client_file=cls.client_a,
            name="Reduce depression symptoms",
            description="Target PHQ-9 below 10",
        )
        PlanTargetMetric.objects.create(
            plan_target=cls.plan_target, metric_def=cls.metric_a
        )

        # --- Note template ---
        cls.note_template = ProgressNoteTemplate.objects.create(
            name="Standard Session"
        )
        ProgressNoteTemplateSection.objects.create(
            template=cls.note_template,
            name="Session Notes",
            section_type="basic",
            sort_order=1,
        )

        # --- Progress note ---
        cls.note = ProgressNote.objects.create(
            client_file=cls.client_a,
            author=cls.staff_user,
            author_program=cls.program_a,
            note_type="quick",
        )
        cls.note.notes_text = "Client seemed well today."
        cls.note.save()

        # --- Event type + event + alert ---
        cls.event_type = EventType.objects.create(
            name="Intake", colour_hex="#22C55E"
        )
        cls.event = Event.objects.create(
            client_file=cls.client_a,
            title="Initial intake",
            event_type=cls.event_type,
            start_timestamp=timezone.now(),
            author_program=cls.program_a,
        )
        cls.alert = Alert.objects.create(
            client_file=cls.client_a,
            content="Safety concern noted",
            author=cls.staff_user,
            author_program=cls.program_a,
        )

        # --- Feature toggles ---
        FeatureToggle.objects.create(
            feature_key="programs", is_enabled=True
        )

    def setUp(self):
        enc_module._fernet = None
        # Don't raise exceptions on server errors — record them as issues
        self.client.raise_request_exception = False

    def tearDown(self):
        enc_module._fernet = None

    @property
    def report(self):
        return get_report()

    # ------------------------------------------------------------------
    # Visit helpers
    # ------------------------------------------------------------------

    def _make_issue(self, severity, url, role, step, description):
        """Helper to create a UxIssue without needing a checker."""
        from .checker import UxIssue
        return UxIssue(
            severity=severity, url=url, role=role, step=step,
            description=description,
        )

    def visit(
        self,
        role: str,
        step: str,
        url: str,
        expected_status: int = 200,
        expected_lang: str = "en",
        role_should_see: list | None = None,
        role_should_not_see: list | None = None,
    ):
        """GET a URL, run full-page UX checks, record results."""
        response = self.client.get(url)
        issues = []

        if response.status_code == 500:
            issues.append(self._make_issue(
                Severity.CRITICAL, url, role, step,
                "Server error (500) — view crashed",
            ))
        elif response.status_code == 200 and expected_status == 200:
            checker = UxChecker(
                response, url, role, step,
                is_partial=False,
                expected_lang=expected_lang,
                role_should_see=role_should_see,
                role_should_not_see=role_should_not_see,
            )
            issues = checker.run_all_checks()
        elif response.status_code != expected_status:
            issues.append(self._make_issue(
                Severity.CRITICAL, url, role, step,
                f"Expected {expected_status}, got {response.status_code}",
            ))

        self.report.record_step(role, step, url, response.status_code, issues)
        return response

    def visit_htmx(
        self,
        role: str,
        step: str,
        url: str,
        role_should_see: list | None = None,
        role_should_not_see: list | None = None,
    ):
        """GET with HX-Request header, run partial UX checks."""
        response = self.client.get(url, HTTP_HX_REQUEST="true")
        issues = []

        if response.status_code == 500:
            issues.append(self._make_issue(
                Severity.CRITICAL, url, role, step,
                "Server error (500) on HTMX partial",
            ))
        elif response.status_code == 200:
            checker = UxChecker(
                response, url, role, step,
                is_partial=True,
                role_should_see=role_should_see,
                role_should_not_see=role_should_not_see,
            )
            issues = checker.run_all_checks()

        self.report.record_step(role, step, url, response.status_code, issues)
        return response

    def visit_and_follow(
        self,
        role: str,
        step: str,
        url: str,
        data: dict,
        expected_redirect: str | None = None,
    ):
        """POST with follow=True, check redirect + success message on landing."""
        response = self.client.post(url, data, follow=True)
        issues = []

        if response.status_code == 500:
            issues.append(self._make_issue(
                Severity.CRITICAL, url, role, step,
                "Server error (500) after POST",
            ))
        else:
            # Check redirect chain
            if response.redirect_chain:
                final_url = response.redirect_chain[-1][0]
                if expected_redirect and expected_redirect not in final_url:
                    issues.append(self._make_issue(
                        Severity.WARNING, url, role, step,
                        f"Expected redirect to contain '{expected_redirect}', "
                        f"got '{final_url}'",
                    ))

            # Run UX checks on the final landing page
            if response.status_code == 200:
                checker = UxChecker(
                    response, url, role, step, is_partial=False,
                )
                issues.extend(checker.run_all_checks())
                # Check for success message
                checker.check_success_message()
                issues.extend(
                    [i for i in checker.issues if i not in issues]
                )

        self.report.record_step(role, step, url, response.status_code, issues)
        return response

    def visit_forbidden(self, role: str, step: str, url: str):
        """Visit a URL that should return 403, check error page quality."""
        response = self.client.get(url)
        issues = []

        if response.status_code == 403:
            checker = UxChecker(response, url, role, step, is_partial=False)
            checker.check_403_quality()
            issues = checker.issues
        else:
            issues.append(self._make_issue(
                Severity.CRITICAL, url, role, step,
                f"Expected 403, got {response.status_code}",
            ))

        self.report.record_step(role, step, url, response.status_code, issues)
        return response

    def visit_redirect(self, role: str, step: str, url: str):
        """Visit a URL that should redirect, follow it, check landing page."""
        response = self.client.get(url, follow=True)
        issues = []

        if response.status_code == 500:
            issues.append(self._make_issue(
                Severity.CRITICAL, url, role, step,
                "Server error (500) on redirect follow",
            ))
        else:
            if not response.redirect_chain:
                issues.append(self._make_issue(
                    Severity.WARNING, url, role, step,
                    "Expected redirect but got direct response",
                ))
            if response.status_code == 200:
                checker = UxChecker(
                    response, url, role, step, is_partial=False,
                )
                issues.extend(checker.run_all_checks())

        self.report.record_step(role, step, url, response.status_code, issues)
        return response
