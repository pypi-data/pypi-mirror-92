import rev.color._rev_color
import typing
import ColorSensorV3
import wpilib._wpilib
import wpilib._wpilib.I2C

__all__ = [
    "CIEColor",
    "ColorMatch",
    "ColorSensorV3"
]


class CIEColor():
    def __init__(self, X: float, Y: float, Z: float) -> None: ...
    def getX(self) -> float: 
        """
        Get the X component of the color

        :returns: CIE X
        """
    def getY(self) -> float: 
        """
        Get the Y component of the color

        :returns: CIE Y
        """
    def getYx(self) -> float: 
        """
        Get the x calculated coordinate
        of the CIE 19313 color space

        https://en.wikipedia.org/wiki/CIE_1931_color_space

        :returns: CIE Yx
        """
    def getYy(self) -> float: 
        """
        Get the y calculated coordinate
        of the CIE 19313 color space

        https://en.wikipedia.org/wiki/CIE_1931_color_space

        :returns: CIE Yy
        """
    def getZ(self) -> float: 
        """
        Get the Z component of the color

        :returns: CIE Z
        """
    pass
class ColorMatch():
    """
    REV Robotics Color Sensor V3.

    This class allows access to a REV Robotics color sensor V3 on an I2C bus.
    """
    def __init__(self) -> None: ...
    def addColorMatch(self, color: wpilib._wpilib.Color) -> None: 
        """
        Add color to match object

        :param color: color to add to matching
        """
    def matchClosestColor(self, colorToMatch: wpilib._wpilib.Color, confidence: float) -> wpilib._wpilib.Color: 
        """
        MatchColor uses euclidean distance to compare a given normalized RGB
        vector against stored values

        :param colorToMatch: color to compare against stored colors

        :param confidence: The confidence value for this match, this is
         simply 1 - euclidean distance of the two color vectors

        :returns: Closest matching color
        """
    @typing.overload
    def matchColor(self, colorToMatch: wpilib._wpilib.Color) -> typing.Optional[wpilib._wpilib.Color]: 
        """
        MatchColor uses euclidean distance to compare a given normalized RGB
        vector against stored values

        :param colorToMatch: color to compare against stored colors

        :returns: Matched color if detected

        MatchColor uses euclidean distance to compare a given normalized RGB
        vector against stored values

        :param colorToMatch: color to compare against stored colors

        :param confidence: The confidence value for this match, this is
         simply 1 - euclidean distance of the two color vectors

        :returns: Matched color if detected
        """
    @typing.overload
    def matchColor(self, colorToMatch: wpilib._wpilib.Color, confidence: float) -> typing.Optional[wpilib._wpilib.Color]: ...
    def setConfidenceThreshold(self, confidence: float) -> None: 
        """
        Set the confidence interval for determining color. Defaults to 0.95

        :param confidence: A value between 0 and 1
        """
    pass
