from typing import Any, Dict, Optional, List  # noqa
import argparse

import attr
from path import Path
import schema
import ruamel.yaml

import tsrc.config

MANIFEST_CONFIG_SCHEMA = schema.Schema({
    "url": str,
    schema.Optional("branch"): str,
    schema.Optional("tag"): str,
    schema.Optional("groups"): [str],
    schema.Optional("shallow"): bool,
})


@attr.s
class ManifestConfig:
    url = attr.ib(default=None)  # type: str
    branch = attr.ib(default="master")  # type: str
    tag = attr.ib(default=None)  # type: Optional[str]
    shallow = attr.ib(default=False)  # type: bool
    groups = attr.ib(default=list())  # type: List[str]


def from_dict(as_dict: dict) -> ManifestConfig:
    res = ManifestConfig()
    res.url = as_dict["url"]
    res.branch = as_dict.get("branch", "master")
    res.tag = as_dict.get("tag")
    res.shallow = as_dict.get("shallow", False)
    res.groups = as_dict.get("groups") or list()
    return res


def from_args(args: argparse.Namespace) -> ManifestConfig:
    as_dict = vars(args)  # type: dict
    return from_dict(as_dict)


def from_file(cfg_path: Path) -> ManifestConfig:
    as_dict = tsrc.config.parse_config_file(cfg_path, MANIFEST_CONFIG_SCHEMA)  # type: dict
    return from_dict(as_dict)


def to_file(config: ManifestConfig, cfg_path: Path) -> None:
    as_dict = dict()  # type: Dict[str, Any]
    as_dict["url"] = config.url
    as_dict["branch"] = config.branch
    if config.tag:
        as_dict["tag"] = config.tag
    if config.groups:
        as_dict["groups"] = config.groups
    as_dict["shallow"] = config.shallow
    with cfg_path.open("w") as fp:
        ruamel.yaml.dump(as_dict, fp)
