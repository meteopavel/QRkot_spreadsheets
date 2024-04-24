from datetime import datetime, timedelta

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMATTED_DT_NOW = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
HEADER_ROWS_COUNT = 3
SHEET_COLUMNS_COUNT = 3


async def spreadsheets_create(
        wrapper_services: Aiogoogle,
        projects: list
) -> tuple[str, str]:
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {
            'title': f'Отчёт по проектам от {FORMATTED_DT_NOW}',
            'locale': 'ru_RU'
        },
        'sheets': [
            {'properties': {'sheetType': 'GRID',
                            'sheetId': 0,
                            'title': 'Лист1',
                            'gridProperties': {
                                'rowCount': len(projects) + HEADER_ROWS_COUNT,
                                'columnCount': SHEET_COLUMNS_COUNT
                            }}}
        ]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId'], response['spreadsheetUrl']


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        wrapper_services: Aiogoogle,
        projects: list
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчёт от', FORMATTED_DT_NOW],
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
