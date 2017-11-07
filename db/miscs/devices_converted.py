from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Chassis(Base):
    table_name = "chassis"

    ModelEntity = Column()
    ModelManufacturer = Column()
    ModelChassisType = Column()
    DeviceName = Column(String)
    DeviceId = Column(primary_key=True)
    DeviceDescription = Column()
    DeviceSku = Column()
    DeviceSerialNumber = Column(Float)
    DevicePartNumber = Column(Float)
    DeviceSparePartNumber = Column(Float)
    DeviceAssetTag = Column(String)
    DeviceIndicatorLed = Column()
    DevicePowerState = Column()
    DeviceHeightMm = Column()
    DeviceWidthMm = Column()
    DeviceDepthMn = Column()
    DeviceWeightKg = Column()
    StatusEntityState = Column()
    StatusEntityHealthRollup = Column()
    StatusEntityHealth = Column()


class Server(Base):
    table_name = "server"

    ModelEntity = Column()
    ModelManufacturer = Column()
    ModelTrustedModules = Column()
    DeviceId = Column(primary_key=True)
    DeviceUUID = Column(primary_key=True)
    DeviceBiosVersion = Column(String)
    DeviceDescription = Column()
    DeviceName = Column(String)
    DeviceUri = Column()
    DeviceSku = Column()
    DeviceSerialNumber = Column(Float)
    DevicePartNumber = Column(Float)
    DeviceSparePartNumber = Column(Float)
    DeviceAssetTag = Column(String)
    DeviceHostName = Column(String)
    DeviceHostingRole = Column()
    DeviceBoot = Column()
    StatusEntityState = Column()
    StatusEntityHealth = Column()
    StatusPowerState = Column()


class Pcie(Base):
    table_name = "pcie"

    ModelManufacturer = Column()
    ModelEntity = Column()
    DeviceId = Column(primary_key=True)
    DeviceName = Column(String)
    DeviceDescription = Column()
    DeviceSKU = Column()
    DeviceSerialNumber = Column(Float)
    DevicePartNumber = Column(Float)
    DeviceSparePartNumber = Column(Float)
    DeviceAssetTag = Column(String)
    StatusEntityState = Column()
    StatusEntityHealthRollup = Column()
    StatusEntityHealth = Column()


class Power(Base):
    table_name = "power"

    DeviceId = Column(primary_key=True)
    DeviceName = Column(String)
    DeviceDescription = Column()
    StatusEntityState = Column()
    StatusEntityHealthRollup = Column()
    StatusEntityHealth = Column()


class Board(Base):
    table_name = "board"

    ModelDeviceType = Column()
    ModelManufacturer = Column()
    ModelCPLDVersion = Column(String)
    DeviceId = Column(primary_key=True)
    DeviceName = Column(String)
    DeviceDescription = Column()
    DeviceSku = Column()
    DeviceSerialNumber = Column(Float)
    DevicePartNumber = Column(Float)
    DeviceSparePartNumber = Column(Float)
    DeviceAssetTag = Column(String)
    DeviceCardNo = Column(Integer)
    DeviceDeviceLocator = Column()
    DeviceLocation = Column()
    DeviceBoardName = Column(String)
    DeviceBoardId = Column(primary_key=True)
    DeviceManufactureDate = Column()
    StatusEntityState = Column()
    StatusEntityHealthRollup = Column()
    StatusEntityHealth = Column()


class Raid(Base):
    table_name = "raid"

    ModelEntity = Column()
    ModelManufacturer = Column()
    DeviceId = Column(primary_key=True)
    DeviceName = Column(String)
    DeviceDescription = Column()
    DeviceMemberId = Column(primary_key=True)
    DeviceFirmwareVersion = Column(String)
    DeviceSpeedGbps = Column()
    DeviceSku = Column()
    DeviceSerialNumber = Column(Float)
    DevicePartNumber = Column(Float)
    DeviceSparePartNumber = Column(Float)
    DeviceAssetTag = Column(String)
    StatusEntityState = Column()
    StatusEntityHealthRollup = Column()
    StatusEntityHealth = Column()


