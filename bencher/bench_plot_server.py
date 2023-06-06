import logging
from diskcache import Cache

from bencher.plt_cfg import BenchPlotter
from bencher.bench_cfg import BenchPlotSrvCfg, BenchCfg

logging.basicConfig(level=logging.INFO)
import panel as pn
from typing import Tuple, List


class BenchPlotServer:
    def __init__(self) -> None:
        """Create a new BenchPlotServer object"""
        pass

    def plot_server(
        self, bench_name: str, plot_cfg: BenchPlotSrvCfg = BenchPlotSrvCfg(), plots_instance=None
    ) -> None:
        """Load previously calculated benchmark data from the database and start a plot server to display it

        Args:
            bench_name (str): The name of the benchmark and output folder for the figures
            plot_cfg (BenchPlotSrvCfg, optional): Options for the plot server. Defaults to BenchPlotSrvCfg().

        Raises:
            FileNotFoundError: No data found was found in the database to plot
        """
        if plots_instance is None:
            plots_instance = self.load_data_from_cache(bench_name)
        self.serve(bench_name, plots_instance, port=plot_cfg.port)

    def load_data_from_cache(self, bench_name: str) -> Tuple[BenchCfg, List[pn.panel]] | None:
        """Load previously calculated benchmark data from the database and start a plot server to display it

        Args:
            bench_name (str): The name of the benchmark and output folder for the figures

        Returns:
            Tuple[BenchCfg, List[pn.panel]] | None: benchmark result data and any additional panels

        Raises:
            FileNotFoundError: No data found was found in the database to plot
        """

        with Cache("cachedir/benchmark_inputs") as c:
            if bench_name in c:
                logging.info(f"loading benchmarks: {bench_name}")
                # use the benchmark name to look up the hash of the results
                bench_cfg_hashes = c[bench_name]
                plots_instance = None
                for bench_cfg_hash in bench_cfg_hashes:
                    # load the results based on the hash retrieved from the benchmark name
                    if bench_cfg_hash in c:
                        logging.info(f"loading cached results from key: {bench_cfg_hash}")
                        bench_cfg = c[bench_cfg_hash]
                        logging.info(f"loaded: {bench_cfg.title}")

                        plots_instance = BenchPlotter.plot(bench_cfg, plots_instance)
                    else:
                        raise FileNotFoundError(
                            "The benchmarks have been run and saved, but the specific results you are trying to load do not exist.  This should not happen and could be because the cache was cleared."
                        )
                return plots_instance
            else:
                raise FileNotFoundError(
                    "This benchmark name does not exist in the results cache. Was not able to load the results to plot!  Make sure to run the bencher to generate and save results to the cache"
                )

    def serve(self, bench_name: str, plots_instance: List[pn.panel], port: int = None) -> None:
        """Launch a panel server to view results


        Args:
            bench_cfg (BenchCfg): benchmark results
            plots_instance (List[pn.panel]): list of panel objects to display
            port (int): use a fixed port to lauch the server
        """

        if port is not None:
            pn.serve(plots_instance, title=bench_name, websocket_origin=["*"], port=port)
        else:
            logging.getLogger().setLevel(logging.WARNING)
            pn.serve(plots_instance, title=bench_name)
