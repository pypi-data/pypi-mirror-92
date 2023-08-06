"""
Implementation of repositories using TinyDB
"""
from lifeguard.notifications import NotificationStatus
from lifeguard.validations import ValidationResponse
from tinydb import TinyDB, Query

from lifeguard_tinydb.settings import LIFEGUARD_TINYDB_LOCATION

DATABASE = TinyDB(LIFEGUARD_TINYDB_LOCATION)


def save_or_update(table, query, data):
    """
    Check if entry exists and create or update entry
    :param collection:
    :param query:
    :param data:
    """
    if table.count(query):
        table.update(data, query)
    else:
        table.insert(data)


class TinyDBValidationRepository:
    def __init__(self):
        self.table = DATABASE.table("validations")

    def save_validation_result(self, validation_result):
        save_or_update(
            self.table,
            self.__get_key(validation_result.validation_name),
            {
                "validation_name": validation_result.validation_name,
                "status": validation_result.status,
                "details": validation_result.details,
                "settings": validation_result.settings,
                "last_execution": validation_result.last_execution,
            },
        )

    def fetch_last_validation_result(self, validation_name):
        result = self.table.get(self.__get_key(validation_name))
        if result:
            return self.__convert_to_validation(result)
        return None

    def fetch_all_validation_results(self):
        results = []
        for result in self.table.all():
            results.append(self.__convert_to_validation(result))

        return results

    def __convert_to_validation(self, entry):
        return ValidationResponse(
            entry["validation_name"],
            entry["status"],
            entry["details"],
            entry["settings"],
            last_execution=entry["last_execution"],
        )

    def __get_key(self, validation_name):
        query = Query()
        return query.validation_name == validation_name


class TinyDBNotificationRepository:
    def __init__(self):
        self.table = DATABASE.table("notifications")

    def save_last_notification_for_a_validation(self, notification):
        save_or_update(
            self.table,
            self.__get_key(notification.validation_name),
            {
                "validation_name": notification.validation_name,
                "thread_ids": notification.thread_ids,
                "is_opened": notification.is_opened,
                "options": notification.options,
                "last_notification": notification.last_notification,
            },
        )

    def fetch_last_notification_for_a_validation(self, validation_name):
        result = self.table.get(self.__get_key(validation_name))
        if result:
            last_notification_status = NotificationStatus(
                validation_name, result["thread_ids"], result["options"]
            )
            last_notification_status.last_notification = result["last_notification"]
            last_notification_status.is_opened = result["is_opened"]
            return last_notification_status
        return None

    def __get_key(self, validation_name):
        query = Query()
        return query.validation_name == validation_name
