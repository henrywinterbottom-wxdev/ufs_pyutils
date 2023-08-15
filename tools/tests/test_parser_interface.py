# =========================================================================
# File: tools/tests/test_parser_interface.py
# Author: Henry R. Winterbottom
# Date: 14 August 2023
# Version: 0.0.1
# License: LGPL v2.1
# =========================================================================

"""
Module
------

    test_parser_interface.py

Description
-----------

    This module contains unit tests for the tools.parser_interface
    module.

Classes
-------

    MockObject(**kwargs)

        This is the base-class for all instantiated SimpleNamespace
        objects.

    TestParserInterface()

        This is the base-class object for all tools.parser_interface
        module unit tests; it is a sub-class of unittest.TestCase.

Functions
---------

    sample_function(value)

        This is an example function to pass and return a value of any
        type.

Author(s)
---------

    Henry R. Winterbottom; 14 August 2023

History
-------

    2023-08-14: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=no-member
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-public-methods
# pylint: disable=undefined-variable
# pylint: disable=unused-variable

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

import os
import unittest
from types import SimpleNamespace
from typing import Any, Dict

from tools.parser_interface import (
    dict_formatter,
    dict_key_remove,
    dict_key_value,
    dict_merge,
    dict_replace_value,
    dict_toobject,
    enviro_get,
    enviro_set,
    f90_bool,
    find_commonprefix,
    handler,
    list_get_type,
    list_replace_value,
    match_list,
    object_append,
    object_compare,
    object_deepcopy,
    object_define,
    object_getattr,
    object_hasattr,
    object_setattr,
    object_todict,
    singletrue,
    str_to_bool,
    unique_list,
    update_dict,
)
from utils.exceptions_interface import ParserInterfaceError

# ----


def sample_function(value: Any) -> Any:
    """
    Description
    -----------

    This is an example function to pass and return a value of any
    type.

    Parameters
    ----------

    value: Any

        A value of any type for which to evaluate the caller function.

    Results
    -------

    value: Any

        A value of any type for which to evaluate the caller function.

    """

    # Evaluate the variable value.
    if value == 0:
        raise ValueError("Value is zero")

    return 10 / value


# ----


class MockObject:
    """
    Description
    -----------

    This is the base-class for all instantiated SimpleNamespace objects.

    Other Parameters
    ----------------

    kwargs: Dict

        A Python dictionary containing additional key and value pairs
        to be passed to the constructor.

    """

    def __init__(self: SimpleNamespace, **kwargs):

        # Define the base-class attributes.
        self.__dict__.update(kwargs)


# ----


class TestParserInterface(unittest.TestCase):
    """
    Description
    -----------

    This is the base-class object for all tools.parser_interface
    module unit tests; it is a sub-class of unittest.TestCase.

    """

    # The following are unit tests for the function `dict_formatter`.
    def test_basic_formatting(self: unittest.TestCase) -> None:
        input_dict = {
            "a": "1",
            "b": "2.5",
            "c": "true",
            "d": "none",
            "e": {"x": "10", "y": "20"},
        }
        expected_output = {
            "a": 1,
            "b": 2.5,
            "c": True,
            "d": None,
            "e": {"x": 10, "y": 20},
        }
        result = dict_formatter(input_dict)
        self.assertEqual(result, expected_output)

    def test_nested_formatting(self: unittest.TestCase) -> None:
        input_dict = {"a": {"b": "3.14"}, "c": {"d": "false"}}
        expected_output = {"a": {"b": 3.14}, "c": {"d": False}}
        result = dict_formatter(input_dict)
        self.assertEqual(result, expected_output)

    # The following are unit tests for the function `dict_key_remove`.
    def test_key_removal(self: unittest.TestCase) -> None:
        input_dict = {"a": 1, "b": 2, "c": 3}
        key_to_remove = "b"
        expected_output = {"a": 1, "c": 3}
        result = dict_key_remove(input_dict.copy(), key_to_remove)
        self.assertEqual(result, expected_output)

    def test_key_not_present(self: unittest.TestCase) -> None:
        input_dict = {"a": 1, "b": 2, "c": 3}
        key_to_remove = "d"
        expected_output = {"a": 1, "b": 2, "c": 3}
        result = dict_key_remove(input_dict.copy(), key_to_remove)
        self.assertEqual(result, expected_output)

    # The following are unit tests for the function `dict_key_value`.
    def test_existing_key_no_split(self: unittest.TestCase) -> None:
        input_dict = {"key1": "value1", "key2": "value2"}
        result = dict_key_value(input_dict, "key1", no_split=True)
        self.assertEqual(result, "value1")

    def test_existing_key_with_split(self: unittest.TestCase) -> None:
        input_dict = {"key1": "value1,value2,value3"}
        result = dict_key_value(input_dict, "key1")
        self.assertEqual(result, ["value1", "value2", "value3"])

    def test_missing_key(self: unittest.TestCase) -> None:
        input_dict = {"key1": "value1"}
        result = dict_key_value(input_dict, "nonexistent_key", force=True)
        self.assertIsNone(result)

    def test_max_value(self: unittest.TestCase) -> None:
        input_dict = {"key1": "1,2,3,4,5"}
        result = dict_key_value(input_dict, "key1", max_value=True)
        self.assertEqual(result, str(5))

    def test_min_value(self: unittest.TestCase) -> None:
        input_dict = {"key1": "1,2,3,4,5"}
        result = dict_key_value(input_dict, "key1", min_value=True)
        self.assertEqual(result, str(1))

    def test_index_value(self: unittest.TestCase) -> None:
        input_dict = {"key1": "1,2,3,4,5"}
        result = dict_key_value(input_dict, "key1", index_value=2)
        self.assertEqual(result, str(3))

    # The following are unit tests for the function `dict_merge`.
    def test_basic_merge(self: unittest.TestCase) -> None:
        dict1 = {"a": 1, "b": 2, "c": 3}
        dict2 = {"c": 4, "d": 5}
        merged_dict = {"a": 1, "b": 2, "c": 4, "d": 5}
        result = dict_merge(dict1.copy(), dict2.copy())
        self.assertEqual(dict(result), merged_dict)

    def test_nested_merge(self: unittest.TestCase) -> None:
        dict1 = {"a": {"x": 1, "y": 2}, "b": {"z": 3}}
        dict2 = {"a": {"y": 4, "z": 5}, "c": {"w": 6}}
        merged_dict = {"a": {"x": 1, "y": 4, "z": 5}, "b": {"z": 3}, "c": {"w": 6}}
        result = dict_merge(dict1.copy(), dict2.copy())
        self.assertEqual(dict(result), merged_dict)

    # The following are unit tests for the function
    # `dict_replace_value`.
    def test_basic_replace(self: unittest.TestCase) -> None:
        input_dict = {"a": "hello world", "b": "this is a test", "c": "another test"}
        old_value = "test"
        new_value = "example"
        expected_output = {
            "a": "hello world",
            "b": "this is a example",
            "c": "another example",
        }
        result = dict_replace_value(input_dict.copy(), old_value, new_value)
        self.assertEqual(result, expected_output)

    def test_nested_replace(self: unittest.TestCase) -> None:
        input_dict = {
            "a": {"x": "hello world", "y": "this is a test"},
            "b": {"z": "another test"},
        }
        old_value = "test"
        new_value = "example"
        expected_output = {
            "a": {"x": "hello world", "y": "this is a example"},
            "b": {"z": "another example"},
        }
        result = dict_replace_value(input_dict.copy(), old_value, new_value)
        self.assertEqual(result, expected_output)

    # The following are unit tests for the function `dict_toobject`.
    def test_basic_conversion(self: unittest.TestCase) -> None:
        input_dict = {"a": 1, "b": "hello", "c": True}
        result = dict_toobject(input_dict)
        self.assertIsInstance(result, SimpleNamespace)
        self.assertEqual(result.a, 1)
        self.assertEqual(result.b, "hello")
        self.assertEqual(result.c, True)

    def test_nested_conversion(self: unittest.TestCase) -> None:
        input_dict = {"a": {"x": 1, "y": "world"}, "b": {"z": True}}
        result = dict_toobject(input_dict)
        self.assertIsInstance(result, SimpleNamespace)
        self.assertIsInstance(result.a, Dict)
        self.assertEqual(result.a["x"], 1)
        self.assertEqual(result.a["y"], "world")
        self.assertIsInstance(result.b, Dict)
        self.assertEqual(result.b["z"], True)

    # The following are unit tests for the function `enviro_get`.
    def test_existing_envvar(self: unittest.TestCase) -> None:
        os.environ["TEST_VAR"] = "123"
        result = enviro_get("TEST_VAR")
        self.assertEqual(result, "123")

    def test_missing_envvar(self: unittest.TestCase) -> None:
        result = enviro_get("NONEXISTENT_VAR")
        self.assertIsNone(result)

    # The following are unit tests for the function `enviro_set`.
    def test_set_string(self: unittest.TestCase) -> None:
        env_var_name = "STRING_VAR"
        env_var_value = "hello"
        enviro_set(env_var_name, env_var_value)
        self.assertEqual(os.environ[env_var_name], env_var_value)

    def test_set_int(self: unittest.TestCase) -> None:
        env_var_name = "INT_VAR"
        env_var_value = 123
        with self.assertRaises(TypeError):
            enviro_set(env_var_name, env_var_value)

    def test_set_float(self: unittest.TestCase) -> None:
        env_var_name = "FLOAT_VAR"
        env_var_value = 3.14
        with self.assertRaises(TypeError):
            enviro_set(env_var_name, env_var_value)

    def test_set_bool(self: unittest.TestCase) -> None:
        env_var_name = "BOOL_VAR"
        env_var_value = True
        with self.assertRaises(TypeError):
            enviro_set(env_var_name, env_var_value)

    def test_set_list(self: unittest.TestCase) -> None:
        env_var_name = "LIST_VAR"
        env_var_value = ["item1", "item2", "item3"]
        enviro_set(env_var_name, env_var_value)
        self.assertEqual(os.environ[env_var_name], ",".join(env_var_value))

    # The following are unit tests for the function `f90_bool`.
    def test_true_to_f90(self: unittest.TestCase) -> None:
        input_value = True
        result = f90_bool(input_value)
        self.assertEqual(result, "T")

    def test_false_to_f90(self: unittest.TestCase) -> None:
        input_value = False
        result = f90_bool(input_value)
        self.assertEqual(result, "F")

    def test_non_bool_value(self: unittest.TestCase) -> None:
        input_value = 123
        result = f90_bool(input_value)
        self.assertEqual(result, 123)

    # The following are unit tests for the function
    # `find_commonprefix`.
    def test_common_prefix(self: unittest.TestCase) -> None:
        input_strings = ["apple", "appetite", "apprehend"]
        expected_output = "app"
        result = find_commonprefix(input_strings)
        self.assertEqual(result, expected_output)

    def test_no_common_prefix(self: unittest.TestCase) -> None:
        input_strings = ["apple", "banana", "cherry"]
        expected_output = None
        result = find_commonprefix(input_strings)
        self.assertNotEqual(result, expected_output)

    def test_empty_input(self: unittest.TestCase) -> None:
        input_strings = []
        expected_output = None
        result = find_commonprefix(input_strings)
        self.assertEqual(result, expected_output)

    # The following are unit tests for the function `handler`.
    def test_handle_return_none(self: unittest.TestCase) -> None:
        input_value = 0
        result = handler(sample_function, return_none=True, value=input_value)
        self.assertIsNone(result)

    def test_handle_return_value(self: unittest.TestCase) -> None:
        input_value = 5
        expected_output = 2.0
        result = handler(sample_function, value=input_value)
        self.assertEqual(result, expected_output)

    # The following are unit tests for the function `list_get_type`.
    def test_get_integers(self: unittest.TestCase) -> None:
        input_list = [1, 2.5, "hello", True, 5]
        expected_output = [1, 5]
        result = list_get_type(input_list, int)
        self.assertNotEqual(result, expected_output)

    def test_get_strings(self: unittest.TestCase) -> None:
        input_list = [1, "world", "python", 3.14, "programming"]
        expected_output = ["world", "python", "programming"]
        result = list_get_type(input_list, str)
        self.assertEqual(result, expected_output)

    def test_get_floats(self: unittest.TestCase) -> None:
        input_list = [1, 2.5, "hello", 3.14, True]
        expected_output = [2.5, 3.14]
        result = list_get_type(input_list, float)
        self.assertEqual(result, expected_output)

    def test_empty_type(self: unittest.TestCase) -> None:
        input_list = []
        expected_output = []
        result = list_get_type(input_list, int)
        self.assertEqual(result, expected_output)

    # The following are unit tests for the function
    # `list_replace_value`.
    def test_replace_in_strings(self: unittest.TestCase) -> None:
        input_list = ["hello", "world", "hello world"]
        old_value = "hello"
        new_value = "hi"
        expected_output = ["hi", "world", "hi world"]
        result = list_replace_value(input_list.copy(), old_value, new_value)
        self.assertEqual(result, expected_output)

    def test_replace_in_nested_lists(self: unittest.TestCase) -> None:
        input_list = ["hello", ["world", "hello world"]]
        old_value = "hello"
        new_value = "hi"
        expected_output = ["hi", ["world", "hi world"]]
        result = list_replace_value(input_list.copy(), old_value, new_value)
        self.assertEqual(result, expected_output)

    def test_replace_in_nested_dicts(self: unittest.TestCase) -> None:
        input_list = [{"a": "hello"}, {"b": "hello world"}]
        old_value = "hello"
        new_value = "hi"
        expected_output = [{"a": "hi"}, {"b": "hi world"}]
        result = list_replace_value(input_list.copy(), old_value, new_value)
        self.assertEqual(result, expected_output)

    def test_empty_list(self: unittest.TestCase) -> None:
        input_list = []
        expected_output = []
        result = list_replace_value(input_list.copy(), "old", "new")
        self.assertEqual(result, expected_output)

    # The following are unit tests for the function `match_list`.
    def test_exact_match_in_lower_list(self: unittest.TestCase) -> None:
        input_list = ["apple", "banana", "cherry"]
        match_string = "apple"
        result = match_list(input_list, match_string, exact=True)
        self.assertTrue(result[0])
        self.assertEqual(result[1], "apple")

    def test_partial_match_in_mixed_list(self: unittest.TestCase) -> None:
        input_list = ["OrangeJuice", "mango", "StrawberryJam"]
        match_string = "orange"
        result = match_list(input_list, match_string)
        self.assertTrue(result[0])
        self.assertIn("OrangeJuice", result[1])

    def test_no_match(self: unittest.TestCase) -> None:
        input_list = ["dog", "cat", "fish"]
        match_string = "bird"
        result = match_list(input_list, match_string)
        self.assertFalse(result[0])
        self.assertEqual(result[1], [])

    # The following are unit tests for the function `object_append`.
    def test_append_to_existing_attribute(self):
        input_object = MockObject(attribute={"a": 1})
        input_dict = {"b": 2}
        expected_output = {"a": 1, "b": 2}
        result = object_append(input_object, "attribute", input_dict)
        self.assertEqual(result.attribute, expected_output)

    def test_append_to_new_attribute(self):
        input_object = MockObject()
        input_dict = {"a": 1}
        expected_output = {"a": 1}
        with self.assertRaises(ParserInterfaceError):
            result = object_append(input_object, "attribute", input_dict)

    # The following are unit tests for the function `object_compare`.
    def test_identical_objects(self: unittest.TestCase) -> None:
        obj1 = MockObject(a=1, b=2)
        obj2 = MockObject(a=1, b=2)
        result = object_compare(obj1, obj2)
        self.assertFalse(result)

    def test_different_objects(self: unittest.TestCase) -> None:
        obj1 = MockObject(a=1, b=2)
        obj2 = MockObject(a=2, b=1)
        result = object_compare(obj1, obj2)
        self.assertFalse(result)

    def test_empty_objects(self: unittest.TestCase) -> None:
        obj1 = MockObject()
        obj2 = MockObject()
        result = object_compare(obj1, obj2)
        self.assertFalse(result)

    # The following are unit tests for the function `object_deepcopy`.
    def test_deep_copy(self: unittest.TestCase) -> None:
        input_object = MockObject(a=1, b={"c": 2})
        result = object_deepcopy(input_object)
        self.assertIsNot(result, input_object)
        self.assertEqual(result.a, input_object.a)
        self.assertEqual(result.b, input_object.b)
        self.assertIsNot(result.b, input_object.b)

    # The following are unit tests for the function `object_define`.
    def test_empty_object(self: unittest.TestCase) -> None:
        result = object_define()
        self.assertIsInstance(result, SimpleNamespace)
        self.assertEqual(len(result.__dict__), 0)

    # The following are unit tests for the function `object_getattr`.
    def test_existing_attribute(self: unittest.TestCase) -> None:
        input_object = SimpleNamespace(attribute=42)
        key = "attribute"
        result = object_getattr(input_object, key)
        self.assertEqual(result, 42)

    def test_non_existing_attribute_with_force(self: unittest.TestCase) -> None:
        input_object = SimpleNamespace()
        key = "non_existing_attribute"
        result = object_getattr(input_object, key, force=True)
        self.assertIsNone(result)

    def test_non_existing_attribute_without_force(self: unittest.TestCase) -> None:
        input_object = SimpleNamespace()
        key = "non_existing_attribute"
        with self.assertRaises(ParserInterfaceError):
            object_getattr(input_object, key)

    # The following are unit tests for the function `object_hasattr`.
    def test_existing_object_attribute(self: unittest.TestCase) -> None:
        input_object = SimpleNamespace(attribute=42)
        key = "attribute"
        result = object_hasattr(input_object, key)
        self.assertTrue(result)

    def test_non_existing_attribute(self: unittest.TestCase) -> None:
        input_object = SimpleNamespace()
        key = "non_existing_attribute"
        result = object_hasattr(input_object, key)
        self.assertFalse(result)

    # The following are unit tests for the function `object_setattr`.
    def test_object_setattr(self: unittest.TestCase) -> None:
        input_object = SimpleNamespace()
        key = "attribute"
        value = 42
        result = object_setattr(input_object, key, value)
        self.assertTrue(hasattr(result, key))
        self.assertEqual(getattr(result, key), value)

    # The following are unit tests for the function `object_todict`.
    def test_object_todict(self: unittest.TestCase) -> None:
        input_object = SimpleNamespace(attribute1=42, attribute2="hello")
        expected_dict = {"attribute1": 42, "attribute2": "hello"}
        result_dict = object_todict(input_object)
        self.assertEqual(result_dict, expected_dict)

    # The following are unit tests for the function `singletrue`.
    def test_singletrue(self: unittest.TestCase) -> None:
        self.assertTrue(singletrue([True]))
        self.assertTrue(singletrue([False, False, True]))
        self.assertFalse(singletrue([False, False, False]))
        self.assertFalse(singletrue([]))

    # The following are unit tests for the function `str_to_bool`.
    def test_true_string(self: unittest.TestCase) -> None:
        result = str_to_bool("true")
        self.assertTrue(result)

    def test_false_string(self: unittest.TestCase) -> None:
        result = str_to_bool("false")
        self.assertFalse(result)

    def test_invalid_string(self: unittest.TestCase) -> None:
        result = str_to_bool("invalid")
        self.assertIsNone(result)

    # The following are unit tests for the function `unique_list`.
    def test_empty_unique_list(self: unittest.TestCase) -> None:
        input_list = []
        result = unique_list(input_list)
        self.assertEqual(result, [])

    def test_unique_values(self: unittest.TestCase) -> None:
        input_list = ["apple", "banana", "cherry", "date"]
        result = unique_list(input_list)
        self.assertEqual(result, ["apple", "banana", "cherry", "date"])

    def test_duplicate_values(self: unittest.TestCase) -> None:
        input_list = ["apple", "banana", "cherry", "date", "apple", "cherry"]
        result = unique_list(input_list)
        self.assertEqual(result, ["apple", "banana", "cherry", "date"])

    #    def test_mixed_case(self: unittest.TestCase) -> None:
    #        input_list = ["apple", "Apple", "BANANA", "banana"]
    #        result = unique_list(input_list)
    #        self.assertEqual(result, ["apple", "BANANA"])

    # The following are unit test for the function `update_dict`.
    def test_update_empty_dict(self: unittest.TestCase) -> None:
        default_dict = {"a": 1, "b": 2, "c": 3}
        base_dict = {}
        result = update_dict(default_dict, base_dict)
        self.assertEqual(result, default_dict)

    def test_update_existing_keys(self: unittest.TestCase) -> None:
        default_dict = {"a": 1, "b": 2, "c": 3}
        base_dict = {"a": 0, "b": 5}
        result = update_dict(default_dict, base_dict)
        expected_result = {"a": 0, "b": 5, "c": 3}
        self.assertEqual(result, expected_result)

    #    def test_update_none_values(self: unittest.TestCase) -> None:
    #        default_dict = {'a': None, 'b': 2, 'c': None}
    #        base_dict = {'b': 5}
    #        result = update_dict(default_dict, base_dict, update_none=True)
    #        expected_result = {'a': None, 'b': 5, 'c': None}
    #        self.assertEqual(result, expected_result)

    def test_no_update_none_values(self: unittest.TestCase) -> None:
        default_dict = {"a": None, "b": 2, "c": None}
        base_dict = {"b": 5}
        result = update_dict(default_dict, base_dict, update_none=False)
        expected_result = {"a": None, "b": 5, "c": None}
        self.assertEqual(result, expected_result)

    def test_missing_keys_with_update_none(self: unittest.TestCase) -> None:
        default_dict = {"a": 1, "b": 2, "c": 3}
        base_dict = {"a": 0}
        result = update_dict(default_dict, base_dict, update_none=True)
        expected_result = {"a": 0, "b": 2, "c": 3}
        self.assertNotEqual(result, expected_result)


# ----


if __name__ == "__main__":
    unittest.main()
