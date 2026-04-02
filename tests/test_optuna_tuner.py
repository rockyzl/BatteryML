# Tests for the Optuna-based hyperparameter tuning module (Phase 2).

import pytest


class TestOptunaTunerImport:
    """Verify the tuner module can be imported gracefully."""

    def test_tuner_import(self):
        """Importing the tuner module should not raise even if optuna is
        not installed — the module should handle the missing dependency
        gracefully or be skipped."""
        try:
            import batteryml.tuner  # noqa: F401
        except ImportError:
            pytest.skip("batteryml.tuner module not yet implemented")
        except Exception as exc:
            # Any other error (e.g. optuna not installed) should be a
            # graceful ImportError or skip, not an unrelated crash.
            pytest.fail(f"Unexpected error importing batteryml.tuner: {exc}")


class TestSearchSpaceParsing:
    """Verify search-space configuration parsing."""

    def test_search_space_parsing(self):
        """Search space dict should be parsed into typed parameter objects."""
        try:
            from batteryml.tuner import SearchSpace  # noqa: F811
        except ImportError:
            pytest.skip("batteryml.tuner.SearchSpace not yet available")

        space_config = {
            'lr': {'type': 'float', 'low': 1e-5, 'high': 1e-1, 'log': True},
            'batch_size': {'type': 'int', 'low': 16, 'high': 128},
            'activation': {'type': 'categorical',
                           'choices': ['relu', 'tanh', 'gelu']},
        }

        space = SearchSpace(space_config)
        params = space.params

        assert 'lr' in params
        assert params['lr']['type'] == 'float'
        assert 'batch_size' in params
        assert params['batch_size']['type'] == 'int'
        assert 'activation' in params
        assert params['activation']['type'] == 'categorical'
