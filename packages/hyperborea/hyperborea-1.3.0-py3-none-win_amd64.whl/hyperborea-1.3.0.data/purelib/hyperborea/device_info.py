import logging
import math

import asphodel
import hyperborea.proxy

logger = logging.getLogger(__name__)


def try_optional(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except asphodel.AsphodelError as e:
        if e.args[1] == "ERROR_CODE_UNIMPLEMENTED_COMMAND":
            return None
        else:
            raise


class Incrementer:
    def __init__(self, progress_pipe, logger):
        self.progress_pipe = progress_pipe
        self.logger = logger

        self.finished = None
        self.total = None

    def increment(self, difference, section_name):
        if self.finished is None or self.total is None:
            self.logger.warning("Incrementing %s before ready", section_name)
            return

        self.finished += difference

        if self.progress_pipe:
            if self.finished > self.total:
                self.logger.warning("Finished count (%s) exceeds total (%s)",
                                    self.finished, self.total)

            self.progress_pipe.send((self.finished, self.total, section_name))

            # TODO: remove this!
            self.logger.debug("%s", (self.finished, self.total, section_name))

    def set_values(self, finished, total):
        if self.finished is not None:
            if finished != self.finished:
                self.logger.warning("Finished count has been changed %s -> %s",
                                    self.finished, finished)
        self.finished = finished

        if self.total is not None:
            if self.total != total:
                self.logger.warning("Total count has been changed %s -> %s",
                                    self.total, total)
        self.total = total


def get_device_info(device, allow_reconnect, diskcache=None,
                    progress_pipe=None):
    device_logger = hyperborea.proxy.get_device_logger(logger, device)
    incrementer = Incrementer(progress_pipe, device_logger)

    try:
        # get all of the parameters needed for cache interaction
        serial_number = device.get_serial_number()
        protocol_type = device.device.protocol_type
        build_info = device.get_build_info()
        build_date = device.get_build_date()
        nvm_hash = try_optional(device.get_nvm_hash)
        setting_hash = try_optional(device.get_setting_hash)

        finished_commands = 4
        total_commands = 4

        # load setting_info from cache, if applicable
        setting_key = (serial_number, protocol_type, build_info, build_date,
                       setting_hash)
        if setting_hash is None and not allow_reconnect:
            # not a simple reconnect, and the device is old-style
            setting_info = {}
        elif diskcache is not None:
            setting_info = diskcache.get(setting_key, default={})
            device_logger.debug("got setting_info from cache: %s",
                                setting_info)
        else:
            setting_info = {}

        # load nvm_info from cache, if applicable
        nvm_key = (serial_number, nvm_hash)
        if nvm_hash is None:
            nvm_info = {}
        elif diskcache is not None:
            nvm_info = diskcache.get(nvm_key, default={})
            device_logger.debug("got nvm_info from cache: %s", nvm_info)
        else:
            nvm_info = {}

        # these values are free, or have already been fetched, and shouldn't be
        # mixed into setting_info (or they would be saved to the cache).
        state_info = {
            'serial_number': serial_number,
            'build_info': build_info,
            'build_date': build_date,
            'nvm_hash': nvm_hash,
            'setting_hash': setting_hash,
            'location_string': device.get_location_string(),
            'library_protocol_version': asphodel.protocol_version_string,
            'library_build_info': asphodel.build_info,
            'library_build_date': asphodel.build_date,
            'supports_rf_power': device.supports_rf_power_commands(),
            'supports_radio': device.supports_radio_commands(),
            'supports_remote': device.supports_remote_commands(),
            'supports_bootloader': device.supports_bootloader_commands(),
            'max_incoming_param_length':
                device.get_max_incoming_param_length(),
            'max_outgoing_param_length':
                device.get_max_outgoing_param_length(),
            'stream_packet_length': device.get_stream_packet_length(),
        }

        nvm_getters = [
            get_nvm
        ]

        setting_getters = [
            single_call('protocol_version', "get_protocol_version_string"),
            single_call('board_info', "get_board_info"),
            single_call('chip_family', "get_chip_family"),
            single_call('chip_model', "get_chip_model"),
            single_call('chip_id', "get_chip_id"),
            single_call('bootloader_info', "get_bootloader_info"),
            single_call('commit_id', "get_commit_id", optional=True),
            single_call('repo_branch', "get_repo_branch", optional=True),
            single_call('repo_name', "get_repo_name", optional=True),
            single_call('nvm_modified', "get_nvm_modified", optional=True),
            get_custom_enums,
            get_setting_categories,
            get_streams,
            get_channels,
            get_channel_calibrations,
            get_supplies,
            get_ctrl_vars,
            get_settings,
            get_rf_power_ctrl_vars,
            get_radio_ctrl_vars,
            get_radio_scan_power,
            get_radio_default_serial,
            get_led_settings,
            get_rgb_settings,
            get_supply_results,
            get_ctrl_var_settings,
            get_rf_power_status,
            get_device_mode,
        ]

        # make a copy of everything
        merged_dict = state_info.copy()
        merged_dict.update(nvm_info)
        merged_dict.update(setting_info)

        info_and_getters = [(nvm_info, nvm_getters),
                            (setting_info, setting_getters)]

        generators_to_process = []

        try:
            for info_dict, getters in info_and_getters:
                for get_fn in getters:
                    gen = get_fn(device, merged_dict, incrementer)

                    # do the first call on the generator
                    try:
                        finished, remaining, d = next(gen)
                    except StopIteration:
                        continue

                    finished_commands += finished
                    total_commands += finished + remaining

                    # push the updates into the dicts
                    merged_dict.update(d)
                    info_dict.update(d)

                    generators_to_process.append((gen, info_dict, remaining))

            incrementer.set_values(finished_commands, total_commands)

            for gen, info_dict, remaining in generators_to_process:
                # do this now in case we get a StopIteration
                finished_commands += remaining

                try:
                    d = next(gen)
                except StopIteration:
                    continue

                # push the updates into the dicts
                merged_dict.update(d)
                info_dict.update(d)

                incrementer.set_values(finished_commands, total_commands)

        finally:
            # store back to cache
            if diskcache is not None:
                device_logger.debug("storing setting_info to %s", setting_key)
                diskcache.set(setting_key, setting_info)
                if nvm_hash is not None:
                    device_logger.debug("storing nvm_info to %s", nvm_key)
                    diskcache.set(nvm_key, nvm_info)

    except Exception:
        device_logger.exception("Unhandled exception in get_device_info()")
        return {}
    finally:
        if progress_pipe:
            progress_pipe.close()

    return merged_dict


def single_call(key_name, func_name, optional=False):
    def func(device, device_info, incrementer):
        if key_name in device_info:
            return

        yield 0, 1, {}

        func = getattr(device, func_name)

        if optional:
            value = try_optional(func)
        else:
            value = func()

        incrementer.increment(1, key_name)

        yield {key_name: value}
    return func


def array_call(key, device_info, incrementer, count_fn,
               element_fn, count_key=None, element_cost=1, skippable=True):
    if count_key is not None:
        if skippable and key in device_info:
            # array fully present in the cache
            return

        # use a different key to get the count
        array_length = len(device_info[count_key])
        yield 0, element_cost * array_length, {}
    elif key in device_info:
        array = device_info[key]
        if skippable and not all(x is None for x in array):
            # array fully present in the cache
            return
        else:
            # array is in the cache, so use that for length
            array_length = len(array)
            yield 0, element_cost * array_length, {}
    else:
        # no length information present in the cache
        array_length = count_fn()
        yield 1, element_cost * array_length, {key: [None] * array_length}

    array = []
    for i in range(array_length):
        element = element_fn(i)
        array.append(element)
        incrementer.increment(element_cost, key)
    yield {key: array}


def get_custom_enums(device, device_info, incrementer):
    if 'custom_enums' in device_info:
        d = device_info['custom_enums']
        if any(v is None for sublist in d.values() for v in sublist):
            # cached values holds only size information
            custom_enum_counts = [len(d[i]) for i in range(len(d))]
            custom_enum_commands = sum(custom_enum_counts)
            yield 0, custom_enum_commands, {}
        else:
            # cached value holds data
            return
    else:
        custom_enum_counts = device.get_custom_enum_counts()
        custom_enum_commands = sum(custom_enum_counts)
        empty = {i: [None] * c for i, c in enumerate(custom_enum_counts)}
        yield 1, custom_enum_commands, {'custom_enums': empty}
    custom_enums = {}
    for i, count in enumerate(custom_enum_counts):
        custom_enums[i] = [device.get_custom_enum_value_name(i, v)
                           for v in range(count)]
        incrementer.increment(count, 'custom_enums')
    yield {'custom_enums': custom_enums}


def get_setting_categories(device, device_info, incrementer):
    def element_fn(i):
        name = device.get_setting_category_name(i)
        settings = device.get_setting_category_settings(i)
        return (name, settings)

    yield from array_call('setting_categories', device_info, incrementer,
                          device.get_setting_category_count,
                          element_fn=element_fn, element_cost=2)


def get_streams(device, device_info, incrementer):
    if 'stream_rate_info' in device_info:
        # already got everything from cache
        return
    if 'streams' in device_info:
        # already have the counts
        stream_count = len(device_info['streams'])
        yield 0, 3 * stream_count, {}
    else:
        stream_count, filler_bits, id_bits = device.get_stream_count()
        d = {'stream_filler_bits': filler_bits,
             'stream_id_bits': id_bits,
             'streams': [None] * stream_count}
        yield 1, 3 * stream_count, d
    streams = []
    stream_rate_info = []
    for i in range(stream_count):
        streams.append(device.get_stream(i))
        stream_rate_info.append(device.get_stream_rate_info(i))
        incrementer.increment(3, 'streams')
    yield {'streams': streams, 'stream_rate_info': stream_rate_info}


def get_channels(device, device_info, incrementer):
    yield from array_call('channels', device_info, incrementer,
                          device.get_channel_count,
                          element_fn=device.get_channel, element_cost=3)


def get_channel_calibrations(device, device_info, incrementer):
    supports_calibration = True

    def element_fn(i):
        nonlocal supports_calibration
        try:
            return device.get_channel_calibration(i)
        except asphodel.AsphodelError as e:
            if e.args[1] == "ERROR_CODE_UNIMPLEMENTED_COMMAND":
                supports_calibration = False
                return None
            else:
                raise

    yield from array_call('channel_calibration', device_info, incrementer,
                          count_fn=None, count_key='channels',
                          element_fn=element_fn, element_cost=1)


def get_supplies(device, device_info, incrementer):
    def element_fn(i):
        supply_name = device.get_supply_name(i)
        supply_info = device.get_supply_info(i)
        return (supply_name, supply_info)

    yield from array_call('supplies', device_info, incrementer,
                          device.get_supply_count,
                          element_fn=element_fn, element_cost=2)


def get_supply_results(device, device_info, incrementer):
    def element_fn(i):
        try:
            return device.check_supply(i)
        except asphodel.AsphodelError:
            return None

    yield from array_call('supply_results', device_info, incrementer,
                          count_fn=None, count_key='supplies',
                          element_fn=element_fn, skippable=False)


def get_ctrl_vars(device, device_info, incrementer):
    def element_fn(i):
        ctrl_var_name = device.get_ctrl_var_name(i)
        ctrl_var_info = device.get_ctrl_var_info(i)
        return (ctrl_var_name, ctrl_var_info, None)

    yield from array_call('ctrl_vars', device_info, incrementer,
                          device.get_ctrl_var_count,
                          element_fn=element_fn, element_cost=2)


def get_ctrl_var_settings(device, device_info, incrementer):
    ctrl_var_count = len(device_info['ctrl_vars'])
    yield 0, ctrl_var_count, {}

    old_ctrl_vars = device_info['ctrl_vars']
    new_ctrl_vars = []
    for i, (name, info, _old_setting) in enumerate(old_ctrl_vars):
        new_setting = device.get_ctrl_var(i)
        new_ctrl_vars.append((name, info, new_setting))
        incrementer.increment(1, 'ctrl_var_settings')
    yield {'ctrl_vars': new_ctrl_vars}


def get_settings(device, device_info, incrementer):
    yield from array_call('settings', device_info, incrementer,
                          device.get_setting_count,
                          element_fn=device.get_setting, element_cost=3)


def get_nvm(device, device_info, incrementer):
    if 'nvm' in device_info:
        return

    nvm_size = device.get_nvm_size()
    nvm_bpc = (device.get_max_incoming_param_length() // 4) * 4
    nvm_commands = math.ceil(nvm_size / nvm_bpc)

    yield 1, 1 + nvm_commands, {}

    nvm_bytes = device.read_nvm_section(0, nvm_size)
    incrementer.increment(nvm_commands, "nvm")

    tag_locations = device.get_user_tag_locations()
    incrementer.increment(1, 'tag_locations')

    def read_user_tag_string(offset, length):
        b = nvm_bytes[offset:offset + length]
        b = b.rstrip(b"\xff\x00")
        try:
            return b.decode("UTF-8")
        except UnicodeDecodeError:
            return None

    user_tag_1 = read_user_tag_string(*tag_locations[0])
    user_tag_2 = read_user_tag_string(*tag_locations[1])

    yield {'nvm': nvm_bytes, 'tag_locations': tag_locations,
           'user_tag_1': user_tag_1, 'user_tag_2': user_tag_2}


def get_led_settings(device, device_info, incrementer):
    yield from array_call('led_settings', device_info, incrementer,
                          device.get_led_count,
                          element_fn=device.get_led_value, skippable=False)


def get_rgb_settings(device, device_info, incrementer):
    yield from array_call('rgb_settings', device_info, incrementer,
                          device.get_rgb_count,
                          element_fn=device.get_rgb_values, skippable=False)


def get_rf_power_status(device, device_info, incrementer):
    if not device.supports_rf_power_commands():
        return
    yield 0, 1, {}
    rf_power_status = device.get_rf_power_status()
    incrementer.increment(1, 'rf_power_status')
    yield {'rf_power_status': rf_power_status}


def get_rf_power_ctrl_vars(device, device_info, incrementer):
    if 'rf_power_ctrl_vars' in device_info:
        return
    if not device.supports_rf_power_commands():
        return
    yield 0, 1, {}
    rf_power_ctrl_vars = device.get_rf_power_ctrl_vars()
    incrementer.increment(1, 'rf_power_ctrl_vars')
    yield {'rf_power_ctrl_vars': rf_power_ctrl_vars}


def get_radio_ctrl_vars(device, device_info, incrementer):
    if 'radio_ctrl_vars' in device_info:
        return
    if not device.supports_radio_commands():
        return
    yield 0, 1, {}
    radio_ctrl_vars = device.get_radio_ctrl_vars()
    incrementer.increment(1, 'radio_ctrl_vars')
    yield {'radio_ctrl_vars': radio_ctrl_vars}


def get_radio_scan_power(device, device_info, incrementer):
    if 'radio_scan_power' in device_info:
        return
    if not device.supports_radio_commands():
        return
    yield 0, 1, {}
    try:
        device.get_radio_scan_power([0])
        radio_scan_power = True
    except Exception:
        radio_scan_power = False
    incrementer.increment(1, 'radio_scan_power')
    yield {'radio_scan_power': radio_scan_power}


def get_radio_default_serial(device, device_info, incrementer):
    if 'radio_default_serial' in device_info:
        return
    if not device.supports_radio_commands():
        return
    yield 0, 1, {}
    radio_default_serial = device.get_radio_default_serial()
    incrementer.increment(1, 'radio_default_serial')
    yield {'radio_default_serial': radio_default_serial}


def get_device_mode(device, device_info, incrementer):
    if 'supports_device_mode' in device_info:
        if not device_info['supports_device_mode']:
            return
    yield 0, 1, {}

    try:
        device_mode = device.get_device_mode()
        d = {'device_mode': device_mode,
             'supports_device_mode': True}
    except asphodel.AsphodelError as e:
        if e.args[1] == "ERROR_CODE_UNIMPLEMENTED_COMMAND":
            d = {'supports_device_mode': False}
        else:
            raise
    incrementer.increment(1, 'device_mode')
    yield d
