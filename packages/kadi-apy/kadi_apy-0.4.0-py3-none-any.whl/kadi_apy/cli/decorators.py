# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import sys
from functools import wraps

import click
from requests.exceptions import SSLError
from xmlhelpy import Integer
from xmlhelpy import option

from kadi_apy.cli.lib.users import CLIUser
from kadi_apy.lib.core import KadiAPI
from kadi_apy.lib.exceptions import KadiAPYException
from kadi_apy.lib.exceptions import KadiAPYInputError


def _item_init(class_type, identifier=None, id=None):
    """Try to init an item."""

    try:
        return class_type(identifier=identifier, id=id)
    except KadiAPYException as e:
        click.echo(e, err=True)
        sys.exit(1)


def apy_command(func):
    """Decorator to handle the default arguments and exceptions of an APY command."""

    option(
        "host",
        char="h",
        description="Host name of the Kadi4Mat instance to use for the API.",
    )(func)

    option(
        "token", char="k", description="Personal access token (PAT) to use for the API."
    )(func)

    option(
        "skip-verify",
        char="s",
        is_flag=True,
        description="Skip verifying the SSL/TLS certificate of the host.",
    )(func)

    @wraps(func)
    def decorated_command(token, host, skip_verify, *args, **kwargs):
        KadiAPI.token = token if token is not None else os.environ.get("KADI_PAT")
        KadiAPI.host = host if host is not None else os.environ.get("KADI_HOST")
        KadiAPI.verify = not skip_verify

        try:
            func(*args, **kwargs)
        except KadiAPYException as e:
            click.echo(e, err=True)
            sys.exit(1)
        except SSLError as e:
            click.echo(e, err=True)
            click.echo(
                "Use the '-s' option to skip verifying the SSL/TLS certificate of the"
                " host."
            )
            sys.exit(1)

    return decorated_command


def id_identifier_options(
    class_type, helptext=None, get_id=False, init=False, name=None
):
    """Decorator to handle the common ID and identifier options of commands."""

    def decorator(func):

        help_id = f"ID of the {class_type.name}"
        if helptext:
            help_id = f"{help_id} {helptext}"

        help_identifier = f"Identifier of the {class_type.name}"
        if helptext:
            help_identifier = f"{help_identifier} {helptext}"

        if name is None:
            text_option = f"{class_type.name}-id"
            char_option = f"{class_type.name[0].lower()}"
        else:
            text_option = f"{class_type.name}-id-{name.lower()}"
            char_option = f"{name[0].lower()}"

        option(
            text_option,
            char=char_option,
            description=help_id,
            default=None,
            param_type=Integer,
        )(func)

        if name is None:
            text_option = f"{class_type.name}-identifier"
            char_option = f"{class_type.name[0].upper()}"
        else:
            text_option = f"{class_type.name}-identifier-{name.lower()}"
            char_option = f"{name[0].upper()}"

        option(
            text_option,
            char=char_option,
            description=help_identifier,
            default=None,
        )(func)

        @wraps(func)
        def decorated_command(*args, **kwargs):
            if name is None:
                text_id = f"{class_type.name}_id"
                text_identifier = f"{class_type.name}_identifier"
            else:
                text_id = f"{class_type.name}_id_{name.lower()}"
                text_identifier = f"{class_type.name}_identifier_{name.lower()}"

            item_id = kwargs[f"{text_id}"]
            item_identifier = kwargs[f"{text_identifier}"]
            if (item_id is None and item_identifier is None) or (
                item_id is not None and item_identifier is not None
            ):
                text = (
                    f"Please specify either the id or the identifier of the"
                    f" {class_type.name}"
                )
                if helptext:
                    text = f"{text} {helptext}"
                click.echo(f"{text}.")
                sys.exit(1)

            # Init the item either by the id or the identifier.
            # The item is directly passed to the function as e.g. record in case of
            # records or {name} if a name is given
            if init:
                item = _item_init(class_type, identifier=item_identifier, id=item_id)
                if name is None:
                    kwargs[f"{class_type.name}"] = item
                else:
                    kwargs[f"{name.lower()}"] = item

                del kwargs[f"{text_id}"]
                del kwargs[f"{text_identifier}"]

            # The item_id is fetched via the identifier if the item_id is empty.
            # The item is directly passed to the function as e.g. records_id in case of
            # records or records_id_{name} if a name is given
            elif get_id:
                if item_id is None:
                    item = _item_init(class_type, identifier=item_identifier)
                    kwargs[f"{text_id}"] = item.id
                del kwargs[f"{text_identifier}"]

            func(*args, **kwargs)

        return decorated_command

    return decorator


def user_id_options(helptext=None, required=True):
    """Decorator to handle options to identify a user."""

    def decorator(func):

        description = "ID of the user"
        if helptext:
            description = f"{description} {helptext}"

        option(
            "user",
            char="u",
            description=description,
            default=None,
            param_type=Integer,
        )(func)

        description = "Username of the user"
        if helptext:
            description = f"{description} {helptext}"

        option(
            "username",
            char="U",
            description=description,
            default=None,
        )(func)

        description = "Identity type of the user"
        if helptext:
            description = f"{description} {helptext}"

        option(
            "identity-type",
            char="I",
            description=description,
            default="ldap",
        )(func)

        @wraps(func)
        def decorated_command(user, username, identity_type, *args, **kwargs):

            if user is None and username is None:
                if required:
                    raise KadiAPYInputError(
                        f"Please specify the user via id or username and identity type."
                    )
                kwargs[f"user"] = None

            else:
                kwargs[f"user"] = CLIUser(
                    id=user, username=username, identity_type=identity_type, **kwargs
                )

            func(*args, **kwargs)

        return decorated_command

    return decorator


def file_id_options(helptext=None, required=True):
    """Decorator to handle options to identify a file of a record."""

    def decorator(func):

        description = "Name of the file"
        if helptext:
            description = f"{description} {helptext}"

        option(
            "file-name",
            char="n",
            description=description,
            default=None,
        )(func)

        description = "ID of the file"
        if helptext:
            description = f"{description} {helptext}"

        option(
            "file-id",
            char="i",
            description=description,
            default=None,
        )(func)

        @wraps(func)
        def decorated_command(file_name, file_id, *args, **kwargs):

            if required:
                if (file_name is None and file_id is None) or (
                    file_name is not None and file_id is not None
                ):
                    text = "Please specify either the name or the id of the file."
                    if helptext:
                        text = f"{text} {helptext}"
                    click.echo(f"{text}.")
                    sys.exit(1)

            if file_name:
                record = kwargs["record"]
                kwargs["file_id"] = record.get_file_id(file_name)
            else:
                kwargs["file_id"] = file_id

            func(*args, **kwargs)

        return decorated_command

    return decorator
