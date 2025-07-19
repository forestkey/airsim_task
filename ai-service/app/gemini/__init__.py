from .client_with_proxy import get_gemini_client

# Lazy initialization wrapper
class LazyGeminiClient:
    def __init__(self):
        self._client = None
    
    def __getattr__(self, name):
        if self._client is None:
            self._client = get_gemini_client()
        return getattr(self._client, name)

# Export lazy client
gemini_client = LazyGeminiClient()

__all__ = ["gemini_client"] 