class ColorSensorV3():
    """
    REV Robotics Color Sensor V3.

    This class allows access to a REV Robotics color sensor V3 on an I2C bus.
    """
    class ColorMeasurementRate():
        """
        Members:

          k25ms

          k50ms

          k100ms

          k200ms

          k500ms

          k1000ms

          k2000ms
        """
        def __eq__(self, other: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
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
        __members__: dict # value = {'k25ms': <ColorMeasurementRate.k25ms: 0>, 'k50ms': <ColorMeasurementRate.k50ms: 1>, 'k100ms': <ColorMeasurementRate.k100ms: 2>, 'k200ms': <ColorMeasurementRate.k200ms: 3>, 'k500ms': <ColorMeasurementRate.k500ms: 4>, 'k1000ms': <ColorMeasurementRate.k1000ms: 5>, 'k2000ms': <ColorMeasurementRate.k2000ms: 7>}
        k1000ms: rev.color._rev_color.ColorSensorV3.ColorMeasurementRate # value = <ColorMeasurementRate.k1000ms: 5>
        k100ms: rev.color._rev_color.ColorSensorV3.ColorMeasurementRate # value = <ColorMeasurementRate.k100ms: 2>
        k2000ms: rev.color._rev_color.ColorSensorV3.ColorMeasurementRate # value = <ColorMeasurementRate.k2000ms: 7>
        k200ms: rev.color._rev_color.ColorSensorV3.ColorMeasurementRate # value = <ColorMeasurementRate.k200ms: 3>
        k25ms: rev.color._rev_color.ColorSensorV3.ColorMeasurementRate # value = <ColorMeasurementRate.k25ms: 0>
        k500ms: rev.color._rev_color.ColorSensorV3.ColorMeasurementRate # value = <ColorMeasurementRate.k500ms: 4>
        k50ms: rev.color._rev_color.ColorSensorV3.ColorMeasurementRate # value = <ColorMeasurementRate.k50ms: 1>
        pass
    class ColorResolution():
        """
        Members:

          k20bit

          k19bit

          k18bit

          k17bit

          k16bit

          k13bit
        """
        def __eq__(self, other: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
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
        __members__: dict # value = {'k20bit': <ColorResolution.k20bit: 0>, 'k19bit': <ColorResolution.k19bit: 16>, 'k18bit': <ColorResolution.k18bit: 32>, 'k17bit': <ColorResolution.k17bit: 48>, 'k16bit': <ColorResolution.k16bit: 64>, 'k13bit': <ColorResolution.k13bit: 80>}
        k13bit: rev.color._rev_color.ColorSensorV3.ColorResolution # value = <ColorResolution.k13bit: 80>
        k16bit: rev.color._rev_color.ColorSensorV3.ColorResolution # value = <ColorResolution.k16bit: 64>
        k17bit: rev.color._rev_color.ColorSensorV3.ColorResolution # value = <ColorResolution.k17bit: 48>
        k18bit: rev.color._rev_color.ColorSensorV3.ColorResolution # value = <ColorResolution.k18bit: 32>
        k19bit: rev.color._rev_color.ColorSensorV3.ColorResolution # value = <ColorResolution.k19bit: 16>
        k20bit: rev.color._rev_color.ColorSensorV3.ColorResolution # value = <ColorResolution.k20bit: 0>
        pass
    class GainFactor():
        """
        Members:

          k1x

          k3x

          k6x

          k9x

          k18x
        """
        def __eq__(self, other: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
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
        __members__: dict # value = {'k1x': <GainFactor.k1x: 0>, 'k3x': <GainFactor.k3x: 1>, 'k6x': <GainFactor.k6x: 2>, 'k9x': <GainFactor.k9x: 3>, 'k18x': <GainFactor.k18x: 4>}
        k18x: rev.color._rev_color.ColorSensorV3.GainFactor # value = <GainFactor.k18x: 4>
        k1x: rev.color._rev_color.ColorSensorV3.GainFactor # value = <GainFactor.k1x: 0>
        k3x: rev.color._rev_color.ColorSensorV3.GainFactor # value = <GainFactor.k3x: 1>
        k6x: rev.color._rev_color.ColorSensorV3.GainFactor # value = <GainFactor.k6x: 2>
        k9x: rev.color._rev_color.ColorSensorV3.GainFactor # value = <GainFactor.k9x: 3>
        pass
    class LEDCurrent():
        """
        Members:

          kPulse2mA

          kPulse5mA

          kPulse10mA

          kPulse25mA

          kPulse50mA

          kPulse75mA

          kPulse100mA

          kPulse125mA
        """
        def __eq__(self, other: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
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
        __members__: dict # value = {'kPulse2mA': <LEDCurrent.kPulse2mA: 0>, 'kPulse5mA': <LEDCurrent.kPulse5mA: 1>, 'kPulse10mA': <LEDCurrent.kPulse10mA: 2>, 'kPulse25mA': <LEDCurrent.kPulse25mA: 3>, 'kPulse50mA': <LEDCurrent.kPulse50mA: 4>, 'kPulse75mA': <LEDCurrent.kPulse75mA: 5>, 'kPulse100mA': <LEDCurrent.kPulse100mA: 6>, 'kPulse125mA': <LEDCurrent.kPulse125mA: 7>}
        kPulse100mA: rev.color._rev_color.ColorSensorV3.LEDCurrent # value = <LEDCurrent.kPulse100mA: 6>
        kPulse10mA: rev.color._rev_color.ColorSensorV3.LEDCurrent # value = <LEDCurrent.kPulse10mA: 2>
        kPulse125mA: rev.color._rev_color.ColorSensorV3.LEDCurrent # value = <LEDCurrent.kPulse125mA: 7>
        kPulse25mA: rev.color._rev_color.ColorSensorV3.LEDCurrent # value = <LEDCurrent.kPulse25mA: 3>
        kPulse2mA: rev.color._rev_color.ColorSensorV3.LEDCurrent # value = <LEDCurrent.kPulse2mA: 0>
        kPulse50mA: rev.color._rev_color.ColorSensorV3.LEDCurrent # value = <LEDCurrent.kPulse50mA: 4>
        kPulse5mA: rev.color._rev_color.ColorSensorV3.LEDCurrent # value = <LEDCurrent.kPulse5mA: 1>
        kPulse75mA: rev.color._rev_color.ColorSensorV3.LEDCurrent # value = <LEDCurrent.kPulse75mA: 5>
        pass
    class LEDPulseFrequency():
        """
        Members:

          k60kHz

          k70kHz

          k80kHz

          k90kHz

          k100kHz
        """
        def __eq__(self, other: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
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
        __members__: dict # value = {'k60kHz': <LEDPulseFrequency.k60kHz: 24>, 'k70kHz': <LEDPulseFrequency.k70kHz: 64>, 'k80kHz': <LEDPulseFrequency.k80kHz: 40>, 'k90kHz': <LEDPulseFrequency.k90kHz: 48>, 'k100kHz': <LEDPulseFrequency.k100kHz: 56>}
        k100kHz: rev.color._rev_color.ColorSensorV3.LEDPulseFrequency # value = <LEDPulseFrequency.k100kHz: 56>
        k60kHz: rev.color._rev_color.ColorSensorV3.LEDPulseFrequency # value = <LEDPulseFrequency.k60kHz: 24>
        k70kHz: rev.color._rev_color.ColorSensorV3.LEDPulseFrequency # value = <LEDPulseFrequency.k70kHz: 64>
        k80kHz: rev.color._rev_color.ColorSensorV3.LEDPulseFrequency # value = <LEDPulseFrequency.k80kHz: 40>
        k90kHz: rev.color._rev_color.ColorSensorV3.LEDPulseFrequency # value = <LEDPulseFrequency.k90kHz: 48>
        pass
    class ProximityMeasurementRate():
        """
        Members:

          k6ms

          k12ms

          k25ms

          k50ms

          k100ms

          k200ms

          k400ms
        """
        def __eq__(self, other: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
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
        __members__: dict # value = {'k6ms': <ProximityMeasurementRate.k6ms: 1>, 'k12ms': <ProximityMeasurementRate.k12ms: 2>, 'k25ms': <ProximityMeasurementRate.k25ms: 3>, 'k50ms': <ProximityMeasurementRate.k50ms: 4>, 'k100ms': <ProximityMeasurementRate.k100ms: 5>, 'k200ms': <ProximityMeasurementRate.k200ms: 6>, 'k400ms': <ProximityMeasurementRate.k400ms: 7>}
        k100ms: rev.color._rev_color.ColorSensorV3.ProximityMeasurementRate # value = <ProximityMeasurementRate.k100ms: 5>
        k12ms: rev.color._rev_color.ColorSensorV3.ProximityMeasurementRate # value = <ProximityMeasurementRate.k12ms: 2>
        k200ms: rev.color._rev_color.ColorSensorV3.ProximityMeasurementRate # value = <ProximityMeasurementRate.k200ms: 6>
        k25ms: rev.color._rev_color.ColorSensorV3.ProximityMeasurementRate # value = <ProximityMeasurementRate.k25ms: 3>
        k400ms: rev.color._rev_color.ColorSensorV3.ProximityMeasurementRate # value = <ProximityMeasurementRate.k400ms: 7>
        k50ms: rev.color._rev_color.ColorSensorV3.ProximityMeasurementRate # value = <ProximityMeasurementRate.k50ms: 4>
        k6ms: rev.color._rev_color.ColorSensorV3.ProximityMeasurementRate # value = <ProximityMeasurementRate.k6ms: 1>
        pass
    class ProximityResolution():
        """
        Members:

          k8bit

          k9bit

          k10bit

          k11bit
        """
        def __eq__(self, other: object) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
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
        __members__: dict # value = {'k8bit': <ProximityResolution.k8bit: 0>, 'k9bit': <ProximityResolution.k9bit: 8>, 'k10bit': <ProximityResolution.k10bit: 16>, 'k11bit': <ProximityResolution.k11bit: 24>}
        k10bit: rev.color._rev_color.ColorSensorV3.ProximityResolution # value = <ProximityResolution.k10bit: 16>
        k11bit: rev.color._rev_color.ColorSensorV3.ProximityResolution # value = <ProximityResolution.k11bit: 24>
        k8bit: rev.color._rev_color.ColorSensorV3.ProximityResolution # value = <ProximityResolution.k8bit: 0>
        k9bit: rev.color._rev_color.ColorSensorV3.ProximityResolution # value = <ProximityResolution.k9bit: 8>
        pass
    class RawColor():
        def __init__(self, r: int, g: int, b: int, _ir: int) -> None: ...
        @property
        def blue(self) -> int:
            """
            :type: int
            """
        @blue.setter
        def blue(self, arg0: int) -> None:
            pass
        @property
        def green(self) -> int:
            """
            :type: int
            """
        @green.setter
        def green(self, arg0: int) -> None:
            pass
        @property
        def ir(self) -> int:
            """
            :type: int
            """
        @ir.setter
        def ir(self, arg0: int) -> None:
            pass
        @property
        def red(self) -> int:
            """
            :type: int
            """
        @red.setter
        def red(self, arg0: int) -> None:
            pass
        pass
    def __init__(self, port: wpilib._wpilib.I2C.Port) -> None: 
        """
        Constructs a ColorSensorV3.

        Note that the REV Color Sensor is really two devices in one package:
        a color sensor providing red, green, blue and IR values, and a proximity
        sensor.

        :param port: The I2C port the color sensor is attached to
        """
    def configureColorSensor(self, res: ColorSensorV3.ColorResolution, rate: ColorSensorV3.ColorMeasurementRate) -> None: 
        """
        Configure the color sensor.

        These settings are only needed for advanced users, the defaults
        will work fine for most teams. Consult the APDS-9151 for more
        information on these configuration settings and how they will affect
        color sensor measurements.

        :param res: Bit resolution output by the respective light sensor ADCs

        :param rate: Measurement rate of the light sensor
        """
    def configureProximitySensor(self, res: ColorSensorV3.ProximityResolution, rate: ColorSensorV3.ProximityMeasurementRate) -> None: 
        """
        Configure the proximity sensor.

        These settings are only needed for advanced users, the defaults
        will work fine for most teams. Consult the APDS-9151 for more
        information on these configuration settings and how they will affect
        proximity sensor measurements.

        :param res: Bit resolution output by the proximity sensor ADC.

        :param rate: Measurement rate of the proximity sensor
        """
    def configureProximitySensorLED(self, freq: ColorSensorV3.LEDPulseFrequency, current: ColorSensorV3.LEDCurrent, pulses: int) -> None: 
        """
        Configure the the IR LED used by the proximity sensor.

        These settings are only needed for advanced users, the defaults
        will work fine for most teams. Consult the APDS-9151 for more
        information on these configuration settings and how they will affect
        proximity sensor measurements.

        :param freq: The pulse modulation frequency for the proximity
         sensor LED

        :param curr: The pulse current for the proximity sensor LED

        :param pulses: The number of pulses per measurement of the
         proximity sensor LED
        """
    def getCIEColor(self) -> CIEColor: 
        """
        Get the color converted to CIE XYZ color space using factory
        calibrated constants.

        https://en.wikipedia.org/wiki/CIE_1931_color_space

        :returns: CIEColor value from sensor
        """
    def getColor(self) -> wpilib._wpilib.Color: 
        """
        Get the normalized RGB color from the sensor (normalized based on
        total R + G + B)

        :returns: frc::Color class with normalized sRGB values
        """
    def getIR(self) -> float: 
        """
        Get the normalzied IR value from the sensor. Works best when within 2 inches and
        perpendicular to surface of interest.

        :returns: Color class with normalized values
        """
    def getProximity(self) -> int: 
        """
        Get the raw proximity value from the sensor ADC. This value is largest
        when an object is close to the sensor and smallest when
        far away.

        :returns: Proximity measurement value, ranging from 0 to 2047 in
                  default configuration
        """
    def getRawColor(self) -> ColorSensorV3.RawColor: 
        """
        Get the raw color value from the sensor.

        :returns: Raw color values from sensopr
        """
    def hasReset(self) -> bool: 
        """
        Indicates if the device reset. Based on the power on status flag in the
        status register. Per the datasheet:

        Part went through a power-up event, either because the part was turned
        on or because there was power supply voltage disturbance (default at
        first register read).

        This flag is self clearing

        :returns: bool indicating if the device was reset
        """
    def setGain(self, gain: ColorSensorV3.GainFactor) -> None: 
        """
        Set the gain factor applied to color ADC measurements.

        By default, the gain is set to 3x.

        :param gain: Gain factor applied to color ADC measurements
         measurements
        """
    pass
