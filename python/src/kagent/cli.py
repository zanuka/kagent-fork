import typer
from autogen_core import CancellationToken
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

from kagent.tools.argo._argo_rollouts_k8sgw_installation import (
    check_plugin_logs,
    verify_gateway_plugin,
)
from kagent.tools.argo._kubectl_argo_rollouts import (
    pause_rollout,
    promote_rollout,
    set_rollout_image,
    verify_argo_rollouts_controller_install,
    verify_kubectl_plugin_install,
)
from kagent.tools.helm._helm import (
    helm_get_release,
    helm_list_releases,
    helm_repo_add,
    helm_repo_update,
    helm_uninstall,
    upgrade_release,
)
from kagent.tools.istio._istioctl import (
    analyze_cluster_configuration,
    apply_waypoint,
    delete_waypoint,
    generate_manifest,
    generate_waypoint,
    install_istio,
    list_waypoints,
    proxy_config,
    proxy_status,
    remote_clusters,
    ztunnel_config,
)
from kagent.tools.k8s._kubectl import (
    annotate_resource,
    apply_manifest,
    check_service_connectivity,
    create_resource,
    delete_resource,
    describe_resource,
    get_available_api_resources,
    get_cluster_configuration,
    get_events,
    get_pod_logs,
    get_resource_yaml,
    get_resources,
    label_resource,
    patch_resource,
    remove_annotation,
    remove_label,
    rollout,
    scale,
)
from kagent.tools.prometheus._prometheus import (
    AlertmanagersInput,
    AlertmanagersTool,
    AlertsInput,
    AlertsTool,
    BaseTool,
    BuildInfoInput,
    BuildInfoTool,
    Config,
    LabelNamesInput,
    LabelNamesTool,
    LabelValuesInput,
    LabelValuesTool,
    MetadataInput,
    MetadataTool,
    QueryInput,
    QueryRangeInput,
    QueryRangeTool,
    QueryTool,
    RulesInput,
    RulesTool,
    RuntimeInfoInput,
    RuntimeInfoTool,
    SeriesInput,
    SeriesQueryTool,
    StatusConfigInput,
    StatusConfigTool,
    StatusFlagsInput,
    StatusFlagsTool,
    TargetMetadataInput,
    TargetMetadataTool,
    TargetsInput,
    TargetsTool,
    TSDBStatusInput,
    TSDBStatusTool,
)
from kagent.tools.hello import hello_tool

app = typer.Typer()

mcp = FastMCP("Hello App")


def add_typed_tool(cfg_type: type[BaseModel], tool: BaseTool):
    def query_tool(cfg: cfg_type):
        return tool.run_json(cfg.model_dump(), CancellationToken())

    mcp.add_tool(
        query_tool,
        tool.name,
        tool.description,
    )


