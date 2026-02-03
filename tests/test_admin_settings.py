"""Tests for Phase 6: admin settings, terminology, features, users."""
from django.test import TestCase, Client, override_settings
from cryptography.fernet import Fernet

from apps.admin_settings.models import (
    DEFAULT_TERMS, FeatureToggle, InstanceSetting, TerminologyOverride,
)
from apps.auth_app.models import User
import konote.encryption as enc_module

TEST_KEY = Fernet.generate_key().decode()


@override_settings(FIELD_ENCRYPTION_KEY=TEST_KEY)
class AdminSettingsDashboardTest(TestCase):
    def setUp(self):
        enc_module._fernet = None
        self.client = Client()
        self.admin = User.objects.create_user(username="admin", password="testpass123", is_admin=True)
        self.staff = User.objects.create_user(username="staff", password="testpass123", is_admin=False)

    def test_admin_can_view_dashboard(self):
        self.client.login(username="admin", password="testpass123")
        resp = self.client.get("/admin/settings/")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Terminology")

    def test_staff_cannot_view_dashboard(self):
        self.client.login(username="staff", password="testpass123")
        resp = self.client.get("/admin/settings/")
        self.assertEqual(resp.status_code, 403)


@override_settings(FIELD_ENCRYPTION_KEY=TEST_KEY)
class TerminologyTest(TestCase):
    def setUp(self):
        enc_module._fernet = None
        self.client = Client()
        self.admin = User.objects.create_user(username="admin", password="testpass123", is_admin=True)

    def test_admin_can_view_terminology(self):
        self.client.login(username="admin", password="testpass123")
        resp = self.client.get("/admin/settings/terminology/")
        self.assertEqual(resp.status_code, 200)

    def test_admin_can_update_terminology(self):
        self.client.login(username="admin", password="testpass123")
        data = {key: val for key, val in DEFAULT_TERMS.items()}
        data["client"] = "Participant"
        resp = self.client.post("/admin/settings/terminology/", data)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            TerminologyOverride.objects.get(term_key="client").display_value,
            "Participant",
        )

    def test_default_value_deletes_override(self):
        self.client.login(username="admin", password="testpass123")
        TerminologyOverride.objects.create(term_key="client", display_value="Participant")
        data = {key: val for key, val in DEFAULT_TERMS.items()}
        # Submit with default value — should remove override
        resp = self.client.post("/admin/settings/terminology/", data)
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(TerminologyOverride.objects.filter(term_key="client").exists())


@override_settings(FIELD_ENCRYPTION_KEY=TEST_KEY)
class FeatureToggleTest(TestCase):
    def setUp(self):
        enc_module._fernet = None
        self.client = Client()
        self.admin = User.objects.create_user(username="admin", password="testpass123", is_admin=True)

    def test_admin_can_view_features(self):
        self.client.login(username="admin", password="testpass123")
        resp = self.client.get("/admin/settings/features/")
        self.assertEqual(resp.status_code, 200)

    def test_admin_can_enable_feature(self):
        self.client.login(username="admin", password="testpass123")
        resp = self.client.post("/admin/settings/features/", {
            "feature_key": "programs",
            "action": "enable",
        })
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(FeatureToggle.objects.get(feature_key="programs").is_enabled)

    def test_admin_can_disable_feature(self):
        self.client.login(username="admin", password="testpass123")
        FeatureToggle.objects.create(feature_key="programs", is_enabled=True)
        resp = self.client.post("/admin/settings/features/", {
            "feature_key": "programs",
            "action": "disable",
        })
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(FeatureToggle.objects.get(feature_key="programs").is_enabled)


