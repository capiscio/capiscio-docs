"""
Validation tests for SDK documentation examples.

This file verifies that all code examples in the documentation
actually work against the real SDK. If any test fails, the
corresponding documentation is incorrect.
"""

import pytest
import json
import tempfile
import os
from pathlib import Path


class TestSimpleGuardImports:
    """Test that all documented import patterns work."""

    def test_import_simple_guard_from_module(self):
        """Docs: from capiscio_sdk.simple_guard import SimpleGuard"""
        from capiscio_sdk.simple_guard import SimpleGuard
        assert SimpleGuard is not None

    def test_import_simple_guard_from_package(self):
        """Docs: from capiscio_sdk import SimpleGuard"""
        from capiscio_sdk import SimpleGuard
        assert SimpleGuard is not None

    def test_import_verification_error(self):
        """Docs: from capiscio_sdk.errors import VerificationError"""
        from capiscio_sdk.errors import VerificationError
        assert VerificationError is not None

    def test_import_configuration_error(self):
        """Docs: from capiscio_sdk.errors import ConfigurationError"""
        from capiscio_sdk.errors import ConfigurationError
        assert ConfigurationError is not None

    def test_import_security_config(self):
        """Docs: from capiscio_sdk import SecurityConfig"""
        from capiscio_sdk import SecurityConfig
        assert SecurityConfig is not None

    def test_import_downstream_config(self):
        """Docs: from capiscio_sdk import DownstreamConfig"""
        from capiscio_sdk import DownstreamConfig
        assert DownstreamConfig is not None

    def test_import_upstream_config(self):
        """Docs: from capiscio_sdk import UpstreamConfig"""
        from capiscio_sdk import UpstreamConfig
        assert UpstreamConfig is not None


class TestSimpleGuardInit:
    """Test SimpleGuard initialization patterns from docs."""

    def test_dev_mode_init(self):
        """Docs: guard = SimpleGuard(dev_mode=True)"""
        from capiscio_sdk.simple_guard import SimpleGuard
        guard = SimpleGuard(dev_mode=True)
        assert guard is not None

    def test_dev_mode_explicit_false_in_empty_dir(self):
        """Docs: guard = SimpleGuard()  # dev_mode=False is default - raises if no keys"""
        from capiscio_sdk.simple_guard import SimpleGuard
        from capiscio_sdk.errors import ConfigurationError
        import tempfile
        
        # In a directory with no agent-card.json, should raise ConfigurationError
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                with pytest.raises(ConfigurationError):
                    guard = SimpleGuard(dev_mode=False)
            finally:
                os.chdir(original_cwd)

    def test_base_dir_param_type(self):
        """Verify base_dir accepts string path"""
        from capiscio_sdk.simple_guard import SimpleGuard
        from capiscio_sdk.errors import ConfigurationError
        # Should fail because path doesn't exist, but parameter is valid
        with pytest.raises(ConfigurationError):
            guard = SimpleGuard(base_dir="/nonexistent/path")


class TestSimpleGuardSignOutbound:
    """Test sign_outbound method signature from docs."""

    def test_sign_outbound_basic(self):
        """Docs: jws = guard.sign_outbound({}, body=body_bytes)"""
        from capiscio_sdk.simple_guard import SimpleGuard
        guard = SimpleGuard(dev_mode=True)
        
        jws = guard.sign_outbound({}, body=b"test body")
        assert isinstance(jws, str)
        assert len(jws) > 0
        # JWS format: header.payload.signature
        assert jws.count('.') == 2

    def test_sign_outbound_with_payload(self):
        """Docs: jws = guard.sign_outbound(payload, body=body_bytes)"""
        from capiscio_sdk.simple_guard import SimpleGuard
        guard = SimpleGuard(dev_mode=True)
        
        payload = {"custom": "claim", "iss": "test-agent"}
        jws = guard.sign_outbound(payload, body=b"request body")
        assert isinstance(jws, str)

    def test_sign_outbound_no_body(self):
        """Docs: body parameter is optional"""
        from capiscio_sdk.simple_guard import SimpleGuard
        guard = SimpleGuard(dev_mode=True)
        
        jws = guard.sign_outbound({})
        assert isinstance(jws, str)


