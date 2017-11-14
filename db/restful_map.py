board_map = {
    'model': {
        'device_type': 'DeviceType',
        'manufacturer': 'Manufacturer',
        'cpld_version': 'CPLDVersion',
    },
    'device': {
        'id': 'Id',
        'name': 'Name',
        'description': 'Description',
        'sku': 'Sku',
        'serial_number': 'SerialNumber',
        'part_number': 'PartNumber',
        'spare_part_number': 'SparePartNumber',
        'asset_tag': 'AssetTag',
        'card_no': 'CardNo',
        'device_locator': 'DeviceLocator',
        'location': 'Location',
        'board_name': 'BoardName',
        'board_id': 'BoardId',
        'manufacture_date': 'ManufactureDate',
    },
    'status': {
        'state': 'State',
        'health_rollup': 'HealthRollup',
        'health': 'Health',
    },
}

chassis_map = {
    'model': {
        'model': 'Model',
        'manufacturer': 'Manufacturer',
        'chassis_type': 'ChassisType',
    },
    'device': {
        'name': 'Name',
        'id': 'Id',
        'description': 'Description',
        'sku': 'Sku',
        'serial_number': 'SerialNumber',
        'part_number': 'PartNumber',
        'spare_part_number': 'SparePartNumber',
        'asset_tag': 'AssetTag',
        'indicator_led': 'IndicatorLed',
        'power_state': 'PowerState',
        'height_mm': 'HeightMm',
        'width_mm': 'WidthMm',
        'depth_mn': 'DepthMn',
        'weight_kg': 'WeightKg',
    },
    'status': {
        'state': 'State',
        'health_rollup': 'HealthRollup',
        'health': 'Health',
    },
}

ethernetInterface_map = {
    'model': {
        'mtu_size': 'MTUSize',
        'max_ipv6_static_addresses': 'MaxIPv6StaticAddresses',
    },
    'device': {
        'id': 'Id',
        'name': 'Name',
        'description': 'Description',
        'uefi_device_path': 'UefiDevicePath',
        'permanent_mac_address': 'PermanentMACAddress',
        'mac_address': 'MACAddress',
        'speed_mbps': 'SpeedMbps',
        'auto_neg': 'AutoNeg',
        'full_duplex': 'FullDuplex',
        'hostname': 'HostName',
        'fqdn': 'FQDN',
        'ipv4_addresses': 'IPv4Addresses',
        'ipv6_static_addresses': 'IPv6StaticAddresses',
        'ipv6_default_gateway': 'IPv6DefaultGateway',
    },
    'status': {
        'state': 'State',
        'health_rollup': 'HealthRollup',
        'health': 'Health',
        'link_status': 'LinkStatus',
        'interface_enabled': 'InterfaceEnabled',
    },
}

fan_map = {
    'model': {
        'model': 'Model',
        'manufacturer': 'Manufacturer',
        'lower_threshold_fatal': 'LowerThresholdFatal',
        'lower_threshold_critical': 'LowerThresholdCritical',
        'lower_threshold_non_critical': 'LowerThresholdNonCritical',
        'upper_threshold_fatal': 'UpperThresholdFatal',
        'upper_threshold_critical': 'UpperThresholdCritical',
        'upper_threshold_non_critical': 'UpperThresholdNonCritical',
    },
    'device': {
        'id': 'Id',
        'name': 'Name',
        'description': 'Description',
        'sku': 'Sku',
        'serial_number': 'SerialNumber',
        'part_number': 'PartNumber',
        'spare_part_number': 'SparePartNumber',
        'asset_tag': 'AssetTag',
        'indicator_led': 'IndicatorLED',
        'reading_units': 'ReadingUnits',
        'physical_context': 'PhysicalContext',
        'member_id': 'MemberId',
    },
    'status': {
        'state': 'State',
        'health_rollup': 'HealthRollup',
        'health': 'Health',
    },
}

manager_map = {
    'model': {
        'model': 'Model',
        'manager_type': 'ManagerType',
    },
    'device': {
        'id': 'Id',
        'name': 'Name',
        'description': 'Description',
        'firmware_version': 'FirmwareVersion',
        'service_entry_point_uuid': 'ServiceEntryPointUUID',
        'uuid': 'UUID',
        'date_time': 'DateTime',
        'date_time_local_offset': 'DateTimeLocalOffset',
    },
    'status': {
        'state': 'State',
        'health_rollup': 'HealthRollup',
        'health': 'Health',
        'power_state': 'PowerState',
    },
}

