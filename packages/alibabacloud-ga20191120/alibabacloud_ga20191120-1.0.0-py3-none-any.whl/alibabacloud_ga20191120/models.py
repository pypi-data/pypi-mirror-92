# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel
from typing import Dict, List


class AttachDdosToAcceleratorRequest(TeaModel):
    def __init__(
        self,
        accelerator_id: str = None,
        ddos_id: str = None,
        ddos_region_id: str = None,
        region_id: str = None,
    ):
        self.accelerator_id = accelerator_id
        self.ddos_id = ddos_id
        self.ddos_region_id = ddos_region_id
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.accelerator_id is not None:
            result['AcceleratorId'] = self.accelerator_id
        if self.ddos_id is not None:
            result['DdosId'] = self.ddos_id
        if self.ddos_region_id is not None:
            result['DdosRegionId'] = self.ddos_region_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AcceleratorId') is not None:
            self.accelerator_id = m.get('AcceleratorId')
        if m.get('DdosId') is not None:
            self.ddos_id = m.get('DdosId')
        if m.get('DdosRegionId') is not None:
            self.ddos_region_id = m.get('DdosRegionId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class AttachDdosToAcceleratorResponseBody(TeaModel):
    def __init__(
        self,
        ddos_id: str = None,
        request_id: str = None,
        ga_id: str = None,
    ):
        self.ddos_id = ddos_id
        self.request_id = request_id
        self.ga_id = ga_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.ddos_id is not None:
            result['DdosId'] = self.ddos_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.ga_id is not None:
            result['GaId'] = self.ga_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DdosId') is not None:
            self.ddos_id = m.get('DdosId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('GaId') is not None:
            self.ga_id = m.get('GaId')
        return self


class AttachDdosToAcceleratorResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: AttachDdosToAcceleratorResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = AttachDdosToAcceleratorResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class BandwidthPackageAddAcceleratorRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        bandwidth_package_id: str = None,
        accelerator_id: str = None,
    ):
        self.region_id = region_id
        self.bandwidth_package_id = bandwidth_package_id
        self.accelerator_id = accelerator_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.bandwidth_package_id is not None:
            result['BandwidthPackageId'] = self.bandwidth_package_id
        if self.accelerator_id is not None:
            result['AcceleratorId'] = self.accelerator_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('BandwidthPackageId') is not None:
            self.bandwidth_package_id = m.get('BandwidthPackageId')
        if m.get('AcceleratorId') is not None:
            self.accelerator_id = m.get('AcceleratorId')
        return self


class BandwidthPackageAddAcceleratorResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        accelerators: List[str] = None,
        bandwidth_package_id: str = None,
    ):
        self.request_id = request_id
        self.accelerators = accelerators
        self.bandwidth_package_id = bandwidth_package_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.accelerators is not None:
            result['Accelerators'] = self.accelerators
        if self.bandwidth_package_id is not None:
            result['BandwidthPackageId'] = self.bandwidth_package_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Accelerators') is not None:
            self.accelerators = m.get('Accelerators')
        if m.get('BandwidthPackageId') is not None:
            self.bandwidth_package_id = m.get('BandwidthPackageId')
        return self


class BandwidthPackageAddAcceleratorResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: BandwidthPackageAddAcceleratorResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = BandwidthPackageAddAcceleratorResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class BandwidthPackageRemoveAcceleratorRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        bandwidth_package_id: str = None,
        accelerator_id: str = None,
    ):
        self.region_id = region_id
        self.bandwidth_package_id = bandwidth_package_id
        self.accelerator_id = accelerator_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.bandwidth_package_id is not None:
            result['BandwidthPackageId'] = self.bandwidth_package_id
        if self.accelerator_id is not None:
            result['AcceleratorId'] = self.accelerator_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('BandwidthPackageId') is not None:
            self.bandwidth_package_id = m.get('BandwidthPackageId')
        if m.get('AcceleratorId') is not None:
            self.accelerator_id = m.get('AcceleratorId')
        return self


class BandwidthPackageRemoveAcceleratorResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        accelerators: List[str] = None,
        bandwidth_package_id: str = None,
    ):
        self.request_id = request_id
        self.accelerators = accelerators
        self.bandwidth_package_id = bandwidth_package_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.accelerators is not None:
            result['Accelerators'] = self.accelerators
        if self.bandwidth_package_id is not None:
            result['BandwidthPackageId'] = self.bandwidth_package_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Accelerators') is not None:
            self.accelerators = m.get('Accelerators')
        if m.get('BandwidthPackageId') is not None:
            self.bandwidth_package_id = m.get('BandwidthPackageId')
        return self


class BandwidthPackageRemoveAcceleratorResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: BandwidthPackageRemoveAcceleratorResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = BandwidthPackageRemoveAcceleratorResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ConfigEndpointProbeRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        client_token: str = None,
        endpoint_group_id: str = None,
        endpoint_type: str = None,
        endpoint: str = None,
        probe_protocol: str = None,
        probe_port: str = None,
        enable: str = None,
    ):
        self.region_id = region_id
        self.client_token = client_token
        self.endpoint_group_id = endpoint_group_id
        self.endpoint_type = endpoint_type
        self.endpoint = endpoint
        self.probe_protocol = probe_protocol
        self.probe_port = probe_port
        self.enable = enable

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.endpoint_group_id is not None:
            result['EndpointGroupId'] = self.endpoint_group_id
        if self.endpoint_type is not None:
            result['EndpointType'] = self.endpoint_type
        if self.endpoint is not None:
            result['Endpoint'] = self.endpoint
        if self.probe_protocol is not None:
            result['ProbeProtocol'] = self.probe_protocol
        if self.probe_port is not None:
            result['ProbePort'] = self.probe_port
        if self.enable is not None:
            result['Enable'] = self.enable
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('EndpointGroupId') is not None:
            self.endpoint_group_id = m.get('EndpointGroupId')
        if m.get('EndpointType') is not None:
            self.endpoint_type = m.get('EndpointType')
        if m.get('Endpoint') is not None:
            self.endpoint = m.get('Endpoint')
        if m.get('ProbeProtocol') is not None:
            self.probe_protocol = m.get('ProbeProtocol')
        if m.get('ProbePort') is not None:
            self.probe_port = m.get('ProbePort')
        if m.get('Enable') is not None:
            self.enable = m.get('Enable')
        return self


class ConfigEndpointProbeResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ConfigEndpointProbeResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ConfigEndpointProbeResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ConfigEndpointProbeResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateAcceleratorRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        client_token: str = None,
        name: str = None,
        duration: int = None,
        pricing_cycle: str = None,
        spec: str = None,
        auto_pay: bool = None,
        auto_use_coupon: str = None,
        promotion_option_no: str = None,
    ):
        self.region_id = region_id
        self.client_token = client_token
        self.name = name
        self.duration = duration
        self.pricing_cycle = pricing_cycle
        self.spec = spec
        self.auto_pay = auto_pay
        self.auto_use_coupon = auto_use_coupon
        self.promotion_option_no = promotion_option_no

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.name is not None:
            result['Name'] = self.name
        if self.duration is not None:
            result['Duration'] = self.duration
        if self.pricing_cycle is not None:
            result['PricingCycle'] = self.pricing_cycle
        if self.spec is not None:
            result['Spec'] = self.spec
        if self.auto_pay is not None:
            result['AutoPay'] = self.auto_pay
        if self.auto_use_coupon is not None:
            result['AutoUseCoupon'] = self.auto_use_coupon
        if self.promotion_option_no is not None:
            result['PromotionOptionNo'] = self.promotion_option_no
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Duration') is not None:
            self.duration = m.get('Duration')
        if m.get('PricingCycle') is not None:
            self.pricing_cycle = m.get('PricingCycle')
        if m.get('Spec') is not None:
            self.spec = m.get('Spec')
        if m.get('AutoPay') is not None:
            self.auto_pay = m.get('AutoPay')
        if m.get('AutoUseCoupon') is not None:
            self.auto_use_coupon = m.get('AutoUseCoupon')
        if m.get('PromotionOptionNo') is not None:
            self.promotion_option_no = m.get('PromotionOptionNo')
        return self


class CreateAcceleratorResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        order_id: str = None,
        accelerator_id: str = None,
    ):
        self.request_id = request_id
        self.order_id = order_id
        self.accelerator_id = accelerator_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.order_id is not None:
            result['OrderId'] = self.order_id
        if self.accelerator_id is not None:
            result['AcceleratorId'] = self.accelerator_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('OrderId') is not None:
            self.order_id = m.get('OrderId')
        if m.get('AcceleratorId') is not None:
            self.accelerator_id = m.get('AcceleratorId')
        return self


class CreateAcceleratorResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateAcceleratorResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateAcceleratorResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateBandwidthPackageRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        bandwidth: int = None,
        duration: str = None,
        pricing_cycle: str = None,
        auto_pay: bool = None,
        client_token: str = None,
        type: str = None,
        bandwidth_type: str = None,
        auto_use_coupon: str = None,
        ratio: int = None,
        billing_type: str = None,
        charge_type: str = None,
        cbn_geographic_region_id_a: str = None,
        cbn_geographic_region_id_b: str = None,
        promotion_option_no: str = None,
    ):
        self.region_id = region_id
        self.bandwidth = bandwidth
        self.duration = duration
        self.pricing_cycle = pricing_cycle
        self.auto_pay = auto_pay
        self.client_token = client_token
        self.type = type
        self.bandwidth_type = bandwidth_type
        self.auto_use_coupon = auto_use_coupon
        self.ratio = ratio
        self.billing_type = billing_type
        self.charge_type = charge_type
        self.cbn_geographic_region_id_a = cbn_geographic_region_id_a
        self.cbn_geographic_region_id_b = cbn_geographic_region_id_b
        self.promotion_option_no = promotion_option_no

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.bandwidth is not None:
            result['Bandwidth'] = self.bandwidth
        if self.duration is not None:
            result['Duration'] = self.duration
        if self.pricing_cycle is not None:
            result['PricingCycle'] = self.pricing_cycle
        if self.auto_pay is not None:
            result['AutoPay'] = self.auto_pay
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.type is not None:
            result['Type'] = self.type
        if self.bandwidth_type is not None:
            result['BandwidthType'] = self.bandwidth_type
        if self.auto_use_coupon is not None:
            result['AutoUseCoupon'] = self.auto_use_coupon
        if self.ratio is not None:
            result['Ratio'] = self.ratio
        if self.billing_type is not None:
            result['BillingType'] = self.billing_type
        if self.charge_type is not None:
            result['ChargeType'] = self.charge_type
        if self.cbn_geographic_region_id_a is not None:
            result['CbnGeographicRegionIdA'] = self.cbn_geographic_region_id_a
        if self.cbn_geographic_region_id_b is not None:
            result['CbnGeographicRegionIdB'] = self.cbn_geographic_region_id_b
        if self.promotion_option_no is not None:
            result['PromotionOptionNo'] = self.promotion_option_no
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Bandwidth') is not None:
            self.bandwidth = m.get('Bandwidth')
        if m.get('Duration') is not None:
            self.duration = m.get('Duration')
        if m.get('PricingCycle') is not None:
            self.pricing_cycle = m.get('PricingCycle')
        if m.get('AutoPay') is not None:
            self.auto_pay = m.get('AutoPay')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('BandwidthType') is not None:
            self.bandwidth_type = m.get('BandwidthType')
        if m.get('AutoUseCoupon') is not None:
            self.auto_use_coupon = m.get('AutoUseCoupon')
        if m.get('Ratio') is not None:
            self.ratio = m.get('Ratio')
        if m.get('BillingType') is not None:
            self.billing_type = m.get('BillingType')
        if m.get('ChargeType') is not None:
            self.charge_type = m.get('ChargeType')
        if m.get('CbnGeographicRegionIdA') is not None:
            self.cbn_geographic_region_id_a = m.get('CbnGeographicRegionIdA')
        if m.get('CbnGeographicRegionIdB') is not None:
            self.cbn_geographic_region_id_b = m.get('CbnGeographicRegionIdB')
        if m.get('PromotionOptionNo') is not None:
            self.promotion_option_no = m.get('PromotionOptionNo')
        return self


class CreateBandwidthPackageResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        bandwidth_package_id: str = None,
        order_id: str = None,
    ):
        self.request_id = request_id
        self.bandwidth_package_id = bandwidth_package_id
        self.order_id = order_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.bandwidth_package_id is not None:
            result['BandwidthPackageId'] = self.bandwidth_package_id
        if self.order_id is not None:
            result['OrderId'] = self.order_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('BandwidthPackageId') is not None:
            self.bandwidth_package_id = m.get('BandwidthPackageId')
        if m.get('OrderId') is not None:
            self.order_id = m.get('OrderId')
        return self


class CreateBandwidthPackageResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateBandwidthPackageResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateBandwidthPackageResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateEndpointGroupRequestEndpointConfigurations(TeaModel):
    def __init__(
        self,
        type: str = None,
        enable_client_ippreservation: bool = None,
        weight: int = None,
        endpoint: str = None,
    ):
        self.type = type
        self.enable_client_ippreservation = enable_client_ippreservation
        self.weight = weight
        self.endpoint = endpoint

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.enable_client_ippreservation is not None:
            result['EnableClientIPPreservation'] = self.enable_client_ippreservation
        if self.weight is not None:
            result['Weight'] = self.weight
        if self.endpoint is not None:
            result['Endpoint'] = self.endpoint
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('EnableClientIPPreservation') is not None:
            self.enable_client_ippreservation = m.get('EnableClientIPPreservation')
        if m.get('Weight') is not None:
            self.weight = m.get('Weight')
        if m.get('Endpoint') is not None:
            self.endpoint = m.get('Endpoint')
        return self


class CreateEndpointGroupRequestPortOverrides(TeaModel):
    def __init__(
        self,
        listener_port: int = None,
        endpoint_port: int = None,
    ):
        self.listener_port = listener_port
        self.endpoint_port = endpoint_port

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.listener_port is not None:
            result['ListenerPort'] = self.listener_port
        if self.endpoint_port is not None:
            result['EndpointPort'] = self.endpoint_port
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ListenerPort') is not None:
            self.listener_port = m.get('ListenerPort')
        if m.get('EndpointPort') is not None:
            self.endpoint_port = m.get('EndpointPort')
        return self


class CreateEndpointGroupRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        client_token: str = None,
        accelerator_id: str = None,
        name: str = None,
        description: str = None,
        endpoint_group_region: str = None,
        listener_id: str = None,
        traffic_percentage: int = None,
        health_check_interval_seconds: int = None,
        health_check_path: str = None,
        health_check_port: int = None,
        health_check_protocol: str = None,
        threshold_count: int = None,
        endpoint_configurations: List[CreateEndpointGroupRequestEndpointConfigurations] = None,
        endpoint_request_protocol: str = None,
        endpoint_group_type: str = None,
        port_overrides: List[CreateEndpointGroupRequestPortOverrides] = None,
    ):
        self.region_id = region_id
        self.client_token = client_token
        self.accelerator_id = accelerator_id
        self.name = name
        self.description = description
        self.endpoint_group_region = endpoint_group_region
        self.listener_id = listener_id
        self.traffic_percentage = traffic_percentage
        self.health_check_interval_seconds = health_check_interval_seconds
        self.health_check_path = health_check_path
        self.health_check_port = health_check_port
        self.health_check_protocol = health_check_protocol
        self.threshold_count = threshold_count
        self.endpoint_configurations = endpoint_configurations
        self.endpoint_request_protocol = endpoint_request_protocol
        self.endpoint_group_type = endpoint_group_type
        self.port_overrides = port_overrides

    def validate(self):
        if self.endpoint_configurations:
            for k in self.endpoint_configurations:
                if k:
                    k.validate()
        if self.port_overrides:
            for k in self.port_overrides:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.accelerator_id is not None:
            result['AcceleratorId'] = self.accelerator_id
        if self.name is not None:
            result['Name'] = self.name
        if self.description is not None:
            result['Description'] = self.description
        if self.endpoint_group_region is not None:
            result['EndpointGroupRegion'] = self.endpoint_group_region
        if self.listener_id is not None:
            result['ListenerId'] = self.listener_id
        if self.traffic_percentage is not None:
            result['TrafficPercentage'] = self.traffic_percentage
        if self.health_check_interval_seconds is not None:
            result['HealthCheckIntervalSeconds'] = self.health_check_interval_seconds
        if self.health_check_path is not None:
            result['HealthCheckPath'] = self.health_check_path
        if self.health_check_port is not None:
            result['HealthCheckPort'] = self.health_check_port
        if self.health_check_protocol is not None:
            result['HealthCheckProtocol'] = self.health_check_protocol
        if self.threshold_count is not None:
            result['ThresholdCount'] = self.threshold_count
        result['EndpointConfigurations'] = []
        if self.endpoint_configurations is not None:
            for k in self.endpoint_configurations:
                result['EndpointConfigurations'].append(k.to_map() if k else None)
        if self.endpoint_request_protocol is not None:
            result['EndpointRequestProtocol'] = self.endpoint_request_protocol
        if self.endpoint_group_type is not None:
            result['EndpointGroupType'] = self.endpoint_group_type
        result['PortOverrides'] = []
        if self.port_overrides is not None:
            for k in self.port_overrides:
                result['PortOverrides'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('AcceleratorId') is not None:
            self.accelerator_id = m.get('AcceleratorId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('EndpointGroupRegion') is not None:
            self.endpoint_group_region = m.get('EndpointGroupRegion')
        if m.get('ListenerId') is not None:
            self.listener_id = m.get('ListenerId')
        if m.get('TrafficPercentage') is not None:
            self.traffic_percentage = m.get('TrafficPercentage')
        if m.get('HealthCheckIntervalSeconds') is not None:
            self.health_check_interval_seconds = m.get('HealthCheckIntervalSeconds')
        if m.get('HealthCheckPath') is not None:
            self.health_check_path = m.get('HealthCheckPath')
        if m.get('HealthCheckPort') is not None:
            self.health_check_port = m.get('HealthCheckPort')
        if m.get('HealthCheckProtocol') is not None:
            self.health_check_protocol = m.get('HealthCheckProtocol')
        if m.get('ThresholdCount') is not None:
            self.threshold_count = m.get('ThresholdCount')
        self.endpoint_configurations = []
        if m.get('EndpointConfigurations') is not None:
            for k in m.get('EndpointConfigurations'):
                temp_model = CreateEndpointGroupRequestEndpointConfigurations()
                self.endpoint_configurations.append(temp_model.from_map(k))
        if m.get('EndpointRequestProtocol') is not None:
            self.endpoint_request_protocol = m.get('EndpointRequestProtocol')
        if m.get('EndpointGroupType') is not None:
            self.endpoint_group_type = m.get('EndpointGroupType')
        self.port_overrides = []
        if m.get('PortOverrides') is not None:
            for k in m.get('PortOverrides'):
                temp_model = CreateEndpointGroupRequestPortOverrides()
                self.port_overrides.append(temp_model.from_map(k))
        return self


class CreateEndpointGroupResponseBody(TeaModel):
    def __init__(
        self,
        endpoint_group_id: str = None,
        request_id: str = None,
    ):
        self.endpoint_group_id = endpoint_group_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.endpoint_group_id is not None:
            result['EndpointGroupId'] = self.endpoint_group_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndpointGroupId') is not None:
            self.endpoint_group_id = m.get('EndpointGroupId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class CreateEndpointGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateEndpointGroupResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateEndpointGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateForwardingRulesRequestForwardingRulesRuleConditionsPathConfig(TeaModel):
    def __init__(
        self,
        values: List[str] = None,
    ):
        self.values = values

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.values is not None:
            result['Values'] = self.values
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Values') is not None:
            self.values = m.get('Values')
        return self


class CreateForwardingRulesRequestForwardingRulesRuleConditionsHostConfig(TeaModel):
    def __init__(
        self,
        values: List[str] = None,
    ):
        self.values = values

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.values is not None:
            result['Values'] = self.values
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Values') is not None:
            self.values = m.get('Values')
        return self


class CreateForwardingRulesRequestForwardingRulesRuleConditions(TeaModel):
    def __init__(
        self,
        rule_condition_type: str = None,
        path_config: CreateForwardingRulesRequestForwardingRulesRuleConditionsPathConfig = None,
        host_config: CreateForwardingRulesRequestForwardingRulesRuleConditionsHostConfig = None,
    ):
        self.rule_condition_type = rule_condition_type
        self.path_config = path_config
        self.host_config = host_config

    def validate(self):
        if self.path_config:
            self.path_config.validate()
        if self.host_config:
            self.host_config.validate()

    def to_map(self):
        result = dict()
        if self.rule_condition_type is not None:
            result['RuleConditionType'] = self.rule_condition_type
        if self.path_config is not None:
            result['PathConfig'] = self.path_config.to_map()
        if self.host_config is not None:
            result['HostConfig'] = self.host_config.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RuleConditionType') is not None:
            self.rule_condition_type = m.get('RuleConditionType')
        if m.get('PathConfig') is not None:
            temp_model = CreateForwardingRulesRequestForwardingRulesRuleConditionsPathConfig()
            self.path_config = temp_model.from_map(m['PathConfig'])
        if m.get('HostConfig') is not None:
            temp_model = CreateForwardingRulesRequestForwardingRulesRuleConditionsHostConfig()
            self.host_config = temp_model.from_map(m['HostConfig'])
        return self


class CreateForwardingRulesRequestForwardingRulesRuleActionsForwardGroupConfigServerGroupTuples(TeaModel):
    def __init__(
        self,
        endpoint_group_id: str = None,
    ):
        self.endpoint_group_id = endpoint_group_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.endpoint_group_id is not None:
            result['EndpointGroupId'] = self.endpoint_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndpointGroupId') is not None:
            self.endpoint_group_id = m.get('EndpointGroupId')
        return self


class CreateForwardingRulesRequestForwardingRulesRuleActionsForwardGroupConfig(TeaModel):
    def __init__(
        self,
        server_group_tuples: List[CreateForwardingRulesRequestForwardingRulesRuleActionsForwardGroupConfigServerGroupTuples] = None,
    ):
        self.server_group_tuples = server_group_tuples

    def validate(self):
        if self.server_group_tuples:
            for k in self.server_group_tuples:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['ServerGroupTuples'] = []
        if self.server_group_tuples is not None:
            for k in self.server_group_tuples:
                result['ServerGroupTuples'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.server_group_tuples = []
        if m.get('ServerGroupTuples') is not None:
            for k in m.get('ServerGroupTuples'):
                temp_model = CreateForwardingRulesRequestForwardingRulesRuleActionsForwardGroupConfigServerGroupTuples()
                self.server_group_tuples.append(temp_model.from_map(k))
        return self


class CreateForwardingRulesRequestForwardingRulesRuleActions(TeaModel):
    def __init__(
        self,
        order: int = None,
        rule_action_type: str = None,
        forward_group_config: CreateForwardingRulesRequestForwardingRulesRuleActionsForwardGroupConfig = None,
    ):
        self.order = order
        self.rule_action_type = rule_action_type
        self.forward_group_config = forward_group_config

    def validate(self):
        if self.forward_group_config:
            self.forward_group_config.validate()

    def to_map(self):
        result = dict()
        if self.order is not None:
            result['Order'] = self.order
        if self.rule_action_type is not None:
            result['RuleActionType'] = self.rule_action_type
        if self.forward_group_config is not None:
            result['ForwardGroupConfig'] = self.forward_group_config.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('RuleActionType') is not None:
            self.rule_action_type = m.get('RuleActionType')
        if m.get('ForwardGroupConfig') is not None:
            temp_model = CreateForwardingRulesRequestForwardingRulesRuleActionsForwardGroupConfig()
            self.forward_group_config = temp_model.from_map(m['ForwardGroupConfig'])
        return self


class CreateForwardingRulesRequestForwardingRules(TeaModel):
    def __init__(
        self,
        priority: int = None,
        rule_conditions: List[CreateForwardingRulesRequestForwardingRulesRuleConditions] = None,
        rule_actions: List[CreateForwardingRulesRequestForwardingRulesRuleActions] = None,
        forwarding_rule_name: str = None,
    ):
        self.priority = priority
        self.rule_conditions = rule_conditions
        self.rule_actions = rule_actions
        self.forwarding_rule_name = forwarding_rule_name

    def validate(self):
        if self.rule_conditions:
            for k in self.rule_conditions:
                if k:
                    k.validate()
        if self.rule_actions:
            for k in self.rule_actions:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.priority is not None:
            result['Priority'] = self.priority
        result['RuleConditions'] = []
        if self.rule_conditions is not None:
            for k in self.rule_conditions:
                result['RuleConditions'].append(k.to_map() if k else None)
        result['RuleActions'] = []
        if self.rule_actions is not None:
            for k in self.rule_actions:
                result['RuleActions'].append(k.to_map() if k else None)
        if self.forwarding_rule_name is not None:
            result['ForwardingRuleName'] = self.forwarding_rule_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Priority') is not None:
            self.priority = m.get('Priority')
        self.rule_conditions = []
        if m.get('RuleConditions') is not None:
            for k in m.get('RuleConditions'):
                temp_model = CreateForwardingRulesRequestForwardingRulesRuleConditions()
                self.rule_conditions.append(temp_model.from_map(k))
        self.rule_actions = []
        if m.get('RuleActions') is not None:
            for k in m.get('RuleActions'):
                temp_model = CreateForwardingRulesRequestForwardingRulesRuleActions()
                self.rule_actions.append(temp_model.from_map(k))
        if m.get('ForwardingRuleName') is not None:
            self.forwarding_rule_name = m.get('ForwardingRuleName')
        return self


class CreateForwardingRulesRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        client_token: str = None,
        accelerator_id: str = None,
        listener_id: str = None,
        forwarding_rules: List[CreateForwardingRulesRequestForwardingRules] = None,
    ):
        self.region_id = region_id
        self.client_token = client_token
        self.accelerator_id = accelerator_id
        self.listener_id = listener_id
        self.forwarding_rules = forwarding_rules

    def validate(self):
        if self.forwarding_rules:
            for k in self.forwarding_rules:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.accelerator_id is not None:
            result['AcceleratorId'] = self.accelerator_id
        if self.listener_id is not None:
            result['ListenerId'] = self.listener_id
        result['ForwardingRules'] = []
        if self.forwarding_rules is not None:
            for k in self.forwarding_rules:
                result['ForwardingRules'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('AcceleratorId') is not None:
            self.accelerator_id = m.get('AcceleratorId')
        if m.get('ListenerId') is not None:
            self.listener_id = m.get('ListenerId')
        self.forwarding_rules = []
        if m.get('ForwardingRules') is not None:
            for k in m.get('ForwardingRules'):
                temp_model = CreateForwardingRulesRequestForwardingRules()
                self.forwarding_rules.append(temp_model.from_map(k))
        return self


class CreateForwardingRulesResponseBodyForwardingRules(TeaModel):
    def __init__(
        self,
        forwarding_rule_id: str = None,
    ):
        self.forwarding_rule_id = forwarding_rule_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.forwarding_rule_id is not None:
            result['ForwardingRuleId'] = self.forwarding_rule_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ForwardingRuleId') is not None:
            self.forwarding_rule_id = m.get('ForwardingRuleId')
        return self


class CreateForwardingRulesResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        forwarding_rules: List[CreateForwardingRulesResponseBodyForwardingRules] = None,
    ):
        self.request_id = request_id
        self.forwarding_rules = forwarding_rules

    def validate(self):
        if self.forwarding_rules:
            for k in self.forwarding_rules:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['ForwardingRules'] = []
        if self.forwarding_rules is not None:
            for k in self.forwarding_rules:
                result['ForwardingRules'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.forwarding_rules = []
        if m.get('ForwardingRules') is not None:
            for k in m.get('ForwardingRules'):
                temp_model = CreateForwardingRulesResponseBodyForwardingRules()
                self.forwarding_rules.append(temp_model.from_map(k))
        return self


class CreateForwardingRulesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateForwardingRulesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateForwardingRulesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateIpSetsRequestAccelerateRegion(TeaModel):
    def __init__(
        self,
        accelerate_region_id: str = None,
        ip_version: str = None,
        bandwidth: int = None,
    ):
        self.accelerate_region_id = accelerate_region_id
        self.ip_version = ip_version
        self.bandwidth = bandwidth

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.accelerate_region_id is not None:
            result['AccelerateRegionId'] = self.accelerate_region_id
        if self.ip_version is not None:
            result['IpVersion'] = self.ip_version
        if self.bandwidth is not None:
            result['Bandwidth'] = self.bandwidth
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccelerateRegionId') is not None:
            self.accelerate_region_id = m.get('AccelerateRegionId')
        if m.get('IpVersion') is not None:
            self.ip_version = m.get('IpVersion')
        if m.get('Bandwidth') is not None:
            self.bandwidth = m.get('Bandwidth')
        return self


class CreateIpSetsRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        client_token: str = None,
        accelerator_id: str = None,
        accelerate_region: List[CreateIpSetsRequestAccelerateRegion] = None,
    ):
        self.region_id = region_id
        self.client_token = client_token
        self.accelerator_id = accelerator_id
        self.accelerate_region = accelerate_region

    def validate(self):
        if self.accelerate_region:
            for k in self.accelerate_region:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.accelerator_id is not None:
            result['AcceleratorId'] = self.accelerator_id
        result['AccelerateRegion'] = []
        if self.accelerate_region is not None:
            for k in self.accelerate_region:
                result['AccelerateRegion'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('AcceleratorId') is not None:
            self.accelerator_id = m.get('AcceleratorId')
        self.accelerate_region = []
        if m.get('AccelerateRegion') is not None:
            for k in m.get('AccelerateRegion'):
                temp_model = CreateIpSetsRequestAccelerateRegion()
                self.accelerate_region.append(temp_model.from_map(k))
        return self


class CreateIpSetsResponseBodyIpSets(TeaModel):
    def __init__(
        self,
        accelerate_region_id: str = None,
        bandwidth: int = None,
        ip_set_id: str = None,
        ip_list: List[str] = None,
    ):
        self.accelerate_region_id = accelerate_region_id
        self.bandwidth = bandwidth
        self.ip_set_id = ip_set_id
        self.ip_list = ip_list

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.accelerate_region_id is not None:
            result['AccelerateRegionId'] = self.accelerate_region_id
        if self.bandwidth is not None:
            result['Bandwidth'] = self.bandwidth
        if self.ip_set_id is not None:
            result['IpSetId'] = self.ip_set_id
        if self.ip_list is not None:
            result['IpList'] = self.ip_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccelerateRegionId') is not None:
            self.accelerate_region_id = m.get('AccelerateRegionId')
        if m.get('Bandwidth') is not None:
            self.bandwidth = m.get('Bandwidth')
        if m.get('IpSetId') is not None:
            self.ip_set_id = m.get('IpSetId')
        if m.get('IpList') is not None:
            self.ip_list = m.get('IpList')
        return self


class CreateIpSetsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        ip_sets: List[CreateIpSetsResponseBodyIpSets] = None,
        accelerator_id: str = None,
    ):
        self.request_id = request_id
        self.ip_sets = ip_sets
        self.accelerator_id = accelerator_id

    def validate(self):
        if self.ip_sets:
            for k in self.ip_sets:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['IpSets'] = []
        if self.ip_sets is not None:
            for k in self.ip_sets:
                result['IpSets'].append(k.to_map() if k else None)
        if self.accelerator_id is not None:
            result['AcceleratorId'] = self.accelerator_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.ip_sets = []
        if m.get('IpSets') is not None:
            for k in m.get('IpSets'):
                temp_model = CreateIpSetsResponseBodyIpSets()
                self.ip_sets.append(temp_model.from_map(k))
        if m.get('AcceleratorId') is not None:
            self.accelerator_id = m.get('AcceleratorId')
        return self


class CreateIpSetsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateIpSetsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateIpSetsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateListenerRequestPortRanges(TeaModel):
    def __init__(
        self,
        from_port: int = None,
        to_port: int = None,
    ):
        self.from_port = from_port
        self.to_port = to_port

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.from_port is not None:
            result['FromPort'] = self.from_port
        if self.to_port is not None:
            result['ToPort'] = self.to_port
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FromPort') is not None:
            self.from_port = m.get('FromPort')
        if m.get('ToPort') is not None:
            self.to_port = m.get('ToPort')
        return self


class CreateListenerRequestCertificates(TeaModel):
    def __init__(
        self,
        id: str = None,
    ):
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class CreateListenerRequestBackendPorts(TeaModel):
    def __init__(self):
        pass

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        return self


class CreateListenerRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        client_token: str = None,
        accelerator_id: str = None,
        name: str = None,
        description: str = None,
        client_affinity: str = None,
        protocol: str = None,
        proxy_protocol: bool = None,
        port_ranges: List[CreateListenerRequestPortRanges] = None,
        certificates: List[CreateListenerRequestCertificates] = None,
        backend_ports: List[CreateListenerRequestBackendPorts] = None,
    ):
        self.region_id = region_id
        self.client_token = client_token
        self.accelerator_id = accelerator_id
        self.name = name
        self.description = description
        self.client_affinity = client_affinity
        self.protocol = protocol
        self.proxy_protocol = proxy_protocol
        self.port_ranges = port_ranges
        self.certificates = certificates
        # 转发端口迁移至终端节点组portoverride
        self.backend_ports = backend_ports

    def validate(self):
        if self.port_ranges:
            for k in self.port_ranges:
                if k:
                    k.validate()
        if self.certificates:
            for k in self.certificates:
                if k:
                    k.validate()
        if self.backend_ports:
            for k in self.backend_ports:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.accelerator_id is not None:
            result['AcceleratorId'] = self.accelerator_id
        if self.name is not None:
            result['Name'] = self.name
        if self.description is not None:
            result['Description'] = self.description
        if self.client_affinity is not None:
            result['ClientAffinity'] = self.client_affinity
        if self.protocol is not None:
            result['Protocol'] = self.protocol
        if self.proxy_protocol is not None:
            result['ProxyProtocol'] = self.proxy_protocol
        result['PortRanges'] = []
        if self.port_ranges is not None:
            for k in self.port_ranges:
                result['PortRanges'].append(k.to_map() if k else None)
        result['Certificates'] = []
        if self.certificates is not None:
            for k in self.certificates:
                result['Certificates'].append(k.to_map() if k else None)
        result['BackendPorts'] = []
        if self.backend_ports is not None:
            for k in self.backend_ports:
                result['BackendPorts'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('AcceleratorId') is not None:
            self.accelerator_id = m.get('AcceleratorId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('ClientAffinity') is not None:
            self.client_affinity = m.get('ClientAffinity')
        if m.get('Protocol') is not None:
            self.protocol = m.get('Protocol')
        if m.get('ProxyProtocol') is not None:
            self.proxy_protocol = m.get('ProxyProtocol')
        self.port_ranges = []
        if m.get('PortRanges') is not None:
            for k in m.get('PortRanges'):
                temp_model = CreateListenerRequestPortRanges()
                self.port_ranges.append(temp_model.from_map(k))
        self.certificates = []
        if m.get('Certificates') is not None:
            for k in m.get('Certificates'):
                temp_model = CreateListenerRequestCertificates()
                self.certificates.append(temp_model.from_map(k))
        self.backend_ports = []
        if m.get('BackendPorts') is not None:
            for k in m.get('BackendPorts'):
                temp_model = CreateListenerRequestBackendPorts()
                self.backend_ports.append(temp_model.from_map(k))
        return self


class CreateListenerResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        listener_id: str = None,
    ):
        self.request_id = request_id
        self.listener_id = listener_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.listener_id is not None:
            result['ListenerId'] = self.listener_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ListenerId') is not None:
            self.listener_id = m.get('ListenerId')
        return self


class CreateListenerResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateListenerResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateListenerResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteAcceleratorRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        accelerator_id: str = None,
    ):
        self.region_id = region_id
        self.accelerator_id = accelerator_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.accelerator_id is not None:
            result['AcceleratorId'] = self.accelerator_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('AcceleratorId') is not None:
            self.accelerator_id = m.get('AcceleratorId')
        return self


class DeleteAcceleratorResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        accelerator_id: str = None,
    ):
        self.request_id = request_id
        self.accelerator_id = accelerator_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.accelerator_id is not None:
            result['AcceleratorId'] = self.accelerator_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('AcceleratorId') is not None:
            self.accelerator_id = m.get('AcceleratorId')
        return self


class DeleteAcceleratorResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteAcceleratorResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteAcceleratorResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteBandwidthPackageRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        bandwidth_package_id: str = None,
        client_token: str = None,
    ):
        self.region_id = region_id
        self.bandwidth_package_id = bandwidth_package_id
        self.client_token = client_token

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.bandwidth_package_id is not None:
            result['BandwidthPackageId'] = self.bandwidth_package_id
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('BandwidthPackageId') is not None:
            self.bandwidth_package_id = m.get('BandwidthPackageId')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        return self


class DeleteBandwidthPackageResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        bandwidth_package_id: str = None,
    ):
        self.request_id = request_id
        self.bandwidth_package_id = bandwidth_package_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.bandwidth_package_id is not None:
            result['BandwidthPackageId'] = self.bandwidth_package_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('BandwidthPackageId') is not None:
            self.bandwidth_package_id = m.get('BandwidthPackageId')
        return self


class DeleteBandwidthPackageResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteBandwidthPackageResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteBandwidthPackageResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteEndpointGroupRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        client_token: str = None,
        accelerator_id: str = None,
        endpoint_group_id: str = None,
    ):
        self.region_id = region_id
        self.client_token = client_token
        self.accelerator_id = accelerator_id
        self.endpoint_group_id = endpoint_group_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.accelerator_id is not None:
            result['AcceleratorId'] = self.accelerator_id
        if self.endpoint_group_id is not None:
            result['EndpointGroupId'] = self.endpoint_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('AcceleratorId') is not None:
            self.accelerator_id = m.get('AcceleratorId')
        if m.get('EndpointGroupId') is not None:
            self.endpoint_group_id = m.get('EndpointGroupId')
        return self


class DeleteEndpointGroupResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteEndpointGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteEndpointGroupResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteEndpointGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteForwardingRulesRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        client_token: str = None,
        forwarding_rule_ids: List[str] = None,
        accelerator_id: str = None,
        listener_id: str = None,
    ):
        self.region_id = region_id
        self.client_token = client_token
        self.forwarding_rule_ids = forwarding_rule_ids
        self.accelerator_id = accelerator_id
        self.listener_id = listener_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.forwarding_rule_ids is not None:
            result['ForwardingRuleIds'] = self.forwarding_rule_ids
        if self.accelerator_id is not None:
            result['AcceleratorId'] = self.accelerator_id
        if self.listener_id is not None:
            result['ListenerId'] = self.listener_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('ForwardingRuleIds') is not None:
            self.forwarding_rule_ids = m.get('ForwardingRuleIds')
        if m.get('AcceleratorId') is not None:
            self.accelerator_id = m.get('AcceleratorId')
        if m.get('ListenerId') is not None:
            self.listener_id = m.get('ListenerId')
        return self


class DeleteForwardingRulesResponseBodyForwardingRules(TeaModel):
    def __init__(
        self,
        forwarding_rule_id: str = None,
    ):
        self.forwarding_rule_id = forwarding_rule_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.forwarding_rule_id is not None:
            result['ForwardingRuleId'] = self.forwarding_rule_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ForwardingRuleId') is not None:
            self.forwarding_rule_id = m.get('ForwardingRuleId')
        return self


class DeleteForwardingRulesResponseBody(TeaModel):
    def __init__(
        self,
        forwarding_rules: List[DeleteForwardingRulesResponseBodyForwardingRules] = None,
        request_id: str = None,
    ):
        self.forwarding_rules = forwarding_rules
        self.request_id = request_id

    def validate(self):
        if self.forwarding_rules:
            for k in self.forwarding_rules:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['ForwardingRules'] = []
        if self.forwarding_rules is not None:
            for k in self.forwarding_rules:
                result['ForwardingRules'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.forwarding_rules = []
        if m.get('ForwardingRules') is not None:
            for k in m.get('ForwardingRules'):
                temp_model = DeleteForwardingRulesResponseBodyForwardingRules()
                self.forwarding_rules.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteForwardingRulesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteForwardingRulesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteForwardingRulesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteIpSetRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        client_token: str = None,
        accelerator_id: str = None,
        ip_set_id: str = None,
    ):
        self.region_id = region_id
        self.client_token = client_token
        self.accelerator_id = accelerator_id
        self.ip_set_id = ip_set_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.accelerator_id is not None:
            result['AcceleratorId'] = self.accelerator_id
        if self.ip_set_id is not None:
            result['IpSetId'] = self.ip_set_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('AcceleratorId') is not None:
            self.accelerator_id = m.get('AcceleratorId')
        if m.get('IpSetId') is not None:
            self.ip_set_id = m.get('IpSetId')
        return self


class DeleteIpSetResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteIpSetResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteIpSetResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteIpSetResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteIpSetsRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        ip_set_ids: List[str] = None,
    ):
        self.region_id = region_id
        self.ip_set_ids = ip_set_ids

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.ip_set_ids is not None:
            result['IpSetIds'] = self.ip_set_ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('IpSetIds') is not None:
            self.ip_set_ids = m.get('IpSetIds')
        return self


class DeleteIpSetsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteIpSetsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteIpSetsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteIpSetsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DeleteListenerRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        client_token: str = None,
        accelerator_id: str = None,
        listener_id: str = None,
    ):
        self.region_id = region_id
        self.client_token = client_token
        self.accelerator_id = accelerator_id
        self.listener_id = listener_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.accelerator_id is not None:
            result['AcceleratorId'] = self.accelerator_id
        if self.listener_id is not None:
            result['ListenerId'] = self.listener_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('AcceleratorId') is not None:
            self.accelerator_id = m.get('AcceleratorId')
        if m.get('ListenerId') is not None:
            self.listener_id = m.get('ListenerId')
        return self


class DeleteListenerResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DeleteListenerResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DeleteListenerResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DeleteListenerResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeAcceleratorRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        accelerator_id: str = None,
    ):
        self.region_id = region_id
        self.accelerator_id = accelerator_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.accelerator_id is not None:
            result['AcceleratorId'] = self.accelerator_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('AcceleratorId') is not None:
            self.accelerator_id = m.get('AcceleratorId')
        return self


class DescribeAcceleratorResponseBodyCrossDomainBandwidthPackage(TeaModel):
    def __init__(
        self,
        bandwidth: int = None,
        instance_id: str = None,
    ):
        self.bandwidth = bandwidth
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.bandwidth is not None:
            result['Bandwidth'] = self.bandwidth
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Bandwidth') is not None:
            self.bandwidth = m.get('Bandwidth')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class DescribeAcceleratorResponseBodyBasicBandwidthPackage(TeaModel):
    def __init__(
        self,
        bandwidth: int = None,
        bandwidth_type: str = None,
        instance_id: str = None,
    ):
        self.bandwidth = bandwidth
        self.bandwidth_type = bandwidth_type
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.bandwidth is not None:
            result['Bandwidth'] = self.bandwidth
        if self.bandwidth_type is not None:
            result['BandwidthType'] = self.bandwidth_type
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Bandwidth') is not None:
            self.bandwidth = m.get('Bandwidth')
        if m.get('BandwidthType') is not None:
            self.bandwidth_type = m.get('BandwidthType')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class DescribeAcceleratorResponseBody(TeaModel):
    def __init__(
        self,
        ddos_id: str = None,
        dns_name: str = None,
        description: str = None,
        request_id: str = None,
        instance_charge_type: str = None,
        create_time: int = None,
        cross_domain_bandwidth_package: DescribeAcceleratorResponseBodyCrossDomainBandwidthPackage = None,
        second_dns_name: str = None,
        name: str = None,
        basic_bandwidth_package: DescribeAcceleratorResponseBodyBasicBandwidthPackage = None,
        state: str = None,
        expired_time: int = None,
        cen_id: str = None,
        region_id: str = None,
        spec: str = None,
        accelerator_id: str = None,
    ):
        self.ddos_id = ddos_id
        self.dns_name = dns_name
        self.description = description
        self.request_id = request_id
        self.instance_charge_type = instance_charge_type
        self.create_time = create_time
        self.cross_domain_bandwidth_package = cross_domain_bandwidth_package
        self.second_dns_name = second_dns_name
        self.name = name
        self.basic_bandwidth_package = basic_bandwidth_package
        self.state = state
        self.expired_time = expired_time
        self.cen_id = cen_id
        self.region_id = region_id
        self.spec = spec
        self.accelerator_id = accelerator_id

    def validate(self):
        if self.cross_domain_bandwidth_package:
            self.cross_domain_bandwidth_package.validate()
        if self.basic_bandwidth_package:
            self.basic_bandwidth_package.validate()

    def to_map(self):
        result = dict()
        if self.ddos_id is not None:
            result['DdosId'] = self.ddos_id
        if self.dns_name is not None:
            result['DnsName'] = self.dns_name
        if self.description is not None:
            result['Description'] = self.description
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.instance_charge_type is not None:
            result['InstanceChargeType'] = self.instance_charge_type
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.cross_domain_bandwidth_package is not None:
            result['CrossDomainBandwidthPackage'] = self.cross_domain_bandwidth_package.to_map()
        if self.second_dns_name is not None:
            result['SecondDnsName'] = self.second_dns_name
        if self.name is not None:
            result['Name'] = self.name
        if self.basic_bandwidth_package is not None:
            result['BasicBandwidthPackage'] = self.basic_bandwidth_package.to_map()
        if self.state is not None:
            result['State'] = self.state
        if self.expired_time is not None:
            result['ExpiredTime'] = self.expired_time
        if self.cen_id is not None:
            result['CenId'] = self.cen_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.spec is not None:
            result['Spec'] = self.spec
        if self.accelerator_id is not None:
            result['AcceleratorId'] = self.accelerator_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DdosId') is not None:
            self.ddos_id = m.get('DdosId')
        if m.get('DnsName') is not None:
            self.dns_name = m.get('DnsName')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('InstanceChargeType') is not None:
            self.instance_charge_type = m.get('InstanceChargeType')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('CrossDomainBandwidthPackage') is not None:
            temp_model = DescribeAcceleratorResponseBodyCrossDomainBandwidthPackage()
            self.cross_domain_bandwidth_package = temp_model.from_map(m['CrossDomainBandwidthPackage'])
        if m.get('SecondDnsName') is not None:
            self.second_dns_name = m.get('SecondDnsName')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('BasicBandwidthPackage') is not None:
            temp_model = DescribeAcceleratorResponseBodyBasicBandwidthPackage()
            self.basic_bandwidth_package = temp_model.from_map(m['BasicBandwidthPackage'])
        if m.get('State') is not None:
            self.state = m.get('State')
        if m.get('ExpiredTime') is not None:
            self.expired_time = m.get('ExpiredTime')
        if m.get('CenId') is not None:
            self.cen_id = m.get('CenId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Spec') is not None:
            self.spec = m.get('Spec')
        if m.get('AcceleratorId') is not None:
            self.accelerator_id = m.get('AcceleratorId')
        return self


class DescribeAcceleratorResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeAcceleratorResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeAcceleratorResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeBandwidthPackageRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        bandwidth_package_id: str = None,
    ):
        self.region_id = region_id
        self.bandwidth_package_id = bandwidth_package_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.bandwidth_package_id is not None:
            result['BandwidthPackageId'] = self.bandwidth_package_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('BandwidthPackageId') is not None:
            self.bandwidth_package_id = m.get('BandwidthPackageId')
        return self


class DescribeBandwidthPackageResponseBody(TeaModel):
    def __init__(
        self,
        cbn_geographic_region_id_b: str = None,
        cbn_geographic_region_id_a: str = None,
        description: str = None,
        request_id: str = None,
        create_time: str = None,
        name: str = None,
        bandwidth_type: str = None,
        type: str = None,
        accelerators: List[str] = None,
        state: str = None,
        charge_type: str = None,
        bandwidth: int = None,
        expired_time: str = None,
        bandwidth_package_id: str = None,
        region_id: str = None,
        billing_type: str = None,
    ):
        self.cbn_geographic_region_id_b = cbn_geographic_region_id_b
        self.cbn_geographic_region_id_a = cbn_geographic_region_id_a
        self.description = description
        self.request_id = request_id
        self.create_time = create_time
        self.name = name
        self.bandwidth_type = bandwidth_type
        self.type = type
        self.accelerators = accelerators
        self.state = state
        self.charge_type = charge_type
        self.bandwidth = bandwidth
        self.expired_time = expired_time
        self.bandwidth_package_id = bandwidth_package_id
        self.region_id = region_id
        self.billing_type = billing_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.cbn_geographic_region_id_b is not None:
            result['CbnGeographicRegionIdB'] = self.cbn_geographic_region_id_b
        if self.cbn_geographic_region_id_a is not None:
            result['CbnGeographicRegionIdA'] = self.cbn_geographic_region_id_a
        if self.description is not None:
            result['Description'] = self.description
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.name is not None:
            result['Name'] = self.name
        if self.bandwidth_type is not None:
            result['BandwidthType'] = self.bandwidth_type
        if self.type is not None:
            result['Type'] = self.type
        if self.accelerators is not None:
            result['Accelerators'] = self.accelerators
        if self.state is not None:
            result['State'] = self.state
        if self.charge_type is not None:
            result['ChargeType'] = self.charge_type
        if self.bandwidth is not None:
            result['Bandwidth'] = self.bandwidth
        if self.expired_time is not None:
            result['ExpiredTime'] = self.expired_time
        if self.bandwidth_package_id is not None:
            result['BandwidthPackageId'] = self.bandwidth_package_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.billing_type is not None:
            result['BillingType'] = self.billing_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CbnGeographicRegionIdB') is not None:
            self.cbn_geographic_region_id_b = m.get('CbnGeographicRegionIdB')
        if m.get('CbnGeographicRegionIdA') is not None:
            self.cbn_geographic_region_id_a = m.get('CbnGeographicRegionIdA')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('BandwidthType') is not None:
            self.bandwidth_type = m.get('BandwidthType')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Accelerators') is not None:
            self.accelerators = m.get('Accelerators')
        if m.get('State') is not None:
            self.state = m.get('State')
        if m.get('ChargeType') is not None:
            self.charge_type = m.get('ChargeType')
        if m.get('Bandwidth') is not None:
            self.bandwidth = m.get('Bandwidth')
        if m.get('ExpiredTime') is not None:
            self.expired_time = m.get('ExpiredTime')
        if m.get('BandwidthPackageId') is not None:
            self.bandwidth_package_id = m.get('BandwidthPackageId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('BillingType') is not None:
            self.billing_type = m.get('BillingType')
        return self


class DescribeBandwidthPackageResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeBandwidthPackageResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeBandwidthPackageResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeEndpointGroupRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        endpoint_group_id: str = None,
    ):
        self.region_id = region_id
        self.endpoint_group_id = endpoint_group_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.endpoint_group_id is not None:
            result['EndpointGroupId'] = self.endpoint_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('EndpointGroupId') is not None:
            self.endpoint_group_id = m.get('EndpointGroupId')
        return self


class DescribeEndpointGroupResponseBodyEndpointConfigurations(TeaModel):
    def __init__(
        self,
        type: str = None,
        enable_client_ippreservation: bool = None,
        weight: int = None,
        probe_protocol: str = None,
        endpoint: str = None,
        probe_port: int = None,
    ):
        self.type = type
        self.enable_client_ippreservation = enable_client_ippreservation
        self.weight = weight
        self.probe_protocol = probe_protocol
        self.endpoint = endpoint
        self.probe_port = probe_port

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.enable_client_ippreservation is not None:
            result['EnableClientIPPreservation'] = self.enable_client_ippreservation
        if self.weight is not None:
            result['Weight'] = self.weight
        if self.probe_protocol is not None:
            result['ProbeProtocol'] = self.probe_protocol
        if self.endpoint is not None:
            result['Endpoint'] = self.endpoint
        if self.probe_port is not None:
            result['ProbePort'] = self.probe_port
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('EnableClientIPPreservation') is not None:
            self.enable_client_ippreservation = m.get('EnableClientIPPreservation')
        if m.get('Weight') is not None:
            self.weight = m.get('Weight')
        if m.get('ProbeProtocol') is not None:
            self.probe_protocol = m.get('ProbeProtocol')
        if m.get('Endpoint') is not None:
            self.endpoint = m.get('Endpoint')
        if m.get('ProbePort') is not None:
            self.probe_port = m.get('ProbePort')
        return self


