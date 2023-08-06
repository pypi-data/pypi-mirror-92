import enum
import json
class FieldType(enum.Enum):
    STRING = 'string'
    FLOAT = "float"
    INTEGER = "integer"
    DATE = "date"
    STRING_ARRAY = "array<string>"
    FLOAT_ARRAY = "array<float>"
    INTEGER_ARRAY = "array<integer>"
    DATE_ARRAY = "array<date>"
    ENUM = "enum"
    OBJECT = "object"
    OBJECT_ARRAY = "array<object>"


class SchemaDefinition:

    def __init__(self, name: str, version: str, fields=[]):
        self.name = name
        self.version = version
        self.fields = fields

    def add_field(self, name: str, type: str, enumValues: dict = {}):
        field = self.__generate_new_child(name, type, enumValues)
        self.fields.append(field)

    def add_child_field(self, name: str, type: str, parentField: str, enumValues: dict = {}):
        child = self.__generate_new_child(name, type, enumValues)
        root = {
            'name': 'root',
            'type': 'object',
            'fields': list(self.fields)
        }
        self.__append_child(root, parentField, child)
        self.fields = root['fields']

    def json_serialize(self):
        return {
            'name': self.name,
            'version': self.version,
            'fields': self.fields
        }

    def __generate_new_child(self, name: str, type: str, enumValues: dict = {}):
        child = {
            'name': name,
            'type': type
        }
        if type == 'enum':
            child['enum'] = enumValues
        if type == 'array<object>' or type == 'object':
            child['fields'] = []
        return child

    def __append_child(self, current: dict, parentFieldName: str, child: dict):
        if current.name == parentFieldName:
            current.fields.append(child)
            return 'added'

        if current.fields:
            for field in current.fields:
                if self.__append_child(field, parentFieldName, child) is not None:
                    return 'added'

        return None