@app.command()
def prometheus(
    url: str = typer.Option(..., "--url", "-u"),
):
    cfg = Config(base_url=url)

    def query_tool(input: QueryInput):
        return QueryTool(cfg).run_json(input.model_dump(), CancellationToken())

    mcp.add_tool(query_tool, QueryTool(cfg).name, QueryTool(cfg).description)

    def query_range_tool(input: QueryRangeInput):
        return QueryRangeTool(cfg).run_json(input.model_dump(), CancellationToken())

    mcp.add_tool(query_range_tool, QueryRangeTool(cfg).name, QueryRangeTool(cfg).description)

    def series_query_tool(input: SeriesInput):
        return SeriesQueryTool(cfg).run_json(input.model_dump(), CancellationToken())

    mcp.add_tool(series_query_tool, SeriesQueryTool(cfg).name, SeriesQueryTool(cfg).description)

    def label_names_tool(input: LabelNamesInput):
        return LabelNamesTool(cfg).run_json(input.model_dump(), CancellationToken())

    mcp.add_tool(label_names_tool, LabelNamesTool(cfg).name, LabelNamesTool(cfg).description)

    def label_values_tool(input: LabelValuesInput):
        return LabelValuesTool(cfg).run_json(input.model_dump(), CancellationToken())

    mcp.add_tool(label_values_tool, LabelValuesTool(cfg).name, LabelValuesTool(cfg).description)

    def alertmanagers_tool(input: AlertmanagersInput):
        return AlertmanagersTool(cfg).run_json(input.model_dump(), CancellationToken())

    mcp.add_tool(alertmanagers_tool, AlertmanagersTool(cfg).name, AlertmanagersTool(cfg).description)

    def target_metadata_tool(input: TargetMetadataInput):
        return TargetMetadataTool(cfg).run_json(input.model_dump(), CancellationToken())

    mcp.add_tool(target_metadata_tool, TargetMetadataTool(cfg).name, TargetMetadataTool(cfg).description)

    def status_config_tool(input: StatusConfigInput):
        return StatusConfigTool(cfg).run_json(input.model_dump(), CancellationToken())

    mcp.add_tool(status_config_tool, StatusConfigTool(cfg).name, StatusConfigTool(cfg).description)

    def status_flags_tool(input: StatusFlagsInput):
        return StatusFlagsTool(cfg).run_json(input.model_dump(), CancellationToken())

    mcp.add_tool(status_flags_tool, StatusFlagsTool(cfg).name, StatusFlagsTool(cfg).description)

    def runtime_info_tool(input: RuntimeInfoInput):
        return RuntimeInfoTool(cfg).run_json(input.model_dump(), CancellationToken())

    mcp.add_tool(runtime_info_tool, RuntimeInfoTool(cfg).name, RuntimeInfoTool(cfg).description)

    def build_info_tool(input: BuildInfoInput):
        return BuildInfoTool(cfg).run_json(input.model_dump(), CancellationToken())

    mcp.add_tool(build_info_tool, BuildInfoTool(cfg).name, BuildInfoTool(cfg).description)

    def tsdb_status_tool(input: TSDBStatusInput):
        return TSDBStatusTool(cfg).run_json(input.model_dump(), CancellationToken())

    mcp.add_tool(tsdb_status_tool, TSDBStatusTool(cfg).name, TSDBStatusTool(cfg).description)

    def metadata_tool(input: MetadataInput):
        return MetadataTool(cfg).run_json(input.model_dump(), CancellationToken())

    mcp.add_tool(metadata_tool, MetadataTool(cfg).name, MetadataTool(cfg).description)

    def alerts_tool(input: AlertsInput):
        return AlertsTool(cfg).run_json(input.model_dump(), CancellationToken())

    mcp.add_tool(alerts_tool, AlertsTool(cfg).name, AlertsTool(cfg).description)

    def rules_tool(input: RulesInput):
        return RulesTool(cfg).run_json(input.model_dump(), CancellationToken())

    mcp.add_tool(rules_tool, RulesTool(cfg).name, RulesTool(cfg).description)

    def targets_tool(input: TargetsInput):
        return TargetsTool(cfg).run_json(input.model_dump(), CancellationToken())

    mcp.add_tool(targets_tool, TargetsTool(cfg).name, TargetsTool(cfg).description)

    mcp.run()


@app.command()
def argo():
    mcp.add_tool(verify_gateway_plugin.run, verify_gateway_plugin.name, verify_gateway_plugin.description)
    mcp.add_tool(check_plugin_logs.run, check_plugin_logs.name, check_plugin_logs.description)
    mcp.add_tool(
        verify_kubectl_plugin_install.run,
        verify_kubectl_plugin_install.name,
        verify_kubectl_plugin_install.description,
    )
    mcp.add_tool(
        verify_argo_rollouts_controller_install.run,
        verify_argo_rollouts_controller_install.name,
        verify_argo_rollouts_controller_install.description,
    )
    mcp.add_tool(pause_rollout.run, pause_rollout.name, pause_rollout.description)
    mcp.add_tool(promote_rollout.run, promote_rollout.name, promote_rollout.description)
    mcp.add_tool(set_rollout_image.run, set_rollout_image.name, set_rollout_image.description)

    mcp.run()


@app.command()
def istio():
    mcp.add_tool(
        analyze_cluster_configuration.run,
        analyze_cluster_configuration.name,
        analyze_cluster_configuration.description,
    )
    mcp.add_tool(apply_waypoint.run, apply_waypoint.name, apply_waypoint.description)
    mcp.add_tool(delete_waypoint.run, delete_waypoint.name, delete_waypoint.description)
    mcp.add_tool(list_waypoints.run, list_waypoints.name, list_waypoints.description)
    mcp.add_tool(generate_manifest.run, generate_manifest.name, generate_manifest.description)
    mcp.add_tool(generate_waypoint.run, generate_waypoint.name, generate_waypoint.description)
    mcp.add_tool(install_istio.run, install_istio.name, install_istio.description)
    mcp.add_tool(proxy_config.run, proxy_config.name, proxy_config.description)
    mcp.add_tool(proxy_status.run, proxy_status.name, proxy_status.description)
    mcp.add_tool(remote_clusters.run, remote_clusters.name, remote_clusters.description)
    mcp.add_tool(ztunnel_config.run, ztunnel_config.name, ztunnel_config.description)
    mcp.add_tool(proxy_status.run, proxy_status.name, proxy_status.description)
    mcp.add_tool(remote_clusters.run, remote_clusters.name, remote_clusters.description)

    mcp.run()


