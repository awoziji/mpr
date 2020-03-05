from aiohttp.test_utils import TestServer
from behave import when
from behave import then
from behave.api.async_step import async_run_until_complete

from mpr.cutout_index import get_cutout_index
from . import format_decimal
from . import server


@when('I request the CME cutout index')
@async_run_until_complete
async def request_cutout(context):
    async with TestServer(server, port=8080):
        context.report = await get_cutout_index(context.start, context.end)


@then('I will receive a report of cutout prices from June 2019')
def verify_cutout_values(context):
    for expected, (index, row) in zip(context.table, context.report.iterrows()):
        assert index.strftime('%Y-%m-%d') == expected['date']
        assert format_decimal(row[0]) == expected['Cutout Index']
        assert format_decimal(row[1]) == expected['Index Change']
        assert format_decimal(row[2]) == expected['Carcass Price']
        assert format_decimal(row[3]) == expected['Price Change']
        assert format_decimal(row[4]) == expected['Total Loads']
        assert format_decimal(row[5]) == expected['Loin Price']
        assert format_decimal(row[6]) == expected['Belly Price']
        assert format_decimal(row[7]) == expected['Butt Price']
        assert format_decimal(row[8]) == expected['Ham Price']
        assert format_decimal(row[9]) == expected['Rib Price']
        assert format_decimal(row[10]) == expected['Picnic Price']
