import pytest

from eegeyenet.datasets import fetch_eegeyenet

@pytest.mark.parametrize(
        "subject, run",
        [
            ("EP10", 1),
            ("BZ4", 1),
        ]
)
def test_fetch_eegeyenet(subject, run):
    """Test downloading eegeyenet data."""
    fetch_dataset_kwargs = dict(force_update=True)
    fname = fetch_eegeyenet(
        subject=subject,
        run=run,
        fetch_dataset_kwargs=fetch_dataset_kwargs
        )
    assert fname.exists()
