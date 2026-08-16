#!/usr/bin/env python3
"""Validate the portable APP_CHECKER JSON manifest without extra packages."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


VALID_APP_TYPES = {
    "website",
    "web-app",
    "browser-game",
    "educational-app",
    "mobile",
    "desktop",
    "other",
}
VALID_INPUTS = {"pointer", "keyboard", "touch", "gamepad", "screen-reader"}


def fail(message: str) -> None:
    print(f"ERROR: {message}")


def validate(data: Any) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(data, dict):
        return ["manifest root must be a JSON object"], warnings

    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.append("name must be a non-empty string")

    url = data.get("url")
    start_command = data.get("startCommand")
    if not (isinstance(url, str) and url.strip()) and not (
        isinstance(start_command, str) and start_command.strip()
    ):
        errors.append("provide at least one non-empty url or startCommand")

    journeys = data.get("criticalJourneys")
    if not isinstance(journeys, list) or not journeys:
        errors.append("criticalJourneys must be a non-empty array")
    elif any(not isinstance(item, str) or not item.strip() for item in journeys):
        errors.append("every criticalJourneys item must be a non-empty string")

    app_type = data.get("appType")
    if app_type is not None and app_type not in VALID_APP_TYPES:
        warnings.append(
            f"appType {app_type!r} is not one of: {', '.join(sorted(VALID_APP_TYPES))}"
        )

    inputs = data.get("supportedInputs")
    if inputs is not None:
        if not isinstance(inputs, list):
            errors.append("supportedInputs must be an array")
        else:
            unknown = [item for item in inputs if item not in VALID_INPUTS]
            if unknown:
                warnings.append(f"unrecognized supportedInputs: {unknown}")

    viewports = data.get("viewports")
    if viewports is not None:
        if not isinstance(viewports, list):
            errors.append("viewports must be an array")
        else:
            for index, viewport in enumerate(viewports):
                if not isinstance(viewport, dict):
                    errors.append(f"viewports[{index}] must be an object")
                    continue
                for dimension in ("width", "height"):
                    value = viewport.get(dimension)
                    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                        errors.append(
                            f"viewports[{index}].{dimension} must be a positive integer"
                        )

    for field in ("criticalControls", "learningGoals", "appSpecificAssertions"):
        value = data.get(field)
        if value is not None and (
            not isinstance(value, list)
            or any(not isinstance(item, str) or not item.strip() for item in value)
        ):
            errors.append(f"{field} must be an array of non-empty strings")

    if not data.get("supportedInputs"):
        warnings.append("supportedInputs is absent; infer and record the tested inputs")
    if not data.get("viewports"):
        warnings.append("viewports is absent; infer and record representative sizes")

    return errors, warnings


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_manifest.py <app-checker.json>")
        return 2

    path = Path(sys.argv[1])
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError:
        fail(f"file not found: {path}")
        return 2
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}")
        return 1
    except OSError as exc:
        fail(f"could not read {path}: {exc}")
        return 2

    errors, warnings = validate(data)
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        fail(error)

    if errors:
        print(f"INVALID: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    print(f"OK: {path} ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
