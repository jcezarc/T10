import os
import uuid


def add_record(service):
    record = service.table.default_values()
    return service.insert(record)


class Tester:

    def __init__(self, callback):
        self.callback = callback

    @staticmethod
    def temp_file(path= './tests/temp'):
        if not os.path.exists(path):
            os.makedirs(path)
        return os.path.join(
            path,
            str(uuid.uuid4())+'.db'
        )

    def status_of_find(self, insert_before=False):
        service = self.callback()
        if insert_before:
            data = add_record(service)[0]['data']
        else:
            data = service.table.default_values()
        key = service.table.pk_fields[0]
        return service.find(None, data[key])[1]

    def find_success(self):
        status_code = self.status_of_find(insert_before=True)
        assert status_code == 200

    def find_failure(self):
        # --- Faz a pesquisa SEM dados: ---
        assert self.status_of_find() == 404

    def insert_success(self):
        service = self.callback()
        status_code = add_record(service)[1]
        assert status_code == 201

    def insert_failure(self):
        service = self.callback()
        status_code = service.insert({})[1]
        assert status_code == 400
