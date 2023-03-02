import pytest

from contexts.shared.domain.value_objects import Uuid


class TestUuid:
    @pytest.mark.parametrize(
        "uuid_str",
        [
            "5a4756bf-aeb1-4226-89b7-130a68d67fb3",
            "5e7b1c21-9cb9-495f-9664-2b26bdbb37d1",
        ],
    )
    def test_should_instantiate_from_valid_string(self, uuid_str):
        uuid = Uuid(uuid_str)
        assert uuid.value == uuid_str

    @pytest.mark.parametrize(
        "uuid_str",
        ["some-value", "some-text"],
    )
    def test_should_fail_instantiate_from_invalid_string(self, uuid_str):
        with pytest.raises(ValueError):
            Uuid(uuid_str)

    def test_should_create_random_uuid(self):
        uuid = Uuid.random()
        isinstance(uuid, Uuid)
