# Generated by CodiumAI
from diskcache import Cache
import unittest
import bencher as bch

from bencher.example.benchmark_data import SimpleBenchClass

# from concurrent.futures import Future
import concurrent.futures


class TestBenchPlotServer(unittest.TestCase):
    # Tests that the plot server loads previously calculated benchmark data from the database
    def test_plot_server_load_data_from_database(self):
        sbc = SimpleBenchClass()
        bench = bch.Bench("test_bench_server", sbc)
        bench.plot_sweep(
            title="test_bench_server",
            input_vars=[sbc.param.var1],
            result_vars=[sbc.param.result],
            run_cfg=bch.BenchRunCfg(auto_plot=False),
        )
        bench.save()

        bps = bch.BenchPlotServer()

        bps.load_data_from_cache(bench.bench_name)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(bps.plot_server, bench.bench_name)

    # Tests that the plot server raises FileNotFoundError when no data is found in the cache
    def test_plot_server_no_data_in_cache(self):
        server = bch.BenchPlotServer()
        bench_name = "test_bench"
        with self.assertRaises(FileNotFoundError):
            server.load_data_from_cache(bench_name)

    # Tests that the plot server raises FileNotFoundError when no data is found in the database
    def test_plot_server_no_data_in_database(self):
        server = bch.BenchPlotServer()
        bench_name = "test_bench"
        with Cache("cachedir/benchmark_inputs") as cache:
            if bench_name in cache:
                with self.assertRaises(FileNotFoundError):
                    server.load_data_from_cache(bench_name)
            else:
                with self.assertRaises(FileNotFoundError):
                    server.load_data_from_cache(bench_name)
