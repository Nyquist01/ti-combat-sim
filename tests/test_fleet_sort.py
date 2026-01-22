from src.main import sort_fleet, Dreadnaught, Fighter, Carrier, Ship

import pytest



@pytest.mark.parametrize(
    ("fleet", "expected_ship", "expected_hp"),
    [
        (
            [Dreadnaught(hp=1), Dreadnaught(hp=2), Dreadnaught(hp=3)],
            Dreadnaught,
            3
        ),
        (
            [Dreadnaught(hp=1), Dreadnaught(hp=2), Fighter(), Fighter(), Carrier()],
            Carrier,
            1
        ),
    ]
)
def test_sort_fleet(fleet: list[Ship], expected_ship, expected_hp):
    """
    When a homogenous fleet is sorted, the ship with the high HP should be
    put first.
    """
    sort_fleet(fleet)

    assert isinstance(fleet[0], expected_ship)
    assert fleet[0].hp == expected_hp
