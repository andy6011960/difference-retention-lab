# ==================================================================================================
# demo_environment.py
#
# Difference Retention Laboratory
# Demo Book Environment v1
#
# Version : 1.1
# Status  : DEMO ENVIRONMENT / NO PHYSICS
#
# Назначение:
#   Демонстрационная среда для проверки Book Environment Core.
#
# Принцип:
#   Этот файл содержит только тестовую конфигурацию книги:
#       - demo pages
#       - demo spines
#       - demo local dynamics
#       - demo transition actions
#
# ==================================================================================================


from __future__ import annotations

from book_environment_core_v1 import BookEnvironment, Spine
from invariant import DeltaInvariant
from page import Page
from state import BookState


# ==================================================================================================
# DEMO PAGE DYNAMICS
# ==================================================================================================


def demo_decay_page(state: BookState) -> BookState:
    decay = float(state.metadata.get("decay", 0.90))
    state.update_delta(state.delta * decay)
    return state


def demo_inverse_page(state: BookState) -> BookState:
    decay = float(state.metadata.get("inverse_decay", 0.92))
    state.update_delta(state.delta * -decay)
    return state


# ==================================================================================================
# DEMO BOUNDARIES / TRANSITIONS
# ==================================================================================================


def demo_boundary_low_delta(state: BookState) -> bool:
    threshold = float(state.metadata.get("turn_threshold", 0.25))
    return abs(state.delta) < threshold


def demo_turn_action(state: BookState) -> BookState:
    boost = float(state.metadata.get("turn_boost", 1.6))
    state.update_delta(state.delta * -boost)
    return state


# ==================================================================================================
# ENVIRONMENT BUILDER
# ==================================================================================================


def build_demo_environment() -> BookEnvironment:
    env = BookEnvironment(
        book_id="DEMO_BOOK_ENVIRONMENT_v1_2",
        title="Demo Book Environment",
        invariant=DeltaInvariant(
            threshold=0.05,
        ),
    )

    env.register_page(
        Page(
            page_id="PAGE_POSITIVE_DECAY",
            title="Positive Decay Page",
            description="Demo page with monotonic delta decay.",
            local_step=demo_decay_page,
            capabilities=[
                "decay",
                "delta_retention",
                "positive_orientation",
            ],
        ),
        initial=True,
    )

    env.register_page(
        Page(
            page_id="PAGE_INVERSE",
            title="Inverse Orientation Page",
            description="Demo page that flips orientation during local dynamics.",
            local_step=demo_inverse_page,
            capabilities=[
                "decay",
                "orientation_flip",
                "delta_retention",
            ],
        ),
    )

    env.register_spine(
        Spine(
            spine_id="SPINE_LOW_DELTA_TURN",
            from_page="PAGE_POSITIVE_DECAY",
            to_page="PAGE_INVERSE",
            condition=demo_boundary_low_delta,
            action=demo_turn_action,
            description="Turn page when |delta| becomes too low.",
        )
    )

    env.register_spine(
        Spine(
            spine_id="SPINE_RETURN_AFTER_INVERSION",
            from_page="PAGE_INVERSE",
            to_page="PAGE_POSITIVE_DECAY",
            condition=demo_boundary_low_delta,
            action=demo_turn_action,
            description="Return page after inversion when |delta| becomes too low.",
        )
    )

    env.initialize_state(
        delta=1.0,
        dt=1.0,
        metadata={
            "decay": 0.82,
            "inverse_decay": 0.88,
            "turn_threshold": 0.25,
            "turn_boost": 1.8,
        },
    )

    return env