class DescribeEndpointGroupResponseBodyPortOverrides(TeaModel):
    def __init__(
        self,
        listener_port: int = None,
        endpoint_port: int = None,
    ):
        self.listener_port = listener_port
        self.endpoint_port = endpoint_port

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.listener_port is not None:
            result['ListenerPort'] = self.listener_port
        if self.endpoint_port is not None:
            result['EndpointPort'] = self.endpoint_port
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ListenerPort') is not None:
            self.listener_port = m.get('ListenerPort')
        if m.get('EndpointPort') is not None:
            self.endpoint_port = m.get('EndpointPort')
        return self


class DescribeEndpointGroupResponseBody(TeaModel):
    def __init__(
        self,
        health_check_interval_seconds: int = None,
        traffic_percentage: int = None,
        endpoint_group_id: str = None,
        description: str = None,
        request_id: str = None,
        health_check_path: str = None,
        threshold_count: int = None,
        name: str = None,
        endpoint_group_region: str = None,
        total_count: int = None,
        state: str = None,
        health_check_protocol: str = None,
        health_check_port: int = None,
        endpoint_configurations: List[DescribeEndpointGroupResponseBodyEndpointConfigurations] = None,
        port_overrides: List[DescribeEndpointGroupResponseBodyPortOverrides] = None,
        endpoint_request_protocol: str = None,
        endpoint_group_type: str = None,
        forwarding_rule_ids: List[str] = None,
        listener_id: str = None,
    ):
        self.health_check_interval_seconds = health_check_interval_seconds
        self.traffic_percentage = traffic_percentage
        self.endpoint_group_id = endpoint_group_id
        self.description = description
        self.request_id = request_id
        self.health_check_path = health_check_path
        self.threshold_count = threshold_count
        self.name = name
        self.endpoint_group_region = endpoint_group_region
        self.total_count = total_count
        self.state = state
        self.health_check_protocol = health_check_protocol
        self.health_check_port = health_check_port
        self.endpoint_configurations = endpoint_configurations
        self.port_overrides = port_overrides
        self.endpoint_request_protocol = endpoint_request_protocol
        self.endpoint_group_type = endpoint_group_type
        self.forwarding_rule_ids = forwarding_rule_ids
        self.listener_id = listener_id

    def validate(self):
        if self.endpoint_configurations:
            for k in self.endpoint_configurations:
                if k:
                    k.validate()
        if self.port_overrides:
            for k in self.port_overrides:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.health_check_interval_seconds is not None:
            result['HealthCheckIntervalSeconds'] = self.health_check_interval_seconds
        if self.traffic_percentage is not None:
            result['TrafficPercentage'] = self.traffic_percentage
        if self.endpoint_group_id is not None:
            result['EndpointGroupId'] = self.endpoint_group_id
        if self.description is not None:
            result['Description'] = self.description
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.health_check_path is not None:
            result['HealthCheckPath'] = self.health_check_path
        if self.threshold_count is not None:
            result['ThresholdCount'] = self.threshold_count
        if self.name is not None:
            result['Name'] = self.name
        if self.endpoint_group_region is not None:
            result['EndpointGroupRegion'] = self.endpoint_group_region
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.state is not None:
            result['State'] = self.state
        if self.health_check_protocol is not None:
            result['HealthCheckProtocol'] = self.health_check_protocol
        if self.health_check_port is not None:
            result['HealthCheckPort'] = self.health_check_port
        result['EndpointConfigurations'] = []
        if self.endpoint_configurations is not None:
            for k in self.endpoint_configurations:
                result['EndpointConfigurations'].append(k.to_map() if k else None)
        result['PortOverrides'] = []
        if self.port_overrides is not None:
            for k in self.port_overrides:
                result['PortOverrides'].append(k.to_map() if k else None)
        if self.endpoint_request_protocol is not None:
            result['EndpointRequestProtocol'] = self.endpoint_request_protocol
        if self.endpoint_group_type is not None:
            result['EndpointGroupType'] = self.endpoint_group_type
        if self.forwarding_rule_ids is not None:
            result['ForwardingRuleIds'] = self.forwarding_rule_ids
        if self.listener_id is not None:
            result['ListenerId'] = self.listener_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('HealthCheckIntervalSeconds') is not None:
            self.health_check_interval_seconds = m.get('HealthCheckIntervalSeconds')
        if m.get('TrafficPercentage') is not None:
            self.traffic_percentage = m.get('TrafficPercentage')
        if m.get('EndpointGroupId') is not None:
            self.endpoint_group_id = m.get('EndpointGroupId')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('HealthCheckPath') is not None:
            self.health_check_path = m.get('HealthCheckPath')
        if m.get('ThresholdCount') is not None:
            self.threshold_count = m.get('ThresholdCount')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('EndpointGroupRegion') is not None:
            self.endpoint_group_region = m.get('EndpointGroupRegion')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('State') is not None:
            self.state = m.get('State')
        if m.get('HealthCheckProtocol') is not None:
            self.health_check_protocol = m.get('HealthCheckProtocol')
        if m.get('HealthCheckPort') is not None:
            self.health_check_port = m.get('HealthCheckPort')
        self.endpoint_configurations = []
        if m.get('EndpointConfigurations') is not None:
            for k in m.get('EndpointConfigurations'):
                temp_model = DescribeEndpointGroupResponseBodyEndpointConfigurations()
                self.endpoint_configurations.append(temp_model.from_map(k))
        self.port_overrides = []
        if m.get('PortOverrides') is not None:
            for k in m.get('PortOverrides'):
                temp_model = DescribeEndpointGroupResponseBodyPortOverrides()
                self.port_overrides.append(temp_model.from_map(k))
        if m.get('EndpointRequestProtocol') is not None:
            self.endpoint_request_protocol = m.get('EndpointRequestProtocol')
        if m.get('EndpointGroupType') is not None:
            self.endpoint_group_type = m.get('EndpointGroupType')
        if m.get('ForwardingRuleIds') is not None:
            self.forwarding_rule_ids = m.get('ForwardingRuleIds')
        if m.get('ListenerId') is not None:
            self.listener_id = m.get('ListenerId')
        return self


class DescribeEndpointGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeEndpointGroupResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeEndpointGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeIpSetRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        ip_set_id: str = None,
    ):
        self.region_id = region_id
        self.ip_set_id = ip_set_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.ip_set_id is not None:
            result['IpSetId'] = self.ip_set_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('IpSetId') is not None:
            self.ip_set_id = m.get('IpSetId')
        return self


class DescribeIpSetResponseBody(TeaModel):
    def __init__(
        self,
        ip_set_id: str = None,
        request_id: str = None,
        ip_version: str = None,
        state: str = None,
        bandwidth: int = None,
        ip_address_list: List[str] = None,
        accelerate_region_id: str = None,
    ):
        self.ip_set_id = ip_set_id
        self.request_id = request_id
        self.ip_version = ip_version
        self.state = state
        self.bandwidth = bandwidth
        self.ip_address_list = ip_address_list
        self.accelerate_region_id = accelerate_region_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.ip_set_id is not None:
            result['IpSetId'] = self.ip_set_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.ip_version is not None:
            result['IpVersion'] = self.ip_version
        if self.state is not None:
            result['State'] = self.state
        if self.bandwidth is not None:
            result['Bandwidth'] = self.bandwidth
        if self.ip_address_list is not None:
            result['IpAddressList'] = self.ip_address_list
        if self.accelerate_region_id is not None:
            result['AccelerateRegionId'] = self.accelerate_region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('IpSetId') is not None:
            self.ip_set_id = m.get('IpSetId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('IpVersion') is not None:
            self.ip_version = m.get('IpVersion')
        if m.get('State') is not None:
            self.state = m.get('State')
        if m.get('Bandwidth') is not None:
            self.bandwidth = m.get('Bandwidth')
        if m.get('IpAddressList') is not None:
            self.ip_address_list = m.get('IpAddressList')
        if m.get('AccelerateRegionId') is not None:
            self.accelerate_region_id = m.get('AccelerateRegionId')
        return self


class DescribeIpSetResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeIpSetResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeIpSetResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeListenerRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        listener_id: str = None,
    ):
        self.region_id = region_id
        self.listener_id = listener_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.listener_id is not None:
            result['ListenerId'] = self.listener_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ListenerId') is not None:
            self.listener_id = m.get('ListenerId')
        return self


class DescribeListenerResponseBodyPortRanges(TeaModel):
    def __init__(
        self,
        from_port: int = None,
        to_port: int = None,
    ):
        self.from_port = from_port
        self.to_port = to_port

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.from_port is not None:
            result['FromPort'] = self.from_port
        if self.to_port is not None:
            result['ToPort'] = self.to_port
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FromPort') is not None:
            self.from_port = m.get('FromPort')
        if m.get('ToPort') is not None:
            self.to_port = m.get('ToPort')
        return self


class DescribeListenerResponseBodyBackendPorts(TeaModel):
    def __init__(
        self,
        from_port: str = None,
        to_port: str = None,
    ):
        self.from_port = from_port
        self.to_port = to_port

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.from_port is not None:
            result['FromPort'] = self.from_port
        if self.to_port is not None:
            result['ToPort'] = self.to_port
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FromPort') is not None:
            self.from_port = m.get('FromPort')
        if m.get('ToPort') is not None:
            self.to_port = m.get('ToPort')
        return self


class DescribeListenerResponseBodyCertificates(TeaModel):
    def __init__(
        self,
        type: str = None,
        id: str = None,
    ):
        self.type = type
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class DescribeListenerResponseBody(TeaModel):
    def __init__(
        self,
        description: str = None,
        request_id: str = None,
        state: str = None,
        create_time: str = None,
        port_ranges: List[DescribeListenerResponseBodyPortRanges] = None,
        backend_ports: List[DescribeListenerResponseBodyBackendPorts] = None,
        certificates: List[DescribeListenerResponseBodyCertificates] = None,
        protocol: str = None,
        listener_id: str = None,
        client_affinity: str = None,
        name: str = None,
    ):
        self.description = description
        self.request_id = request_id
        self.state = state
        self.create_time = create_time
        self.port_ranges = port_ranges
        self.backend_ports = backend_ports
        self.certificates = certificates
        self.protocol = protocol
        self.listener_id = listener_id
        self.client_affinity = client_affinity
        self.name = name

    def validate(self):
        if self.port_ranges:
            for k in self.port_ranges:
                if k:
                    k.validate()
        if self.backend_ports:
            for k in self.backend_ports:
                if k:
                    k.validate()
        if self.certificates:
            for k in self.certificates:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.description is not None:
            result['Description'] = self.description
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.state is not None:
            result['State'] = self.state
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        result['PortRanges'] = []
        if self.port_ranges is not None:
            for k in self.port_ranges:
                result['PortRanges'].append(k.to_map() if k else None)
        result['BackendPorts'] = []
        if self.backend_ports is not None:
            for k in self.backend_ports:
                result['BackendPorts'].append(k.to_map() if k else None)
        result['Certificates'] = []
        if self.certificates is not None:
            for k in self.certificates:
                result['Certificates'].append(k.to_map() if k else None)
        if self.protocol is not None:
            result['Protocol'] = self.protocol
        if self.listener_id is not None:
            result['ListenerId'] = self.listener_id
        if self.client_affinity is not None:
            result['ClientAffinity'] = self.client_affinity
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('State') is not None:
            self.state = m.get('State')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        self.port_ranges = []
        if m.get('PortRanges') is not None:
            for k in m.get('PortRanges'):
                temp_model = DescribeListenerResponseBodyPortRanges()
                self.port_ranges.append(temp_model.from_map(k))
        self.backend_ports = []
        if m.get('BackendPorts') is not None:
            for k in m.get('BackendPorts'):
                temp_model = DescribeListenerResponseBodyBackendPorts()
                self.backend_ports.append(temp_model.from_map(k))
        self.certificates = []
        if m.get('Certificates') is not None:
            for k in m.get('Certificates'):
                temp_model = DescribeListenerResponseBodyCertificates()
                self.certificates.append(temp_model.from_map(k))
        if m.get('Protocol') is not None:
            self.protocol = m.get('Protocol')
        if m.get('ListenerId') is not None:
            self.listener_id = m.get('ListenerId')
        if m.get('ClientAffinity') is not None:
            self.client_affinity = m.get('ClientAffinity')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class DescribeListenerResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeListenerResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeListenerResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeRegionsRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
    ):
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class DescribeRegionsResponseBodyRegions(TeaModel):
    def __init__(
        self,
        local_name: str = None,
        region_id: str = None,
    ):
        self.local_name = local_name
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.local_name is not None:
            result['LocalName'] = self.local_name
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LocalName') is not None:
            self.local_name = m.get('LocalName')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class DescribeRegionsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        regions: List[DescribeRegionsResponseBodyRegions] = None,
    ):
        self.request_id = request_id
        self.regions = regions

    def validate(self):
        if self.regions:
            for k in self.regions:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Regions'] = []
        if self.regions is not None:
            for k in self.regions:
                result['Regions'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.regions = []
        if m.get('Regions') is not None:
            for k in m.get('Regions'):
                temp_model = DescribeRegionsResponseBodyRegions()
                self.regions.append(temp_model.from_map(k))
        return self


class DescribeRegionsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeRegionsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeRegionsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DetachDdosFromAcceleratorRequest(TeaModel):
    def __init__(
        self,
        accelerator_id: str = None,
        region_id: str = None,
    ):
        self.accelerator_id = accelerator_id
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.accelerator_id is not None:
            result['AcceleratorId'] = self.accelerator_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AcceleratorId') is not None:
            self.accelerator_id = m.get('AcceleratorId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class DetachDdosFromAcceleratorResponseBody(TeaModel):
    def __init__(
        self,
        ddos_id: str = None,
        request_id: str = None,
    ):
        self.ddos_id = ddos_id
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.ddos_id is not None:
            result['DdosId'] = self.ddos_id
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DdosId') is not None:
            self.ddos_id = m.get('DdosId')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DetachDdosFromAcceleratorResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DetachDdosFromAcceleratorResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DetachDdosFromAcceleratorResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListAccelerateAreasRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
    ):
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class ListAccelerateAreasResponseBodyAreasRegionList(TeaModel):
    def __init__(
        self,
        local_name: str = None,
        region_id: str = None,
    ):
        self.local_name = local_name
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.local_name is not None:
            result['LocalName'] = self.local_name
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LocalName') is not None:
            self.local_name = m.get('LocalName')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class ListAccelerateAreasResponseBodyAreas(TeaModel):
    def __init__(
        self,
        local_name: str = None,
        area_id: str = None,
        region_list: List[ListAccelerateAreasResponseBodyAreasRegionList] = None,
    ):
        self.local_name = local_name
        self.area_id = area_id
        self.region_list = region_list

    def validate(self):
        if self.region_list:
            for k in self.region_list:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.local_name is not None:
            result['LocalName'] = self.local_name
        if self.area_id is not None:
            result['AreaId'] = self.area_id
        result['RegionList'] = []
        if self.region_list is not None:
            for k in self.region_list:
                result['RegionList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LocalName') is not None:
            self.local_name = m.get('LocalName')
        if m.get('AreaId') is not None:
            self.area_id = m.get('AreaId')
        self.region_list = []
        if m.get('RegionList') is not None:
            for k in m.get('RegionList'):
                temp_model = ListAccelerateAreasResponseBodyAreasRegionList()
                self.region_list.append(temp_model.from_map(k))
        return self


class ListAccelerateAreasResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        areas: List[ListAccelerateAreasResponseBodyAreas] = None,
    ):
        self.request_id = request_id
        self.areas = areas

    def validate(self):
        if self.areas:
            for k in self.areas:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Areas'] = []
        if self.areas is not None:
            for k in self.areas:
                result['Areas'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.areas = []
        if m.get('Areas') is not None:
            for k in m.get('Areas'):
                temp_model = ListAccelerateAreasResponseBodyAreas()
                self.areas.append(temp_model.from_map(k))
        return self


class ListAccelerateAreasResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListAccelerateAreasResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListAccelerateAreasResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListAcceleratorsRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        page_number: int = None,
        page_size: int = None,
        accelerator_id: str = None,
    ):
        self.region_id = region_id
        self.page_number = page_number
        self.page_size = page_size
        self.accelerator_id = accelerator_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.accelerator_id is not None:
            result['AcceleratorId'] = self.accelerator_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('AcceleratorId') is not None:
            self.accelerator_id = m.get('AcceleratorId')
        return self


class ListAcceleratorsResponseBodyAcceleratorsBasicBandwidthPackage(TeaModel):
    def __init__(
        self,
        bandwidth: int = None,
        bandwidth_type: str = None,
        instance_id: str = None,
    ):
        self.bandwidth = bandwidth
        self.bandwidth_type = bandwidth_type
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.bandwidth is not None:
            result['Bandwidth'] = self.bandwidth
        if self.bandwidth_type is not None:
            result['BandwidthType'] = self.bandwidth_type
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Bandwidth') is not None:
            self.bandwidth = m.get('Bandwidth')
        if m.get('BandwidthType') is not None:
            self.bandwidth_type = m.get('BandwidthType')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class ListAcceleratorsResponseBodyAcceleratorsCrossDomainBandwidthPackage(TeaModel):
    def __init__(
        self,
        bandwidth: int = None,
        instance_id: str = None,
    ):
        self.bandwidth = bandwidth
        self.instance_id = instance_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.bandwidth is not None:
            result['Bandwidth'] = self.bandwidth
        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Bandwidth') is not None:
            self.bandwidth = m.get('Bandwidth')
        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')
        return self


