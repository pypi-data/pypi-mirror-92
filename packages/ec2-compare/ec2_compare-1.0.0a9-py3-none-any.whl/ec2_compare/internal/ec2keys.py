
from typing import List


def keys_dict() -> dict:
    # pylint: disable=all
    return {'str': ['NetworkPerformance', 'InstanceType', 'EnaSupport', 'Hypervisor', 'EbsOptimizedSupport', 'EncryptionSupport'], 'bool': ['InstanceStorageSupported', 'CurrentGeneration', 'AutoRecoverySupported', 'Ipv6Supported', 'FreeTierEligible', 'HibernationSupported', 'BurstablePerformanceSupported', 'DedicatedHostsSupported', 'BareMetal'], 'list': ['SupportedStrategies', 'Accelerators', 'ValidCores', 'SupportedUsageClasses', 'Fpgas', 'Disks', 'Gpus', 'ValidThreadsPerCore', 'SupportedRootDeviceTypes', 'SupportedArchitectures'], 'dict': ['VCpuInfo', 'InferenceAcceleratorInfo', 'GpuInfo', 'EbsInfo', 'FpgaInfo', 'PlacementGroupInfo', 'ProcessorInfo', 'MemoryInfo', 'InstanceStorageInfo', 'NetworkInfo'], 'int': ['Ipv6AddressesPerInterface', 'DefaultThreadsPerCore', 'TotalGpuMemoryInMiB', 'MaximumNetworkInterfaces', 'HibernationSupported', 'TotalFpgaMemoryInMiB', 'TotalSizeInGB', 'DefaultVCpus', 'AutoRecoverySupported', 'DedicatedHostsSupported', 'CurrentGeneration', 'InstanceStorageSupported', 'Ipv6Supported', 'SizeInMiB', 'Ipv4AddressesPerInterface', 'DefaultCores', 'FreeTierEligible', 'BurstablePerformanceSupported', 'BareMetal'], 'float': ['SustainedClockSpeedInGhz'], 'other': []}  # noqa: E501


def keys_structure(*arg, **kw) -> List:
    return [elem for k, v in keys_dict().items()
            if k in arg or not arg for elem in v]
