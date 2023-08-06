nexpose-py
==========

Python3 bindings and CLI tools for
`Nexpose <https://www.rapid7.com/products/nexpose/>`_
API version 3.

cli programs
------------

nsc-exporter
~~~~~~~~~~~~

A `Prometheus <https://prometheus.io/>`_ exporter for
Nexpose scan console metrics.

A ``systemd`` service file is provided at
``etc/systemd/system/nexpose-exporter.service``,
and a sample env file at ``etc/defaults/nexpose-exporter.env``.
These will be relative to your virtualenv for a virtualenv install,
relative to ``$HOME/.local`` for a ``pip install --user`` install,
and (probably, depending on your OS) relative to ``/usr/local`` for a
root pip install.

nsc-janitor
~~~~~~~~~~~~

Maintenance service for Nexpose scan console.

A ``systemd`` service file is provided at
``etc/systemd/system/nexpose-janitor.service``,
and a sample env file at ``etc/defaults/nexpose-janitor.env``.
These will be relative to your virtualenv for a virtualenv install,
relative to ``$HOME/.local`` for a ``pip install --user`` install,
and (probably, depending on your OS) relative to ``/usr/local`` for a
root pip install.

nsc-remove-old-reports
~~~~~~~~~~~~~~~~~~~~~~

nsc-remove-old-sites
~~~~~~~~~~~~~~~~~~~~

library usage
~~~~~~~~~~~~~

Basic usage:

.. code-block:: python

    import nexpose.nexpose as nexpose

    login = nexpose.login(
        base_url='https://localhost:3780',
        user='some_nexpose_user',
        password='secure_nexpose_password',
    )

    nexpose.engines(nlogin=login)


With CLI argument parsing:

.. code-block:: python

    import nexpose.nexpose as nexpose
    import nexpose.args as nexposeargs

    parser = nexposeargs.parser
    parser.description = "My nexpose script"
    parser.add_argument(
        "-f",
        "--foo",
        help="foo argument",
        action="store",
    )

    args = parser.parse_args()
    config = nexpose.config(args)

    nexpose.engines(nlogin=config)
    print(f"my foo argument was {args.foo}")


alternatives
------------

``nexpose`` (`<https://pypi.org/project/nexpose/>`_ )
is the official python binding for Nexpose API versions 1.1 and 1.2.

``nexpose-rest`` (`<https://pypi.org/project/nexpose-rest/>`_) is unofficial.
It is (partially?) auto-generated and more comprehensive than ``nexpose-py``.
