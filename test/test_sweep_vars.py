import unittest
from hypothesis import given, strategies as st  # pylint: disable=unused-import
import pytest
from bencher.variables.inputs import IntSweep, EnumSweep, StringSweep, BoolSweep, FloatSweep
from enum import auto
from strenum import StrEnum


class TestVarSweeps(unittest.TestCase):
    def test_int_sweep_01(self):
        int_sweep = IntSweep(bounds=[0, 1])
        self.assertEqual(int_sweep.default, 0)
        self.assertListEqual(int_sweep.values(False), [0, 1])
        self.assertListEqual(int_sweep.values(True), [0, 1])

    def test_int_sweep_06(self):
        int_sweep = IntSweep(bounds=[0, 6])
        self.assertEqual(int_sweep.default, 0)
        self.assertListEqual(int_sweep.values(False), [0, 1, 2, 3, 4, 5, 6])
        self.assertListEqual(int_sweep.values(True), [0, 6])

    def test_int_sweep_06_debug_sampes(self):
        int_sweep = IntSweep(bounds=[0, 6], samples_debug=4)
        self.assertEqual(int_sweep.default, 0)
        self.assertListEqual(int_sweep.values(False), [0, 1, 2, 3, 4, 5, 6])
        self.assertListEqual(int_sweep.values(True), [0, 2, 4, 6])

    def test_int_sweep_10_debug_sampes(self):
        int_sweep = IntSweep(bounds=[0, 10])
        self.assertEqual(int_sweep.default, 0)
        self.assertListEqual(int_sweep.values(False), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertListEqual(int_sweep.values(True), [0, 10])

    def test_int_sweep_10_with_values_(self):
        int_sweep = IntSweep(bounds=[0, 10])
        self.assertEqual(int_sweep.default, 0)
        self.assertListEqual(int_sweep.values(False), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertListEqual(int_sweep.with_samples(3).values(True), [0, 10])
        self.assertListEqual(int_sweep.with_samples(3).values(False), [0, 5, 10])

    def test_int_sweep_level_10_with_values_(self):
        int_sweep = IntSweep(bounds=[0, 10])
        self.assertListEqual(int_sweep.with_level(0).values(), [0, 10])
        self.assertListEqual(int_sweep.with_level(1).values(), [0, 5, 10])
        self.assertListEqual(int_sweep.with_level(2).values(), [0, 2, 5, 7, 10])
        self.assertListEqual(int_sweep.with_level(3).values(), [0, 1, 2, 3, 5, 6, 7, 8, 10])
        self.assertListEqual(int_sweep.with_level(4).values(), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def test_float_sweep(self):
        float_sweep = FloatSweep(bounds=[0, 1])

        self.assertListEqual(list(float_sweep.with_level(1).values()), [0.0])
        self.assertListEqual(list(float_sweep.with_level(2).values()), [0.0, 1.0])
        self.assertListEqual(list(float_sweep.with_level(3).values()), [0.0, 0.5, 1.0])
        self.assertListEqual(list(float_sweep.with_level(4).values()), [0.0, 0.25, 0.5, 0.75, 1.0])

    def test_enum_sweep_level(self):
        class Enum1(StrEnum):
            VAL1 = auto()
            VAL2 = auto()
            VAL3 = auto()
            VAL4 = auto()

        enum_sweep = EnumSweep(Enum1)

        self.assertListEqual(enum_sweep.with_level(0).values(), [Enum1.VAL1, Enum1.VAL4])

        self.assertListEqual(
            enum_sweep.with_level(1).values(), [Enum1.VAL1, Enum1.VAL2, Enum1.VAL4]
        )
        self.assertListEqual(
            enum_sweep.with_level(2).values(), [Enum1.VAL1, Enum1.VAL2, Enum1.VAL3, Enum1.VAL4]
        )
        self.assertListEqual(
            enum_sweep.with_level(3).values(), [Enum1.VAL1, Enum1.VAL2, Enum1.VAL3, Enum1.VAL4]
        )

    def test_bool_sweep_level(self):
        bool_sweep = BoolSweep()

        self.assertListEqual(bool_sweep.with_level(1).values(), [True])
        self.assertListEqual(bool_sweep.with_level(1).values(), [True, False])
        self.assertListEqual(bool_sweep.with_level(2).values(), [True, False])

    def test_string_sweep_level(self):
        string_sweep = StringSweep(["VAL1", "VAL2", "VAL3", "VAL4"])
        self.assertListEqual(string_sweep.with_level(1).values(), ["VAL1"])
        self.assertListEqual(string_sweep.with_level(2).values(), ["VAL1", "VAL4"])
        self.assertListEqual(string_sweep.with_level(3).values(), ["VAL1", "VAL2", "VAL4"])
        self.assertListEqual(string_sweep.with_level(4).values(), ["VAL1", "VAL2", "VAL3", "VAL4"])
        self.assertListEqual(string_sweep.with_level(5).values(), ["VAL1", "VAL2", "VAL3", "VAL4"])

    @given(st.integers(min_value=1, max_value=10))
    def test_int_sweep_samples(self, samples):
        int_sweep = IntSweep(bounds=[0, 10], samples=samples)
        self.assertEqual(int_sweep.default, 0)
        self.assertEqual(len(int_sweep.values(False)), samples)

    @given(st.integers(min_value=1, max_value=10))
    def test_int_sweep_debug_samples(self, samples_debug):
        int_sweep = IntSweep(bounds=[0, 10], samples_debug=samples_debug)
        self.assertEqual(int_sweep.default, 0)
        self.assertEqual(len(int_sweep.values(True)), samples_debug)

    @pytest.mark.skip
    @given(st.integers(min_value=1, max_value=10), st.integers(min_value=1, max_value=10))
    def test_int_sweep_samples_all(self, samples, samples_debug):
        int_sweep = IntSweep(bounds=[0, 10], samples=samples)
        self.assertEqual(int_sweep.default, 0)
        self.assertEqual(len(int_sweep.values(False)), samples)
        self.assertEqual(len(int_sweep.values(True)), samples_debug)
