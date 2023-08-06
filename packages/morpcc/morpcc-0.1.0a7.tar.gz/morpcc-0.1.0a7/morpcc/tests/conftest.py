# Copyright (c) 2019 Mohd Izhar Firdaus Bin Ismail
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from pytest_postgresql import factories

pgsql_proc = factories.postgresql_proc(
    executable="/usr/bin/pg_ctl", host="localhost", port=45678, user="postgres"
)
pgsql_db = factories.postgresql("pgsql_proc", db_name="morpcc_tests")
pgsql_db_warehouse = factories.postgresql("pgsql_proc", db_name="morpcc_warehouse")
pgsql_db_cache = factories.postgresql("pgsql_proc", db_name="morpcc_cache")
