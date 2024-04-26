import copy
from datetime import datetime, timedelta

from aiogoogle import Aiogoogle

from app.core.config import settings

DT_FORMAT = '%Y/%m/%d %H:%M:%S'
HEADER_ROWS_COUNT = 3
SHEET_COLUMNS_COUNT = 3
PERMISSIONS_BODY = {
    'type': 'user', 'role': 'writer', 'emailAddress': settings.email
}
SPREADSHEET_BODY_TEMPLATE = {
    'properties': {
        'title': 'Отчёт по проектам', 'locale': 'ru_RU'
    },
    'sheets': [
        {
            'properties': {
                'sheetType': 'GRID', 'sheetId': 0, 'title': 'Лист1',
                'gridProperties': {
                    'rowCount': HEADER_ROWS_COUNT,
                    'columnCount': SHEET_COLUMNS_COUNT
                }
            }
        }
    ]
}


async def spreadsheets_create(
        wrapper_services: Aiogoogle,
        projects: list,
        spreadsheet_body: dict = SPREADSHEET_BODY_TEMPLATE
) -> tuple[str, str]:
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body_copy = copy.deepcopy(spreadsheet_body)
    spreadsheet_body_copy['properties']['title'] = (
        f'Отчёт по проектам от {datetime.now().strftime(DT_FORMAT)}'
    )
    spreadsheet_props = spreadsheet_body_copy['sheets'][0]['properties']
    spreadsheet_props['gridProperties']['columnCount'] += len(projects)
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body_copy)
    )
    return response['spreadsheetId'], response['spreadsheetUrl']


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=PERMISSIONS_BODY,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        wrapper_services: Aiogoogle,
        projects: list,
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчёт от', f'{datetime.now().strftime(DT_FORMAT)}'],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание'],
        *[(title, str(timedelta(days=rate)), description)
          for title, rate, description in projects]
    ]
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=f'R1C1:'
                  f'R{len(table_values)}'
                  f'C{SHEET_COLUMNS_COUNT}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
