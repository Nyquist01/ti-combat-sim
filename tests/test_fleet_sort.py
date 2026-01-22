from src.main import sort_fleet, Dreadnaught


def test_sort():
    fleet = [Dreadnaught(hp=1), Dreadnaught(hp=2)]
    sort_fleet(fleet)
    assert fleet[0].hp == 2
