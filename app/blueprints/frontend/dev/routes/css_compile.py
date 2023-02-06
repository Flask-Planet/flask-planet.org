from pathlib import Path

from flask import current_app

from app import logger
from .. import bp


@bp.get("/css-compile")
def css_compile():
    logger.debug("CSS Compile")

    static_folder = Path(current_app.root_path) / "theme" / "static"
    css_folder = static_folder / "css"
    split_css_folder = static_folder / "split_css"
    main_css = css_folder / "main.css"

    logger.debug(f"Creating CSS File: {main_css.name}")

    if main_css.exists():
        main_css.unlink()

    main_css.touch()

    css_files = list(split_css_folder.glob("*.css"))
    css_files.sort()

    for css_file in css_files:
        logger.debug(f"Adding CSS File: {css_file.name}")
        with open(css_file, "r") as f:
            with open(main_css, "a") as f2:
                f2.write(
f"""
/* {css_file.name} */

{f.read()}
"""
                )

    return {"main.css": "Done"}
