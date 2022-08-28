from __future__ import annotations

import pytest

from poetry.core.version.pep440 import Release
from poetry.core.version.pep440 import ReleaseTag
from poetry.core.version.pep440.segments import RELEASE_PHASE_NORMALIZATIONS


@pytest.mark.parametrize(
    "parts,result",
    [
        ((1,), Release(1)),
        ((1, 2), Release(1, 2)),
        ((1, 2, 3), Release(1, 2, 3)),
        ((1, 2, 3, 4), Release(1, 2, 3, 4)),
        ((1, 2, 3, 4, 5, 6), Release(1, 2, 3, (4, 5, 6))),
    ],
)
def test_pep440_release_segment_from_parts(
    parts: tuple[int, ...], result: Release
) -> None:
    assert Release.from_parts(*parts) == result


@pytest.mark.parametrize(
    "parts,result",
    [
        (("a",), ReleaseTag("alpha", 0)),
        (("a", 1), ReleaseTag("alpha", 1)),
        (("b",), ReleaseTag("beta", 0)),
        (("b", 1), ReleaseTag("beta", 1)),
        (("pre",), ReleaseTag("preview", 0)),
        (("pre", 1), ReleaseTag("preview", 1)),
        (("c",), ReleaseTag("rc", 0)),
        (("c", 1), ReleaseTag("rc", 1)),
        (("r",), ReleaseTag("rev", 0)),
        (("r", 1), ReleaseTag("rev", 1)),
    ],
)
def test_pep440_release_tag_normalisation(
    parts: tuple[str] | tuple[str, int], result: ReleaseTag
) -> None:
    tag = ReleaseTag(*parts)
    assert tag == result
    assert tag.to_string() == result.to_string()


@pytest.mark.parametrize(
    "parts,result",
    [
        (("a",), ReleaseTag("beta")),
        (("b",), ReleaseTag("rc")),
        (("post",), None),
        (("rc",), None),
        (("rev",), None),
        (("dev",), None),
    ],
)
def test_pep440_release_tag_next_phase(
    parts: tuple[str], result: ReleaseTag | None
) -> None:
    assert ReleaseTag(*parts).next_phase() == result


@pytest.mark.parametrize("phase", list({*RELEASE_PHASE_NORMALIZATIONS.keys()}))
def test_pep440_release_tag_next(phase: str) -> None:
    tag = ReleaseTag(phase=phase).next()
    assert tag.phase == RELEASE_PHASE_NORMALIZATIONS[phase]
    assert tag.number == 1