import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import display, uart
from esphome.const import CONF_ID, CONF_LAMBDA
from . import nextion_ns

DEPENDENCIES = ['uart']
AUTO_LOAD = ['binary_sensor']
AUTO_LOAD = ['switch']
AUTO_LOAD = ['sensor']

Nextion = nextion_ns.class_('Nextion', cg.PollingComponent, uart.UARTDevice)
NextionRef = Nextion.operator('ref')

CONFIG_SCHEMA = display.BASIC_DISPLAY_SCHEMA.extend({
    cv.GenerateID(): cv.declare_id(Nextion),
}).extend(cv.polling_component_schema('5s')).extend(uart.UART_DEVICE_SCHEMA)


def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)
    yield uart.register_uart_device(var, config)

    if CONF_LAMBDA in config:
        lambda_ = yield cg.process_lambda(config[CONF_LAMBDA], [(NextionRef, 'it')],
                                          return_type=cg.void)
        cg.add(var.set_writer(lambda_))

    yield display.register_display(var, config)
