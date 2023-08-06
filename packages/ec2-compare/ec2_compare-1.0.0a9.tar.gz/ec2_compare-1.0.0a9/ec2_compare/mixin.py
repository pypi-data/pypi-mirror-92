"""
Mixins.
"""
from typing import Union, Dict, List
import re
import ec2_compare.data
from ec2_compare.internal.ec2keys import keys_structure as ec2keys


# from ec2_compare.utils import dict_values


class ComparableMixin:
    """
    A class inheriting from ComparableMixin must implement only two functions to
    get all comparison methods.
    `_cmp_key` returns a key for comparing the objects.
    `_is_valid_operand` takes another object and determines if this class knows
    how to compare them.
    For more complex comparisons (where type-checking needs to occur and
    comparisons to other types are allowed), simply override _compare() instead
    of ec2_cmpkey().
    """

    def ec2_cmpkey(self):
        """
        The comparison key must be implemented by the child class and
        used by the comparison operators.
        """
        raise NotImplementedError('Please implement ec2_cmpkey method')

    def _compare(self, other, method):
        try:
            if isinstance(other, self.__class__):
                return method(self.ec2_cmpkey(), other.ec2_cmpkey())
            raise NotImplementedError(
                f'Please implement _compare with {other.__class__}')
        except AttributeError:
            raise NotImplementedError(
                'Please implement ec2_cmpkey method') from None
        except TypeError as err:
            raise NotImplementedError(err) from None

    def __lt__(self, other):
        return self._compare(other, lambda s, o: s < o)

    def __le__(self, other):
        return self._compare(other, lambda s, o: s <= o)

    def __eq__(self, other):
        return self._compare(other, lambda s, o: s == o)

    def __ge__(self, other):
        return self._compare(other, lambda s, o: s >= o)

    def __gt__(self, other):
        return self._compare(other, lambda s, o: s > o)

    def __ne__(self, other):
        return self._compare(other, lambda s, o: s != o)

    def __repr__(self):
        return str(self.ec2_cmpkey)


