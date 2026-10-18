# ==================================================================================================
# topology_engine.py
#
# Difference Retention Laboratory
# Topology Engine v1
#
# Version : 1.0
# Status  : CORE PROCESS ENGINE / NO PHYSICS
#
# Назначение:
#   Движок топологии среды.
#
# Принцип:
#   TopologyEngine не выполняет переходы.
#   TopologyEngine не вычисляет инварианты.
#   TopologyEngine не наблюдает среду.
#   TopologyEngine не управляет памятью и удержанием.
#
#   Его обязанность:
#       хранить и проверять структурную связность Pages и Spines.
#
# ==================================================================================================


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from page import Page
from spine import Spine


# ==================================================================================================
# TOPOLOGY REPORT
# ==================================================================================================


@dataclass
class TopologyReport:
    valid: bool
    pages_count: int
    spines_count: int
    page_ids: list[str]
    spine_ids: list[str]
    invalid_spines: list[str] = field(default_factory=list)
    details: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "pages_count": self.pages_count,
            "spines_count": self.spines_count,
            "page_ids": list(self.page_ids),
            "spine_ids": list(self.spine_ids),
            "invalid_spines": list(self.invalid_spines),
            "details": self.details,
        }


# ==================================================================================================
# TOPOLOGY ENGINE
# ==================================================================================================


@dataclass
class TopologyEngine:
    name: str = "TOPOLOGY_ENGINE_v1"

    def validate(
        self,
        pages: dict[str, Page],
        spines: list[Spine],
    ) -> TopologyReport:
        page_ids = list(pages.keys())
        spine_ids = [
            spine.spine_id
            for spine in spines
        ]

        invalid_spines: list[str] = []

        for spine in spines:
            if spine.from_page not in pages or spine.to_page not in pages:
                invalid_spines.append(spine.spine_id)

        valid = len(invalid_spines) == 0

        return TopologyReport(
            valid=valid,
            pages_count=len(pages),
            spines_count=len(spines),
            page_ids=page_ids,
            spine_ids=spine_ids,
            invalid_spines=invalid_spines,
            details=(
                "Topology is valid."
                if valid
                else "Topology contains invalid spine endpoints."
            ),
        )

    def register_page(
        self,
        pages: dict[str, Page],
        page: Page,
    ) -> dict[str, Page]:
        if page.page_id in pages:
            raise ValueError(f"Page already registered: {page.page_id}")

        pages[page.page_id] = page

        return pages

    def register_spine(
        self,
        pages: dict[str, Page],
        spines: list[Spine],
        spine: Spine,
    ) -> list[Spine]:
        if spine.from_page not in pages:
            raise ValueError(f"Spine source page not registered: {spine.from_page}")

        if spine.to_page not in pages:
            raise ValueError(f"Spine target page not registered: {spine.to_page}")

        spines.append(spine)

        return spines

    def to_dict(
        self,
        pages: dict[str, Page],
        spines: list[Spine],
    ) -> dict[str, Any]:
        report = self.validate(
            pages=pages,
            spines=spines,
        )

        return {
            "name": self.name,
            "report": report.to_dict(),
        }