@app.command()
def k8s():
    def wrap_tool(tool):
        def wrapped(args):
            return tool.run(args, CancellationToken())
        return wrapped

    mcp.add_tool(wrap_tool(apply_manifest), apply_manifest.name, apply_manifest.description)
    mcp.add_tool(wrap_tool(get_pod_logs), get_pod_logs.name, get_pod_logs.description)
    mcp.add_tool(wrap_tool(get_resources), get_resources.name, get_resources.description)
    mcp.add_tool(wrap_tool(get_resource_yaml), get_resource_yaml.name, get_resource_yaml.description)
    mcp.add_tool(wrap_tool(get_cluster_configuration), get_cluster_configuration.name, get_cluster_configuration.description)
    mcp.add_tool(wrap_tool(describe_resource), describe_resource.name, describe_resource.description)
    mcp.add_tool(wrap_tool(delete_resource), delete_resource.name, delete_resource.description)
    mcp.add_tool(wrap_tool(label_resource), label_resource.name, label_resource.description)
    mcp.add_tool(wrap_tool(annotate_resource), annotate_resource.name, annotate_resource.description)
    mcp.add_tool(wrap_tool(remove_label), remove_label.name, remove_label.description)
    mcp.add_tool(wrap_tool(remove_annotation), remove_annotation.name, remove_annotation.description)
    mcp.add_tool(wrap_tool(rollout), rollout.name, rollout.description)
    mcp.add_tool(wrap_tool(scale), scale.name, scale.description)
    mcp.add_tool(wrap_tool(patch_resource), patch_resource.name, patch_resource.description)
    mcp.add_tool(wrap_tool(check_service_connectivity), check_service_connectivity.name, check_service_connectivity.description)
    mcp.add_tool(wrap_tool(create_resource), create_resource.name, create_resource.description)
    mcp.add_tool(wrap_tool(get_events), get_events.name, get_events.description)
    mcp.add_tool(wrap_tool(get_available_api_resources), get_available_api_resources.name, get_available_api_resources.description)
    mcp.run()


@app.command()
def helm():
    mcp.add_tool(helm_list_releases.run, helm_list_releases.name, helm_list_releases.description)
    mcp.add_tool(helm_get_release.run, helm_get_release.name, helm_get_release.description)
    mcp.add_tool(helm_uninstall.run, helm_uninstall.name, helm_uninstall.description)
    mcp.add_tool(upgrade_release.run, upgrade_release.name, upgrade_release.description)
    mcp.add_tool(helm_repo_add.run, helm_repo_add.name, helm_repo_add.description)
    mcp.add_tool(helm_repo_update.run, helm_repo_update.name, helm_repo_update.description)
    mcp.run()


@app.command()
def serve(
    host: str = "127.0.0.1",
    port: int = 8081,
):
    import logging
    import os

    from autogenstudio.cli import ui
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
    from opentelemetry.instrumentation.openai import OpenAIInstrumentor
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    logging.basicConfig(level=logging.INFO)
    tracing_enabled = os.getenv("OTEL_TRACING_ENABLED", "false").lower() == "true"
    if tracing_enabled:
        logging.info("Enabling tracing")
        tracer_provider = TracerProvider(resource=Resource({"service.name": "kagent"}))
        processor = BatchSpanProcessor(OTLPSpanExporter())
        tracer_provider.add_span_processor(processor)
        trace.set_tracer_provider(tracer_provider)
        HTTPXClientInstrumentor().instrument()
        OpenAIInstrumentor().instrument()

    ui(host=host, port=port)


@app.command()
def hello():
    mcp.add_tool(
        hello_tool.run,
        hello_tool.name,
        hello_tool.description,
    )
    mcp.run()


def run():
    app()


if __name__ == "__main__":
    run()