class AwsInstanceMixin(ComparableMixin):
    """
    A class inheriting from ComparableMixin is used for EC2 instances.
    """
    ec3__keys: List[str] = ['InstanceType', 'SupportedArchitectures',
                            'Hypervisor', 'CurrentGeneration']
    ec3__defaults: Dict[str, Union[int, str, bool, List]] = {
        # "SupportedArchitectures": ['arm64'],
        # "SupportedUsageClasses": ['on-demand']
        # "BareMetal": False,
        # "SupportedRootDeviceTypes": ["ebs"],
        # 'EbsOptimizedSupport': 'default',
        # 'EncryptionSupport': 'supported',
        # "Cores": 0,
        # "SustainedClockSpeedInGhz": 0,
        # "SizeInMiB": 0
    }

    @staticmethod
    def ec3__get_rawdata(instance_type: str) -> List:
        """
        Returns unfiltered raw data by instance family
        """
        if isinstance(instance_type, str) and instance_type:
            val = [instance_type.split(".")[0]]
            _regexp = re.match(r"^(.*?)\d+", instance_type)
            if _regexp:
                val = [_regexp.group(1), _regexp.group(0)]
            for k in val:
                try:
                    return ec2_compare.data.get(
                        key='InstanceType', value=k)
                except ValueError:
                    continue
        from ec2_compare.internal.ec2data import get_instances_list  # pylint: disable=C0415
        return get_instances_list()

    def ec3__handle_empty_dict(self):
        """
        The handling empty request must be implemented by the child class.
        """
        raise NotImplementedError('Please implement handle_empty_dict method')

    # pylint: disable=too-many-arguments,too-many-locals
    def ec3__get_instances(self, cpu: int = 0, ram: int = 0,
                           num: int = 1,
                           max_cpu: int = 0, min_cpu: int = 0,
                           max_ram: int = 0, min_ram: int = 0,
                           **kwargs) -> List:
        """
        Returns list of the instances filtered from kwargs,
        calculated minimum amount of machines needed for requested RAM & CPU

        Parameters:
            num (int): number of machines
            cpu (int): number of CPU
            ram (int): number of MiB
        TODO:
            mixed (bool): False - If Instances will be mixed
                         True - only same family
        """
        data = self.ec3__from_dict(**kwargs)
        if num == 0 or not isinstance(num, (int, float)):
            num = 1
        if not data:
            return []
        bench_cpu = max_cpu if max_cpu else max(min_cpu, 1)
        bench_ram = max_ram if max_ram else max(min_ram, 1)
        filter_max_cpu = max_cpu if max_cpu >= min_cpu else cpu
        filter_max_ram = max_ram if max_ram >= min_ram else ram

        res_bench = sorted([
            {
                **x,
                'machine_times': min(
                    float(x['DefaultVCpus'] / bench_cpu),
                    float(x['SizeInMiB'] / bench_ram)
                )
            } for x in data
            if (
                       (cpu == 0 and max_cpu == 0) or (
                       'DefaultVCpus' in x and min_cpu <= x['DefaultVCpus'] <= filter_max_cpu
               ))
               and (
                       (ram == 0 and max_ram == 0) or (
                       'SizeInMiB' in x and min_ram <= x['SizeInMiB'] <= filter_max_ram
               ))
        ], key=lambda x: x['machine_times'], reverse=True)

        if len(res_bench) < 1:
            return []

        res_filtered = [
            x['InstanceType'] for x in res_bench if x['machine_times'] >= 1
        ]
        if len(res_filtered) > 0:
            return res_filtered
        return [max(res_bench, key=lambda x: x['machine_times'])['InstanceType']]

    def ec3__from_dict(self, **kwargs):
        """Returns AWS Instances from the request.

        You can provide range or exec value for int or float keys.
        Example: SustainedClockSpeedInGhz = float(2.3) or [2, 3]

        Parameters:
            InstanceType (str, list): EC2 Instance type or family
                default is all families

        """
        if not kwargs:
            self.ec3__handle_empty_dict()
        instance_type = kwargs.get('InstanceType')
        instance_type_tuple = ('')
        if isinstance(instance_type, (list, set, str)) and instance_type:
            instance_type_tuple = tuple(instance_type)

        _partial = self.ec3__get_rawdata(instance_type=instance_type)

        flat_keys = set(ec2keys('str', 'bool')).intersection(
            set(kwargs.keys())) - {'InstanceType'}

        # filtered list or set keys with values
        list_keys = [{k: kwargs.get(k)
        if isinstance(kwargs.get(k), (list, set))
        else [kwargs.get(k)]
                      }
                     for k in set(ec2keys('set', 'list')).intersection(
                set(kwargs.keys()))
                     ]

        numeric_keys = [{k: (kwargs.get(k) + kwargs.get(k))[:2]
        if isinstance(kwargs.get(k), list)
        else [kwargs.get(k), kwargs.get(k)]
                         }
                        for k in set(ec2keys('int', 'float')).intersection(
                set(kwargs.keys()))
                        if isinstance(kwargs.get(k), (list, int, float))]

        return [x for x in _partial
                # # checking that all keys in the found element
                # if all(elem in x.keys() for elem in complex_filter_keys)
                # check that bool & string equal
                if all(x[elem] == kwargs[elem] for elem in flat_keys)
                # filter by InstanceType if it was defined
                and x['InstanceType'].startswith(instance_type_tuple)
                # filter by list keys
                and all(
                all([
                    any([val in x[k] for val in v])
                    for k, v in sublist.items()
                ]) for sublist in list_keys if sublist.items()
            )
                # filter by numeric keys with ability to specify range
                and all((k in x
                         and isinstance(x[k], (int, float))
                         and v[0] <= x[k] <= v[1])
                        for numeric_keys_elem in numeric_keys
                        for k, v in numeric_keys_elem.items() if v)

                ]


class EmrRequestMixin(AwsInstanceMixin):
    """
    A class for building the request.
    """

    def ec3__handle_empty_dict(self):
        """
        The handling empty request must be implemented by the child class.
        """
        raise NotImplementedError('Please implement handle_empty_dict method')

    def ec3__get_machines_for_fleet_request(self, max_instances=5, **kwargs) -> List:
        """
        Returns a list for fleet reuest.
        """
        return self.ec3__get_instances(**kwargs)[:max_instances]

    def ec3__get_machines(self, max_instances=5, **kwargs) -> List:
        """
        Returns a list of machines.
        """
        return self.ec3__get_instances(**kwargs)[:max_instances]

# class OperableMixin(object):
#     def __add__(self, other):
#         pass
#
#     def __iadd__(self, other):
#         pass

#
# a = ComparableMixin()
# b = ComparableMixin()
# print(a == b)
# print(a.compare(b, lambda s,o: s < o))
