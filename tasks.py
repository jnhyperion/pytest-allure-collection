import os
import sys
import shutil
import logging
from pathlib import Path
from invoke import task

logger = logging
logger_kwargs = {
    "level": logging.INFO,
    "format": "%(asctime)s %(levelname)s - %(message)s",
    "force": True,
}
logger.basicConfig(**logger_kwargs)

pkg_folder_name = "pytest_allure_collection"


def _get_ctx_abs_path(ctx, *path) -> str:
    return os.path.join(os.path.abspath(ctx.cwd), *path)


@task
def clean(ctx):
    shutil.rmtree(
        _get_ctx_abs_path(ctx, "htmlcov"),
        ignore_errors=True,
    )
    shutil.rmtree(
        _get_ctx_abs_path(ctx, ".pytest_cache"),
        ignore_errors=True,
    )
    shutil.rmtree(
        _get_ctx_abs_path(ctx, ".tox"),
        ignore_errors=True,
    )
    Path(_get_ctx_abs_path(ctx, ".coverage")).unlink(missing_ok=True)
    shutil.rmtree(_get_ctx_abs_path(ctx, "build"), ignore_errors=True)
    shutil.rmtree(_get_ctx_abs_path(ctx, "dist"), ignore_errors=True)
    shutil.rmtree(
        _get_ctx_abs_path(ctx, f"{pkg_folder_name}.egg-info"),
        ignore_errors=True,
    )


@task(clean)
def build(ctx, skip_uninstall=False):
    ctx.run(f"{sys.executable} setup.py bdist_wheel", hide="out")
    dist = _get_ctx_abs_path(ctx, "dist")
    wheel_file = os.path.join(dist, os.listdir(dist)[0])
    assert wheel_file.endswith(".whl")
    ctx.run(f"pip install {wheel_file}", hide="out")
    if not skip_uninstall:
        uninstall(ctx)


@task(clean)
def install(ctx):
    uninstall(ctx)
    build(ctx, skip_uninstall=True)
    clean(ctx)


@task
def uninstall(ctx):
    ctx.run(f"pip uninstall pytest-allure-collection -y", hide="out")


@task
def style_check(ctx):
    ctx.run("black . --check --diff")


@task
def reformat_code(ctx):
    ctx.run("black .")


@task
def test(ctx):
    ctx.run(f"tox")


@task
def lint(ctx):
    ctx.run(
        f"pylint ./{pkg_folder_name} --disable=R,C,W1514,W0703,W0212,W0123,W1203"
        f" --extension-pkg-whitelist=cv2,numpy",
    )


@task(build)
def publish(ctx):
    ctx.run(f"{sys.executable} -m twine upload dist/*")
