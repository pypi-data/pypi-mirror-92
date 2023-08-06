from bmlx_components.xdl_base.driver import XdlDriver
from bmlx.execution.execution import ExecutionInfo
from bmlx.flow import Channel, Pipeline, DriverArgs, Component
from typing import Text, Any, Dict


class XdlConverterDriver(XdlDriver):
    # override super method
    def pre_execution(
        self,
        input_dict: Dict[Text, Channel],
        output_dict: Dict[Text, Channel],
        exec_properties: Dict[Text, Any],
        pipeline: Pipeline,
        component: Component,
        driver_args: DriverArgs,
    ) -> ExecutionInfo:
        ret = super(XdlConverterDriver, self).pre_execution(
            input_dict,
            output_dict,
            exec_properties,
            pipeline,
            component,
            driver_args,
        )
        # 通过worker数量判断是否是单机版
        if ret.exec_properties["runtime_configs"][
            "resources"
        ]["worker"]["instances"].as_number() == 1:
            ret.output_dict["single_machine"][0].meta.uri = "single"
        else:
            ret.output_dict["single_machine"][0].meta.uri = "multi"
        return ret

    def _rewrite_launch_config(self, exec_properties):
        pass

    def _resolve_model_paths(self, input_dict, exec_properties):
        return "", ""