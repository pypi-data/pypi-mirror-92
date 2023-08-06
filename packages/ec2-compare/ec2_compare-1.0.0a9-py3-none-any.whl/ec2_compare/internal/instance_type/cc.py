
# Automatically generated

# pylint: disable=all
get = [{'SupportedArchitectures': ['x86_64'], 'SustainedClockSpeedInGhz': 2.6, 'DefaultVCpus': 32, 'DefaultCores': 16, 'DefaultThreadsPerCore': 2, 'ValidCores': [2, 4, 6, 8, 10, 12, 14, 16], 'ValidThreadsPerCore': [1, 2], 'SizeInMiB': 61952, 'TotalSizeInGB': 3360, 'Disks': [{'SizeInGB': 840, 'Count': 4, 'Type': 'hdd'}], 'EbsOptimizedSupport': 'unsupported', 'EncryptionSupport': 'unsupported', 'NetworkPerformance': '10 Gigabit', 'MaximumNetworkInterfaces': 8, 'Ipv4AddressesPerInterface': 30, 'Ipv6AddressesPerInterface': 0, 'Ipv6Supported': False, 'EnaSupport': 'unsupported', 'SupportedStrategies': ['cluster', 'partition', 'spread'], 'InstanceType': 'cc2.8xlarge', 'CurrentGeneration': False, 'FreeTierEligible': False, 'SupportedUsageClasses': ['on-demand'], 'SupportedRootDeviceTypes': ['ebs', 'instance-store'], 'BareMetal': False, 'Hypervisor': 'xen', 'ProcessorInfo': {'SupportedArchitectures': ['x86_64'], 'SustainedClockSpeedInGhz': 2.6}, 'VCpuInfo': {'DefaultVCpus': 32, 'DefaultCores': 16, 'DefaultThreadsPerCore': 2, 'ValidCores': [2, 4, 6, 8, 10, 12, 14, 16], 'ValidThreadsPerCore': [1, 2]}, 'MemoryInfo': {'SizeInMiB': 61952}, 'InstanceStorageSupported': True, 'InstanceStorageInfo': {'TotalSizeInGB': 3360, 'Disks': [{'SizeInGB': 840, 'Count': 4, 'Type': 'hdd'}]}, 'EbsInfo': {'EbsOptimizedSupport': 'unsupported', 'EncryptionSupport': 'unsupported'}, 'NetworkInfo': {'NetworkPerformance': '10 Gigabit', 'MaximumNetworkInterfaces': 8, 'Ipv4AddressesPerInterface': 30, 'Ipv6AddressesPerInterface': 0, 'Ipv6Supported': False, 'EnaSupport': 'unsupported'}, 'PlacementGroupInfo': {'SupportedStrategies': ['cluster', 'partition', 'spread']}, 'HibernationSupported': False, 'BurstablePerformanceSupported': False, 'DedicatedHostsSupported': False, 'AutoRecoverySupported': False}]  # noqa: E501


def get_instances_list() -> list:
    '''Returns list EC2 instances with InstanceType = cc .'''
    # pylint: disable=all
    return get