@override_settings(FIELD_ENCRYPTION_KEY=TEST_KEY)
class InstanceSettingsTest(TestCase):
    def setUp(self):
        enc_module._fernet = None
        self.client = Client()
        self.admin = User.objects.create_user(username="admin", password="testpass123", is_admin=True)

    def test_admin_can_view_settings(self):
        self.client.login(username="admin", password="testpass123")
        resp = self.client.get("/admin/settings/instance/")
        self.assertEqual(resp.status_code, 200)

    def test_admin_can_save_settings(self):
        self.client.login(username="admin", password="testpass123")
        resp = self.client.post("/admin/settings/instance/", {
            "product_name": "MyApp",
            "date_format": "Y-m-d",
            "session_timeout_minutes": "60",
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(InstanceSetting.get("product_name"), "MyApp")


@override_settings(FIELD_ENCRYPTION_KEY=TEST_KEY)
class UserManagementTest(TestCase):
    def setUp(self):
        enc_module._fernet = None
        self.client = Client()
        self.admin = User.objects.create_user(
            username="admin", password="testpass123", is_admin=True, display_name="Admin",
        )

    def test_admin_can_list_users(self):
        self.client.login(username="admin", password="testpass123")
        resp = self.client.get("/auth/users/")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Admin")

    def test_admin_can_create_user(self):
        self.client.login(username="admin", password="testpass123")
        resp = self.client.post("/auth/users/new/", {
            "username": "newuser",
            "display_name": "New User",
            "password": "securepass1",
            "password_confirm": "securepass1",
            "is_admin": False,
        })
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_password_mismatch_rejected(self):
        self.client.login(username="admin", password="testpass123")
        resp = self.client.post("/auth/users/new/", {
            "username": "newuser",
            "display_name": "New User",
            "password": "securepass1",
            "password_confirm": "differentpass",
            "is_admin": False,
        })
        self.assertEqual(resp.status_code, 200)  # Re-renders form
        self.assertFalse(User.objects.filter(username="newuser").exists())

    def test_admin_can_edit_user(self):
        self.client.login(username="admin", password="testpass123")
        user = User.objects.create_user(
            username="editme", password="testpass123", display_name="Edit Me",
        )
        resp = self.client.post(f"/auth/users/{user.pk}/edit/", {
            "display_name": "Edited Name",
            "is_admin": False,
            "is_active": True,
        })
        self.assertEqual(resp.status_code, 302)
        user.refresh_from_db()
        self.assertEqual(user.display_name, "Edited Name")

    def test_admin_can_deactivate_user(self):
        self.client.login(username="admin", password="testpass123")
        user = User.objects.create_user(
            username="deactivateme", password="testpass123", display_name="Deactivate Me",
        )
        resp = self.client.post(f"/auth/users/{user.pk}/deactivate/")
        self.assertEqual(resp.status_code, 302)
        user.refresh_from_db()
        self.assertFalse(user.is_active)

    def test_admin_cannot_deactivate_self(self):
        self.client.login(username="admin", password="testpass123")
        resp = self.client.post(f"/auth/users/{self.admin.pk}/deactivate/")
        self.assertEqual(resp.status_code, 302)
        self.admin.refresh_from_db()
        self.assertTrue(self.admin.is_active)

    def test_staff_cannot_list_users(self):
        staff = User.objects.create_user(
            username="staff", password="testpass123", is_admin=False,
        )
        self.client.login(username="staff", password="testpass123")
        resp = self.client.get("/auth/users/")
        self.assertEqual(resp.status_code, 403)


@override_settings(FIELD_ENCRYPTION_KEY=TEST_KEY)
class DocumentStorageSettingsTest(TestCase):
    """Tests for document storage configuration (DOC5)."""

    def setUp(self):
        enc_module._fernet = None
        self.client = Client()
        self.admin = User.objects.create_user(
            username="admin", password="testpass123", is_admin=True
        )

    def test_admin_can_save_document_storage_settings(self):
        """Admin can configure SharePoint document storage."""
        self.client.login(username="admin", password="testpass123")
        resp = self.client.post("/admin/settings/instance/", {
            "product_name": "TestApp",
            "date_format": "Y-m-d",
            "session_timeout_minutes": "30",
            "document_storage_provider": "sharepoint",
            "document_storage_url_template": "https://contoso.sharepoint.com/sites/KoNote/Clients/{record_id}/",
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            InstanceSetting.get("document_storage_provider"),
            "sharepoint",
        )
        self.assertEqual(
            InstanceSetting.get("document_storage_url_template"),
            "https://contoso.sharepoint.com/sites/KoNote/Clients/{record_id}/",
        )

    def test_admin_can_configure_google_drive(self):
        """Admin can configure Google Drive document storage."""
        self.client.login(username="admin", password="testpass123")
        resp = self.client.post("/admin/settings/instance/", {
            "product_name": "TestApp",
            "date_format": "Y-m-d",
            "session_timeout_minutes": "30",
            "document_storage_provider": "google_drive",
            "document_storage_url_template": "https://drive.google.com/drive/search?q={record_id}",
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            InstanceSetting.get("document_storage_provider"),
            "google_drive",
        )

    def test_admin_can_disable_document_storage(self):
        """Admin can disable document storage by setting provider to 'none'."""
        self.client.login(username="admin", password="testpass123")
        # First enable
        InstanceSetting.objects.create(
            setting_key="document_storage_provider", setting_value="sharepoint"
        )
        # Then disable
        resp = self.client.post("/admin/settings/instance/", {
            "product_name": "TestApp",
            "date_format": "Y-m-d",
            "session_timeout_minutes": "30",
            "document_storage_provider": "none",
            "document_storage_url_template": "",
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            InstanceSetting.get("document_storage_provider"),
            "none",
        )


@override_settings(FIELD_ENCRYPTION_KEY=TEST_KEY)
class DocumentFolderUrlHelperTest(TestCase):
    """Tests for get_document_folder_url() helper function."""

    def setUp(self):
        enc_module._fernet = None
        from django.core.cache import cache
        cache.clear()

    def test_returns_none_when_not_configured(self):
        """Returns None when document storage is not configured."""
        from apps.clients.helpers import get_document_folder_url
        from apps.clients.models import ClientFile

        client = ClientFile.objects.create()
        client.first_name = "Jane"
        client.last_name = "Doe"
        client.record_id = "REC-2024-001"
        client.save()

        url = get_document_folder_url(client)
        self.assertIsNone(url)

    def test_returns_none_when_provider_is_none(self):
        """Returns None when provider is explicitly 'none'."""
        from apps.clients.helpers import get_document_folder_url
        from apps.clients.models import ClientFile
        from django.core.cache import cache

        InstanceSetting.objects.create(
            setting_key="document_storage_provider", setting_value="none"
        )
        cache.clear()

        client = ClientFile.objects.create()
        client.first_name = "Jane"
        client.last_name = "Doe"
        client.record_id = "REC-2024-001"
        client.save()

        url = get_document_folder_url(client)
        self.assertIsNone(url)

    def test_returns_url_with_record_id_substituted(self):
        """Returns URL with {record_id} replaced by client's record ID."""
        from apps.clients.helpers import get_document_folder_url
        from apps.clients.models import ClientFile
        from django.core.cache import cache

        InstanceSetting.objects.create(
            setting_key="document_storage_provider", setting_value="sharepoint"
        )
        InstanceSetting.objects.create(
            setting_key="document_storage_url_template",
            setting_value="https://contoso.sharepoint.com/sites/KoNote/Clients/{record_id}/",
        )
        cache.clear()

        client = ClientFile.objects.create()
        client.first_name = "Jane"
        client.last_name = "Doe"
        client.record_id = "REC-2024-042"
        client.save()

        url = get_document_folder_url(client)
        self.assertEqual(
            url,
            "https://contoso.sharepoint.com/sites/KoNote/Clients/REC-2024-042/",
        )

    def test_returns_none_when_client_has_no_record_id(self):
        """Returns None when client has no record ID."""
        from apps.clients.helpers import get_document_folder_url
        from apps.clients.models import ClientFile
        from django.core.cache import cache

        InstanceSetting.objects.create(
            setting_key="document_storage_provider", setting_value="sharepoint"
        )
        InstanceSetting.objects.create(
            setting_key="document_storage_url_template",
            setting_value="https://contoso.sharepoint.com/sites/KoNote/Clients/{record_id}/",
        )
        cache.clear()

        client = ClientFile.objects.create()
        client.first_name = "Jane"
        client.last_name = "Doe"
        client.record_id = ""  # No record ID
        client.save()

        url = get_document_folder_url(client)
        self.assertIsNone(url)

    def test_google_drive_search_url(self):
        """Google Drive URL uses search with record_id query."""
        from apps.clients.helpers import get_document_folder_url
        from apps.clients.models import ClientFile
        from django.core.cache import cache

        InstanceSetting.objects.create(
            setting_key="document_storage_provider", setting_value="google_drive"
        )
        InstanceSetting.objects.create(
            setting_key="document_storage_url_template",
            setting_value="https://drive.google.com/drive/search?q={record_id}",
        )
        cache.clear()

        client = ClientFile.objects.create()
        client.first_name = "Marcus"
        client.last_name = "Jones"
        client.record_id = "REC-2024-100"
        client.save()

        url = get_document_folder_url(client)
        self.assertEqual(
            url,
            "https://drive.google.com/drive/search?q=REC-2024-100",
        )
