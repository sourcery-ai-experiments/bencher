# Generated by CodiumAI
import unittest
from unittest.mock import Mock
from bencher.example.benchmark_data import SimpleBenchClass, SimpleBenchClassFloat, AllSweepVars
import bencher as bch


class TestBenchRunner(unittest.TestCase):
    # Tests that bch.BenchRunner can be created with default configuration and the import statement in the bch.BenchRunner class is fixed
    def test_benchrunner_default_configuration_fixed(self):
        bench_runner = bch.BenchRunner("bench_runner_test")
        self.assertEqual(bench_runner.run_cfg.use_sample_cache, True)
        self.assertEqual(bench_runner.run_cfg.only_hash_tag, True)
        self.assertEqual(bench_runner.run_cfg.level, 1)
        self.assertEqual(bench_runner.publisher, None)
        self.assertEqual(bench_runner.bench_fns, [])

    # Tests that Benchable functions can be added to bch.BenchRunner instance
    def test_benchrunner_add_benchable_functions(self):
        bench_runner = bch.BenchRunner("bench_runner_test")
        bench_fn1 = Mock()
        bench_fn2 = Mock()
        bench_runner.add_run(bench_fn1)
        bench_runner.add_run(bench_fn2)
        self.assertEqual(len(bench_runner.bench_fns), 2)
        self.assertIn(bench_fn1, bench_runner.bench_fns)
        self.assertIn(bench_fn2, bench_runner.bench_fns)

    def test_benchrunner_handle_empty_list(self):
        bench_runner = bch.BenchRunner("bench_runner_test")
        results = bench_runner.run()
        self.assertEqual(len(results), 0)

    def test_benchrunner_benchable_class(self):
        bench_runner = bch.BenchRunner("bench_runner_test")
        bench_runner.add_bench(SimpleBenchClass())
        results = bench_runner.run(run_cfg=bch.BenchRunCfg(run_tag="1"))

        self.assertEqual(results[0].run_tag, "1")

    def test_benchrunner_benchable_class_run_constructor(self):
        bench_runner = bch.BenchRunner("bench_runner_test", run_cfg=bch.BenchRunCfg(run_tag="1"))
        bench_runner.add_bench(SimpleBenchClass())
        results = bench_runner.run()
        self.assertEqual(results[0].run_tag, "1")

    def test_benchrunner_level_1(self):
        results = bch.BenchRunner("bench_runner_test", AllSweepVars()).run(min_level=1)
        ds = results[0].ds.to_dataframe()
        self.assertEqual(ds.shape[0], 1)

    def test_benchrunner_level_1_only(self):
        results = bch.BenchRunner("bench_runner_test", AllSweepVars()).run(level=1)
        ds = results[0].ds.to_dataframe()
        self.assertEqual(ds.shape[0], 1)

    def test_benchrunner_repeats(self):
        res = bch.Bench(
            "float", SimpleBenchClassFloat(), run_cfg=bch.BenchRunCfg(level=2, repeats=1)
        ).plot_sweep("float")
        self.assertEqual(res.samples(), 2)

        res = bch.Bench(
            "float", SimpleBenchClassFloat(), run_cfg=bch.BenchRunCfg(level=2, repeats=5)
        ).plot_sweep("float")
        self.assertEqual(res.samples(), 10)

    # # Tests that bch.BenchRunner can run Benchable functions with default configuration (fixed)
    # def test_benchrunner_run_default_configuration_fixed(self):

    #     bench_runner = bch.BenchRunner()
    #     bench_fn1 = Mock()
    #     bench_fn2 = Mock()
    #     bench_runner.add_run(bench_fn1)
    #     bench_runner.add_run(bench_fn2)
    #     results = bench_runner.run()

    #     self.assertEqual(len(results), 10)
    #     self.assertEqual(results[0].level, 1)
    #     self.assertEqual(results[1].level, 1)
    #     self.assertEqual(results[2].level, 2)
    #     self.assertEqual(results[3].level, 2)
    #     self.assertEqual(results[4].level, 3)
    #     self.assertEqual(results[5].level, 3)
    #     self.assertEqual(results[6].level, 4)
    #     self.assertEqual(results[7].level, 4)
    #     self.assertEqual(results[8].level, 5)
    #     self.assertEqual(results[9].level, 5)

    # Tests that bch.BenchRunner can run Benchable functions with custom configuration, after fixing the import statements
    # def test_benchrunner_run_custom_configuration_fixed_fixed_import_statements(self):

    #     bench_runner = bch.BenchRunner()
    #     bench_fn1 = Mock()
    #     bench_fn2 = Mock()
    #     bench_runner.add_run(bench_fn1)
    #     bench_runner.add_run(bench_fn2)
    #     run_cfg = bch.BenchRunCfg()
    #     run_cfg.use_sample_cache = False
    #     run_cfg.only_hash_tag = False
    #     run_cfg.level = 3
    #     results = bench_runner.run(run_cfg=run_cfg)
    #     self.assertEqual(len(results), 2)
    #     self.assertEqual(results[0].level, 3)
    #     self.assertEqual(results[1].level, 3)

    # Tests that bch.BenchRunner can publish results of Benchable functions (fixed)
    # def test_benchrunner_publish_results_fixed(self):
    #     class MockBenchable:
    #         def bench(self, run_cfg: bch.BenchRunCfg) -> bch.BenchCfg:
    #             return bch.BenchCfg()

    #     bench_runner = bch.BenchRunner(publisher=Mock())
    #     bench_fn1 = MockBenchable()
    #     bench_fn2 = MockBenchable()
    #     bench_runner.add_run(bench_fn1)
    #     bench_runner.add_run(bench_fn2)
    #     results = bench_runner.run(publish=True)
    #     self.assertEqual(len(results), 10)
    #     self.assertEqual(bench_runner.publisher.call_count, 10)
    #     self.assertEqual(bench_runner.publisher.call_args_list[0][0][0], results[0])
    #     self.assertEqual(bench_runner.publisher.call_args_list[1][0][0], results[1])
    #     self.assertEqual(bench_runner.publisher.call_args_list[2][0][0], results[2])
    #     self.assertEqual(bench_runner.publisher.call_args_list[3][0][0], results[3])
    #     self.assertEqual(bench_runner.publisher.call_args_list[4][0][0], results[4])
    #     self.assertEqual(bench_runner.publisher.call_args_list[5][0][0], results[5])
    #     self.assertEqual(bench_runner.publisher.call_args_list[6][0][0], results[6])
    #     self.assertEqual(bench_runner.publisher.call_args_list[7][0][0], results[7])
    #     self.assertEqual(bench_runner.publisher.call_args_list[8][0][0], results[8])
    #     self.assertEqual(bench_runner.publisher.call_args_list[9][0][0], results[9])

    # Tests that bch.BenchRunner can handle empty list of Benchable functions

    # Tests that bch.BenchRunner can handle empty list of Benchable functions
    # def test_benchrunner_handle_empty_list(self):

    #     def benchable(run_cfg:bch.BenchRunCfg)->bch.BenchCfg:
    #         bench = bch.Bench("sbc",SimpleBenchClass(),run_cfg=run_cfg)
    #         return bench.plot_sweep("sweep1")

    #     bench_runner = bch.BenchRunner()
    #     bench_runner.add_run(benchable)

    #     results = bench_runner.run(run_cfg=bch.BenchRunCfg(run_tag="1"))

    #     self.assertEqual(results[0].run_tag, "1")

    # Tests that bch.BenchRunner can handle empty list of Benchable functions
