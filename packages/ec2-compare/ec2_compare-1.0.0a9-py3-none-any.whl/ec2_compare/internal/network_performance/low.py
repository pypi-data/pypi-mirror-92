
# Automatically generated

# pylint: disable=all
get = [{'SupportedArchitectures': ['i386', 'x86_64'], 'DefaultVCpus': 1, 'DefaultCores': 1, 'DefaultThreadsPerCore': 1, 'ValidCores': [1], 'ValidThreadsPerCore': [1], 'SizeInMiB': 1740, 'TotalSizeInGB': 160, 'Disks': [{'SizeInGB': 160, 'Count': 1, 'Type': 'hdd'}], 'EbsOptimizedSupport': 'unsupported', 'EncryptionSupport': 'unsupported', 'NetworkPerformance': 'Low', 'MaximumNetworkInterfaces': 2, 'Ipv4AddressesPerInterface': 4, 'Ipv6AddressesPerInterface': 0, 'Ipv6Supported': False, 'EnaSupport': 'unsupported', 'SupportedStrategies': ['partition', 'spread'], 'InstanceType': 'm1.small', 'CurrentGeneration': False, 'FreeTierEligible': False, 'SupportedUsageClasses': ['on-demand', 'spot'], 'SupportedRootDeviceTypes': ['ebs', 'instance-store'], 'BareMetal': False, 'Hypervisor': 'xen', 'ProcessorInfo': {'SupportedArchitectures': ['i386', 'x86_64']}, 'VCpuInfo': {'DefaultVCpus': 1, 'DefaultCores': 1, 'DefaultThreadsPerCore': 1, 'ValidCores': [1], 'ValidThreadsPerCore': [1]}, 'MemoryInfo': {'SizeInMiB': 1740}, 'InstanceStorageSupported': True, 'InstanceStorageInfo': {'TotalSizeInGB': 160, 'Disks': [{'SizeInGB': 160, 'Count': 1, 'Type': 'hdd'}]}, 'EbsInfo': {'EbsOptimizedSupport': 'unsupported', 'EncryptionSupport': 'unsupported'}, 'NetworkInfo': {'NetworkPerformance': 'Low', 'MaximumNetworkInterfaces': 2, 'Ipv4AddressesPerInterface': 4, 'Ipv6AddressesPerInterface': 0, 'Ipv6Supported': False, 'EnaSupport': 'unsupported'}, 'PlacementGroupInfo': {'SupportedStrategies': ['partition', 'spread']}, 'HibernationSupported': False, 'BurstablePerformanceSupported': False, 'DedicatedHostsSupported': False, 'AutoRecoverySupported': False}]  # noqa: E501


def get_instances_list() -> list:
    '''Returns list EC2 instances with NetworkPerformance = Low .'''
    # pylint: disable=all
    return get
