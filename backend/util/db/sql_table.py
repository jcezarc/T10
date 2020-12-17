import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from marshmallow.fields import Str, Nested
from util.db.fmt_table import FormatTable

CON_STR = '{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}'

class SqlTable(FormatTable):
    def config(self, table_name, schema, params):
        super().config(table_name, schema, params)
        engine = create_engine(
            CON_STR.format(**params)
        )
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def insert(self, json_data):
        errors = super().insert(json_data)
        if errors:
            return errors
        command = self.get_command(
            json_data,
            is_insert=True,
            use_quotes=False
        )
        print('-'*100)
        print(command)
        print('-'*100)
        self.session.execute(command)
        self.session.commit()
        return None

    def update(self, json_data):
        command = self.get_command(
            json_data,
            is_insert=False,
            use_quotes=False
        )
        print('-'*100)
        print(command)
        print('-'*100)
        self.session.execute(command)
        self.session.commit()

    def find_all(self, limit=0, filter_expr='', allow_left_joins=True):
        if allow_left_joins:
            field_list, curr_table, expr_join = self.query_elements()
        else:
            field_list = self.allowed_fields()
            curr_table = self.table_name
            expr_join = ''
        command = 'SELECT {} \nFROM {} {}'.format(
            ',\n\t'.join(field_list),
            curr_table,
            expr_join
        )
        if filter_expr:
            has_where = 'WHERE' in filter_expr.upper()
            if not has_where:
                filter_expr = 'WHERE ' + filter_expr
            command += '\n' + filter_expr
        print('-'*100)
        print(command)
        print('-'*100)
        dataset = self.session.execute(command)
        result = []
        for row in dataset.fetchall():
            record = {}
            for item in row.items():
                key, value = self.inflate(
                    str(item[1]),
                    record,
                    item[0].split('__')
                )
                record[key] = value
            result.append(record)
            if len(result) == limit:
                break
        return result

    def find_one(self, values):
        found = self.find_all(
            1, self.get_conditions(values)
        )
        if found:
            found = found[0]
        return found

    def delete(self, values):
        command = 'DELETE FROM {} WHERE {}'.format(
            self.table_name,
            self.get_conditions(values)
        )
        print('-'*100)
        print(command)
        print('-'*100)
        self.session.execute(command)
        self.session.commit()
