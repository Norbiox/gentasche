import pytest
import gentasche


def test_random_swap_in():
    l = [1,2,3,4,5,6]
    new_l = gentasche.random_swap_in(l)
    assert new_l != l
    assert set(new_l) == set(l)


def test_reading_dataset_file(tmpdir):
    p = tmpdir / 'data.data'
    content = "3\n2\n1 2\n4 5\n7 8"
    p.write(content)
    filepath = p.strpath
    dataset = gentasche.Dataset.read(filepath)
    assert dataset.name == 'data.data'
    assert dataset.n_tasks == 3
    assert dataset.n_processors == 2
    assert dataset.time_matrix[1][1] == 5.0
