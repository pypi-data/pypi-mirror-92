#!/usr/bin/env python3

import os
import re
from datetime import date


def determine_tags(version_string, app_env, include_major):
    tags = ""

    if "-" in version_string:
        extra_info = version_string[version_string.find("-") :]
        version_string = version_string[: version_string.find("-")]
    else:
        extra_info = ""

    if app_env:
        app_env = "-" + app_env
    else:
        app_env = ""

    while "." in version_string:
        tags = tags + version_string + extra_info + app_env + ","
        version_string = version_string[: version_string.rfind(".")]

    if include_major == "yes" and version_string != "0":
        tags = tags + version_string + extra_info + app_env
    else:
        tags = tags[:-1]

    return tags


def write_tags_to_file(tags):
    with open(".tags", "w") as file:
        file.write(tags)


def main():
    # app_name = os.environ("APP_NAME")
    version_type = os.getenv("VERSION_TYPE", "")  # docker_env, docker_from or date
    app_name = os.getenv("APP_NAME", "")
    dockerfile_path = os.getenv("DOCKERFILE_PATH", "Dockerfile")
    app_env = os.getenv("APP_ENV", "")
    custom_tags = os.getenv("CUSTOM_TAGS", "")
    include_major = os.getenv("INCLUDE_MAJOR", "yes")

    if version_type == "docker_env":
        with open(dockerfile_path) as dockerfile:
            for line in dockerfile:
                if re.search(rf"ENV {app_name}_VERSION .*", line):
                    version_string = line[line.find(" ", 4) + 1 :].strip()
                    break

        if version_string[0] == "v":
            version_string = version_string[1:]

        tags = determine_tags(version_string, app_env, include_major)

    elif version_type == "docker_from":
        with open(dockerfile_path) as dockerfile:
            for line in dockerfile:
                if re.search(rf"FROM {app_name}:.*", line):
                    version_string = line[line.find(":") + 1 :].strip()
                    break

        if "@" in version_string:
            version_string = version_string[: version_string.find("@")]

        tags = determine_tags(version_string, app_env, include_major)

    elif version_type == "date":
        version_string = date.today().strftime("%Y%m%d")
        tags = version_string

    elif custom_tags and not version_type:
        tags = custom_tags
        custom_tags = ""

    else:
        exit(-1)

    if custom_tags:
        tags += "," + custom_tags

    write_tags_to_file(tags)


if __name__ == "__main__":
    main()
