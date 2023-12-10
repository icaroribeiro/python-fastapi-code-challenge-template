# from unittest.mock import patch
#
# import pytest
# from src import create_app
# from tests.src.infrastructure.db.test_db_fixtures import TestDBFixtures
#
#
# class TestAPPFixtures(TestDBFixtures):
#     @pytest.fixture
#     def test_client(self, session):
#         with patch("src.infrastructure.db.db.DB.build_session") as datastore_mock:
#             datastore_mock.return_value = session
#
#             flask_app = create_app()
#             with flask_app.test_client() as flask_client:
#                 with flask_app.app_context():
#                     yield flask_client