class ListAcceleratorsResponseBodyAccelerators(TeaModel):
    def __init__(
        self,
        dns_name: str = None,
        type: str = None,
        second_dns_name: str = None,
        spec: str = None,
        state: str = None,
        create_time: int = None,
        cen_id: str = None,
        ddos_id: str = None,
        basic_bandwidth_package: ListAcceleratorsResponseBodyAcceleratorsBasicBandwidthPackage = None,
        region_id: str = None,
        instance_charge_type: str = None,
        accelerator_id: str = None,
        description: str = None,
        bandwidth: int = None,
        expired_time: int = None,
        name: str = None,
        cross_domain_bandwidth_package: ListAcceleratorsResponseBodyAcceleratorsCrossDomainBandwidthPackage = None,
    ):
        self.dns_name = dns_name
        self.type = type
        self.second_dns_name = second_dns_name
        self.spec = spec
        self.state = state
        self.create_time = create_time
        self.cen_id = cen_id
        self.ddos_id = ddos_id
        self.basic_bandwidth_package = basic_bandwidth_package
        self.region_id = region_id
        self.instance_charge_type = instance_charge_type
        self.accelerator_id = accelerator_id
        self.description = description
        self.bandwidth = bandwidth
        self.expired_time = expired_time
        self.name = name
        self.cross_domain_bandwidth_package = cross_domain_bandwidth_package

    def validate(self):
        if self.basic_bandwidth_package:
            self.basic_bandwidth_package.validate()
        if self.cross_domain_bandwidth_package:
            self.cross_domain_bandwidth_package.validate()

    def to_map(self):
        result = dict()
        if self.dns_name is not None:
            result['DnsName'] = self.dns_name
        if self.type is not None:
            result['Type'] = self.type
        if self.second_dns_name is not None:
            result['SecondDnsName'] = self.second_dns_name
        if self.spec is not None:
            result['Spec'] = self.spec
        if self.state is not None:
            result['State'] = self.state
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.cen_id is not None:
            result['CenId'] = self.cen_id
        if self.ddos_id is not None:
            result['DdosId'] = self.ddos_id
        if self.basic_bandwidth_package is not None:
            result['BasicBandwidthPackage'] = self.basic_bandwidth_package.to_map()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.instance_charge_type is not None:
            result['InstanceChargeType'] = self.instance_charge_type
        if self.accelerator_id is not None:
            result['AcceleratorId'] = self.accelerator_id
        if self.description is not None:
            result['Description'] = self.description
        if self.bandwidth is not None:
            result['Bandwidth'] = self.bandwidth
        if self.expired_time is not None:
            result['ExpiredTime'] = self.expired_time
        if self.name is not None:
            result['Name'] = self.name
        if self.cross_domain_bandwidth_package is not None:
            result['CrossDomainBandwidthPackage'] = self.cross_domain_bandwidth_package.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DnsName') is not None:
            self.dns_name = m.get('DnsName')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('SecondDnsName') is not None:
            self.second_dns_name = m.get('SecondDnsName')
        if m.get('Spec') is not None:
            self.spec = m.get('Spec')
        if m.get('State') is not None:
            self.state = m.get('State')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('CenId') is not None:
            self.cen_id = m.get('CenId')
        if m.get('DdosId') is not None:
            self.ddos_id = m.get('DdosId')
        if m.get('BasicBandwidthPackage') is not None:
            temp_model = ListAcceleratorsResponseBodyAcceleratorsBasicBandwidthPackage()
            self.basic_bandwidth_package = temp_model.from_map(m['BasicBandwidthPackage'])
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('InstanceChargeType') is not None:
            self.instance_charge_type = m.get('InstanceChargeType')
        if m.get('AcceleratorId') is not None:
            self.accelerator_id = m.get('AcceleratorId')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Bandwidth') is not None:
            self.bandwidth = m.get('Bandwidth')
        if m.get('ExpiredTime') is not None:
            self.expired_time = m.get('ExpiredTime')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('CrossDomainBandwidthPackage') is not None:
            temp_model = ListAcceleratorsResponseBodyAcceleratorsCrossDomainBandwidthPackage()
            self.cross_domain_bandwidth_package = temp_model.from_map(m['CrossDomainBandwidthPackage'])
        return self


class ListAcceleratorsResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        accelerators: List[ListAcceleratorsResponseBodyAccelerators] = None,
        page_number: int = None,
    ):
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.accelerators = accelerators
        self.page_number = page_number

    def validate(self):
        if self.accelerators:
            for k in self.accelerators:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Accelerators'] = []
        if self.accelerators is not None:
            for k in self.accelerators:
                result['Accelerators'].append(k.to_map() if k else None)
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.accelerators = []
        if m.get('Accelerators') is not None:
            for k in m.get('Accelerators'):
                temp_model = ListAcceleratorsResponseBodyAccelerators()
                self.accelerators.append(temp_model.from_map(k))
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        return self


class ListAcceleratorsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListAcceleratorsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListAcceleratorsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListAvailableAccelerateAreasRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        accelerator_id: str = None,
    ):
        self.region_id = region_id
        self.accelerator_id = accelerator_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.accelerator_id is not None:
            result['AcceleratorId'] = self.accelerator_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('AcceleratorId') is not None:
            self.accelerator_id = m.get('AcceleratorId')
        return self


class ListAvailableAccelerateAreasResponseBodyAreasRegionList(TeaModel):
    def __init__(
        self,
        local_name: str = None,
        region_id: str = None,
    ):
        self.local_name = local_name
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.local_name is not None:
            result['LocalName'] = self.local_name
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LocalName') is not None:
            self.local_name = m.get('LocalName')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class ListAvailableAccelerateAreasResponseBodyAreas(TeaModel):
    def __init__(
        self,
        local_name: str = None,
        area_id: str = None,
        region_list: List[ListAvailableAccelerateAreasResponseBodyAreasRegionList] = None,
    ):
        self.local_name = local_name
        self.area_id = area_id
        self.region_list = region_list

    def validate(self):
        if self.region_list:
            for k in self.region_list:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.local_name is not None:
            result['LocalName'] = self.local_name
        if self.area_id is not None:
            result['AreaId'] = self.area_id
        result['RegionList'] = []
        if self.region_list is not None:
            for k in self.region_list:
                result['RegionList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LocalName') is not None:
            self.local_name = m.get('LocalName')
        if m.get('AreaId') is not None:
            self.area_id = m.get('AreaId')
        self.region_list = []
        if m.get('RegionList') is not None:
            for k in m.get('RegionList'):
                temp_model = ListAvailableAccelerateAreasResponseBodyAreasRegionList()
                self.region_list.append(temp_model.from_map(k))
        return self


class ListAvailableAccelerateAreasResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        areas: List[ListAvailableAccelerateAreasResponseBodyAreas] = None,
    ):
        self.request_id = request_id
        self.areas = areas

    def validate(self):
        if self.areas:
            for k in self.areas:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Areas'] = []
        if self.areas is not None:
            for k in self.areas:
                result['Areas'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.areas = []
        if m.get('Areas') is not None:
            for k in m.get('Areas'):
                temp_model = ListAvailableAccelerateAreasResponseBodyAreas()
                self.areas.append(temp_model.from_map(k))
        return self


class ListAvailableAccelerateAreasResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListAvailableAccelerateAreasResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListAvailableAccelerateAreasResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListAvailableBusiRegionsRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        accelerator_id: str = None,
    ):
        self.region_id = region_id
        self.accelerator_id = accelerator_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.accelerator_id is not None:
            result['AcceleratorId'] = self.accelerator_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('AcceleratorId') is not None:
            self.accelerator_id = m.get('AcceleratorId')
        return self


class ListAvailableBusiRegionsResponseBodyRegions(TeaModel):
    def __init__(
        self,
        local_name: str = None,
        region_id: str = None,
    ):
        self.local_name = local_name
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.local_name is not None:
            result['LocalName'] = self.local_name
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LocalName') is not None:
            self.local_name = m.get('LocalName')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class ListAvailableBusiRegionsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        regions: List[ListAvailableBusiRegionsResponseBodyRegions] = None,
    ):
        self.request_id = request_id
        self.regions = regions

    def validate(self):
        if self.regions:
            for k in self.regions:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Regions'] = []
        if self.regions is not None:
            for k in self.regions:
                result['Regions'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.regions = []
        if m.get('Regions') is not None:
            for k in m.get('Regions'):
                temp_model = ListAvailableBusiRegionsResponseBodyRegions()
                self.regions.append(temp_model.from_map(k))
        return self


class ListAvailableBusiRegionsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListAvailableBusiRegionsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListAvailableBusiRegionsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListBandwidthackagesRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        page_number: int = None,
        page_size: int = None,
    ):
        self.region_id = region_id
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class ListBandwidthackagesResponseBodyBandwidthPackages(TeaModel):
    def __init__(
        self,
        bandwidth_package_id: str = None,
        bandwidth: int = None,
        description: str = None,
        expired_time: str = None,
        state: str = None,
        create_time: str = None,
        charge_type: str = None,
        accelerators: List[str] = None,
        name: str = None,
        region_id: str = None,
    ):
        self.bandwidth_package_id = bandwidth_package_id
        self.bandwidth = bandwidth
        self.description = description
        self.expired_time = expired_time
        self.state = state
        self.create_time = create_time
        self.charge_type = charge_type
        self.accelerators = accelerators
        self.name = name
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.bandwidth_package_id is not None:
            result['BandwidthPackageId'] = self.bandwidth_package_id
        if self.bandwidth is not None:
            result['Bandwidth'] = self.bandwidth
        if self.description is not None:
            result['Description'] = self.description
        if self.expired_time is not None:
            result['ExpiredTime'] = self.expired_time
        if self.state is not None:
            result['State'] = self.state
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.charge_type is not None:
            result['ChargeType'] = self.charge_type
        if self.accelerators is not None:
            result['Accelerators'] = self.accelerators
        if self.name is not None:
            result['Name'] = self.name
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BandwidthPackageId') is not None:
            self.bandwidth_package_id = m.get('BandwidthPackageId')
        if m.get('Bandwidth') is not None:
            self.bandwidth = m.get('Bandwidth')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('ExpiredTime') is not None:
            self.expired_time = m.get('ExpiredTime')
        if m.get('State') is not None:
            self.state = m.get('State')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('ChargeType') is not None:
            self.charge_type = m.get('ChargeType')
        if m.get('Accelerators') is not None:
            self.accelerators = m.get('Accelerators')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class ListBandwidthackagesResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        bandwidth_packages: List[ListBandwidthackagesResponseBodyBandwidthPackages] = None,
    ):
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.bandwidth_packages = bandwidth_packages

    def validate(self):
        if self.bandwidth_packages:
            for k in self.bandwidth_packages:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        result['BandwidthPackages'] = []
        if self.bandwidth_packages is not None:
            for k in self.bandwidth_packages:
                result['BandwidthPackages'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        self.bandwidth_packages = []
        if m.get('BandwidthPackages') is not None:
            for k in m.get('BandwidthPackages'):
                temp_model = ListBandwidthackagesResponseBodyBandwidthPackages()
                self.bandwidth_packages.append(temp_model.from_map(k))
        return self


class ListBandwidthackagesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListBandwidthackagesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListBandwidthackagesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListBandwidthPackagesRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        page_number: int = None,
        page_size: int = None,
        state: str = None,
        type: str = None,
        bandwidth_package_id: str = None,
    ):
        self.region_id = region_id
        self.page_number = page_number
        self.page_size = page_size
        self.state = state
        self.type = type
        self.bandwidth_package_id = bandwidth_package_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.state is not None:
            result['State'] = self.state
        if self.type is not None:
            result['Type'] = self.type
        if self.bandwidth_package_id is not None:
            result['BandwidthPackageId'] = self.bandwidth_package_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('State') is not None:
            self.state = m.get('State')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('BandwidthPackageId') is not None:
            self.bandwidth_package_id = m.get('BandwidthPackageId')
        return self


class ListBandwidthPackagesResponseBodyBandwidthPackages(TeaModel):
    def __init__(
        self,
        type: str = None,
        bandwidth_type: str = None,
        state: str = None,
        create_time: str = None,
        charge_type: str = None,
        region_id: str = None,
        cbn_geographic_region_id_a: str = None,
        bandwidth_package_id: str = None,
        bandwidth: int = None,
        description: str = None,
        expired_time: str = None,
        accelerators: List[str] = None,
        cbn_geographic_region_id_b: str = None,
        name: str = None,
        billing_type: str = None,
    ):
        self.type = type
        self.bandwidth_type = bandwidth_type
        self.state = state
        self.create_time = create_time
        self.charge_type = charge_type
        self.region_id = region_id
        self.cbn_geographic_region_id_a = cbn_geographic_region_id_a
        self.bandwidth_package_id = bandwidth_package_id
        self.bandwidth = bandwidth
        self.description = description
        self.expired_time = expired_time
        self.accelerators = accelerators
        self.cbn_geographic_region_id_b = cbn_geographic_region_id_b
        self.name = name
        self.billing_type = billing_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.bandwidth_type is not None:
            result['BandwidthType'] = self.bandwidth_type
        if self.state is not None:
            result['State'] = self.state
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.charge_type is not None:
            result['ChargeType'] = self.charge_type
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.cbn_geographic_region_id_a is not None:
            result['CbnGeographicRegionIdA'] = self.cbn_geographic_region_id_a
        if self.bandwidth_package_id is not None:
            result['BandwidthPackageId'] = self.bandwidth_package_id
        if self.bandwidth is not None:
            result['Bandwidth'] = self.bandwidth
        if self.description is not None:
            result['Description'] = self.description
        if self.expired_time is not None:
            result['ExpiredTime'] = self.expired_time
        if self.accelerators is not None:
            result['Accelerators'] = self.accelerators
        if self.cbn_geographic_region_id_b is not None:
            result['CbnGeographicRegionIdB'] = self.cbn_geographic_region_id_b
        if self.name is not None:
            result['Name'] = self.name
        if self.billing_type is not None:
            result['BillingType'] = self.billing_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('BandwidthType') is not None:
            self.bandwidth_type = m.get('BandwidthType')
        if m.get('State') is not None:
            self.state = m.get('State')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('ChargeType') is not None:
            self.charge_type = m.get('ChargeType')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('CbnGeographicRegionIdA') is not None:
            self.cbn_geographic_region_id_a = m.get('CbnGeographicRegionIdA')
        if m.get('BandwidthPackageId') is not None:
            self.bandwidth_package_id = m.get('BandwidthPackageId')
        if m.get('Bandwidth') is not None:
            self.bandwidth = m.get('Bandwidth')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('ExpiredTime') is not None:
            self.expired_time = m.get('ExpiredTime')
        if m.get('Accelerators') is not None:
            self.accelerators = m.get('Accelerators')
        if m.get('CbnGeographicRegionIdB') is not None:
            self.cbn_geographic_region_id_b = m.get('CbnGeographicRegionIdB')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('BillingType') is not None:
            self.billing_type = m.get('BillingType')
        return self


class ListBandwidthPackagesResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        bandwidth_packages: List[ListBandwidthPackagesResponseBodyBandwidthPackages] = None,
    ):
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.bandwidth_packages = bandwidth_packages

    def validate(self):
        if self.bandwidth_packages:
            for k in self.bandwidth_packages:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        result['BandwidthPackages'] = []
        if self.bandwidth_packages is not None:
            for k in self.bandwidth_packages:
                result['BandwidthPackages'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        self.bandwidth_packages = []
        if m.get('BandwidthPackages') is not None:
            for k in m.get('BandwidthPackages'):
                temp_model = ListBandwidthPackagesResponseBodyBandwidthPackages()
                self.bandwidth_packages.append(temp_model.from_map(k))
        return self


class ListBandwidthPackagesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListBandwidthPackagesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListBandwidthPackagesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListBusiRegionsRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
    ):
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class ListBusiRegionsResponseBodyRegions(TeaModel):
    def __init__(
        self,
        local_name: str = None,
        region_id: str = None,
    ):
        self.local_name = local_name
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.local_name is not None:
            result['LocalName'] = self.local_name
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LocalName') is not None:
            self.local_name = m.get('LocalName')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class ListBusiRegionsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        regions: List[ListBusiRegionsResponseBodyRegions] = None,
    ):
        self.request_id = request_id
        self.regions = regions

    def validate(self):
        if self.regions:
            for k in self.regions:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        result['Regions'] = []
        if self.regions is not None:
            for k in self.regions:
                result['Regions'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        self.regions = []
        if m.get('Regions') is not None:
            for k in m.get('Regions'):
                temp_model = ListBusiRegionsResponseBodyRegions()
                self.regions.append(temp_model.from_map(k))
        return self


class ListBusiRegionsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListBusiRegionsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListBusiRegionsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListEndpointGroupsRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        page_number: int = None,
        page_size: int = None,
        accelerator_id: str = None,
        listener_id: str = None,
        endpoint_group_type: str = None,
    ):
        self.region_id = region_id
        self.page_number = page_number
        self.page_size = page_size
        self.accelerator_id = accelerator_id
        self.listener_id = listener_id
        self.endpoint_group_type = endpoint_group_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.accelerator_id is not None:
            result['AcceleratorId'] = self.accelerator_id
        if self.listener_id is not None:
            result['ListenerId'] = self.listener_id
        if self.endpoint_group_type is not None:
            result['EndpointGroupType'] = self.endpoint_group_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('AcceleratorId') is not None:
            self.accelerator_id = m.get('AcceleratorId')
        if m.get('ListenerId') is not None:
            self.listener_id = m.get('ListenerId')
        if m.get('EndpointGroupType') is not None:
            self.endpoint_group_type = m.get('EndpointGroupType')
        return self


