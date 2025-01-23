"""Script to write a small subset of the EEGEyeNet dataset to BIDS."""
import itertools
from pathlib import Path

from eegeyenet.datasets.eegeyenet import fetch_eegeyenet, get_subjects_runs
from eegeyenet.io import read_raw_eegeyenet

import mne_bids

BIDS_DIR = Path(__file__).resolve().parent.parent / "bids"
subjects_runs = get_subjects_runs()
# Just take the 5 first subjects from this dictionary
for subject, runs in itertools.islice(subjects_runs.items(), 3):
    use_run = runs.min() # e.g. 1, or 2 in some cases if run 1 in missing.
    fpath = fetch_eegeyenet(subject=subject, run=use_run)
    raw = read_raw_eegeyenet(fpath)

    raw.drop_channels(["TIME"])  # original dataset has a TIME channel. We don't need it
    raw.set_montage("GSN-HydroCel-129", match_case=False, match_alias=True)
    bids_path = mne_bids.BIDSPath(
        root=BIDS_DIR,
        subject=subject,
        session="01",
        run=str(use_run).zfill(2),
        datatype="eeg",
        task="dots"
        )
    mne_bids.write_raw_bids(
        raw,
        bids_path,
        allow_preload=True,
        format="EDF",
        overwrite=True
        )

# Now write the dataset description
bids_path = mne_bids.BIDSPath(
    root=bids_path.root,
)

mne_bids.make_dataset_description(
    path=bids_path.root,
    name="EEGEyeNet Dataset",
    dataset_type="raw",
    data_license="Please see the file named license.txt at https://osf.io/ktv7m/",
    authors=[
        "Martyna Beata Płomecka",
        "Ard Kastrati",
        "Nicolas Langer"
    ],
    acknowledgements="We thank the authors of the original EEGEyeNet paper for Making this dataset available.",
    how_to_acknowledge="Kastrati, A., Płomecka, M. B., Pascual, D., Wolf, L., Gillioz, V., Wattenhofer, R., & Langer, N. (2021). EEGEyeNet: A Simultaneous Electroencephalography and Eye-tracking Dataset and Benchmark for Eye Movement Prediction (Version 2). arXiv. https://doi.org/10.48550/ARXIV.2111.05100",
    funding=["Velux Stiftung Project No. 1126",  "Schweizerischer Nationalfonds zur Förderungder Wissenschaftlichen Forschung (SNF) Grant 100014175875"],
    ethics_approvals=["The study was approved by the Institutional Review Board of Canton Zurich(BASEC-Nr. 2017-00226)"],
    references_and_links="Kastrati, A., Płomecka, M. B., Pascual, D., Wolf, L., Gillioz, V., Wattenhofer, R., & Langer, N. (2021). EEGEyeNet: A Simultaneous Electroencephalography and Eye-tracking Dataset and Benchmark for Eye Movement Prediction (Version 2). arXiv. https://doi.org/10.48550/ARXIV.2111.05100",
    doi="10.17605/OSF.IO/KTV7M",
    generated_by=[dict(Name="https://github.com/scott-huberty/example-bids-dataset-eegeyenet.git")],
    source_datasets=[dict(URL="https://osf.io/ktv7m/", DOI="10.17605/OSF.IO/KTV7M")],
    overwrite=True,
)