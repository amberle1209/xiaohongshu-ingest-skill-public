#!/usr/bin/env python3
"""Validate an HTTP(S) URL and each navigation redirect before retrieval."""

from __future__ import annotations

import argparse
import http.client
import ipaddress
import socket
import sys
from urllib.parse import urljoin, urlsplit


REDIRECTS = {301, 302, 303, 307, 308}


def validate_url(url: str) -> tuple[str, str, int, str]:
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("URL scheme must be http or https")
    if not parsed.hostname:
        raise ValueError("URL must include a hostname")
    if parsed.username or parsed.password:
        raise ValueError("URL must not contain embedded credentials")
    try:
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
    except ValueError as exc:
        raise ValueError("URL port is invalid") from exc
    return parsed.scheme, parsed.hostname, port, parsed.path or "/"


def public_addresses(hostname: str, port: int) -> list[str]:
    try:
        addresses = socket.getaddrinfo(hostname, port, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise ValueError(f"hostname cannot be resolved: {hostname}") from exc
    resolved = {entry[4][0] for entry in addresses}
    if not resolved:
        raise ValueError(f"hostname has no addresses: {hostname}")
    for address in resolved:
        if not ipaddress.ip_address(address).is_global:
            raise ValueError(f"hostname resolves to a non-public address: {hostname}")
    return sorted(resolved)


class CheckedHTTPConnection(http.client.HTTPConnection):
    def __init__(self, hostname: str, port: int, address: str, timeout: float):
        super().__init__(hostname, port, timeout=timeout)
        self._address = address

    def connect(self) -> None:
        self.sock = socket.create_connection((self._address, self.port), self.timeout)


class CheckedHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, hostname: str, port: int, address: str, timeout: float):
        super().__init__(hostname, port, timeout=timeout)
        self._address = address

    def connect(self) -> None:
        self.sock = socket.create_connection((self._address, self.port), self.timeout)
        self.sock = self._context.wrap_socket(self.sock, server_hostname=self.host)


def request_once(url: str, timeout: float) -> tuple[int, str | None]:
    scheme, hostname, port, path = validate_url(url)
    address = public_addresses(hostname, port)[0]
    query = urlsplit(url).query
    if query:
        path = f"{path}?{query}"
    connection_class = CheckedHTTPSConnection if scheme == "https" else CheckedHTTPConnection
    connection = connection_class(hostname, port, address, timeout)
    try:
        connection.request("GET", path, headers={"User-Agent": "content-ingest-url-validator/1.0", "Range": "bytes=0-0"})
        response = connection.getresponse()
        response.read(1024)
        return response.status, response.getheader("Location")
    finally:
        connection.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--max-redirects", type=int, default=5)
    parser.add_argument("--timeout", type=float, default=15)
    args = parser.parse_args()
    if args.max_redirects < 0:
        parser.error("--max-redirects must be non-negative")

    current = args.url
    try:
        for _ in range(args.max_redirects + 1):
            status, location = request_once(current, args.timeout)
            if status not in REDIRECTS:
                print(current)
                return 0
            if not location:
                raise ValueError("redirect response is missing Location")
            current = urljoin(current, location)
        raise ValueError("redirect limit exceeded")
    except (OSError, ValueError, http.client.HTTPException) as exc:
        print(f"URL validation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
