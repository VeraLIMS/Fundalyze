"""Client for custom finance API configured via ``finance_api.yaml``.

The optional configuration file ``config/finance_api.yaml`` defines the base
URL, API key, and endpoint paths for retrieving financial data from a custom
source. :class:`FinanceAPIClient` provides a small wrapper around ``requests``
for easy access to these endpoints.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional

import requests
import yaml

from modules.config_utils import CONFIG_DIR

DEFAULT_TIMEOUT = 10
CONFIG_FILE = CONFIG_DIR / "finance_api.yaml"


@dataclass
class FinanceAPIConfig:
    """Configuration options for :class:`FinanceAPIClient`."""

    base_url: str
    api_key: Optional[str] = None
    endpoints: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def load(cls, path: Path | None = None) -> "FinanceAPIConfig":
        """Load configuration from ``path`` or the default location.

        Parameters
        ----------
        path:
            Optional path to a YAML file. If omitted, ``config/finance_api.yaml``
            is used.

        Returns
        -------
        FinanceAPIConfig
            Parsed configuration object.
        """

        cfg_path = path or CONFIG_FILE
        if not cfg_path.is_file():
            raise FileNotFoundError(f"Finance API config not found: {cfg_path}")
        with open(cfg_path, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
        return cls(
            base_url=str(data.get("base_url", "")),
            api_key=data.get("api_key"),
            endpoints=data.get("endpoints", {}) or {},
        )


class FinanceAPIClient:
    """Simple client for a user-configured finance API."""

    def __init__(self, config: FinanceAPIConfig, timeout: int = DEFAULT_TIMEOUT) -> None:
        self.config = config
        self.timeout = timeout

    # ------------------------------------------------------------------
    # internal helpers
    # ------------------------------------------------------------------
    def _build_url(self, endpoint: str, **params: Any) -> str:
        base = self.config.base_url.rstrip("/")
        path = endpoint.format(**params).lstrip("/")
        url = f"{base}/{path}"
        if self.config.api_key:
            sep = "&" if "?" in url else "?"
            url = f"{url}{sep}apikey={self.config.api_key}"
        return url

    def _get(self, endpoint_key: str, **params: Any) -> requests.Response:
        if endpoint_key not in self.config.endpoints:
            raise KeyError(f"Unknown endpoint '{endpoint_key}'")
        url = self._build_url(self.config.endpoints[endpoint_key], **params)
        resp = requests.get(url, timeout=self.timeout)
        resp.raise_for_status()
        return resp

    # ------------------------------------------------------------------
    # public API methods
    # ------------------------------------------------------------------
    def get_profile(self, symbol: str) -> Dict[str, Any]:
        """Return company profile information as JSON."""

        resp = self._get("profile", symbol=symbol)
        return resp.json()

    def get_prices(self, symbol: str, period: str) -> Dict[str, Any]:
        """Return price history as JSON."""

        resp = self._get("prices", symbol=symbol, period=period)
        return resp.json()
