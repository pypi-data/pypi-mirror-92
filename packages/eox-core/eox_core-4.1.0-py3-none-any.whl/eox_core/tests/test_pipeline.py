#!/usr/bin/python
"""
Tests for the pipeline module used in third party auth.
"""
from django.test import TestCase
from mock import MagicMock, PropertyMock, patch

from eox_core.pipeline import check_disconnect_pipeline_enabled, ensure_user_has_profile


class EnsureUserProfileTest(TestCase):
    """
    Test the custom association backend.
    """
    def setUp(self):
        self.backend_mock = MagicMock()
        self.user_mock = MagicMock()

    @patch('eox_core.edxapp_wrapper.users.import_module')
    def test_user_with_profile_works(self, import_mock):
        """
        A user that already has a profile will do nothing
        """
        backend = MagicMock()
        import_mock.side_effect = backend

        ensure_user_has_profile(self.backend_mock, {}, user=self.user_mock)
        backend().get_user_profile().assert_not_called()

    @patch('eox_core.edxapp_wrapper.users.import_module')
    def test_user_without_profile_works(self, import_mock):
        """
        A user that has no profile will create one
        """
        backend = MagicMock()
        import_mock.side_effect = backend
        backend().get_user_profile().DoesNotExist = ValueError
        type(self.user_mock).profile = PropertyMock(side_effect=ValueError)

        ensure_user_has_profile(self.backend_mock, {}, user=self.user_mock)
        backend().get_user_profile().objects.create.assert_called()


class TestDisconnectionPipeline(TestCase):
    """Test disconnection from TPA provider."""

    def setUp(self):
        self.backend_mock = MagicMock()

    def test_disable_disconnect_pipeline(self):
        """
        Test disabling disconnection pipeline through TPA provider settings.
        """
        self.backend_mock.setting.return_value.get.return_value = True

        with self.assertRaises(Exception):
            check_disconnect_pipeline_enabled(self.backend_mock)

    def test_disconnect_pipeline_enable_explicit(self):
        """
        Test explicitly enable disconnection pipeline through TPA provider settings.
        """
        self.backend_mock.setting.return_value.get.return_value = False

        self.assertIsNone(check_disconnect_pipeline_enabled(self.backend_mock))

    def test_disconnect_pipeline_enable_implicit(self):
        """
        Test enable disconnection pipeline by not defining disable setting through TPA
        provider settings.
        """
        self.backend_mock.setting.return_value.get.return_value = None

        self.assertIsNone(check_disconnect_pipeline_enabled(self.backend_mock))