class TestSimpleGuardVerifyInbound:
    """Test verify_inbound method signature from docs."""

    def test_verify_inbound_roundtrip(self):
        """Docs: claims = guard.verify_inbound(jws, body=body)"""
        from capiscio_sdk.simple_guard import SimpleGuard
        guard = SimpleGuard(dev_mode=True)
        
        body = b"test body"
        jws = guard.sign_outbound({}, body=body)
        
        claims = guard.verify_inbound(jws, body=body)
        assert isinstance(claims, dict)

    def test_verify_inbound_returns_dict(self):
        """Docs: verify_inbound returns the decoded JWT payload"""
        from capiscio_sdk.simple_guard import SimpleGuard
        guard = SimpleGuard(dev_mode=True)
        
        payload = {"custom": "data"}
        body = b"body"
        jws = guard.sign_outbound(payload, body=body)
        
        claims = guard.verify_inbound(jws, body=body)
        assert "custom" in claims
        assert claims["custom"] == "data"

    def test_verify_inbound_raises_verification_error(self):
        """Docs: Raises VerificationError on invalid signature"""
        from capiscio_sdk.simple_guard import SimpleGuard
        from capiscio_sdk.errors import VerificationError
        guard = SimpleGuard(dev_mode=True)
        
        with pytest.raises(VerificationError):
            guard.verify_inbound("invalid.jws.token", body=b"body")

    def test_verify_inbound_body_integrity(self):
        """Docs: Body modification detected"""
        from capiscio_sdk.simple_guard import SimpleGuard
        from capiscio_sdk.errors import VerificationError
        guard = SimpleGuard(dev_mode=True)
        
        original_body = b"original"
        jws = guard.sign_outbound({}, body=original_body)
        
        with pytest.raises(VerificationError):
            guard.verify_inbound(jws, body=b"tampered")


class TestSimpleGuardMakeHeaders:
    """Test make_headers method signature from docs."""

    def test_make_headers_returns_dict(self):
        """Docs: headers = guard.make_headers(payload, body=body_bytes)"""
        from capiscio_sdk.simple_guard import SimpleGuard
        guard = SimpleGuard(dev_mode=True)
        
        headers = guard.make_headers({}, body=b"body")
        assert isinstance(headers, dict)

    def test_make_headers_contains_badge(self):
        """Docs: Returns {"X-Capiscio-Badge": token} per RFC-002 §9.1"""
        from capiscio_sdk.simple_guard import SimpleGuard
        guard = SimpleGuard(dev_mode=True)
        
        headers = guard.make_headers({}, body=b"body")
        assert "X-Capiscio-Badge" in headers
        assert isinstance(headers["X-Capiscio-Badge"], str)


class TestDevModeFeatures:
    """Test dev_mode specific behaviors from docs."""

    def test_dev_mode_auto_generates_keys(self):
        """Docs: dev_mode=True auto-generates everything"""
        from capiscio_sdk.simple_guard import SimpleGuard
        guard = SimpleGuard(dev_mode=True)
        
        # Should work without any pre-existing keys
        jws = guard.sign_outbound({}, body=b"test")
        assert jws is not None

    def test_dev_mode_agents_can_verify_each_other(self):
        """Docs: Two dev mode guards sharing keys can verify each other"""
        from capiscio_sdk.simple_guard import SimpleGuard
        import tempfile
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Both guards share the same directory
            guard_a = SimpleGuard(base_dir=tmpdir, dev_mode=True)
            guard_b = SimpleGuard(base_dir=tmpdir, dev_mode=True)
            
            body = b"message"
            jws = guard_a.sign_outbound({}, body=body)
            
            # guard_b should be able to verify guard_a's signature
            claims = guard_b.verify_inbound(jws, body=body)
            assert claims is not None


class TestErrorClasses:
    """Test error class behaviors from docs."""

    def test_verification_error_inherits_from_base(self):
        """Docs: VerificationError for invalid signatures"""
        from capiscio_sdk.errors import VerificationError, CapiscioSecurityError
        assert issubclass(VerificationError, CapiscioSecurityError)

    def test_configuration_error_inherits_from_base(self):
        """Docs: ConfigurationError for missing keys"""
        from capiscio_sdk.errors import ConfigurationError, CapiscioSecurityError
        assert issubclass(ConfigurationError, CapiscioSecurityError)


class TestSecurityConfig:
    """Test SecurityConfig patterns from docs."""

    def test_security_config_development(self):
        """Docs: SecurityConfig.development()"""
        from capiscio_sdk import SecurityConfig
        config = SecurityConfig.development()
        assert config is not None

    def test_security_config_production(self):
        """Docs: SecurityConfig.production()"""
        from capiscio_sdk import SecurityConfig
        config = SecurityConfig.production()
        assert config is not None

    def test_security_config_strict(self):
        """Docs: SecurityConfig.strict()"""
        from capiscio_sdk import SecurityConfig
        config = SecurityConfig.strict()
        assert config is not None

    def test_security_config_has_strict_mode(self):
        """Docs: SecurityConfig has strict_mode field"""
        from capiscio_sdk import SecurityConfig
        config = SecurityConfig.development()
        assert hasattr(config, 'strict_mode')


class TestCapiscioMiddlewareImport:
    """Test FastAPI middleware import from docs."""

    def test_import_capiscio_middleware(self):
        """Docs: from capiscio_sdk.integrations.fastapi import CapiscioMiddleware"""
        try:
            from capiscio_sdk.integrations.fastapi import CapiscioMiddleware
            assert CapiscioMiddleware is not None
        except ImportError as e:
            # FastAPI might not be installed, which is okay
            if "fastapi" in str(e).lower():
                pytest.skip("FastAPI not installed")
            raise


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
