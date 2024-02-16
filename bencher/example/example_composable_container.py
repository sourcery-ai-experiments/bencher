import bencher as bch
from example_image import BenchPolygons


class BenchComposableContainerImage(BenchPolygons):

    compose_method = bch.EnumSweep(bch.ComposeType)
    labels = bch.BoolSweep()
    num_frames = bch.IntSweep(default=5, bounds=[1, 100])
    polygon_vid = bch.ResultVideo()

    def __call__(self, **kwargs):
        self.update_params_from_kwargs(**kwargs)
        var_name = None
        var_value = None

        if self.labels:
            var_name = "sides"
            var_value = self.sides
        vr = bch.ComposableContainerVideo()
        for i in range(self.num_frames):
            res = super().__call__(start_angle=i)
            vr.append(res["polygon"])
        self.polygon_vid = vr.to_video(
            bch.RenderCfg(
                compose_method=self.compose_method,
                var_name=var_name,
                var_value=var_value,
                max_frame_duration=1.0 / 20.0,
            )
        )
        return self.get_results_values_as_dict()


class BenchComposableContainerVideo(BenchComposableContainerImage):

    def __call__(self, **kwargs):
        self.update_params_from_kwargs(**kwargs)
        vr = bch.ComposableContainerVideo()
        clips = []
        for i in range(3, 5):
            res = super().__call__(compose_method=bch.ComposeType.sequence, sides=i, num_frames=i*10)
            clips.append(res["polygon_vid"])

        for c in clips:
            vr.append(c)

        self.polygon_vid = vr.to_video(bch.RenderCfg(compose_method=kwargs.get("compose_method")))
        return self.get_results_values_as_dict()


def example_composable_container_image(
    run_cfg: bch.BenchRunCfg = None, report: bch.BenchReport = None
) -> bch.Bench:
    bench = BenchComposableContainerImage().to_bench(run_cfg, report)
    bench.result_vars = ["polygon_vid"]
    bench.add_plot_callback(bch.BenchResult.to_panes)
    # bench.add_plot_callback(bch.BenchResult.to_video_grid,result_types=(bch.ResultVideo))
    # bench.add_plot_callback(bch.BenchResult.to_video_summary,result_types=(bch.ResultVideo))
    bench.plot_sweep(input_vars=["compose_method", "labels"])
    return bench


def example_composable_container_video(
    run_cfg: bch.BenchRunCfg = None, report: bch.BenchReport = None
) -> bch.Bench:
    bench = BenchComposableContainerVideo().to_bench(run_cfg, report)

    vid = bench.worker(compose_method=bch.ComposeType.down, labels=False)["polygon_vid"]

    # import panel as pn

    # pn.Row(vid).show()

    bench.result_vars = ["polygon_vid"]
    bench.add_plot_callback(bch.BenchResult.to_panes)
    # bench.add_plot_callback(bch.BenchResult.to_video_grid,result_types=(bch.ResultVideo))
    # bench.add_plot_callback(bch.BenchResult.to_video_summary,result_types=(bch.ResultVideo))
    bench.plot_sweep(input_vars=["compose_method", "labels"])
    return bench


if __name__ == "__main__":
    ex_run_cfg = bch.BenchRunCfg()
    ex_run_cfg.use_sample_cache = False
    # ex_run_cfg.level = 2
    ex_report = bch.BenchReport()
    example_composable_container_image(ex_run_cfg, report=ex_report)
    example_composable_container_video(ex_run_cfg, report=ex_report)
    ex_report.show()
