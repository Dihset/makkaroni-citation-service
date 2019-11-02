from aiohttp.web import HTTPClientError, json_response, middleware

# Add your exceptions
@middleware
async def error_middleware(request, handler):
    try:
        return await handler(request)
    except HTTPClientError as error:
        return json_response(
            {'error': error.text},
            status=error.status_code
        )
