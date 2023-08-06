from dependency_injector import containers, providers
from gpiozero.pins.pigpio import PiGPIOFactory

from .devices import LightBulb
from .services import IFTTT
from .devices import sensors


class ServiceContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    # It's not possible to pass the root config 'config.services'
    # because, if the configuration does not contain the service's
    # config (e.g. IFTTT), any object trying to call that service will
    # throw "AttributeError: 'NoneType' object has no attribute 'get'"
    IFTTT = providers.Singleton(IFTTT, config=config.IFTTT)


class DeviceContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    light_bulb: LightBulb = providers.Factory(LightBulb)


class SensorContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    pin_factory = providers.FactoryAggregate(
        pigpio=providers.Factory(
            PiGPIOFactory,
            host=config.pigpio.host,
            port=config.pigpio.port
        ),
    )

    gpio_motion_sensor: sensors.GPIOMotionSensor = providers.Factory(
        sensors.GPIOMotionSensor,
    )


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    devices: DeviceContainer = providers.Container(
        DeviceContainer,
        config=config.devices,
    )

    sensors: SensorContainer = providers.Container(
        SensorContainer,
        config=config.sensors,
    )

    services: ServiceContainer = providers.Container(
        ServiceContainer,
        config=config.services,
    )
