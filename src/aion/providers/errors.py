class ProviderError(Exception):
    """Base error for model provider failures."""


class ProviderQuotaExceeded(ProviderError):
    """The provider has exhausted its available quota."""


class ProviderUnavailable(ProviderError):
    """The provider is temporarily unavailable."""


class ProviderAuthenticationError(ProviderError):
    """The provider credentials are invalid or missing."""


class ProviderRequestError(ProviderError):
    """The request sent to the provider is invalid."""
