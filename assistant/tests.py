from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
import io
import logging

from assistant.exceptions.AssistantError import AssistantError


class AssistantTests(TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.client = APIClient()

    @patch('assistant.core.assistant.Assistant.extract_finance_info')
    def test_assistant_valid(self, mock_extract_finance_info):
        mock_response = {'assets': 'some_value', 'expenditures': "test data", 'income': "test data",}
        mock_extract_finance_info.return_value = mock_response

        file_content = "Martin is a partner in a law firm in London, earning an average of £15,000 per month before taxes."
        file = io.BytesIO(file_content.encode('utf-8'))
        file.name = 'test.txt'
        response = self.client.post('/api/upload/', {'file': file}, format='multipart')

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('assets'), mock_response.get('assets'))
        self.assertEqual(response.data.get('expenditures'), mock_response.get('expenditures'))
        self.assertEqual(response.data.get('income'), mock_response.get('income'))
        mock_extract_finance_info.assert_called_once_with(file_content)

    @patch('assistant.core.assistant.Assistant.extract_finance_info')
    def test_assistant_model_failed(self, mock_extract_finance_info):
        mock_extract_finance_info.side_effect = AssistantError("Test Exception")

        file_content = "Martin is a partner in a law firm in London, earning an average of £15,000 per month before taxes."
        file = io.BytesIO(file_content.encode('utf-8'))
        file.name = 'test.txt'
        response = self.client.post('/api/upload/', {'file': file}, format='multipart')

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        mock_extract_finance_info.assert_called_once_with(file_content)

    def test_assistant_invalid_file_format(self):
        file = io.BytesIO("Some content".encode('utf-8'))
        file.name = 'test.pdf'
        response = self.client.post('/api/upload/', {'file': file}, format='multipart')

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_assistant_empty_file(self):
        file = io.BytesIO("".encode('utf-8'))
        file.name = 'test.txt'
        response = self.client.post('/api/upload/', {'file': file}, format='multipart')

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertIn("File should not be empty.", response.data['message'])
