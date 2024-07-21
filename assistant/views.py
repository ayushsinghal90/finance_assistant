import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.exceptions import ValidationError

from .api.responses import ResponseFactory
from .core.assistant import Assistant
from .exceptions.AssistantError import AssistantError
from .serializer import FinancialInfoSerializer
from .utils import validate_file

logger = logging.getLogger('myapp')
assistant = Assistant()


class AssistantView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_obj = request.data['file']

        try:
            validate_file(
                file_obj,
                max_size_mb=0.5,
                allowed_extensions=['.txt'],
                allowed_content_types=['text/plain']
            )

            content = file_obj.read().decode('utf-8')
            response = assistant.extract_finance_info(content)
            logger.info("Got response from model for finance info")

            serializer = FinancialInfoSerializer(data=response)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=201)
        except Exception as e:
            if isinstance(e, AssistantError):
                logger.error("Error while calling assistant", e)
            elif isinstance(e, ValidationError):
                logger.error("User Input error")
                return ResponseFactory.bad_request(e.message)
            else:
                logger.error("Error while saving response", e)
            return ResponseFactory.server_error()