memory_map = {
    'model': {
        'model': 'Model',
        'manufacturer': 'Manufacturer',
        'memory_type': 'MemoryType',
        'memory_device_type': 'MemoryDeviceType',
        'base_module_type': 'BaseModuleType',
        'memory_media': 'MemoryMedia',
        'capacity_mib': 'CapacityMiB',
        'data_width_bits': 'DataWidthBits',
        'bus_width_bits': 'BusWidthBits',
        'allowed_speedsm_hz': 'AllowedSpeedsMHz',
        'vendorid': 'VendorID',
        'deviceid': 'DeviceID',
        'subsystem_vendorid': 'SubsystemVendorID',
        'subsystem_deviceid': 'SubsystemDeviceID',
        'maxtdp_milli_watts': 'MaxTDPMilliWatts',
        'security_capabilities': 'SecurityCapabilities',
        'spare_device_count': 'SpareDeviceCount',
        'rank_count': 'RankCount',
        'power_management_policy': 'PowerManagementPolicy',
    },
    'device': {
        'id': 'Id',
        'name': 'Name',
        'uri': 'Uri',
        'description': 'Description',
        'sku': 'SKU',
        'serial_number': 'SerialNumber',
        'part_number': 'PartNumber',
        'spare_part_number': 'SparePartNumber',
        'asset_tag': 'AssetTag',
        'firmware_revision': 'FirmwareRevision',
        'firmware_api_version': 'FirmwareApiVersion',
        'error_correction': 'ErrorCorrection',
        'operating_speed_mhz': 'OperatingSpeedMhz',
        'volatile_region_size_limit_mib': 'VolatileRegionSizeLimitMiB',
        'persistent_region_size_limit_mib': 'PersistentRegionSizeLimitMiB',
        'regions': 'Regions',
        'operating_memory_modes': 'OperatingMemoryModes',
        'is_spare_device_enabled': 'IsSpareDeviceEnabled',
        'is_rank_spare_enabled': 'IsRankSpareEnabled',
        'volatile_region_number_limit': 'VolatileRegionNumberLimit',
        'persistent_region_number_limit': 'PersistentRegionNumberLimit',
        'volatile_region_size_max_mib': 'VolatileRegionSizeMaxMiB',
        'persistent_region_size_max_mib': 'PersistentRegionSizeMaxMiB',
        'allocation_increment_mib': 'AllocationIncrementMiB',
        'allocation_alignment_mib': 'AllocationAlignmentMiB',
    },
    'status': {
        'state': 'State',
        'health_rollup': 'HealthRollup',
        'health': 'Health',
    },
    'space': {
        'device_locator': 'DeviceLocator',
        'socket': 'Socket',
        'memory_controller': 'MemoryController',
        'channel': 'Channel',
        'slot': 'Slot',
    },
}

pcie_map = {
    'model': {
        'manufacturer': 'Manufacturer',
        'model': 'Model',
    },
    'device': {
        'id': 'Id',
        'name': 'Name',
        'description': 'Description',
        'sku': 'SKU',
        'serial_number': 'SerialNumber',
        'part_number': 'PartNumber',
        'spare_part_number': 'SparePartNumber',
        'asset_tag': 'AssetTag',
    },
    'status': {
        'state': 'State',
        'health_rollup': 'HealthRollup',
        'health': 'Health',
    },
}

power_map = {
    'model': {
    },
    'device': {
        'id': 'Id',
        'name': 'Name',
        'description': 'Description',
    },
    'status': {
        'state': 'State',
        'health_rollup': 'HealthRollup',
        'health': 'Health',
    },
}

processor_map = {
    'model': {
        'processor_type': 'ProcessorType',
        'processor_architecture': 'ProcessorArchitecture',
        'manufacturer': 'Manufacturer',
        'model': 'Model',
        'instruction_set': 'InstructionSet',
        'max_speedm_hz': 'MaxSpeedMHz',
        'total_cores': 'TotalCores',
        'total_threads': 'TotalThreads',
    },
    'device': {
        'name': 'Name',
        'id': 'Id',
        'processor_id': 'ProcessorId',
        'socket': 'Socket',
        'description': 'Description',
        'sku': 'Sku',
        'serial_number': 'SerialNumber',
        'part_number': 'PartNumber',
        'spare_part_number': 'SparePartNumber',
        'asset_tag': 'AssetTag',
    },
    'status': {
        'state': 'State',
        'health_rollup': 'HealthRollup',
        'health': 'Health',
    },
}

raid_map = {
    'model': {
        'model': 'Model',
        'manufacturer': 'Manufacturer',
    },
    'device': {
        'id': 'Id',
        'name': 'Name',
        'description': 'Description',
        'member_id': 'MemberId',
        'firmware_version': 'FirmwareVersion',
        'speed_gbps': 'SpeedGbps',
        'sku': 'Sku',
        'serial_number': 'SerialNumber',
        'part_number': 'PartNumber',
        'spare_part_number': 'SparePartNumber',
        'asset_tag': 'AssetTag',
    },
    'status': {
        'state': 'State',
        'health_rollup': 'HealthRollup',
        'health': 'Health',
    },
}

server_map = {
    'model': {
        'model_type': 'Model',
        'manufacturer': 'Manufacturer',
        'trusted_modules': 'TrustedModules',
    },
    'device': {
        'id': 'Id',
        'uuid': 'UUID',
        'bios_version': 'BiosVersion',
        'description': 'Description',
        'name': 'Name',
        'uri': 'Uri',
        'sku': 'Sku',
        'serial_number': 'SerialNumber',
        'part_number': 'PartNumber',
        'spare_part_number': 'SparePartNumber',
        'asset_tag': 'AssetTag',
        'hostname': 'HostName',
        'hosting_role': 'HostingRole',
        'boot': 'Boot',
    },
    'status': {
        'state': 'State',
        'health': 'Health',
        'power_state': 'PowerState',
    },
}

