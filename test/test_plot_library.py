import unittest

# Generated by CodiumAI
from bencher.plotting.plot_library import PlotLibrary
from bencher.plotting.plot_types import PlotTypes


class TestPlotLibrary(unittest.TestCase):
    # Tests that the tables PlotCollection only contains table plots
    def test_tables_plot_collection(self) -> None:
        tables_plots = PlotLibrary.tables()
        self.assertIn(PlotTypes.dataframe_multi_index, tables_plots.plotters)
        self.assertIn(PlotTypes.dataframe_mean, tables_plots.plotters)
        self.assertEqual(len(tables_plots.plotters), 2)

    # Tests that the all PlotCollection contains all possible plots
    def test_all_plot_collection(self) -> None:
        all_plots = PlotLibrary.all()
        for pt in list(PlotTypes):
            self.assertIn(pt, all_plots.plotters)
        self.assertEqual(len(all_plots.plotters), len(PlotTypes))

    # Tests that the none PlotCollection contains no active plots
    def test_none_plot_collection(self) -> None:
        none_plots = PlotLibrary.none()
        self.assertEqual(len(none_plots.plotters), 0)

    # Test that adding a plot that is not in the list of available plots raises a ValueError
    def test_adding_plot_not_in_available_plots(self) -> None:
        plt_col = PlotLibrary.none()
        with self.assertRaises(ValueError):
            plt_col.add("invalid_plot")

    # Test that removing a plot that is not in the list of active plots raises an Keyerror
    def test_removing_plot_not_in_active_plots(self) -> None:
        plt_col = PlotLibrary.tables()
        plt_col.remove(PlotTypes.dataframe_multi_index)
        self.assertEqual(len(plt_col.plotters), 1)  # 2 plots in tables by default and 1 removed
        with self.assertRaises(KeyError):
            plt_col.remove(PlotTypes.swarmplot)
