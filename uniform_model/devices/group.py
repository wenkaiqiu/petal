import logging

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('uniform_model.devices.group')
logger.setLevel(logging.DEBUG)


class DeviceGroup:
    def __init__(self, *args):
        logger.info(f"group devices: {args}")
        self.group = list(args)

    def __str__(self):
        return f'<Group: {", ".join(map(str, self.group))}>'

    def __repr__(self):
        return f'<Group: {", ".join(map(str, self.group))}>'
