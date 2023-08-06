
# Automatically generated

# pylint: disable=all
get = [{'SupportedArchitectures': ['x86_64'], 'SustainedClockSpeedInGhz': 2.7, 'DefaultVCpus': 4, 'DefaultCores': 2, 'DefaultThreadsPerCore': 2, 'ValidCores': [1, 2], 'ValidThreadsPerCore': [1, 2], 'SizeInMiB': 31232, 'EbsOptimizedSupport': 'default', 'EncryptionSupport': 'supported', 'NetworkPerformance': 'Up to 10 Gigabit', 'MaximumNetworkInterfaces': 4, 'Ipv4AddressesPerInterface': 15, 'Ipv6AddressesPerInterface': 15, 'Ipv6Supported': True, 'EnaSupport': 'required', 'Gpus': [{'Name': 'M60', 'Manufacturer': 'NVIDIA', 'Count': 1, 'MemoryInfo': {'SizeInMiB': 8192}}], 'TotalGpuMemoryInMiB': 8192, 'SupportedStrategies': ['cluster', 'partition', 'spread'], 'InstanceType': 'g3s.xlarge', 'CurrentGeneration': True, 'FreeTierEligible': False, 'SupportedUsageClasses': ['on-demand', 'spot'], 'SupportedRootDeviceTypes': ['ebs'], 'BareMetal': False, 'Hypervisor': 'xen', 'ProcessorInfo': {'SupportedArchitectures': ['x86_64'], 'SustainedClockSpeedInGhz': 2.7}, 'VCpuInfo': {'DefaultVCpus': 4, 'DefaultCores': 2, 'DefaultThreadsPerCore': 2, 'ValidCores': [1, 2], 'ValidThreadsPerCore': [1, 2]}, 'MemoryInfo': {'SizeInMiB': 31232}, 'InstanceStorageSupported': False, 'EbsInfo': {'EbsOptimizedSupport': 'default', 'EncryptionSupport': 'supported'}, 'NetworkInfo': {'NetworkPerformance': 'Up to 10 Gigabit', 'MaximumNetworkInterfaces': 4, 'Ipv4AddressesPerInterface': 15, 'Ipv6AddressesPerInterface': 15, 'Ipv6Supported': True, 'EnaSupport': 'required'}, 'GpuInfo': {'Gpus': [{'Name': 'M60', 'Manufacturer': 'NVIDIA', 'Count': 1, 'MemoryInfo': {'SizeInMiB': 8192}}], 'TotalGpuMemoryInMiB': 8192}, 'PlacementGroupInfo': {'SupportedStrategies': ['cluster', 'partition', 'spread']}, 'HibernationSupported': False, 'BurstablePerformanceSupported': False, 'DedicatedHostsSupported': False, 'AutoRecoverySupported': False}]  # noqa: E501


def get_instances_list() -> list:
    '''Returns list EC2 instances with InstanceType = g3s .'''
    # pylint: disable=all
    return get