class ListEndpointGroupsResponseBodyEndpointGroupsEndpointConfigurations(TeaModel):
    def __init__(
        self,
        type: str = None,
        enable_client_ippreservation: bool = None,
        weight: int = None,
        probe_protocol: str = None,
        endpoint: str = None,
        probe_port: int = None,
    ):
        self.type = type
        self.enable_client_ippreservation = enable_client_ippreservation
        self.weight = weight
        self.probe_protocol = probe_protocol
        self.endpoint = endpoint
        self.probe_port = probe_port

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.enable_client_ippreservation is not None:
            result['EnableClientIPPreservation'] = self.enable_client_ippreservation
        if self.weight is not None:
            result['Weight'] = self.weight
        if self.probe_protocol is not None:
            result['ProbeProtocol'] = self.probe_protocol
        if self.endpoint is not None:
            result['Endpoint'] = self.endpoint
        if self.probe_port is not None:
            result['ProbePort'] = self.probe_port
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('EnableClientIPPreservation') is not None:
            self.enable_client_ippreservation = m.get('EnableClientIPPreservation')
        if m.get('Weight') is not None:
            self.weight = m.get('Weight')
        if m.get('ProbeProtocol') is not None:
            self.probe_protocol = m.get('ProbeProtocol')
        if m.get('Endpoint') is not None:
            self.endpoint = m.get('Endpoint')
        if m.get('ProbePort') is not None:
            self.probe_port = m.get('ProbePort')
        return self


class ListEndpointGroupsResponseBodyEndpointGroupsPortOverrides(TeaModel):
    def __init__(
        self,
        listener_port: int = None,
        endpoint_port: int = None,
    ):
        self.listener_port = listener_port
        self.endpoint_port = endpoint_port

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.listener_port is not None:
            result['ListenerPort'] = self.listener_port
        if self.endpoint_port is not None:
            result['EndpointPort'] = self.endpoint_port
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ListenerPort') is not None:
            self.listener_port = m.get('ListenerPort')
        if m.get('EndpointPort') is not None:
            self.endpoint_port = m.get('EndpointPort')
        return self


class ListEndpointGroupsResponseBodyEndpointGroups(TeaModel):
    def __init__(
        self,
        endpoint_group_id: str = None,
        endpoint_group_ip_list: List[str] = None,
        state: str = None,
        health_check_path: str = None,
        endpoint_group_region: str = None,
        health_check_interval_seconds: int = None,
        traffic_percentage: int = None,
        health_check_protocol: str = None,
        threshold_count: int = None,
        listener_id: str = None,
        endpoint_configurations: List[ListEndpointGroupsResponseBodyEndpointGroupsEndpointConfigurations] = None,
        port_overrides: List[ListEndpointGroupsResponseBodyEndpointGroupsPortOverrides] = None,
        forwarding_rule_ids: List[str] = None,
        endpoint_group_type: str = None,
        endpoint_request_protocol: str = None,
        description: str = None,
        name: str = None,
        health_check_port: int = None,
    ):
        self.endpoint_group_id = endpoint_group_id
        self.endpoint_group_ip_list = endpoint_group_ip_list
        self.state = state
        self.health_check_path = health_check_path
        self.endpoint_group_region = endpoint_group_region
        self.health_check_interval_seconds = health_check_interval_seconds
        self.traffic_percentage = traffic_percentage
        self.health_check_protocol = health_check_protocol
        self.threshold_count = threshold_count
        self.listener_id = listener_id
        self.endpoint_configurations = endpoint_configurations
        self.port_overrides = port_overrides
        self.forwarding_rule_ids = forwarding_rule_ids
        self.endpoint_group_type = endpoint_group_type
        self.endpoint_request_protocol = endpoint_request_protocol
        self.description = description
        self.name = name
        self.health_check_port = health_check_port

    def validate(self):
        if self.endpoint_configurations:
            for k in self.endpoint_configurations:
                if k:
                    k.validate()
        if self.port_overrides:
            for k in self.port_overrides:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.endpoint_group_id is not None:
            result['EndpointGroupId'] = self.endpoint_group_id
        if self.endpoint_group_ip_list is not None:
            result['EndpointGroupIpList'] = self.endpoint_group_ip_list
        if self.state is not None:
            result['State'] = self.state
        if self.health_check_path is not None:
            result['HealthCheckPath'] = self.health_check_path
        if self.endpoint_group_region is not None:
            result['EndpointGroupRegion'] = self.endpoint_group_region
        if self.health_check_interval_seconds is not None:
            result['HealthCheckIntervalSeconds'] = self.health_check_interval_seconds
        if self.traffic_percentage is not None:
            result['TrafficPercentage'] = self.traffic_percentage
        if self.health_check_protocol is not None:
            result['HealthCheckProtocol'] = self.health_check_protocol
        if self.threshold_count is not None:
            result['ThresholdCount'] = self.threshold_count
        if self.listener_id is not None:
            result['ListenerId'] = self.listener_id
        result['EndpointConfigurations'] = []
        if self.endpoint_configurations is not None:
            for k in self.endpoint_configurations:
                result['EndpointConfigurations'].append(k.to_map() if k else None)
        result['PortOverrides'] = []
        if self.port_overrides is not None:
            for k in self.port_overrides:
                result['PortOverrides'].append(k.to_map() if k else None)
        if self.forwarding_rule_ids is not None:
            result['ForwardingRuleIds'] = self.forwarding_rule_ids
        if self.endpoint_group_type is not None:
            result['EndpointGroupType'] = self.endpoint_group_type
        if self.endpoint_request_protocol is not None:
            result['EndpointRequestProtocol'] = self.endpoint_request_protocol
        if self.description is not None:
            result['Description'] = self.description
        if self.name is not None:
            result['Name'] = self.name
        if self.health_check_port is not None:
            result['HealthCheckPort'] = self.health_check_port
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndpointGroupId') is not None:
            self.endpoint_group_id = m.get('EndpointGroupId')
        if m.get('EndpointGroupIpList') is not None:
            self.endpoint_group_ip_list = m.get('EndpointGroupIpList')
        if m.get('State') is not None:
            self.state = m.get('State')
        if m.get('HealthCheckPath') is not None:
            self.health_check_path = m.get('HealthCheckPath')
        if m.get('EndpointGroupRegion') is not None:
            self.endpoint_group_region = m.get('EndpointGroupRegion')
        if m.get('HealthCheckIntervalSeconds') is not None:
            self.health_check_interval_seconds = m.get('HealthCheckIntervalSeconds')
        if m.get('TrafficPercentage') is not None:
            self.traffic_percentage = m.get('TrafficPercentage')
        if m.get('HealthCheckProtocol') is not None:
            self.health_check_protocol = m.get('HealthCheckProtocol')
        if m.get('ThresholdCount') is not None:
            self.threshold_count = m.get('ThresholdCount')
        if m.get('ListenerId') is not None:
            self.listener_id = m.get('ListenerId')
        self.endpoint_configurations = []
        if m.get('EndpointConfigurations') is not None:
            for k in m.get('EndpointConfigurations'):
                temp_model = ListEndpointGroupsResponseBodyEndpointGroupsEndpointConfigurations()
                self.endpoint_configurations.append(temp_model.from_map(k))
        self.port_overrides = []
        if m.get('PortOverrides') is not None:
            for k in m.get('PortOverrides'):
                temp_model = ListEndpointGroupsResponseBodyEndpointGroupsPortOverrides()
                self.port_overrides.append(temp_model.from_map(k))
        if m.get('ForwardingRuleIds') is not None:
            self.forwarding_rule_ids = m.get('ForwardingRuleIds')
        if m.get('EndpointGroupType') is not None:
            self.endpoint_group_type = m.get('EndpointGroupType')
        if m.get('EndpointRequestProtocol') is not None:
            self.endpoint_request_protocol = m.get('EndpointRequestProtocol')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('HealthCheckPort') is not None:
            self.health_check_port = m.get('HealthCheckPort')
        return self


class ListEndpointGroupsResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        endpoint_groups: List[ListEndpointGroupsResponseBodyEndpointGroups] = None,
    ):
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.endpoint_groups = endpoint_groups

    def validate(self):
        if self.endpoint_groups:
            for k in self.endpoint_groups:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        result['EndpointGroups'] = []
        if self.endpoint_groups is not None:
            for k in self.endpoint_groups:
                result['EndpointGroups'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        self.endpoint_groups = []
        if m.get('EndpointGroups') is not None:
            for k in m.get('EndpointGroups'):
                temp_model = ListEndpointGroupsResponseBodyEndpointGroups()
                self.endpoint_groups.append(temp_model.from_map(k))
        return self


class ListEndpointGroupsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListEndpointGroupsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListEndpointGroupsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListForwardingRulesRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        client_token: str = None,
        listener_id: str = None,
        accelerator_id: str = None,
        forwarding_rule_id: str = None,
        next_token: str = None,
        max_results: int = None,
    ):
        self.region_id = region_id
        self.client_token = client_token
        self.listener_id = listener_id
        self.accelerator_id = accelerator_id
        self.forwarding_rule_id = forwarding_rule_id
        self.next_token = next_token
        self.max_results = max_results

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.listener_id is not None:
            result['ListenerId'] = self.listener_id
        if self.accelerator_id is not None:
            result['AcceleratorId'] = self.accelerator_id
        if self.forwarding_rule_id is not None:
            result['ForwardingRuleId'] = self.forwarding_rule_id
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('ListenerId') is not None:
            self.listener_id = m.get('ListenerId')
        if m.get('AcceleratorId') is not None:
            self.accelerator_id = m.get('AcceleratorId')
        if m.get('ForwardingRuleId') is not None:
            self.forwarding_rule_id = m.get('ForwardingRuleId')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        return self


class ListForwardingRulesResponseBodyForwardingRulesRuleConditionsPathConfig(TeaModel):
    def __init__(
        self,
        values: List[str] = None,
    ):
        self.values = values

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.values is not None:
            result['Values'] = self.values
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Values') is not None:
            self.values = m.get('Values')
        return self


class ListForwardingRulesResponseBodyForwardingRulesRuleConditionsHostConfig(TeaModel):
    def __init__(
        self,
        values: List[str] = None,
    ):
        self.values = values

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.values is not None:
            result['Values'] = self.values
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Values') is not None:
            self.values = m.get('Values')
        return self


class ListForwardingRulesResponseBodyForwardingRulesRuleConditions(TeaModel):
    def __init__(
        self,
        rule_condition_type: str = None,
        path_config: ListForwardingRulesResponseBodyForwardingRulesRuleConditionsPathConfig = None,
        host_config: ListForwardingRulesResponseBodyForwardingRulesRuleConditionsHostConfig = None,
    ):
        self.rule_condition_type = rule_condition_type
        self.path_config = path_config
        self.host_config = host_config

    def validate(self):
        if self.path_config:
            self.path_config.validate()
        if self.host_config:
            self.host_config.validate()

    def to_map(self):
        result = dict()
        if self.rule_condition_type is not None:
            result['RuleConditionType'] = self.rule_condition_type
        if self.path_config is not None:
            result['PathConfig'] = self.path_config.to_map()
        if self.host_config is not None:
            result['HostConfig'] = self.host_config.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RuleConditionType') is not None:
            self.rule_condition_type = m.get('RuleConditionType')
        if m.get('PathConfig') is not None:
            temp_model = ListForwardingRulesResponseBodyForwardingRulesRuleConditionsPathConfig()
            self.path_config = temp_model.from_map(m['PathConfig'])
        if m.get('HostConfig') is not None:
            temp_model = ListForwardingRulesResponseBodyForwardingRulesRuleConditionsHostConfig()
            self.host_config = temp_model.from_map(m['HostConfig'])
        return self


class ListForwardingRulesResponseBodyForwardingRulesRuleActionsForwardGroupConfigServerGroupTuples(TeaModel):
    def __init__(
        self,
        endpoint_group_id: str = None,
    ):
        self.endpoint_group_id = endpoint_group_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.endpoint_group_id is not None:
            result['EndpointGroupId'] = self.endpoint_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndpointGroupId') is not None:
            self.endpoint_group_id = m.get('EndpointGroupId')
        return self


class ListForwardingRulesResponseBodyForwardingRulesRuleActionsForwardGroupConfig(TeaModel):
    def __init__(
        self,
        server_group_tuples: List[ListForwardingRulesResponseBodyForwardingRulesRuleActionsForwardGroupConfigServerGroupTuples] = None,
    ):
        self.server_group_tuples = server_group_tuples

    def validate(self):
        if self.server_group_tuples:
            for k in self.server_group_tuples:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['ServerGroupTuples'] = []
        if self.server_group_tuples is not None:
            for k in self.server_group_tuples:
                result['ServerGroupTuples'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.server_group_tuples = []
        if m.get('ServerGroupTuples') is not None:
            for k in m.get('ServerGroupTuples'):
                temp_model = ListForwardingRulesResponseBodyForwardingRulesRuleActionsForwardGroupConfigServerGroupTuples()
                self.server_group_tuples.append(temp_model.from_map(k))
        return self


class ListForwardingRulesResponseBodyForwardingRulesRuleActions(TeaModel):
    def __init__(
        self,
        order: int = None,
        rule_action_type: str = None,
        forward_group_config: ListForwardingRulesResponseBodyForwardingRulesRuleActionsForwardGroupConfig = None,
    ):
        self.order = order
        self.rule_action_type = rule_action_type
        self.forward_group_config = forward_group_config

    def validate(self):
        if self.forward_group_config:
            self.forward_group_config.validate()

    def to_map(self):
        result = dict()
        if self.order is not None:
            result['Order'] = self.order
        if self.rule_action_type is not None:
            result['RuleActionType'] = self.rule_action_type
        if self.forward_group_config is not None:
            result['ForwardGroupConfig'] = self.forward_group_config.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('RuleActionType') is not None:
            self.rule_action_type = m.get('RuleActionType')
        if m.get('ForwardGroupConfig') is not None:
            temp_model = ListForwardingRulesResponseBodyForwardingRulesRuleActionsForwardGroupConfig()
            self.forward_group_config = temp_model.from_map(m['ForwardGroupConfig'])
        return self


class ListForwardingRulesResponseBodyForwardingRules(TeaModel):
    def __init__(
        self,
        priority: int = None,
        forwarding_rule_id: str = None,
        forwarding_rule_name: str = None,
        forwarding_rule_status: str = None,
        rule_conditions: List[ListForwardingRulesResponseBodyForwardingRulesRuleConditions] = None,
        rule_actions: List[ListForwardingRulesResponseBodyForwardingRulesRuleActions] = None,
        listener_id: str = None,
    ):
        self.priority = priority
        self.forwarding_rule_id = forwarding_rule_id
        self.forwarding_rule_name = forwarding_rule_name
        self.forwarding_rule_status = forwarding_rule_status
        self.rule_conditions = rule_conditions
        self.rule_actions = rule_actions
        self.listener_id = listener_id

    def validate(self):
        if self.rule_conditions:
            for k in self.rule_conditions:
                if k:
                    k.validate()
        if self.rule_actions:
            for k in self.rule_actions:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.priority is not None:
            result['Priority'] = self.priority
        if self.forwarding_rule_id is not None:
            result['ForwardingRuleId'] = self.forwarding_rule_id
        if self.forwarding_rule_name is not None:
            result['ForwardingRuleName'] = self.forwarding_rule_name
        if self.forwarding_rule_status is not None:
            result['ForwardingRuleStatus'] = self.forwarding_rule_status
        result['RuleConditions'] = []
        if self.rule_conditions is not None:
            for k in self.rule_conditions:
                result['RuleConditions'].append(k.to_map() if k else None)
        result['RuleActions'] = []
        if self.rule_actions is not None:
            for k in self.rule_actions:
                result['RuleActions'].append(k.to_map() if k else None)
        if self.listener_id is not None:
            result['ListenerId'] = self.listener_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Priority') is not None:
            self.priority = m.get('Priority')
        if m.get('ForwardingRuleId') is not None:
            self.forwarding_rule_id = m.get('ForwardingRuleId')
        if m.get('ForwardingRuleName') is not None:
            self.forwarding_rule_name = m.get('ForwardingRuleName')
        if m.get('ForwardingRuleStatus') is not None:
            self.forwarding_rule_status = m.get('ForwardingRuleStatus')
        self.rule_conditions = []
        if m.get('RuleConditions') is not None:
            for k in m.get('RuleConditions'):
                temp_model = ListForwardingRulesResponseBodyForwardingRulesRuleConditions()
                self.rule_conditions.append(temp_model.from_map(k))
        self.rule_actions = []
        if m.get('RuleActions') is not None:
            for k in m.get('RuleActions'):
                temp_model = ListForwardingRulesResponseBodyForwardingRulesRuleActions()
                self.rule_actions.append(temp_model.from_map(k))
        if m.get('ListenerId') is not None:
            self.listener_id = m.get('ListenerId')
        return self


class ListForwardingRulesResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        total_count: int = None,
        next_token: str = None,
        max_results: int = None,
        forwarding_rules: List[ListForwardingRulesResponseBodyForwardingRules] = None,
    ):
        self.request_id = request_id
        self.total_count = total_count
        self.next_token = next_token
        self.max_results = max_results
        self.forwarding_rules = forwarding_rules

    def validate(self):
        if self.forwarding_rules:
            for k in self.forwarding_rules:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.max_results is not None:
            result['MaxResults'] = self.max_results
        result['ForwardingRules'] = []
        if self.forwarding_rules is not None:
            for k in self.forwarding_rules:
                result['ForwardingRules'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('MaxResults') is not None:
            self.max_results = m.get('MaxResults')
        self.forwarding_rules = []
        if m.get('ForwardingRules') is not None:
            for k in m.get('ForwardingRules'):
                temp_model = ListForwardingRulesResponseBodyForwardingRules()
                self.forwarding_rules.append(temp_model.from_map(k))
        return self


class ListForwardingRulesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListForwardingRulesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListForwardingRulesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListIpSetsRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        page_number: int = None,
        page_size: int = None,
        accelerator_id: str = None,
    ):
        self.region_id = region_id
        self.page_number = page_number
        self.page_size = page_size
        self.accelerator_id = accelerator_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.accelerator_id is not None:
            result['AcceleratorId'] = self.accelerator_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('AcceleratorId') is not None:
            self.accelerator_id = m.get('AcceleratorId')
        return self


