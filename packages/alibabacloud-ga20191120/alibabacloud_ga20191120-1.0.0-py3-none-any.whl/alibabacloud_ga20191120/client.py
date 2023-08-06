# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from typing import Dict

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_endpoint_util.client import Client as EndpointUtilClient
from alibabacloud_ga20191120 import models as ga_20191120_models
from alibabacloud_tea_util import models as util_models


class Client(OpenApiClient):
    """
    *\
    """
    def __init__(
        self, 
        config: open_api_models.Config,
    ):
        super().__init__(config)
        self._endpoint_rule = 'regional'
        self.check_config(config)
        self._endpoint = self.get_endpoint('ga', self._region_id, self._endpoint_rule, self._network, self._suffix, self._endpoint_map, self._endpoint)

    def get_endpoint(
        self,
        product_id: str,
        region_id: str,
        endpoint_rule: str,
        network: str,
        suffix: str,
        endpoint_map: Dict[str, str],
        endpoint: str,
    ) -> str:
        if not UtilClient.empty(endpoint):
            return endpoint
        if not UtilClient.is_unset(endpoint_map) and not UtilClient.empty(endpoint_map.get(region_id)):
            return endpoint_map.get(region_id)
        return EndpointUtilClient.get_endpoint_rules(product_id, region_id, endpoint_rule, network, suffix)

    def attach_ddos_to_accelerator_with_options(
        self,
        request: ga_20191120_models.AttachDdosToAcceleratorRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.AttachDdosToAcceleratorResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.AttachDdosToAcceleratorResponse().from_map(
            self.do_rpcrequest('AttachDdosToAccelerator', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def attach_ddos_to_accelerator_with_options_async(
        self,
        request: ga_20191120_models.AttachDdosToAcceleratorRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.AttachDdosToAcceleratorResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.AttachDdosToAcceleratorResponse().from_map(
            await self.do_rpcrequest_async('AttachDdosToAccelerator', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def attach_ddos_to_accelerator(
        self,
        request: ga_20191120_models.AttachDdosToAcceleratorRequest,
    ) -> ga_20191120_models.AttachDdosToAcceleratorResponse:
        runtime = util_models.RuntimeOptions()
        return self.attach_ddos_to_accelerator_with_options(request, runtime)

    async def attach_ddos_to_accelerator_async(
        self,
        request: ga_20191120_models.AttachDdosToAcceleratorRequest,
    ) -> ga_20191120_models.AttachDdosToAcceleratorResponse:
        runtime = util_models.RuntimeOptions()
        return await self.attach_ddos_to_accelerator_with_options_async(request, runtime)

    def bandwidth_package_add_accelerator_with_options(
        self,
        request: ga_20191120_models.BandwidthPackageAddAcceleratorRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.BandwidthPackageAddAcceleratorResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.BandwidthPackageAddAcceleratorResponse().from_map(
            self.do_rpcrequest('BandwidthPackageAddAccelerator', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def bandwidth_package_add_accelerator_with_options_async(
        self,
        request: ga_20191120_models.BandwidthPackageAddAcceleratorRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.BandwidthPackageAddAcceleratorResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.BandwidthPackageAddAcceleratorResponse().from_map(
            await self.do_rpcrequest_async('BandwidthPackageAddAccelerator', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def bandwidth_package_add_accelerator(
        self,
        request: ga_20191120_models.BandwidthPackageAddAcceleratorRequest,
    ) -> ga_20191120_models.BandwidthPackageAddAcceleratorResponse:
        runtime = util_models.RuntimeOptions()
        return self.bandwidth_package_add_accelerator_with_options(request, runtime)

    async def bandwidth_package_add_accelerator_async(
        self,
        request: ga_20191120_models.BandwidthPackageAddAcceleratorRequest,
    ) -> ga_20191120_models.BandwidthPackageAddAcceleratorResponse:
        runtime = util_models.RuntimeOptions()
        return await self.bandwidth_package_add_accelerator_with_options_async(request, runtime)

    def bandwidth_package_remove_accelerator_with_options(
        self,
        request: ga_20191120_models.BandwidthPackageRemoveAcceleratorRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.BandwidthPackageRemoveAcceleratorResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.BandwidthPackageRemoveAcceleratorResponse().from_map(
            self.do_rpcrequest('BandwidthPackageRemoveAccelerator', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def bandwidth_package_remove_accelerator_with_options_async(
        self,
        request: ga_20191120_models.BandwidthPackageRemoveAcceleratorRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.BandwidthPackageRemoveAcceleratorResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.BandwidthPackageRemoveAcceleratorResponse().from_map(
            await self.do_rpcrequest_async('BandwidthPackageRemoveAccelerator', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def bandwidth_package_remove_accelerator(
        self,
        request: ga_20191120_models.BandwidthPackageRemoveAcceleratorRequest,
    ) -> ga_20191120_models.BandwidthPackageRemoveAcceleratorResponse:
        runtime = util_models.RuntimeOptions()
        return self.bandwidth_package_remove_accelerator_with_options(request, runtime)

    async def bandwidth_package_remove_accelerator_async(
        self,
        request: ga_20191120_models.BandwidthPackageRemoveAcceleratorRequest,
    ) -> ga_20191120_models.BandwidthPackageRemoveAcceleratorResponse:
        runtime = util_models.RuntimeOptions()
        return await self.bandwidth_package_remove_accelerator_with_options_async(request, runtime)

    def config_endpoint_probe_with_options(
        self,
        request: ga_20191120_models.ConfigEndpointProbeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.ConfigEndpointProbeResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.ConfigEndpointProbeResponse().from_map(
            self.do_rpcrequest('ConfigEndpointProbe', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def config_endpoint_probe_with_options_async(
        self,
        request: ga_20191120_models.ConfigEndpointProbeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.ConfigEndpointProbeResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.ConfigEndpointProbeResponse().from_map(
            await self.do_rpcrequest_async('ConfigEndpointProbe', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def config_endpoint_probe(
        self,
        request: ga_20191120_models.ConfigEndpointProbeRequest,
    ) -> ga_20191120_models.ConfigEndpointProbeResponse:
        runtime = util_models.RuntimeOptions()
        return self.config_endpoint_probe_with_options(request, runtime)

    async def config_endpoint_probe_async(
        self,
        request: ga_20191120_models.ConfigEndpointProbeRequest,
    ) -> ga_20191120_models.ConfigEndpointProbeResponse:
        runtime = util_models.RuntimeOptions()
        return await self.config_endpoint_probe_with_options_async(request, runtime)

    def create_accelerator_with_options(
        self,
        request: ga_20191120_models.CreateAcceleratorRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.CreateAcceleratorResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.CreateAcceleratorResponse().from_map(
            self.do_rpcrequest('CreateAccelerator', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def create_accelerator_with_options_async(
        self,
        request: ga_20191120_models.CreateAcceleratorRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.CreateAcceleratorResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.CreateAcceleratorResponse().from_map(
            await self.do_rpcrequest_async('CreateAccelerator', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def create_accelerator(
        self,
        request: ga_20191120_models.CreateAcceleratorRequest,
    ) -> ga_20191120_models.CreateAcceleratorResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_accelerator_with_options(request, runtime)

    async def create_accelerator_async(
        self,
        request: ga_20191120_models.CreateAcceleratorRequest,
    ) -> ga_20191120_models.CreateAcceleratorResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_accelerator_with_options_async(request, runtime)

    def create_bandwidth_package_with_options(
        self,
        request: ga_20191120_models.CreateBandwidthPackageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.CreateBandwidthPackageResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.CreateBandwidthPackageResponse().from_map(
            self.do_rpcrequest('CreateBandwidthPackage', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def create_bandwidth_package_with_options_async(
        self,
        request: ga_20191120_models.CreateBandwidthPackageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.CreateBandwidthPackageResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.CreateBandwidthPackageResponse().from_map(
            await self.do_rpcrequest_async('CreateBandwidthPackage', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def create_bandwidth_package(
        self,
        request: ga_20191120_models.CreateBandwidthPackageRequest,
    ) -> ga_20191120_models.CreateBandwidthPackageResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_bandwidth_package_with_options(request, runtime)

    async def create_bandwidth_package_async(
        self,
        request: ga_20191120_models.CreateBandwidthPackageRequest,
    ) -> ga_20191120_models.CreateBandwidthPackageResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_bandwidth_package_with_options_async(request, runtime)

    def create_endpoint_group_with_options(
        self,
        request: ga_20191120_models.CreateEndpointGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.CreateEndpointGroupResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.CreateEndpointGroupResponse().from_map(
            self.do_rpcrequest('CreateEndpointGroup', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def create_endpoint_group_with_options_async(
        self,
        request: ga_20191120_models.CreateEndpointGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.CreateEndpointGroupResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.CreateEndpointGroupResponse().from_map(
            await self.do_rpcrequest_async('CreateEndpointGroup', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def create_endpoint_group(
        self,
        request: ga_20191120_models.CreateEndpointGroupRequest,
    ) -> ga_20191120_models.CreateEndpointGroupResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_endpoint_group_with_options(request, runtime)

    async def create_endpoint_group_async(
        self,
        request: ga_20191120_models.CreateEndpointGroupRequest,
    ) -> ga_20191120_models.CreateEndpointGroupResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_endpoint_group_with_options_async(request, runtime)

    def create_forwarding_rules_with_options(
        self,
        request: ga_20191120_models.CreateForwardingRulesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.CreateForwardingRulesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.CreateForwardingRulesResponse().from_map(
            self.do_rpcrequest('CreateForwardingRules', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def create_forwarding_rules_with_options_async(
        self,
        request: ga_20191120_models.CreateForwardingRulesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.CreateForwardingRulesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.CreateForwardingRulesResponse().from_map(
            await self.do_rpcrequest_async('CreateForwardingRules', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def create_forwarding_rules(
        self,
        request: ga_20191120_models.CreateForwardingRulesRequest,
    ) -> ga_20191120_models.CreateForwardingRulesResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_forwarding_rules_with_options(request, runtime)

    async def create_forwarding_rules_async(
        self,
        request: ga_20191120_models.CreateForwardingRulesRequest,
    ) -> ga_20191120_models.CreateForwardingRulesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_forwarding_rules_with_options_async(request, runtime)

    def create_ip_sets_with_options(
        self,
        request: ga_20191120_models.CreateIpSetsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.CreateIpSetsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.CreateIpSetsResponse().from_map(
            self.do_rpcrequest('CreateIpSets', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def create_ip_sets_with_options_async(
        self,
        request: ga_20191120_models.CreateIpSetsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.CreateIpSetsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.CreateIpSetsResponse().from_map(
            await self.do_rpcrequest_async('CreateIpSets', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def create_ip_sets(
        self,
        request: ga_20191120_models.CreateIpSetsRequest,
    ) -> ga_20191120_models.CreateIpSetsResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_ip_sets_with_options(request, runtime)

    async def create_ip_sets_async(
        self,
        request: ga_20191120_models.CreateIpSetsRequest,
    ) -> ga_20191120_models.CreateIpSetsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_ip_sets_with_options_async(request, runtime)

    def create_listener_with_options(
        self,
        request: ga_20191120_models.CreateListenerRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.CreateListenerResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.CreateListenerResponse().from_map(
            self.do_rpcrequest('CreateListener', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def create_listener_with_options_async(
        self,
        request: ga_20191120_models.CreateListenerRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.CreateListenerResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.CreateListenerResponse().from_map(
            await self.do_rpcrequest_async('CreateListener', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def create_listener(
        self,
        request: ga_20191120_models.CreateListenerRequest,
    ) -> ga_20191120_models.CreateListenerResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_listener_with_options(request, runtime)

    async def create_listener_async(
        self,
        request: ga_20191120_models.CreateListenerRequest,
    ) -> ga_20191120_models.CreateListenerResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_listener_with_options_async(request, runtime)

    def delete_accelerator_with_options(
        self,
        request: ga_20191120_models.DeleteAcceleratorRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.DeleteAcceleratorResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.DeleteAcceleratorResponse().from_map(
            self.do_rpcrequest('DeleteAccelerator', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def delete_accelerator_with_options_async(
        self,
        request: ga_20191120_models.DeleteAcceleratorRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.DeleteAcceleratorResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.DeleteAcceleratorResponse().from_map(
            await self.do_rpcrequest_async('DeleteAccelerator', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def delete_accelerator(
        self,
        request: ga_20191120_models.DeleteAcceleratorRequest,
    ) -> ga_20191120_models.DeleteAcceleratorResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_accelerator_with_options(request, runtime)

    async def delete_accelerator_async(
        self,
        request: ga_20191120_models.DeleteAcceleratorRequest,
    ) -> ga_20191120_models.DeleteAcceleratorResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_accelerator_with_options_async(request, runtime)

    def delete_bandwidth_package_with_options(
        self,
        request: ga_20191120_models.DeleteBandwidthPackageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.DeleteBandwidthPackageResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.DeleteBandwidthPackageResponse().from_map(
            self.do_rpcrequest('DeleteBandwidthPackage', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def delete_bandwidth_package_with_options_async(
        self,
        request: ga_20191120_models.DeleteBandwidthPackageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.DeleteBandwidthPackageResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.DeleteBandwidthPackageResponse().from_map(
            await self.do_rpcrequest_async('DeleteBandwidthPackage', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def delete_bandwidth_package(
        self,
        request: ga_20191120_models.DeleteBandwidthPackageRequest,
    ) -> ga_20191120_models.DeleteBandwidthPackageResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_bandwidth_package_with_options(request, runtime)

    async def delete_bandwidth_package_async(
        self,
        request: ga_20191120_models.DeleteBandwidthPackageRequest,
    ) -> ga_20191120_models.DeleteBandwidthPackageResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_bandwidth_package_with_options_async(request, runtime)

    def delete_endpoint_group_with_options(
        self,
        request: ga_20191120_models.DeleteEndpointGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.DeleteEndpointGroupResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.DeleteEndpointGroupResponse().from_map(
            self.do_rpcrequest('DeleteEndpointGroup', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def delete_endpoint_group_with_options_async(
        self,
        request: ga_20191120_models.DeleteEndpointGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.DeleteEndpointGroupResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.DeleteEndpointGroupResponse().from_map(
            await self.do_rpcrequest_async('DeleteEndpointGroup', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def delete_endpoint_group(
        self,
        request: ga_20191120_models.DeleteEndpointGroupRequest,
    ) -> ga_20191120_models.DeleteEndpointGroupResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_endpoint_group_with_options(request, runtime)

    async def delete_endpoint_group_async(
        self,
        request: ga_20191120_models.DeleteEndpointGroupRequest,
    ) -> ga_20191120_models.DeleteEndpointGroupResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_endpoint_group_with_options_async(request, runtime)

    def delete_forwarding_rules_with_options(
        self,
        request: ga_20191120_models.DeleteForwardingRulesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.DeleteForwardingRulesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.DeleteForwardingRulesResponse().from_map(
            self.do_rpcrequest('DeleteForwardingRules', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def delete_forwarding_rules_with_options_async(
        self,
        request: ga_20191120_models.DeleteForwardingRulesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.DeleteForwardingRulesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.DeleteForwardingRulesResponse().from_map(
            await self.do_rpcrequest_async('DeleteForwardingRules', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def delete_forwarding_rules(
        self,
        request: ga_20191120_models.DeleteForwardingRulesRequest,
    ) -> ga_20191120_models.DeleteForwardingRulesResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_forwarding_rules_with_options(request, runtime)

    async def delete_forwarding_rules_async(
        self,
        request: ga_20191120_models.DeleteForwardingRulesRequest,
    ) -> ga_20191120_models.DeleteForwardingRulesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_forwarding_rules_with_options_async(request, runtime)

    def delete_ip_set_with_options(
        self,
        request: ga_20191120_models.DeleteIpSetRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.DeleteIpSetResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.DeleteIpSetResponse().from_map(
            self.do_rpcrequest('DeleteIpSet', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def delete_ip_set_with_options_async(
        self,
        request: ga_20191120_models.DeleteIpSetRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.DeleteIpSetResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.DeleteIpSetResponse().from_map(
            await self.do_rpcrequest_async('DeleteIpSet', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def delete_ip_set(
        self,
        request: ga_20191120_models.DeleteIpSetRequest,
    ) -> ga_20191120_models.DeleteIpSetResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_ip_set_with_options(request, runtime)

    async def delete_ip_set_async(
        self,
        request: ga_20191120_models.DeleteIpSetRequest,
    ) -> ga_20191120_models.DeleteIpSetResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_ip_set_with_options_async(request, runtime)

    def delete_ip_sets_with_options(
        self,
        request: ga_20191120_models.DeleteIpSetsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.DeleteIpSetsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.DeleteIpSetsResponse().from_map(
            self.do_rpcrequest('DeleteIpSets', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def delete_ip_sets_with_options_async(
        self,
        request: ga_20191120_models.DeleteIpSetsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.DeleteIpSetsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.DeleteIpSetsResponse().from_map(
            await self.do_rpcrequest_async('DeleteIpSets', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def delete_ip_sets(
        self,
        request: ga_20191120_models.DeleteIpSetsRequest,
    ) -> ga_20191120_models.DeleteIpSetsResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_ip_sets_with_options(request, runtime)

    async def delete_ip_sets_async(
        self,
        request: ga_20191120_models.DeleteIpSetsRequest,
    ) -> ga_20191120_models.DeleteIpSetsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_ip_sets_with_options_async(request, runtime)

    def delete_listener_with_options(
        self,
        request: ga_20191120_models.DeleteListenerRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.DeleteListenerResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.DeleteListenerResponse().from_map(
            self.do_rpcrequest('DeleteListener', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def delete_listener_with_options_async(
        self,
        request: ga_20191120_models.DeleteListenerRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.DeleteListenerResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.DeleteListenerResponse().from_map(
            await self.do_rpcrequest_async('DeleteListener', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def delete_listener(
        self,
        request: ga_20191120_models.DeleteListenerRequest,
    ) -> ga_20191120_models.DeleteListenerResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_listener_with_options(request, runtime)

    async def delete_listener_async(
        self,
        request: ga_20191120_models.DeleteListenerRequest,
    ) -> ga_20191120_models.DeleteListenerResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_listener_with_options_async(request, runtime)

    def describe_accelerator_with_options(
        self,
        request: ga_20191120_models.DescribeAcceleratorRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.DescribeAcceleratorResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.DescribeAcceleratorResponse().from_map(
            self.do_rpcrequest('DescribeAccelerator', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_accelerator_with_options_async(
        self,
        request: ga_20191120_models.DescribeAcceleratorRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.DescribeAcceleratorResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.DescribeAcceleratorResponse().from_map(
            await self.do_rpcrequest_async('DescribeAccelerator', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_accelerator(
        self,
        request: ga_20191120_models.DescribeAcceleratorRequest,
    ) -> ga_20191120_models.DescribeAcceleratorResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_accelerator_with_options(request, runtime)

    async def describe_accelerator_async(
        self,
        request: ga_20191120_models.DescribeAcceleratorRequest,
    ) -> ga_20191120_models.DescribeAcceleratorResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_accelerator_with_options_async(request, runtime)

    def describe_bandwidth_package_with_options(
        self,
        request: ga_20191120_models.DescribeBandwidthPackageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.DescribeBandwidthPackageResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.DescribeBandwidthPackageResponse().from_map(
            self.do_rpcrequest('DescribeBandwidthPackage', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_bandwidth_package_with_options_async(
        self,
        request: ga_20191120_models.DescribeBandwidthPackageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.DescribeBandwidthPackageResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.DescribeBandwidthPackageResponse().from_map(
            await self.do_rpcrequest_async('DescribeBandwidthPackage', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_bandwidth_package(
        self,
        request: ga_20191120_models.DescribeBandwidthPackageRequest,
    ) -> ga_20191120_models.DescribeBandwidthPackageResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_bandwidth_package_with_options(request, runtime)

    async def describe_bandwidth_package_async(
        self,
        request: ga_20191120_models.DescribeBandwidthPackageRequest,
    ) -> ga_20191120_models.DescribeBandwidthPackageResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_bandwidth_package_with_options_async(request, runtime)

    def describe_endpoint_group_with_options(
        self,
        request: ga_20191120_models.DescribeEndpointGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.DescribeEndpointGroupResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.DescribeEndpointGroupResponse().from_map(
            self.do_rpcrequest('DescribeEndpointGroup', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_endpoint_group_with_options_async(
        self,
        request: ga_20191120_models.DescribeEndpointGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.DescribeEndpointGroupResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.DescribeEndpointGroupResponse().from_map(
            await self.do_rpcrequest_async('DescribeEndpointGroup', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_endpoint_group(
        self,
        request: ga_20191120_models.DescribeEndpointGroupRequest,
    ) -> ga_20191120_models.DescribeEndpointGroupResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_endpoint_group_with_options(request, runtime)

    async def describe_endpoint_group_async(
        self,
        request: ga_20191120_models.DescribeEndpointGroupRequest,
    ) -> ga_20191120_models.DescribeEndpointGroupResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_endpoint_group_with_options_async(request, runtime)

    def describe_ip_set_with_options(
        self,
        request: ga_20191120_models.DescribeIpSetRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.DescribeIpSetResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.DescribeIpSetResponse().from_map(
            self.do_rpcrequest('DescribeIpSet', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_ip_set_with_options_async(
        self,
        request: ga_20191120_models.DescribeIpSetRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.DescribeIpSetResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.DescribeIpSetResponse().from_map(
            await self.do_rpcrequest_async('DescribeIpSet', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_ip_set(
        self,
        request: ga_20191120_models.DescribeIpSetRequest,
    ) -> ga_20191120_models.DescribeIpSetResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_ip_set_with_options(request, runtime)

    async def describe_ip_set_async(
        self,
        request: ga_20191120_models.DescribeIpSetRequest,
    ) -> ga_20191120_models.DescribeIpSetResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_ip_set_with_options_async(request, runtime)

    def describe_listener_with_options(
        self,
        request: ga_20191120_models.DescribeListenerRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.DescribeListenerResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.DescribeListenerResponse().from_map(
            self.do_rpcrequest('DescribeListener', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_listener_with_options_async(
        self,
        request: ga_20191120_models.DescribeListenerRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.DescribeListenerResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.DescribeListenerResponse().from_map(
            await self.do_rpcrequest_async('DescribeListener', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_listener(
        self,
        request: ga_20191120_models.DescribeListenerRequest,
    ) -> ga_20191120_models.DescribeListenerResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_listener_with_options(request, runtime)

    async def describe_listener_async(
        self,
        request: ga_20191120_models.DescribeListenerRequest,
    ) -> ga_20191120_models.DescribeListenerResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_listener_with_options_async(request, runtime)

    def describe_regions_with_options(
        self,
        request: ga_20191120_models.DescribeRegionsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.DescribeRegionsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.DescribeRegionsResponse().from_map(
            self.do_rpcrequest('DescribeRegions', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_regions_with_options_async(
        self,
        request: ga_20191120_models.DescribeRegionsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.DescribeRegionsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.DescribeRegionsResponse().from_map(
            await self.do_rpcrequest_async('DescribeRegions', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_regions(
        self,
        request: ga_20191120_models.DescribeRegionsRequest,
    ) -> ga_20191120_models.DescribeRegionsResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_regions_with_options(request, runtime)

    async def describe_regions_async(
        self,
        request: ga_20191120_models.DescribeRegionsRequest,
    ) -> ga_20191120_models.DescribeRegionsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_regions_with_options_async(request, runtime)

    def detach_ddos_from_accelerator_with_options(
        self,
        request: ga_20191120_models.DetachDdosFromAcceleratorRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.DetachDdosFromAcceleratorResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.DetachDdosFromAcceleratorResponse().from_map(
            self.do_rpcrequest('DetachDdosFromAccelerator', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def detach_ddos_from_accelerator_with_options_async(
        self,
        request: ga_20191120_models.DetachDdosFromAcceleratorRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.DetachDdosFromAcceleratorResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.DetachDdosFromAcceleratorResponse().from_map(
            await self.do_rpcrequest_async('DetachDdosFromAccelerator', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def detach_ddos_from_accelerator(
        self,
        request: ga_20191120_models.DetachDdosFromAcceleratorRequest,
    ) -> ga_20191120_models.DetachDdosFromAcceleratorResponse:
        runtime = util_models.RuntimeOptions()
        return self.detach_ddos_from_accelerator_with_options(request, runtime)

    async def detach_ddos_from_accelerator_async(
        self,
        request: ga_20191120_models.DetachDdosFromAcceleratorRequest,
    ) -> ga_20191120_models.DetachDdosFromAcceleratorResponse:
        runtime = util_models.RuntimeOptions()
        return await self.detach_ddos_from_accelerator_with_options_async(request, runtime)

    def list_accelerate_areas_with_options(
        self,
        request: ga_20191120_models.ListAccelerateAreasRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.ListAccelerateAreasResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.ListAccelerateAreasResponse().from_map(
            self.do_rpcrequest('ListAccelerateAreas', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def list_accelerate_areas_with_options_async(
        self,
        request: ga_20191120_models.ListAccelerateAreasRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.ListAccelerateAreasResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.ListAccelerateAreasResponse().from_map(
            await self.do_rpcrequest_async('ListAccelerateAreas', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def list_accelerate_areas(
        self,
        request: ga_20191120_models.ListAccelerateAreasRequest,
    ) -> ga_20191120_models.ListAccelerateAreasResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_accelerate_areas_with_options(request, runtime)

    async def list_accelerate_areas_async(
        self,
        request: ga_20191120_models.ListAccelerateAreasRequest,
    ) -> ga_20191120_models.ListAccelerateAreasResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_accelerate_areas_with_options_async(request, runtime)

    def list_accelerators_with_options(
        self,
        request: ga_20191120_models.ListAcceleratorsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.ListAcceleratorsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.ListAcceleratorsResponse().from_map(
            self.do_rpcrequest('ListAccelerators', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def list_accelerators_with_options_async(
        self,
        request: ga_20191120_models.ListAcceleratorsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.ListAcceleratorsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.ListAcceleratorsResponse().from_map(
            await self.do_rpcrequest_async('ListAccelerators', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def list_accelerators(
        self,
        request: ga_20191120_models.ListAcceleratorsRequest,
    ) -> ga_20191120_models.ListAcceleratorsResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_accelerators_with_options(request, runtime)

    async def list_accelerators_async(
        self,
        request: ga_20191120_models.ListAcceleratorsRequest,
    ) -> ga_20191120_models.ListAcceleratorsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_accelerators_with_options_async(request, runtime)

    def list_available_accelerate_areas_with_options(
        self,
        request: ga_20191120_models.ListAvailableAccelerateAreasRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.ListAvailableAccelerateAreasResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.ListAvailableAccelerateAreasResponse().from_map(
            self.do_rpcrequest('ListAvailableAccelerateAreas', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def list_available_accelerate_areas_with_options_async(
        self,
        request: ga_20191120_models.ListAvailableAccelerateAreasRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.ListAvailableAccelerateAreasResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.ListAvailableAccelerateAreasResponse().from_map(
            await self.do_rpcrequest_async('ListAvailableAccelerateAreas', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def list_available_accelerate_areas(
        self,
        request: ga_20191120_models.ListAvailableAccelerateAreasRequest,
    ) -> ga_20191120_models.ListAvailableAccelerateAreasResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_available_accelerate_areas_with_options(request, runtime)

    async def list_available_accelerate_areas_async(
        self,
        request: ga_20191120_models.ListAvailableAccelerateAreasRequest,
    ) -> ga_20191120_models.ListAvailableAccelerateAreasResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_available_accelerate_areas_with_options_async(request, runtime)

    def list_available_busi_regions_with_options(
        self,
        request: ga_20191120_models.ListAvailableBusiRegionsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.ListAvailableBusiRegionsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.ListAvailableBusiRegionsResponse().from_map(
            self.do_rpcrequest('ListAvailableBusiRegions', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def list_available_busi_regions_with_options_async(
        self,
        request: ga_20191120_models.ListAvailableBusiRegionsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.ListAvailableBusiRegionsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.ListAvailableBusiRegionsResponse().from_map(
            await self.do_rpcrequest_async('ListAvailableBusiRegions', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def list_available_busi_regions(
        self,
        request: ga_20191120_models.ListAvailableBusiRegionsRequest,
    ) -> ga_20191120_models.ListAvailableBusiRegionsResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_available_busi_regions_with_options(request, runtime)

    async def list_available_busi_regions_async(
        self,
        request: ga_20191120_models.ListAvailableBusiRegionsRequest,
    ) -> ga_20191120_models.ListAvailableBusiRegionsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_available_busi_regions_with_options_async(request, runtime)

    def list_bandwidthackages_with_options(
        self,
        request: ga_20191120_models.ListBandwidthackagesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.ListBandwidthackagesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.ListBandwidthackagesResponse().from_map(
            self.do_rpcrequest('ListBandwidthackages', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def list_bandwidthackages_with_options_async(
        self,
        request: ga_20191120_models.ListBandwidthackagesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.ListBandwidthackagesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.ListBandwidthackagesResponse().from_map(
            await self.do_rpcrequest_async('ListBandwidthackages', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def list_bandwidthackages(
        self,
        request: ga_20191120_models.ListBandwidthackagesRequest,
    ) -> ga_20191120_models.ListBandwidthackagesResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_bandwidthackages_with_options(request, runtime)

    async def list_bandwidthackages_async(
        self,
        request: ga_20191120_models.ListBandwidthackagesRequest,
    ) -> ga_20191120_models.ListBandwidthackagesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_bandwidthackages_with_options_async(request, runtime)

    def list_bandwidth_packages_with_options(
        self,
        request: ga_20191120_models.ListBandwidthPackagesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.ListBandwidthPackagesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.ListBandwidthPackagesResponse().from_map(
            self.do_rpcrequest('ListBandwidthPackages', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def list_bandwidth_packages_with_options_async(
        self,
        request: ga_20191120_models.ListBandwidthPackagesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.ListBandwidthPackagesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.ListBandwidthPackagesResponse().from_map(
            await self.do_rpcrequest_async('ListBandwidthPackages', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def list_bandwidth_packages(
        self,
        request: ga_20191120_models.ListBandwidthPackagesRequest,
    ) -> ga_20191120_models.ListBandwidthPackagesResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_bandwidth_packages_with_options(request, runtime)

    async def list_bandwidth_packages_async(
        self,
        request: ga_20191120_models.ListBandwidthPackagesRequest,
    ) -> ga_20191120_models.ListBandwidthPackagesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_bandwidth_packages_with_options_async(request, runtime)

    def list_busi_regions_with_options(
        self,
        request: ga_20191120_models.ListBusiRegionsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.ListBusiRegionsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.ListBusiRegionsResponse().from_map(
            self.do_rpcrequest('ListBusiRegions', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def list_busi_regions_with_options_async(
        self,
        request: ga_20191120_models.ListBusiRegionsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.ListBusiRegionsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.ListBusiRegionsResponse().from_map(
            await self.do_rpcrequest_async('ListBusiRegions', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def list_busi_regions(
        self,
        request: ga_20191120_models.ListBusiRegionsRequest,
    ) -> ga_20191120_models.ListBusiRegionsResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_busi_regions_with_options(request, runtime)

    async def list_busi_regions_async(
        self,
        request: ga_20191120_models.ListBusiRegionsRequest,
    ) -> ga_20191120_models.ListBusiRegionsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_busi_regions_with_options_async(request, runtime)

    def list_endpoint_groups_with_options(
        self,
        request: ga_20191120_models.ListEndpointGroupsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.ListEndpointGroupsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.ListEndpointGroupsResponse().from_map(
            self.do_rpcrequest('ListEndpointGroups', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def list_endpoint_groups_with_options_async(
        self,
        request: ga_20191120_models.ListEndpointGroupsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.ListEndpointGroupsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.ListEndpointGroupsResponse().from_map(
            await self.do_rpcrequest_async('ListEndpointGroups', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def list_endpoint_groups(
        self,
        request: ga_20191120_models.ListEndpointGroupsRequest,
    ) -> ga_20191120_models.ListEndpointGroupsResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_endpoint_groups_with_options(request, runtime)

    async def list_endpoint_groups_async(
        self,
        request: ga_20191120_models.ListEndpointGroupsRequest,
    ) -> ga_20191120_models.ListEndpointGroupsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_endpoint_groups_with_options_async(request, runtime)

    def list_forwarding_rules_with_options(
        self,
        request: ga_20191120_models.ListForwardingRulesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.ListForwardingRulesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.ListForwardingRulesResponse().from_map(
            self.do_rpcrequest('ListForwardingRules', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def list_forwarding_rules_with_options_async(
        self,
        request: ga_20191120_models.ListForwardingRulesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.ListForwardingRulesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.ListForwardingRulesResponse().from_map(
            await self.do_rpcrequest_async('ListForwardingRules', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def list_forwarding_rules(
        self,
        request: ga_20191120_models.ListForwardingRulesRequest,
    ) -> ga_20191120_models.ListForwardingRulesResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_forwarding_rules_with_options(request, runtime)

    async def list_forwarding_rules_async(
        self,
        request: ga_20191120_models.ListForwardingRulesRequest,
    ) -> ga_20191120_models.ListForwardingRulesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_forwarding_rules_with_options_async(request, runtime)

    def list_ip_sets_with_options(
        self,
        request: ga_20191120_models.ListIpSetsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.ListIpSetsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.ListIpSetsResponse().from_map(
            self.do_rpcrequest('ListIpSets', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def list_ip_sets_with_options_async(
        self,
        request: ga_20191120_models.ListIpSetsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.ListIpSetsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.ListIpSetsResponse().from_map(
            await self.do_rpcrequest_async('ListIpSets', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def list_ip_sets(
        self,
        request: ga_20191120_models.ListIpSetsRequest,
    ) -> ga_20191120_models.ListIpSetsResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_ip_sets_with_options(request, runtime)

    async def list_ip_sets_async(
        self,
        request: ga_20191120_models.ListIpSetsRequest,
    ) -> ga_20191120_models.ListIpSetsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_ip_sets_with_options_async(request, runtime)

    def list_listeners_with_options(
        self,
        request: ga_20191120_models.ListListenersRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.ListListenersResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.ListListenersResponse().from_map(
            self.do_rpcrequest('ListListeners', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def list_listeners_with_options_async(
        self,
        request: ga_20191120_models.ListListenersRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.ListListenersResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.ListListenersResponse().from_map(
            await self.do_rpcrequest_async('ListListeners', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def list_listeners(
        self,
        request: ga_20191120_models.ListListenersRequest,
    ) -> ga_20191120_models.ListListenersResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_listeners_with_options(request, runtime)

    async def list_listeners_async(
        self,
        request: ga_20191120_models.ListListenersRequest,
    ) -> ga_20191120_models.ListListenersResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_listeners_with_options_async(request, runtime)

    def replace_bandwidth_package_with_options(
        self,
        request: ga_20191120_models.ReplaceBandwidthPackageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.ReplaceBandwidthPackageResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.ReplaceBandwidthPackageResponse().from_map(
            self.do_rpcrequest('ReplaceBandwidthPackage', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def replace_bandwidth_package_with_options_async(
        self,
        request: ga_20191120_models.ReplaceBandwidthPackageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.ReplaceBandwidthPackageResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.ReplaceBandwidthPackageResponse().from_map(
            await self.do_rpcrequest_async('ReplaceBandwidthPackage', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def replace_bandwidth_package(
        self,
        request: ga_20191120_models.ReplaceBandwidthPackageRequest,
    ) -> ga_20191120_models.ReplaceBandwidthPackageResponse:
        runtime = util_models.RuntimeOptions()
        return self.replace_bandwidth_package_with_options(request, runtime)

    async def replace_bandwidth_package_async(
        self,
        request: ga_20191120_models.ReplaceBandwidthPackageRequest,
    ) -> ga_20191120_models.ReplaceBandwidthPackageResponse:
        runtime = util_models.RuntimeOptions()
        return await self.replace_bandwidth_package_with_options_async(request, runtime)

    def update_accelerator_with_options(
        self,
        request: ga_20191120_models.UpdateAcceleratorRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.UpdateAcceleratorResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.UpdateAcceleratorResponse().from_map(
            self.do_rpcrequest('UpdateAccelerator', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def update_accelerator_with_options_async(
        self,
        request: ga_20191120_models.UpdateAcceleratorRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.UpdateAcceleratorResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.UpdateAcceleratorResponse().from_map(
            await self.do_rpcrequest_async('UpdateAccelerator', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def update_accelerator(
        self,
        request: ga_20191120_models.UpdateAcceleratorRequest,
    ) -> ga_20191120_models.UpdateAcceleratorResponse:
        runtime = util_models.RuntimeOptions()
        return self.update_accelerator_with_options(request, runtime)

    async def update_accelerator_async(
        self,
        request: ga_20191120_models.UpdateAcceleratorRequest,
    ) -> ga_20191120_models.UpdateAcceleratorResponse:
        runtime = util_models.RuntimeOptions()
        return await self.update_accelerator_with_options_async(request, runtime)

    def update_bandwidth_package_with_options(
        self,
        request: ga_20191120_models.UpdateBandwidthPackageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.UpdateBandwidthPackageResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.UpdateBandwidthPackageResponse().from_map(
            self.do_rpcrequest('UpdateBandwidthPackage', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def update_bandwidth_package_with_options_async(
        self,
        request: ga_20191120_models.UpdateBandwidthPackageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.UpdateBandwidthPackageResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.UpdateBandwidthPackageResponse().from_map(
            await self.do_rpcrequest_async('UpdateBandwidthPackage', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def update_bandwidth_package(
        self,
        request: ga_20191120_models.UpdateBandwidthPackageRequest,
    ) -> ga_20191120_models.UpdateBandwidthPackageResponse:
        runtime = util_models.RuntimeOptions()
        return self.update_bandwidth_package_with_options(request, runtime)

    async def update_bandwidth_package_async(
        self,
        request: ga_20191120_models.UpdateBandwidthPackageRequest,
    ) -> ga_20191120_models.UpdateBandwidthPackageResponse:
        runtime = util_models.RuntimeOptions()
        return await self.update_bandwidth_package_with_options_async(request, runtime)

    def update_endpoint_group_with_options(
        self,
        request: ga_20191120_models.UpdateEndpointGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.UpdateEndpointGroupResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.UpdateEndpointGroupResponse().from_map(
            self.do_rpcrequest('UpdateEndpointGroup', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def update_endpoint_group_with_options_async(
        self,
        request: ga_20191120_models.UpdateEndpointGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.UpdateEndpointGroupResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.UpdateEndpointGroupResponse().from_map(
            await self.do_rpcrequest_async('UpdateEndpointGroup', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def update_endpoint_group(
        self,
        request: ga_20191120_models.UpdateEndpointGroupRequest,
    ) -> ga_20191120_models.UpdateEndpointGroupResponse:
        runtime = util_models.RuntimeOptions()
        return self.update_endpoint_group_with_options(request, runtime)

    async def update_endpoint_group_async(
        self,
        request: ga_20191120_models.UpdateEndpointGroupRequest,
    ) -> ga_20191120_models.UpdateEndpointGroupResponse:
        runtime = util_models.RuntimeOptions()
        return await self.update_endpoint_group_with_options_async(request, runtime)

    def update_endpoint_group_attribute_with_options(
        self,
        request: ga_20191120_models.UpdateEndpointGroupAttributeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.UpdateEndpointGroupAttributeResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.UpdateEndpointGroupAttributeResponse().from_map(
            self.do_rpcrequest('UpdateEndpointGroupAttribute', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def update_endpoint_group_attribute_with_options_async(
        self,
        request: ga_20191120_models.UpdateEndpointGroupAttributeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.UpdateEndpointGroupAttributeResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.UpdateEndpointGroupAttributeResponse().from_map(
            await self.do_rpcrequest_async('UpdateEndpointGroupAttribute', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def update_endpoint_group_attribute(
        self,
        request: ga_20191120_models.UpdateEndpointGroupAttributeRequest,
    ) -> ga_20191120_models.UpdateEndpointGroupAttributeResponse:
        runtime = util_models.RuntimeOptions()
        return self.update_endpoint_group_attribute_with_options(request, runtime)

    async def update_endpoint_group_attribute_async(
        self,
        request: ga_20191120_models.UpdateEndpointGroupAttributeRequest,
    ) -> ga_20191120_models.UpdateEndpointGroupAttributeResponse:
        runtime = util_models.RuntimeOptions()
        return await self.update_endpoint_group_attribute_with_options_async(request, runtime)

    def update_forwarding_rules_with_options(
        self,
        request: ga_20191120_models.UpdateForwardingRulesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.UpdateForwardingRulesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.UpdateForwardingRulesResponse().from_map(
            self.do_rpcrequest('UpdateForwardingRules', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def update_forwarding_rules_with_options_async(
        self,
        request: ga_20191120_models.UpdateForwardingRulesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.UpdateForwardingRulesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.UpdateForwardingRulesResponse().from_map(
            await self.do_rpcrequest_async('UpdateForwardingRules', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def update_forwarding_rules(
        self,
        request: ga_20191120_models.UpdateForwardingRulesRequest,
    ) -> ga_20191120_models.UpdateForwardingRulesResponse:
        runtime = util_models.RuntimeOptions()
        return self.update_forwarding_rules_with_options(request, runtime)

    async def update_forwarding_rules_async(
        self,
        request: ga_20191120_models.UpdateForwardingRulesRequest,
    ) -> ga_20191120_models.UpdateForwardingRulesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.update_forwarding_rules_with_options_async(request, runtime)

    def update_ip_set_with_options(
        self,
        request: ga_20191120_models.UpdateIpSetRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.UpdateIpSetResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.UpdateIpSetResponse().from_map(
            self.do_rpcrequest('UpdateIpSet', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def update_ip_set_with_options_async(
        self,
        request: ga_20191120_models.UpdateIpSetRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.UpdateIpSetResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.UpdateIpSetResponse().from_map(
            await self.do_rpcrequest_async('UpdateIpSet', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def update_ip_set(
        self,
        request: ga_20191120_models.UpdateIpSetRequest,
    ) -> ga_20191120_models.UpdateIpSetResponse:
        runtime = util_models.RuntimeOptions()
        return self.update_ip_set_with_options(request, runtime)

    async def update_ip_set_async(
        self,
        request: ga_20191120_models.UpdateIpSetRequest,
    ) -> ga_20191120_models.UpdateIpSetResponse:
        runtime = util_models.RuntimeOptions()
        return await self.update_ip_set_with_options_async(request, runtime)

    def update_ip_sets_with_options(
        self,
        request: ga_20191120_models.UpdateIpSetsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.UpdateIpSetsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.UpdateIpSetsResponse().from_map(
            self.do_rpcrequest('UpdateIpSets', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def update_ip_sets_with_options_async(
        self,
        request: ga_20191120_models.UpdateIpSetsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.UpdateIpSetsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.UpdateIpSetsResponse().from_map(
            await self.do_rpcrequest_async('UpdateIpSets', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def update_ip_sets(
        self,
        request: ga_20191120_models.UpdateIpSetsRequest,
    ) -> ga_20191120_models.UpdateIpSetsResponse:
        runtime = util_models.RuntimeOptions()
        return self.update_ip_sets_with_options(request, runtime)

    async def update_ip_sets_async(
        self,
        request: ga_20191120_models.UpdateIpSetsRequest,
    ) -> ga_20191120_models.UpdateIpSetsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.update_ip_sets_with_options_async(request, runtime)

    def update_listener_with_options(
        self,
        request: ga_20191120_models.UpdateListenerRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.UpdateListenerResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.UpdateListenerResponse().from_map(
            self.do_rpcrequest('UpdateListener', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def update_listener_with_options_async(
        self,
        request: ga_20191120_models.UpdateListenerRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ga_20191120_models.UpdateListenerResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ga_20191120_models.UpdateListenerResponse().from_map(
            await self.do_rpcrequest_async('UpdateListener', '2019-11-20', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def update_listener(
        self,
        request: ga_20191120_models.UpdateListenerRequest,
    ) -> ga_20191120_models.UpdateListenerResponse:
        runtime = util_models.RuntimeOptions()
        return self.update_listener_with_options(request, runtime)

    async def update_listener_async(
        self,
        request: ga_20191120_models.UpdateListenerRequest,
    ) -> ga_20191120_models.UpdateListenerResponse:
        runtime = util_models.RuntimeOptions()
        return await self.update_listener_with_options_async(request, runtime)
