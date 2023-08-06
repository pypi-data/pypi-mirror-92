import rev._sparkmaxdriver._rev_spark_driver
import typing

__all__ = [
    "frc_deviceType_t",
    "frc_manufacturer_t"
]


class frc_deviceType_t():
    """
    Members:

      deviceBroadcast

      robotController

      motorController

      relayController

      gyroSensor

      accelerometerSensor

      ultrasonicSensor

      gearToothSensor

      powerDistribution

      pneumaticsController

      miscCANDevice

      IOBreakout

      dev_rsvd12

      dev_rsvd13

      dev_rsvd14

      dev_rsvd15

      dev_rsvd16

      dev_rsvd17

      dev_rsvd18

      dev_rsvd19

      dev_rsvd20

      dev_rsvd21

      dev_rsvd22

      dev_rsvd23

      dev_rsvd24

      dev_rsvd25

      dev_rsvd26

      dev_rsvd27

      dev_rsvd28

      dev_rsvd29

      dev_rsvd30

      firmwareUpdate
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    IOBreakout: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.IOBreakout: 11>
    __members__: dict # value = {'deviceBroadcast': <frc_deviceType_t.deviceBroadcast: 0>, 'robotController': <frc_deviceType_t.robotController: 1>, 'motorController': <frc_deviceType_t.motorController: 2>, 'relayController': <frc_deviceType_t.relayController: 3>, 'gyroSensor': <frc_deviceType_t.gyroSensor: 4>, 'accelerometerSensor': <frc_deviceType_t.accelerometerSensor: 5>, 'ultrasonicSensor': <frc_deviceType_t.ultrasonicSensor: 6>, 'gearToothSensor': <frc_deviceType_t.gearToothSensor: 7>, 'powerDistribution': <frc_deviceType_t.powerDistribution: 8>, 'pneumaticsController': <frc_deviceType_t.pneumaticsController: 9>, 'miscCANDevice': <frc_deviceType_t.miscCANDevice: 10>, 'IOBreakout': <frc_deviceType_t.IOBreakout: 11>, 'dev_rsvd12': <frc_deviceType_t.dev_rsvd12: 12>, 'dev_rsvd13': <frc_deviceType_t.dev_rsvd13: 13>, 'dev_rsvd14': <frc_deviceType_t.dev_rsvd14: 14>, 'dev_rsvd15': <frc_deviceType_t.dev_rsvd15: 15>, 'dev_rsvd16': <frc_deviceType_t.dev_rsvd16: 16>, 'dev_rsvd17': <frc_deviceType_t.dev_rsvd17: 17>, 'dev_rsvd18': <frc_deviceType_t.dev_rsvd18: 18>, 'dev_rsvd19': <frc_deviceType_t.dev_rsvd19: 19>, 'dev_rsvd20': <frc_deviceType_t.dev_rsvd20: 20>, 'dev_rsvd21': <frc_deviceType_t.dev_rsvd21: 21>, 'dev_rsvd22': <frc_deviceType_t.dev_rsvd22: 22>, 'dev_rsvd23': <frc_deviceType_t.dev_rsvd23: 23>, 'dev_rsvd24': <frc_deviceType_t.dev_rsvd24: 24>, 'dev_rsvd25': <frc_deviceType_t.dev_rsvd25: 25>, 'dev_rsvd26': <frc_deviceType_t.dev_rsvd26: 26>, 'dev_rsvd27': <frc_deviceType_t.dev_rsvd27: 27>, 'dev_rsvd28': <frc_deviceType_t.dev_rsvd28: 28>, 'dev_rsvd29': <frc_deviceType_t.dev_rsvd29: 29>, 'dev_rsvd30': <frc_deviceType_t.dev_rsvd30: 30>, 'firmwareUpdate': <frc_deviceType_t.firmwareUpdate: 31>}
    accelerometerSensor: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.accelerometerSensor: 5>
    dev_rsvd12: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.dev_rsvd12: 12>
    dev_rsvd13: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.dev_rsvd13: 13>
    dev_rsvd14: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.dev_rsvd14: 14>
    dev_rsvd15: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.dev_rsvd15: 15>
    dev_rsvd16: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.dev_rsvd16: 16>
    dev_rsvd17: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.dev_rsvd17: 17>
    dev_rsvd18: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.dev_rsvd18: 18>
    dev_rsvd19: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.dev_rsvd19: 19>
    dev_rsvd20: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.dev_rsvd20: 20>
    dev_rsvd21: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.dev_rsvd21: 21>
    dev_rsvd22: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.dev_rsvd22: 22>
    dev_rsvd23: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.dev_rsvd23: 23>
    dev_rsvd24: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.dev_rsvd24: 24>
    dev_rsvd25: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.dev_rsvd25: 25>
    dev_rsvd26: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.dev_rsvd26: 26>
    dev_rsvd27: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.dev_rsvd27: 27>
    dev_rsvd28: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.dev_rsvd28: 28>
    dev_rsvd29: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.dev_rsvd29: 29>
    dev_rsvd30: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.dev_rsvd30: 30>
    deviceBroadcast: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.deviceBroadcast: 0>
    firmwareUpdate: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.firmwareUpdate: 31>
    gearToothSensor: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.gearToothSensor: 7>
    gyroSensor: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.gyroSensor: 4>
    miscCANDevice: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.miscCANDevice: 10>
    motorController: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.motorController: 2>
    pneumaticsController: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.pneumaticsController: 9>
    powerDistribution: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.powerDistribution: 8>
    relayController: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.relayController: 3>
    robotController: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.robotController: 1>
    ultrasonicSensor: rev._sparkmaxdriver._rev_spark_driver.frc_deviceType_t # value = <frc_deviceType_t.ultrasonicSensor: 6>
    pass
class frc_manufacturer_t():
    """
    Members:

      manufacturerBroadcast

      NI

      LM

      DEKA

      CTRE

      REV

      Grapple

      MindSensors

      TeamUse
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    CTRE: rev._sparkmaxdriver._rev_spark_driver.frc_manufacturer_t # value = <frc_manufacturer_t.CTRE: 4>
    DEKA: rev._sparkmaxdriver._rev_spark_driver.frc_manufacturer_t # value = <frc_manufacturer_t.DEKA: 3>
    Grapple: rev._sparkmaxdriver._rev_spark_driver.frc_manufacturer_t # value = <frc_manufacturer_t.Grapple: 6>
    LM: rev._sparkmaxdriver._rev_spark_driver.frc_manufacturer_t # value = <frc_manufacturer_t.LM: 2>
    MindSensors: rev._sparkmaxdriver._rev_spark_driver.frc_manufacturer_t # value = <frc_manufacturer_t.MindSensors: 7>
    NI: rev._sparkmaxdriver._rev_spark_driver.frc_manufacturer_t # value = <frc_manufacturer_t.NI: 1>
    REV: rev._sparkmaxdriver._rev_spark_driver.frc_manufacturer_t # value = <frc_manufacturer_t.REV: 5>
    TeamUse: rev._sparkmaxdriver._rev_spark_driver.frc_manufacturer_t # value = <frc_manufacturer_t.TeamUse: 8>
    __members__: dict # value = {'manufacturerBroadcast': <frc_manufacturer_t.manufacturerBroadcast: 0>, 'NI': <frc_manufacturer_t.NI: 1>, 'LM': <frc_manufacturer_t.LM: 2>, 'DEKA': <frc_manufacturer_t.DEKA: 3>, 'CTRE': <frc_manufacturer_t.CTRE: 4>, 'REV': <frc_manufacturer_t.REV: 5>, 'Grapple': <frc_manufacturer_t.Grapple: 6>, 'MindSensors': <frc_manufacturer_t.MindSensors: 7>, 'TeamUse': <frc_manufacturer_t.TeamUse: 8>}
    manufacturerBroadcast: rev._sparkmaxdriver._rev_spark_driver.frc_manufacturer_t # value = <frc_manufacturer_t.manufacturerBroadcast: 0>
    pass