class ListIpSetsResponseBodyIpSets(TeaModel):
    def __init__(
        self,
        accelerate_region_id: str = None,
        ip_version: str = None,
        bandwidth: int = None,
        state: str = None,
        ip_set_id: str = None,
        ip_address_list: List[str] = None,
    ):
        self.accelerate_region_id = accelerate_region_id
        self.ip_version = ip_version
        self.bandwidth = bandwidth
        self.state = state
        self.ip_set_id = ip_set_id
        self.ip_address_list = ip_address_list

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.accelerate_region_id is not None:
            result['AccelerateRegionId'] = self.accelerate_region_id
        if self.ip_version is not None:
            result['IpVersion'] = self.ip_version
        if self.bandwidth is not None:
            result['Bandwidth'] = self.bandwidth
        if self.state is not None:
            result['State'] = self.state
        if self.ip_set_id is not None:
            result['IpSetId'] = self.ip_set_id
        if self.ip_address_list is not None:
            result['IpAddressList'] = self.ip_address_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccelerateRegionId') is not None:
            self.accelerate_region_id = m.get('AccelerateRegionId')
        if m.get('IpVersion') is not None:
            self.ip_version = m.get('IpVersion')
        if m.get('Bandwidth') is not None:
            self.bandwidth = m.get('Bandwidth')
        if m.get('State') is not None:
            self.state = m.get('State')
        if m.get('IpSetId') is not None:
            self.ip_set_id = m.get('IpSetId')
        if m.get('IpAddressList') is not None:
            self.ip_address_list = m.get('IpAddressList')
        return self


class ListIpSetsResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
        ip_sets: List[ListIpSetsResponseBodyIpSets] = None,
    ):
        self.total_count = total_count
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number
        self.ip_sets = ip_sets

    def validate(self):
        if self.ip_sets:
            for k in self.ip_sets:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        result['IpSets'] = []
        if self.ip_sets is not None:
            for k in self.ip_sets:
                result['IpSets'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        self.ip_sets = []
        if m.get('IpSets') is not None:
            for k in m.get('IpSets'):
                temp_model = ListIpSetsResponseBodyIpSets()
                self.ip_sets.append(temp_model.from_map(k))
        return self


class ListIpSetsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListIpSetsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListIpSetsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListListenersRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        page_number: int = None,
        page_size: int = None,
        accelerator_id: str = None,
    ):
        self.region_id = region_id
        self.page_number = page_number
        self.page_size = page_size
        self.accelerator_id = accelerator_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.accelerator_id is not None:
            result['AcceleratorId'] = self.accelerator_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('AcceleratorId') is not None:
            self.accelerator_id = m.get('AcceleratorId')
        return self


class ListListenersResponseBodyListenersCertificates(TeaModel):
    def __init__(
        self,
        type: str = None,
        id: str = None,
    ):
        self.type = type
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class ListListenersResponseBodyListenersBackendPorts(TeaModel):
    def __init__(
        self,
        from_port: str = None,
        to_port: str = None,
    ):
        self.from_port = from_port
        self.to_port = to_port

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.from_port is not None:
            result['FromPort'] = self.from_port
        if self.to_port is not None:
            result['ToPort'] = self.to_port
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FromPort') is not None:
            self.from_port = m.get('FromPort')
        if m.get('ToPort') is not None:
            self.to_port = m.get('ToPort')
        return self


class ListListenersResponseBodyListenersPortRanges(TeaModel):
    def __init__(
        self,
        from_port: int = None,
        to_port: int = None,
    ):
        self.from_port = from_port
        self.to_port = to_port

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.from_port is not None:
            result['FromPort'] = self.from_port
        if self.to_port is not None:
            result['ToPort'] = self.to_port
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FromPort') is not None:
            self.from_port = m.get('FromPort')
        if m.get('ToPort') is not None:
            self.to_port = m.get('ToPort')
        return self


class ListListenersResponseBodyListeners(TeaModel):
    def __init__(
        self,
        certificates: List[ListListenersResponseBodyListenersCertificates] = None,
        backend_ports: List[ListListenersResponseBodyListenersBackendPorts] = None,
        listener_id: str = None,
        description: str = None,
        state: str = None,
        client_affinity: str = None,
        protocol: str = None,
        create_time: int = None,
        port_ranges: List[ListListenersResponseBodyListenersPortRanges] = None,
        name: str = None,
        proxy_protocol: bool = None,
    ):
        self.certificates = certificates
        self.backend_ports = backend_ports
        self.listener_id = listener_id
        self.description = description
        self.state = state
        self.client_affinity = client_affinity
        self.protocol = protocol
        self.create_time = create_time
        self.port_ranges = port_ranges
        self.name = name
        self.proxy_protocol = proxy_protocol

    def validate(self):
        if self.certificates:
            for k in self.certificates:
                if k:
                    k.validate()
        if self.backend_ports:
            for k in self.backend_ports:
                if k:
                    k.validate()
        if self.port_ranges:
            for k in self.port_ranges:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Certificates'] = []
        if self.certificates is not None:
            for k in self.certificates:
                result['Certificates'].append(k.to_map() if k else None)
        result['BackendPorts'] = []
        if self.backend_ports is not None:
            for k in self.backend_ports:
                result['BackendPorts'].append(k.to_map() if k else None)
        if self.listener_id is not None:
            result['ListenerId'] = self.listener_id
        if self.description is not None:
            result['Description'] = self.description
        if self.state is not None:
            result['State'] = self.state
        if self.client_affinity is not None:
            result['ClientAffinity'] = self.client_affinity
        if self.protocol is not None:
            result['Protocol'] = self.protocol
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        result['PortRanges'] = []
        if self.port_ranges is not None:
            for k in self.port_ranges:
                result['PortRanges'].append(k.to_map() if k else None)
        if self.name is not None:
            result['Name'] = self.name
        if self.proxy_protocol is not None:
            result['ProxyProtocol'] = self.proxy_protocol
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.certificates = []
        if m.get('Certificates') is not None:
            for k in m.get('Certificates'):
                temp_model = ListListenersResponseBodyListenersCertificates()
                self.certificates.append(temp_model.from_map(k))
        self.backend_ports = []
        if m.get('BackendPorts') is not None:
            for k in m.get('BackendPorts'):
                temp_model = ListListenersResponseBodyListenersBackendPorts()
                self.backend_ports.append(temp_model.from_map(k))
        if m.get('ListenerId') is not None:
            self.listener_id = m.get('ListenerId')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('State') is not None:
            self.state = m.get('State')
        if m.get('ClientAffinity') is not None:
            self.client_affinity = m.get('ClientAffinity')
        if m.get('Protocol') is not None:
            self.protocol = m.get('Protocol')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        self.port_ranges = []
        if m.get('PortRanges') is not None:
            for k in m.get('PortRanges'):
                temp_model = ListListenersResponseBodyListenersPortRanges()
                self.port_ranges.append(temp_model.from_map(k))
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('ProxyProtocol') is not None:
            self.proxy_protocol = m.get('ProxyProtocol')
        return self


class ListListenersResponseBody(TeaModel):
    def __init__(
        self,
        total_count: int = None,
        listeners: List[ListListenersResponseBodyListeners] = None,
        page_size: int = None,
        request_id: str = None,
        page_number: int = None,
    ):
        self.total_count = total_count
        self.listeners = listeners
        self.page_size = page_size
        self.request_id = request_id
        self.page_number = page_number

    def validate(self):
        if self.listeners:
            for k in self.listeners:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.total_count is not None:
            result['TotalCount'] = self.total_count
        result['Listeners'] = []
        if self.listeners is not None:
            for k in self.listeners:
                result['Listeners'].append(k.to_map() if k else None)
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TotalCount') is not None:
            self.total_count = m.get('TotalCount')
        self.listeners = []
        if m.get('Listeners') is not None:
            for k in m.get('Listeners'):
                temp_model = ListListenersResponseBodyListeners()
                self.listeners.append(temp_model.from_map(k))
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        return self


class ListListenersResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListListenersResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListListenersResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ReplaceBandwidthPackageRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        bandwidth_package_id: str = None,
        target_bandwidth_package_id: str = None,
    ):
        self.region_id = region_id
        self.bandwidth_package_id = bandwidth_package_id
        self.target_bandwidth_package_id = target_bandwidth_package_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.bandwidth_package_id is not None:
            result['BandwidthPackageId'] = self.bandwidth_package_id
        if self.target_bandwidth_package_id is not None:
            result['TargetBandwidthPackageId'] = self.target_bandwidth_package_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('BandwidthPackageId') is not None:
            self.bandwidth_package_id = m.get('BandwidthPackageId')
        if m.get('TargetBandwidthPackageId') is not None:
            self.target_bandwidth_package_id = m.get('TargetBandwidthPackageId')
        return self


class ReplaceBandwidthPackageResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ReplaceBandwidthPackageResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ReplaceBandwidthPackageResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ReplaceBandwidthPackageResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateAcceleratorRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        client_token: str = None,
        name: str = None,
        description: str = None,
        accelerator_id: str = None,
        spec: str = None,
        auto_pay: bool = None,
        auto_use_coupon: bool = None,
        promotion_option_no: str = None,
    ):
        self.region_id = region_id
        self.client_token = client_token
        self.name = name
        self.description = description
        self.accelerator_id = accelerator_id
        self.spec = spec
        self.auto_pay = auto_pay
        self.auto_use_coupon = auto_use_coupon
        self.promotion_option_no = promotion_option_no

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.name is not None:
            result['Name'] = self.name
        if self.description is not None:
            result['Description'] = self.description
        if self.accelerator_id is not None:
            result['AcceleratorId'] = self.accelerator_id
        if self.spec is not None:
            result['Spec'] = self.spec
        if self.auto_pay is not None:
            result['AutoPay'] = self.auto_pay
        if self.auto_use_coupon is not None:
            result['AutoUseCoupon'] = self.auto_use_coupon
        if self.promotion_option_no is not None:
            result['PromotionOptionNo'] = self.promotion_option_no
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('AcceleratorId') is not None:
            self.accelerator_id = m.get('AcceleratorId')
        if m.get('Spec') is not None:
            self.spec = m.get('Spec')
        if m.get('AutoPay') is not None:
            self.auto_pay = m.get('AutoPay')
        if m.get('AutoUseCoupon') is not None:
            self.auto_use_coupon = m.get('AutoUseCoupon')
        if m.get('PromotionOptionNo') is not None:
            self.promotion_option_no = m.get('PromotionOptionNo')
        return self


class UpdateAcceleratorResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateAcceleratorResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateAcceleratorResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateAcceleratorResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateBandwidthPackageRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        bandwidth_package_id: str = None,
        name: str = None,
        description: str = None,
        bandwidth: int = None,
        bandwidth_type: str = None,
        auto_pay: bool = None,
        auto_use_coupon: bool = None,
        promotion_option_no: str = None,
    ):
        self.region_id = region_id
        self.bandwidth_package_id = bandwidth_package_id
        self.name = name
        self.description = description
        self.bandwidth = bandwidth
        self.bandwidth_type = bandwidth_type
        self.auto_pay = auto_pay
        self.auto_use_coupon = auto_use_coupon
        self.promotion_option_no = promotion_option_no

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.bandwidth_package_id is not None:
            result['BandwidthPackageId'] = self.bandwidth_package_id
        if self.name is not None:
            result['Name'] = self.name
        if self.description is not None:
            result['Description'] = self.description
        if self.bandwidth is not None:
            result['Bandwidth'] = self.bandwidth
        if self.bandwidth_type is not None:
            result['BandwidthType'] = self.bandwidth_type
        if self.auto_pay is not None:
            result['AutoPay'] = self.auto_pay
        if self.auto_use_coupon is not None:
            result['AutoUseCoupon'] = self.auto_use_coupon
        if self.promotion_option_no is not None:
            result['PromotionOptionNo'] = self.promotion_option_no
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('BandwidthPackageId') is not None:
            self.bandwidth_package_id = m.get('BandwidthPackageId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Bandwidth') is not None:
            self.bandwidth = m.get('Bandwidth')
        if m.get('BandwidthType') is not None:
            self.bandwidth_type = m.get('BandwidthType')
        if m.get('AutoPay') is not None:
            self.auto_pay = m.get('AutoPay')
        if m.get('AutoUseCoupon') is not None:
            self.auto_use_coupon = m.get('AutoUseCoupon')
        if m.get('PromotionOptionNo') is not None:
            self.promotion_option_no = m.get('PromotionOptionNo')
        return self


class UpdateBandwidthPackageResponseBody(TeaModel):
    def __init__(
        self,
        bandwidth_package: str = None,
        description: str = None,
        request_id: str = None,
        name: str = None,
    ):
        self.bandwidth_package = bandwidth_package
        self.description = description
        self.request_id = request_id
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.bandwidth_package is not None:
            result['BandwidthPackage'] = self.bandwidth_package
        if self.description is not None:
            result['Description'] = self.description
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BandwidthPackage') is not None:
            self.bandwidth_package = m.get('BandwidthPackage')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class UpdateBandwidthPackageResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateBandwidthPackageResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateBandwidthPackageResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateEndpointGroupRequestEndpointConfigurations(TeaModel):
    def __init__(
        self,
        type: str = None,
        enable_client_ippreservation: bool = None,
        weight: int = None,
        endpoint: str = None,
    ):
        self.type = type
        self.enable_client_ippreservation = enable_client_ippreservation
        self.weight = weight
        self.endpoint = endpoint

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.enable_client_ippreservation is not None:
            result['EnableClientIPPreservation'] = self.enable_client_ippreservation
        if self.weight is not None:
            result['Weight'] = self.weight
        if self.endpoint is not None:
            result['Endpoint'] = self.endpoint
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('EnableClientIPPreservation') is not None:
            self.enable_client_ippreservation = m.get('EnableClientIPPreservation')
        if m.get('Weight') is not None:
            self.weight = m.get('Weight')
        if m.get('Endpoint') is not None:
            self.endpoint = m.get('Endpoint')
        return self


class UpdateEndpointGroupRequestPortOverrides(TeaModel):
    def __init__(
        self,
        listener_port: int = None,
        endpoint_port: int = None,
    ):
        self.listener_port = listener_port
        self.endpoint_port = endpoint_port

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.listener_port is not None:
            result['ListenerPort'] = self.listener_port
        if self.endpoint_port is not None:
            result['EndpointPort'] = self.endpoint_port
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ListenerPort') is not None:
            self.listener_port = m.get('ListenerPort')
        if m.get('EndpointPort') is not None:
            self.endpoint_port = m.get('EndpointPort')
        return self


class UpdateEndpointGroupRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        client_token: str = None,
        endpoint_group_id: str = None,
        name: str = None,
        description: str = None,
        endpoint_group_region: str = None,
        traffic_percentage: int = None,
        health_check_interval_seconds: int = None,
        health_check_path: str = None,
        health_check_port: int = None,
        health_check_protocol: str = None,
        threshold_count: int = None,
        endpoint_configurations: List[UpdateEndpointGroupRequestEndpointConfigurations] = None,
        endpoint_request_protocol: str = None,
        port_overrides: List[UpdateEndpointGroupRequestPortOverrides] = None,
    ):
        self.region_id = region_id
        self.client_token = client_token
        self.endpoint_group_id = endpoint_group_id
        self.name = name
        self.description = description
        self.endpoint_group_region = endpoint_group_region
        self.traffic_percentage = traffic_percentage
        self.health_check_interval_seconds = health_check_interval_seconds
        self.health_check_path = health_check_path
        self.health_check_port = health_check_port
        self.health_check_protocol = health_check_protocol
        self.threshold_count = threshold_count
        self.endpoint_configurations = endpoint_configurations
        self.endpoint_request_protocol = endpoint_request_protocol
        self.port_overrides = port_overrides

    def validate(self):
        if self.endpoint_configurations:
            for k in self.endpoint_configurations:
                if k:
                    k.validate()
        if self.port_overrides:
            for k in self.port_overrides:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.endpoint_group_id is not None:
            result['EndpointGroupId'] = self.endpoint_group_id
        if self.name is not None:
            result['Name'] = self.name
        if self.description is not None:
            result['Description'] = self.description
        if self.endpoint_group_region is not None:
            result['EndpointGroupRegion'] = self.endpoint_group_region
        if self.traffic_percentage is not None:
            result['TrafficPercentage'] = self.traffic_percentage
        if self.health_check_interval_seconds is not None:
            result['HealthCheckIntervalSeconds'] = self.health_check_interval_seconds
        if self.health_check_path is not None:
            result['HealthCheckPath'] = self.health_check_path
        if self.health_check_port is not None:
            result['HealthCheckPort'] = self.health_check_port
        if self.health_check_protocol is not None:
            result['HealthCheckProtocol'] = self.health_check_protocol
        if self.threshold_count is not None:
            result['ThresholdCount'] = self.threshold_count
        result['EndpointConfigurations'] = []
        if self.endpoint_configurations is not None:
            for k in self.endpoint_configurations:
                result['EndpointConfigurations'].append(k.to_map() if k else None)
        if self.endpoint_request_protocol is not None:
            result['EndpointRequestProtocol'] = self.endpoint_request_protocol
        result['PortOverrides'] = []
        if self.port_overrides is not None:
            for k in self.port_overrides:
                result['PortOverrides'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('EndpointGroupId') is not None:
            self.endpoint_group_id = m.get('EndpointGroupId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('EndpointGroupRegion') is not None:
            self.endpoint_group_region = m.get('EndpointGroupRegion')
        if m.get('TrafficPercentage') is not None:
            self.traffic_percentage = m.get('TrafficPercentage')
        if m.get('HealthCheckIntervalSeconds') is not None:
            self.health_check_interval_seconds = m.get('HealthCheckIntervalSeconds')
        if m.get('HealthCheckPath') is not None:
            self.health_check_path = m.get('HealthCheckPath')
        if m.get('HealthCheckPort') is not None:
            self.health_check_port = m.get('HealthCheckPort')
        if m.get('HealthCheckProtocol') is not None:
            self.health_check_protocol = m.get('HealthCheckProtocol')
        if m.get('ThresholdCount') is not None:
            self.threshold_count = m.get('ThresholdCount')
        self.endpoint_configurations = []
        if m.get('EndpointConfigurations') is not None:
            for k in m.get('EndpointConfigurations'):
                temp_model = UpdateEndpointGroupRequestEndpointConfigurations()
                self.endpoint_configurations.append(temp_model.from_map(k))
        if m.get('EndpointRequestProtocol') is not None:
            self.endpoint_request_protocol = m.get('EndpointRequestProtocol')
        self.port_overrides = []
        if m.get('PortOverrides') is not None:
            for k in m.get('PortOverrides'):
                temp_model = UpdateEndpointGroupRequestPortOverrides()
                self.port_overrides.append(temp_model.from_map(k))
        return self


class UpdateEndpointGroupResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateEndpointGroupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateEndpointGroupResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateEndpointGroupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateEndpointGroupAttributeRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        client_token: str = None,
        endpoint_group_id: str = None,
        name: str = None,
        description: str = None,
    ):
        self.region_id = region_id
        self.client_token = client_token
        self.endpoint_group_id = endpoint_group_id
        self.name = name
        self.description = description

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.endpoint_group_id is not None:
            result['EndpointGroupId'] = self.endpoint_group_id
        if self.name is not None:
            result['Name'] = self.name
        if self.description is not None:
            result['Description'] = self.description
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('EndpointGroupId') is not None:
            self.endpoint_group_id = m.get('EndpointGroupId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        return self


class UpdateEndpointGroupAttributeResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateEndpointGroupAttributeResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateEndpointGroupAttributeResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateEndpointGroupAttributeResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateForwardingRulesRequestForwardingRulesRuleConditionsPathConfig(TeaModel):
    def __init__(
        self,
        values: List[str] = None,
    ):
        self.values = values

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.values is not None:
            result['Values'] = self.values
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Values') is not None:
            self.values = m.get('Values')
        return self


class UpdateForwardingRulesRequestForwardingRulesRuleConditionsHostConfig(TeaModel):
    def __init__(
        self,
        values: List[str] = None,
    ):
        self.values = values

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.values is not None:
            result['Values'] = self.values
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Values') is not None:
            self.values = m.get('Values')
        return self


class UpdateForwardingRulesRequestForwardingRulesRuleConditions(TeaModel):
    def __init__(
        self,
        rule_condition_type: str = None,
        path_config: UpdateForwardingRulesRequestForwardingRulesRuleConditionsPathConfig = None,
        host_config: UpdateForwardingRulesRequestForwardingRulesRuleConditionsHostConfig = None,
    ):
        self.rule_condition_type = rule_condition_type
        self.path_config = path_config
        self.host_config = host_config

    def validate(self):
        if self.path_config:
            self.path_config.validate()
        if self.host_config:
            self.host_config.validate()

    def to_map(self):
        result = dict()
        if self.rule_condition_type is not None:
            result['RuleConditionType'] = self.rule_condition_type
        if self.path_config is not None:
            result['PathConfig'] = self.path_config.to_map()
        if self.host_config is not None:
            result['HostConfig'] = self.host_config.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RuleConditionType') is not None:
            self.rule_condition_type = m.get('RuleConditionType')
        if m.get('PathConfig') is not None:
            temp_model = UpdateForwardingRulesRequestForwardingRulesRuleConditionsPathConfig()
            self.path_config = temp_model.from_map(m['PathConfig'])
        if m.get('HostConfig') is not None:
            temp_model = UpdateForwardingRulesRequestForwardingRulesRuleConditionsHostConfig()
            self.host_config = temp_model.from_map(m['HostConfig'])
        return self


class UpdateForwardingRulesRequestForwardingRulesRuleActionsForwardGroupConfigServerGroupTuples(TeaModel):
    def __init__(
        self,
        endpoint_group_id: str = None,
    ):
        self.endpoint_group_id = endpoint_group_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.endpoint_group_id is not None:
            result['EndpointGroupId'] = self.endpoint_group_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndpointGroupId') is not None:
            self.endpoint_group_id = m.get('EndpointGroupId')
        return self


class UpdateForwardingRulesRequestForwardingRulesRuleActionsForwardGroupConfig(TeaModel):
    def __init__(
        self,
        server_group_tuples: List[UpdateForwardingRulesRequestForwardingRulesRuleActionsForwardGroupConfigServerGroupTuples] = None,
    ):
        self.server_group_tuples = server_group_tuples

    def validate(self):
        if self.server_group_tuples:
            for k in self.server_group_tuples:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['ServerGroupTuples'] = []
        if self.server_group_tuples is not None:
            for k in self.server_group_tuples:
                result['ServerGroupTuples'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.server_group_tuples = []
        if m.get('ServerGroupTuples') is not None:
            for k in m.get('ServerGroupTuples'):
                temp_model = UpdateForwardingRulesRequestForwardingRulesRuleActionsForwardGroupConfigServerGroupTuples()
                self.server_group_tuples.append(temp_model.from_map(k))
        return self


class UpdateForwardingRulesRequestForwardingRulesRuleActions(TeaModel):
    def __init__(
        self,
        order: int = None,
        rule_action_type: str = None,
        forward_group_config: UpdateForwardingRulesRequestForwardingRulesRuleActionsForwardGroupConfig = None,
    ):
        self.order = order
        self.rule_action_type = rule_action_type
        self.forward_group_config = forward_group_config

    def validate(self):
        if self.forward_group_config:
            self.forward_group_config.validate()

    def to_map(self):
        result = dict()
        if self.order is not None:
            result['Order'] = self.order
        if self.rule_action_type is not None:
            result['RuleActionType'] = self.rule_action_type
        if self.forward_group_config is not None:
            result['ForwardGroupConfig'] = self.forward_group_config.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Order') is not None:
            self.order = m.get('Order')
        if m.get('RuleActionType') is not None:
            self.rule_action_type = m.get('RuleActionType')
        if m.get('ForwardGroupConfig') is not None:
            temp_model = UpdateForwardingRulesRequestForwardingRulesRuleActionsForwardGroupConfig()
            self.forward_group_config = temp_model.from_map(m['ForwardGroupConfig'])
        return self


class UpdateForwardingRulesRequestForwardingRules(TeaModel):
    def __init__(
        self,
        priority: int = None,
        rule_conditions: List[UpdateForwardingRulesRequestForwardingRulesRuleConditions] = None,
        rule_actions: List[UpdateForwardingRulesRequestForwardingRulesRuleActions] = None,
        forwarding_rule_id: str = None,
        forwarding_rule_name: str = None,
    ):
        self.priority = priority
        self.rule_conditions = rule_conditions
        self.rule_actions = rule_actions
        self.forwarding_rule_id = forwarding_rule_id
        self.forwarding_rule_name = forwarding_rule_name

    def validate(self):
        if self.rule_conditions:
            for k in self.rule_conditions:
                if k:
                    k.validate()
        if self.rule_actions:
            for k in self.rule_actions:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.priority is not None:
            result['Priority'] = self.priority
        result['RuleConditions'] = []
        if self.rule_conditions is not None:
            for k in self.rule_conditions:
                result['RuleConditions'].append(k.to_map() if k else None)
        result['RuleActions'] = []
        if self.rule_actions is not None:
            for k in self.rule_actions:
                result['RuleActions'].append(k.to_map() if k else None)
        if self.forwarding_rule_id is not None:
            result['ForwardingRuleId'] = self.forwarding_rule_id
        if self.forwarding_rule_name is not None:
            result['ForwardingRuleName'] = self.forwarding_rule_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Priority') is not None:
            self.priority = m.get('Priority')
        self.rule_conditions = []
        if m.get('RuleConditions') is not None:
            for k in m.get('RuleConditions'):
                temp_model = UpdateForwardingRulesRequestForwardingRulesRuleConditions()
                self.rule_conditions.append(temp_model.from_map(k))
        self.rule_actions = []
        if m.get('RuleActions') is not None:
            for k in m.get('RuleActions'):
                temp_model = UpdateForwardingRulesRequestForwardingRulesRuleActions()
                self.rule_actions.append(temp_model.from_map(k))
        if m.get('ForwardingRuleId') is not None:
            self.forwarding_rule_id = m.get('ForwardingRuleId')
        if m.get('ForwardingRuleName') is not None:
            self.forwarding_rule_name = m.get('ForwardingRuleName')
        return self


class UpdateForwardingRulesRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        client_token: str = None,
        accelerator_id: str = None,
        listener_id: str = None,
        forwarding_rules: List[UpdateForwardingRulesRequestForwardingRules] = None,
    ):
        self.region_id = region_id
        self.client_token = client_token
        self.accelerator_id = accelerator_id
        self.listener_id = listener_id
        self.forwarding_rules = forwarding_rules

    def validate(self):
        if self.forwarding_rules:
            for k in self.forwarding_rules:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.accelerator_id is not None:
            result['AcceleratorId'] = self.accelerator_id
        if self.listener_id is not None:
            result['ListenerId'] = self.listener_id
        result['ForwardingRules'] = []
        if self.forwarding_rules is not None:
            for k in self.forwarding_rules:
                result['ForwardingRules'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('AcceleratorId') is not None:
            self.accelerator_id = m.get('AcceleratorId')
        if m.get('ListenerId') is not None:
            self.listener_id = m.get('ListenerId')
        self.forwarding_rules = []
        if m.get('ForwardingRules') is not None:
            for k in m.get('ForwardingRules'):
                temp_model = UpdateForwardingRulesRequestForwardingRules()
                self.forwarding_rules.append(temp_model.from_map(k))
        return self


class UpdateForwardingRulesResponseBodyForwardingRules(TeaModel):
    def __init__(
        self,
        forwarding_rule_id: str = None,
    ):
        self.forwarding_rule_id = forwarding_rule_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.forwarding_rule_id is not None:
            result['ForwardingRuleId'] = self.forwarding_rule_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ForwardingRuleId') is not None:
            self.forwarding_rule_id = m.get('ForwardingRuleId')
        return self


class UpdateForwardingRulesResponseBody(TeaModel):
    def __init__(
        self,
        forwarding_rules: List[UpdateForwardingRulesResponseBodyForwardingRules] = None,
        request_id: str = None,
    ):
        self.forwarding_rules = forwarding_rules
        self.request_id = request_id

    def validate(self):
        if self.forwarding_rules:
            for k in self.forwarding_rules:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['ForwardingRules'] = []
        if self.forwarding_rules is not None:
            for k in self.forwarding_rules:
                result['ForwardingRules'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.forwarding_rules = []
        if m.get('ForwardingRules') is not None:
            for k in m.get('ForwardingRules'):
                temp_model = UpdateForwardingRulesResponseBodyForwardingRules()
                self.forwarding_rules.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateForwardingRulesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateForwardingRulesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateForwardingRulesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateIpSetRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        client_token: str = None,
        ip_set_id: str = None,
        bandwidth: int = None,
    ):
        self.region_id = region_id
        self.client_token = client_token
        self.ip_set_id = ip_set_id
        self.bandwidth = bandwidth

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.ip_set_id is not None:
            result['IpSetId'] = self.ip_set_id
        if self.bandwidth is not None:
            result['Bandwidth'] = self.bandwidth
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('IpSetId') is not None:
            self.ip_set_id = m.get('IpSetId')
        if m.get('Bandwidth') is not None:
            self.bandwidth = m.get('Bandwidth')
        return self


class UpdateIpSetResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateIpSetResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateIpSetResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateIpSetResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateIpSetsRequestIpSets(TeaModel):
    def __init__(
        self,
        bandwidth: int = None,
        ip_set_id: str = None,
    ):
        self.bandwidth = bandwidth
        self.ip_set_id = ip_set_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.bandwidth is not None:
            result['Bandwidth'] = self.bandwidth
        if self.ip_set_id is not None:
            result['IpSetId'] = self.ip_set_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Bandwidth') is not None:
            self.bandwidth = m.get('Bandwidth')
        if m.get('IpSetId') is not None:
            self.ip_set_id = m.get('IpSetId')
        return self


class UpdateIpSetsRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        ip_sets: List[UpdateIpSetsRequestIpSets] = None,
    ):
        self.region_id = region_id
        self.ip_sets = ip_sets

    def validate(self):
        if self.ip_sets:
            for k in self.ip_sets:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        result['IpSets'] = []
        if self.ip_sets is not None:
            for k in self.ip_sets:
                result['IpSets'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        self.ip_sets = []
        if m.get('IpSets') is not None:
            for k in m.get('IpSets'):
                temp_model = UpdateIpSetsRequestIpSets()
                self.ip_sets.append(temp_model.from_map(k))
        return self


class UpdateIpSetsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateIpSetsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateIpSetsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateIpSetsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateListenerRequestPortRanges(TeaModel):
    def __init__(
        self,
        from_port: int = None,
        to_port: int = None,
    ):
        self.from_port = from_port
        self.to_port = to_port

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.from_port is not None:
            result['FromPort'] = self.from_port
        if self.to_port is not None:
            result['ToPort'] = self.to_port
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FromPort') is not None:
            self.from_port = m.get('FromPort')
        if m.get('ToPort') is not None:
            self.to_port = m.get('ToPort')
        return self


class UpdateListenerRequestCertificates(TeaModel):
    def __init__(
        self,
        id: str = None,
    ):
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class UpdateListenerRequestBackendPorts(TeaModel):
    def __init__(
        self,
        from_port: int = None,
        to_port: int = None,
    ):
        self.from_port = from_port
        self.to_port = to_port

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.from_port is not None:
            result['FromPort'] = self.from_port
        if self.to_port is not None:
            result['ToPort'] = self.to_port
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('FromPort') is not None:
            self.from_port = m.get('FromPort')
        if m.get('ToPort') is not None:
            self.to_port = m.get('ToPort')
        return self


class UpdateListenerRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        client_token: str = None,
        name: str = None,
        description: str = None,
        client_affinity: str = None,
        protocol: str = None,
        listener_id: str = None,
        proxy_protocol: str = None,
        port_ranges: List[UpdateListenerRequestPortRanges] = None,
        certificates: List[UpdateListenerRequestCertificates] = None,
        backend_ports: List[UpdateListenerRequestBackendPorts] = None,
    ):
        self.region_id = region_id
        self.client_token = client_token
        self.name = name
        self.description = description
        self.client_affinity = client_affinity
        self.protocol = protocol
        self.listener_id = listener_id
        self.proxy_protocol = proxy_protocol
        self.port_ranges = port_ranges
        self.certificates = certificates
        self.backend_ports = backend_ports

    def validate(self):
        if self.port_ranges:
            for k in self.port_ranges:
                if k:
                    k.validate()
        if self.certificates:
            for k in self.certificates:
                if k:
                    k.validate()
        if self.backend_ports:
            for k in self.backend_ports:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.name is not None:
            result['Name'] = self.name
        if self.description is not None:
            result['Description'] = self.description
        if self.client_affinity is not None:
            result['ClientAffinity'] = self.client_affinity
        if self.protocol is not None:
            result['Protocol'] = self.protocol
        if self.listener_id is not None:
            result['ListenerId'] = self.listener_id
        if self.proxy_protocol is not None:
            result['ProxyProtocol'] = self.proxy_protocol
        result['PortRanges'] = []
        if self.port_ranges is not None:
            for k in self.port_ranges:
                result['PortRanges'].append(k.to_map() if k else None)
        result['Certificates'] = []
        if self.certificates is not None:
            for k in self.certificates:
                result['Certificates'].append(k.to_map() if k else None)
        result['BackendPorts'] = []
        if self.backend_ports is not None:
            for k in self.backend_ports:
                result['BackendPorts'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('ClientAffinity') is not None:
            self.client_affinity = m.get('ClientAffinity')
        if m.get('Protocol') is not None:
            self.protocol = m.get('Protocol')
        if m.get('ListenerId') is not None:
            self.listener_id = m.get('ListenerId')
        if m.get('ProxyProtocol') is not None:
            self.proxy_protocol = m.get('ProxyProtocol')
        self.port_ranges = []
        if m.get('PortRanges') is not None:
            for k in m.get('PortRanges'):
                temp_model = UpdateListenerRequestPortRanges()
                self.port_ranges.append(temp_model.from_map(k))
        self.certificates = []
        if m.get('Certificates') is not None:
            for k in m.get('Certificates'):
                temp_model = UpdateListenerRequestCertificates()
                self.certificates.append(temp_model.from_map(k))
        self.backend_ports = []
        if m.get('BackendPorts') is not None:
            for k in m.get('BackendPorts'):
                temp_model = UpdateListenerRequestBackendPorts()
                self.backend_ports.append(temp_model.from_map(k))
        return self


class UpdateListenerResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateListenerResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateListenerResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateListenerResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


