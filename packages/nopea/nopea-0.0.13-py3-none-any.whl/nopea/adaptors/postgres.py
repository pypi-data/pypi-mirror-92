#!/usr/bin/env python
# coding: utf-8

import psycopg2

from nopea.dbobject import DbObject
from nopea.fields import ForeignKey, PkField


class IsNull:
    """ Used as identifier for NULL values in query_args """

    def __init__(self):
        pass


class PostgreSQLAdaptor(object):

    PLACEHOLDER = '%s'

    def __init__(self, database_settings):
        self.database_settings = database_settings

    def get_connection_and_cursor(self):
        connection = psycopg2.connect(**self.database_settings)
        cursor = connection.cursor()
        return connection, cursor

    def execute_query(self, query, query_args):
        connection, cursor = self.get_connection_and_cursor()
        if not query_args:
            cursor.execute(query)
        else:
            query_args = [q for q in query_args if not isinstance(q, IsNull)]
            cursor.execute(query, query_args)
        connection.commit()
        try:
            result = cursor.fetchall()
        except psycopg2.ProgrammingError:
            result = []
        try:
            last_id = result[0]
        except IndexError:
            last_id = None

        connection.close()
        return (result, last_id)

    def get_filter_query(self, filter_partial):
        key, value = list(filter_partial.items())[0]
        if key.endswith('__in'):
            query = ('%s IN (%s)' % (key.replace('__in', ''), ', '.join(["%s" for i in value])))
        elif key.endswith('__lt'):
            query = '%s < %s' % (key.replace('__lt', ''), '%s')
        elif key.endswith('__lte'):
            query = '%s <= %s' % (key.replace('__lte', ''), '%s')
        elif key.endswith('__gt'):
            query = '%s > %s' % (key.replace('__gt', ''), '%s')
        elif key.endswith('__gte'):
            query = '%s >= %s' % (key.replace('__gte', ''), '%s')
        elif key.endswith('__contains'):
            query = '%s LIKE %s' % (key.replace('__contains', ''), '%s')
            value = '%' + value + '%'
        elif key.endswith('__startswith'):
            query = '%s LIKE %s' % (key.replace('__startswith', ''), '%s')
            value = value + '%'
        elif key.endswith('__endswith'):
            query = '%s LIKE %s' % (key.replace('__endswith', ''), '%s')
            value = '%' + value
        else:
            if value is not None:
                query = '%s=%%s' % key
            else:
                query = '%s IS NULL' % key
                value = IsNull()
        return query, value

    def get_exclude_query(self, exclude_partial):
        key, value = list(exclude_partial.items())[0]
        if key.endswith('__in'):
            query = ('%s NOT IN (%s)' % (key.replace('__in', ''), ', '.join(["%s" for i in value])))
        elif key.endswith('__lt'):
            query = '%s >= %s' % (key.replace('__lt', ''), '%s')
        elif key.endswith('__lte'):
            query = '%s > %s' % (key.replace('__lte', ''), '%s')
        elif key.endswith('__gt'):
            query = '%s <= %s' % (key.replace('__gt', ''), '%s')
        elif key.endswith('__gte'):
            query = '%s < %s' % (key.replace('__gte', ''), '%s')
        elif key.endswith('__startswith'):
            query = '%s NOT LIKE %s' % (key.replace('__startswith', ''), '%s')
            value = value + '%'
        elif key.endswith('__endswith'):
            query = '%s NOT LIKE %s' % (key.replace('__endswith', ''), '%s')
            value = '%' + value
        else:
            if value is not None:
                query = '%s <> %%s' % key
            else:
                value = IsNull()
                query = '%s IS NOT NULL' % key
        return query, value

    def get_offset_query(self, offset, limit):
        # Limit is required for SQLite. Can be ignored here
        return f" OFFSET {offset}"

    def get_limit_query(self, limit, offset):
        if offset and offset > 0:
            limit = limit - offset
        return f" LIMIT {limit}"

    def get_select_query(self, base, *args, **kwargs):
        query = 'SELECT %s FROM "%s"' % (', '.join(base.fieldnames), base.tablename)
        return query

    def get_count_query(self, base, *args, **kwargs):
        query = f'SELECT COUNT(*) FROM "{base.tablename}"'
        return query

    def get_insert_query(self, base, create_partial):
        values = []
        fieldnames = [field.fieldname for field in base.fields]
        for field in base.fields:
            value = create_partial.get(field.fieldname)
            if isinstance(value, DbObject):
                value = value.id
            if value is None:
                try:
                    value = field.default
                except AttributeError:
                    pass
            if value is None and isinstance(field, PkField):
                fieldnames = [field.fieldname for field in base.fields if not isinstance(field, PkField)]
            else:
                values.append(value)
        query = 'INSERT INTO "%s" (%s) VALUES (%s) RETURNING id' % (base.tablename,
                                                                  ', '.join(fieldnames),
                                                                  ', '.join(['%s' for item in fieldnames]))
        return (query, tuple(values))

    def get_delete_query(self, base):
        query = "DELETE FROM %s " % base.tablename
        return query

    def get_update_query(self, base, update_partial):
        values = []
        affected_fields = []
        settings = ''
        for field in base.fields:
            value = update_partial.get(field.fieldname)
            if not value:
                pass
            else:
                values.append(value)
                affected_fields.append(field.fieldname)

        settings = ', '.join(['%s=%%s' % item for item in affected_fields])
        query = "UPDATE %s SET %s " % (base.tablename, settings)
        return (query, tuple(values))

    def bulk_create(self, objects, base):
        max_params = 2000
        max_inserts_per_query = int(max_params / len(base.fieldnames))
        iterations = (len(base.fieldnames) * len(objects)) / max_params

        lower = 0
        for i in range(0, int(iterations) + 1):
            lower = int(i * max_inserts_per_query)
            upper = int(lower + max_inserts_per_query)
            query, query_args = self.get_bulk_insert_query(objects[lower:upper], base)
            self.execute_query(query, query_args)

    def get_bulk_insert_query(self, objects, base):
        fieldnames = [field.fieldname for field in base.fields if not isinstance(field, PkField)]
        values = [tuple(getattr(item, fieldname) for fieldname in fieldnames) for item in objects]
        placeholders = ', '.join(['(%s)' % (', '.join(["%s" for i in item])) for item in values])
        query = '''INSERT INTO "%s" (%s) VALUES %s''' % (base.tablename, ', '.join(fieldnames), placeholders)
        return (query, tuple(v for tupl in values for v in tupl))

    def get_create_table_query(self, base, tablename):
        if not tablename:
            tablename = base.tablename
        query = 'CREATE TABLE "%s" (%%s);' % tablename
        fk_fields = []
        fields = []
        fieldnames = []
        for field in base.fields:
            if isinstance(field, ForeignKey):
                fk_fields.append(field)
            fields.append(field)
            fieldnames.append(field.fieldname)

        field_queries = [field.partial_create_table_query for field in fields]

        for field in fk_fields:
            fieldnames.append(field.fieldname)
        field_queries.extend([field.partial_create_table_query_extension for field in fk_fields])

        query = query % ', '.join(field_queries)
        query = query % tuple(fieldnames)
        return (query, None)

    def get_drop_table_query(self, base, tablename):
        if not tablename:
            tablename = base.tablename
        query = "DROP TABLE %s;" % tablename
        return (query, None)

    def get_drop_column_query(self, field, base):
        return f'ALTER TABLE "{base.tablename}" DROP COLUMN "{field.fieldname}"'

    def get_pkfield_create_query(self):
        return '%s SERIAL PRIMARY KEY'

    def get_integer_field_create_query(self, field):
        query = '%s INTEGER'
        if field.default is not None:
            query += ' DEFAULT %s' % field.default
        return query

    def get_integer_field_create_column_query(self, field):
        query = 'ALTER TABLE %%s ADD COLUMN %s INTEGER' % field.fieldname
        if field.default is not None:
            query += ' DEFAULT %s' % field.default
        return query

    def get_char_field_create_query(self, field):
        query = '%%s VARCHAR(%s)' % field.max_length
        if field.default is not None:
            query += ' DEFAULT %s' % field.default
        return query

    def get_charfield_create_column_query(self, field):
        query = 'ALTER TABLE %%s ADD COLUMN %s VARCHAR(%s)' % (field.fieldname, field.max_length)
        if field.default is not None:
            query += ' DEFAULT %s' % field.default
        return query

    def get_text_field_create_query(self):
        return '%s TEXT'

    def get_datetime_field_create_query(self, default):
        if default is None:
            return '%s TIMESTAMP NULL DEFAULT NULL'
        elif default == 'now':
            return '%s TIMESTAMP DEFAULT CURRENT_TIMESTAMP'

    def get_boolean_field_create_query(self, default):
        return '%%s BOOLEAN DEFAULT %s' % default

    def get_foreignkey_field_create_query_base(self):
        return '%s INTEGER'

    def get_foreignkey_field_create_query_extension(self, reference):
        if type(DbObject) == type(reference):
            reference = reference.tablename
        return 'FOREIGN KEY(%%s) REFERENCES "%s"(id)' % (reference)

    def create_migration_table(self):
        query = """CREATE TABLE IF NOT EXISTS nopea_migrations
                    (name VARCHAR(250), id SERIAL PRIMARY KEY)"""
        self.execute_query(query, None)

    def get_done_migrations(self):
        query = "SELECT id, name FROM nopea_migrations"
        return self.execute_query(query, None)

    def insert_migration(self, name):
        query = "INSERT INTO nopea_migrations (name) VALUES (%s)"
        return self.execute_query(query, (name,))
