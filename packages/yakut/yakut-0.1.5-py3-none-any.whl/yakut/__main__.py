# Copyright (c) 2020 UAVCAN Consortium
# This software is distributed under the terms of the MIT License.
# Author: Pavel Kirienko <pavel@uavcan.org>

if __name__ == "__main__":
    from yakut import main

    main(auto_envvar_prefix="YAKUT")  # pylint: disable=no-value-for-parameter,unexpected-keyword-arg