class Memory(Base):
    table_name = "memory"

    ModelEntity = Column()
    ModelManufacturer = Column()
    ModelMemoryType = Column()
    ModelMemoryDeviceType = Column()
    ModelBaseModuleType = Column()
    ModelMemoryMedia = Column()
    ModelCapacityMiB = Column()
    ModelDataWidthBits = Column()
    ModelBusWidthBits = Column()
    ModelAllowedSpeedsMHz = Column()
    ModelVendorID = Column(primary_key=True)
    ModelDeviceID = Column(primary_key=True)
    ModelSubsystemVendorID = Column(primary_key=True)
    ModelSubsystemDeviceID = Column(primary_key=True)
    ModelMaxTDPMilliWatts = Column()
    ModelSecurityCapabilities = Column()
    ModelSpareDeviceCount = Column()
    ModelRankCount = Column()
    ModelPowerManagementPolicy = Column()
    DeviceId = Column(primary_key=True)
    DeviceName = Column(String)
    DeviceUri = Column()
    DeviceDescription = Column()
    DeviceSKU = Column()
    DeviceSerialNumber = Column(Float)
    DevicePartNumber = Column(Float)
    DeviceSparePartNumber = Column(Float)
    DeviceAssetTag = Column(String)
    DeviceFirmwareRevision = Column()
    DeviceFirmwareApiVersion = Column(String)
    DeviceErrorCorrection = Column()
    DeviceOperatingSpeedMhz = Column()
    DeviceVolatileRegionSizeLimitMiB = Column()
    DevicePersistentRegionSizeLimitMiB = Column()
    DeviceRegions = Column()
    DeviceOperatingMemoryModes = Column()
    DeviceIsSpareDeviceEnabled = Column()
    DeviceIsRankSpareEnabled = Column()
    DeviceVolatileRegionNumberLimit = Column()
    DevicePersistentRegionNumberLimit = Column()
    DeviceVolatileRegionSizeMaxMiB = Column()
    DevicePersistentRegionSizeMaxMiB = Column()
    DeviceAllocationIncrementMiB = Column()
    DeviceAllocationAlignmentMiB = Column()
    StatusEntityState = Column()
    StatusEntityHealthRollup = Column()
    StatusEntityHealth = Column()
    SpaceDeviceLocator = Column()
    SpaceSocket = Column()
    SpaceMemoryController = Column()
    SpaceChannel = Column()
    SpaceSlot = Column()


class Fan(Base):
    table_name = "fan"

    ModelEntity = Column()
    ModelManufacturer = Column()
    ModelLowerThresholdFatal = Column()
    ModelLowerThresholdCritical = Column()
    ModelLowerThresholdNonCritical = Column()
    ModelUpperThresholdFatal = Column()
    ModelUpperThresholdCritical = Column()
    ModelUpperThresholdNonCritical = Column()
    DeviceId = Column(primary_key=True)
    DeviceName = Column(String)
    DeviceDescription = Column()
    DeviceSku = Column()
    DeviceSerialNumber = Column(Float)
    DevicePartNumber = Column(Float)
    DeviceSparePartNumber = Column(Float)
    DeviceAssetTag = Column(String)
    DeviceIndicatorLED = Column()
    DeviceReadingUnits = Column()
    DevicePhysicalContext = Column()
    DeviceMemberId = Column(primary_key=True)
    StatusEntityState = Column()
    StatusEntityHealthRollup = Column()
    StatusEntityHealth = Column()


class Processor(Base):
    table_name = "processor"

    ModelProcessorType = Column()
    ModelProcessorArchitecture = Column()
    ModelManufacturer = Column()
    ModelEntity = Column()
    ModelInstructionSet = Column()
    ModelMaxSpeedMHz = Column()
    ModelTotalCores = Column()
    ModelTotalThreads = Column()
    DeviceName = Column(String)
    DeviceId = Column(primary_key=True)
    DeviceProcessorId = Column(primary_key=True)
    DeviceSocket = Column()
    DeviceDescription = Column()
    DeviceSku = Column()
    DeviceSerialNumber = Column(Float)
    DevicePartNumber = Column(Float)
    DeviceSparePartNumber = Column(Float)
    DeviceAssetTag = Column(String)
    StatusEntityState = Column()
    StatusEntityHealthRollup = Column()
    StatusEntityHealth = Column()


class Ethernetinterface(Base):
    table_name = "ethernetInterface"

    ModelMTUSize = Column()
    ModelMaxIPv6StaticAddresses = Column()
    DeviceId = Column(primary_key=True)
    DeviceName = Column(String)
    DeviceDescription = Column()
    DeviceUefiDevicePath = Column()
    DevicePermanentMACAddress = Column()
    DeviceMACAddress = Column()
    DeviceSpeedMbps = Column()
    DeviceAutoNeg = Column()
    DeviceFullDuplex = Column()
    DeviceHostName = Column(String)
    DeviceFQDN = Column()
    DeviceIPv4Addresses = Column()
    DeviceIPv6StaticAddresses = Column()
    DeviceIPv6DefaultGateway = Column()
    StatusEntityState = Column()
    StatusEntityHealthRollup = Column()
    StatusEntityHealth = Column()
    StatusLinkStatus = Column()
    StatusInterfaceEnabled = Column()


class Manager(Base):
    table_name = "manager"

    ModelEntity = Column()
    ModelManagerType = Column()
    DeviceId = Column(primary_key=True)
    DeviceName = Column(String)
    DeviceDescription = Column()
    DeviceFirmwareVersion = Column(String)
    DeviceServiceEntryPointUUID = Column(primary_key=True)
    DeviceUUID = Column(primary_key=True)
    DeviceDateTime = Column(DateTime)
    DeviceDateTimeLocalOffset = Column()
    StatusEntityState = Column()
    StatusEntityHealthRollup = Column()
    StatusEntityHealth = Column()
    StatusPowerState = Column()


