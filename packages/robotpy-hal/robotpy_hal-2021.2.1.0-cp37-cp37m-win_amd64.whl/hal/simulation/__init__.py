from . import _init_simulation

# autogenerated by 'robotpy-build create-imports hal.simulation'
from ._simulation import (
    AnalogTriggerMode,
    NotifierInfo,
    cancelAccelerometerActiveCallback,
    cancelAccelerometerRangeCallback,
    cancelAccelerometerXCallback,
    cancelAccelerometerYCallback,
    cancelAccelerometerZCallback,
    cancelAddressableLEDDataCallback,
    cancelAddressableLEDInitializedCallback,
    cancelAddressableLEDLengthCallback,
    cancelAddressableLEDOutputPortCallback,
    cancelAddressableLEDRunningCallback,
    cancelAnalogGyroAngleCallback,
    cancelAnalogGyroInitializedCallback,
    cancelAnalogGyroRateCallback,
    cancelAnalogInAccumulatorCenterCallback,
    cancelAnalogInAccumulatorCountCallback,
    cancelAnalogInAccumulatorDeadbandCallback,
    cancelAnalogInAccumulatorInitializedCallback,
    cancelAnalogInAccumulatorValueCallback,
    cancelAnalogInAverageBitsCallback,
    cancelAnalogInInitializedCallback,
    cancelAnalogInOversampleBitsCallback,
    cancelAnalogInVoltageCallback,
    cancelAnalogOutInitializedCallback,
    cancelAnalogOutVoltageCallback,
    cancelAnalogTriggerInitializedCallback,
    cancelAnalogTriggerTriggerLowerBoundCallback,
    cancelAnalogTriggerTriggerModeCallback,
    cancelAnalogTriggerTriggerUpperBoundCallback,
    cancelDIOFilterIndexCallback,
    cancelDIOInitializedCallback,
    cancelDIOIsInputCallback,
    cancelDIOPulseLengthCallback,
    cancelDIOValueCallback,
    cancelDigitalPWMDutyCycleCallback,
    cancelDigitalPWMInitializedCallback,
    cancelDigitalPWMPinCallback,
    cancelDriverStationAllianceStationIdCallback,
    cancelDriverStationAutonomousCallback,
    cancelDriverStationDsAttachedCallback,
    cancelDriverStationEStopCallback,
    cancelDriverStationEnabledCallback,
    cancelDriverStationFmsAttachedCallback,
    cancelDriverStationMatchTimeCallback,
    cancelDriverStationNewDataCallback,
    cancelDriverStationTestCallback,
    cancelDutyCycleFrequencyCallback,
    cancelDutyCycleInitializedCallback,
    cancelDutyCycleOutputCallback,
    cancelEncoderCountCallback,
    cancelEncoderDirectionCallback,
    cancelEncoderDistancePerPulseCallback,
    cancelEncoderInitializedCallback,
    cancelEncoderMaxPeriodCallback,
    cancelEncoderPeriodCallback,
    cancelEncoderResetCallback,
    cancelEncoderReverseDirectionCallback,
    cancelEncoderSamplesToAverageCallback,
    cancelJoystickAxesCallback,
    cancelJoystickButtonsCallback,
    cancelJoystickDescriptorCallback,
    cancelJoystickOutputsCallback,
    cancelJoystickPOVsCallback,
    cancelMatchInfoCallback,
    cancelPCMAnySolenoidInitializedCallback,
    cancelPCMClosedLoopEnabledCallback,
    cancelPCMCompressorCurrentCallback,
    cancelPCMCompressorInitializedCallback,
    cancelPCMCompressorOnCallback,
    cancelPCMPressureSwitchCallback,
    cancelPCMSolenoidInitializedCallback,
    cancelPCMSolenoidOutputCallback,
    cancelPDPCurrentCallback,
    cancelPDPInitializedCallback,
    cancelPDPTemperatureCallback,
    cancelPDPVoltageCallback,
    cancelPWMInitializedCallback,
    cancelPWMPeriodScaleCallback,
    cancelPWMPositionCallback,
    cancelPWMRawValueCallback,
    cancelPWMSpeedCallback,
    cancelPWMZeroLatchCallback,
    cancelRelayForwardCallback,
    cancelRelayInitializedForwardCallback,
    cancelRelayInitializedReverseCallback,
    cancelRelayReverseCallback,
    cancelRoboRioFPGAButtonCallback,
    cancelRoboRioUserActive3V3Callback,
    cancelRoboRioUserActive5VCallback,
    cancelRoboRioUserActive6VCallback,
    cancelRoboRioUserCurrent3V3Callback,
    cancelRoboRioUserCurrent5VCallback,
    cancelRoboRioUserCurrent6VCallback,
    cancelRoboRioUserFaults3V3Callback,
    cancelRoboRioUserFaults5VCallback,
    cancelRoboRioUserFaults6VCallback,
    cancelRoboRioUserVoltage3V3Callback,
    cancelRoboRioUserVoltage5VCallback,
    cancelRoboRioUserVoltage6VCallback,
    cancelRoboRioVInCurrentCallback,
    cancelRoboRioVInVoltageCallback,
    cancelSPIAccelerometerActiveCallback,
    cancelSPIAccelerometerRangeCallback,
    cancelSPIAccelerometerXCallback,
    cancelSPIAccelerometerYCallback,
    cancelSPIAccelerometerZCallback,
    cancelSimDeviceCreatedCallback,
    cancelSimDeviceFreedCallback,
    cancelSimPeriodicAfterCallback,
    cancelSimPeriodicBeforeCallback,
    cancelSimValueChangedCallback,
    cancelSimValueCreatedCallback,
    cancelSimValueResetCallback,
    findAddressableLEDForChannel,
    findAnalogTriggerForChannel,
    findDigitalPWMForChannel,
    findDutyCycleForChannel,
    findEncoderForChannel,
    getAccelerometerActive,
    getAccelerometerRange,
    getAccelerometerX,
    getAccelerometerY,
    getAccelerometerZ,
    getAddressableLEDData,
    getAddressableLEDInitialized,
    getAddressableLEDLength,
    getAddressableLEDOutputPort,
    getAddressableLEDRunning,
    getAnalogGyroAngle,
    getAnalogGyroInitialized,
    getAnalogGyroRate,
    getAnalogInAccumulatorCenter,
    getAnalogInAccumulatorCount,
    getAnalogInAccumulatorDeadband,
    getAnalogInAccumulatorInitialized,
    getAnalogInAccumulatorValue,
    getAnalogInAverageBits,
    getAnalogInInitialized,
    getAnalogInOversampleBits,
    getAnalogInSimDevice,
    getAnalogInVoltage,
    getAnalogOutInitialized,
    getAnalogOutVoltage,
    getAnalogTriggerInitialized,
    getAnalogTriggerTriggerLowerBound,
    getAnalogTriggerTriggerMode,
    getAnalogTriggerTriggerUpperBound,
    getDIOFilterIndex,
    getDIOInitialized,
    getDIOIsInput,
    getDIOPulseLength,
    getDIOSimDevice,
    getDIOValue,
    getDigitalPWMDutyCycle,
    getDigitalPWMInitialized,
    getDigitalPWMPin,
    getDriverStationAllianceStationId,
    getDriverStationAutonomous,
    getDriverStationDsAttached,
    getDriverStationEStop,
    getDriverStationEnabled,
    getDriverStationFmsAttached,
    getDriverStationMatchTime,
    getDriverStationTest,
    getDutyCycleDigitalChannel,
    getDutyCycleFrequency,
    getDutyCycleInitialized,
    getDutyCycleOutput,
    getDutyCycleSimDevice,
    getEncoderCount,
    getEncoderDigitalChannelA,
    getEncoderDigitalChannelB,
    getEncoderDirection,
    getEncoderDistance,
    getEncoderDistancePerPulse,
    getEncoderInitialized,
    getEncoderMaxPeriod,
    getEncoderPeriod,
    getEncoderRate,
    getEncoderReset,
    getEncoderReverseDirection,
    getEncoderSamplesToAverage,
    getEncoderSimDevice,
    getJoystickAxes,
    getJoystickButtons,
    getJoystickCounts,
    getJoystickDescriptor,
    getJoystickOutputs,
    getJoystickPOVs,
    getMatchInfo,
    getNextNotifierTimeout,
    getNotifierInfo,
    getNumNotifiers,
    getPCMAllSolenoids,
    getPCMAnySolenoidInitialized,
    getPCMClosedLoopEnabled,
    getPCMCompressorCurrent,
    getPCMCompressorInitialized,
    getPCMCompressorOn,
    getPCMPressureSwitch,
    getPCMSolenoidInitialized,
    getPCMSolenoidOutput,
    getPDPAllCurrents,
    getPDPCurrent,
    getPDPInitialized,
    getPDPTemperature,
    getPDPVoltage,
    getPWMInitialized,
    getPWMPeriodScale,
    getPWMPosition,
    getPWMRawValue,
    getPWMSpeed,
    getPWMZeroLatch,
    getProgramStarted,
    getRelayForward,
    getRelayInitializedForward,
    getRelayInitializedReverse,
    getRelayReverse,
    getRoboRioFPGAButton,
    getRoboRioUserActive3V3,
    getRoboRioUserActive5V,
    getRoboRioUserActive6V,
    getRoboRioUserCurrent3V3,
    getRoboRioUserCurrent5V,
    getRoboRioUserCurrent6V,
    getRoboRioUserFaults3V3,
    getRoboRioUserFaults5V,
    getRoboRioUserFaults6V,
    getRoboRioUserVoltage3V3,
    getRoboRioUserVoltage5V,
    getRoboRioUserVoltage6V,
    getRoboRioVInCurrent,
    getRoboRioVInVoltage,
    getSPIAccelerometerActive,
    getSPIAccelerometerRange,
    getSPIAccelerometerX,
    getSPIAccelerometerY,
    getSPIAccelerometerZ,
    getSimDeviceHandle,
    getSimDeviceName,
    getSimValueDeviceHandle,
    getSimValueHandle,
    isSimDeviceEnabled,
    isTimingPaused,
    notifyDriverStationNewData,
    pauseTiming,
    resetAccelerometerData,
    resetAddressableLEDData,
    resetAnalogGyroData,
    resetAnalogInData,
    resetAnalogOutData,
    resetAnalogTriggerData,
    resetDIOData,
    resetDigitalPWMData,
    resetDriverStationData,
    resetDutyCycleData,
    resetEncoderData,
    resetPCMData,
    resetPDPData,
    resetPWMData,
    resetRelayData,
    resetRoboRioData,
    resetSPIAccelerometerData,
    resetSimDeviceData,
    restartTiming,
    resumeTiming,
    setAccelerometerActive,
    setAccelerometerRange,
    setAccelerometerX,
    setAccelerometerY,
    setAccelerometerZ,
    setAddressableLEDData,
    setAddressableLEDInitialized,
    setAddressableLEDLength,
    setAddressableLEDOutputPort,
    setAddressableLEDRunning,
    setAnalogGyroAngle,
    setAnalogGyroInitialized,
    setAnalogGyroRate,
    setAnalogInAccumulatorCenter,
    setAnalogInAccumulatorCount,
    setAnalogInAccumulatorDeadband,
    setAnalogInAccumulatorInitialized,
    setAnalogInAccumulatorValue,
    setAnalogInAverageBits,
    setAnalogInInitialized,
    setAnalogInOversampleBits,
    setAnalogInVoltage,
    setAnalogOutInitialized,
    setAnalogOutVoltage,
    setAnalogTriggerInitialized,
    setAnalogTriggerTriggerLowerBound,
    setAnalogTriggerTriggerMode,
    setAnalogTriggerTriggerUpperBound,
    setDIOFilterIndex,
    setDIOInitialized,
    setDIOIsInput,
    setDIOPulseLength,
    setDIOValue,
    setDigitalPWMDutyCycle,
    setDigitalPWMInitialized,
    setDigitalPWMPin,
    setDriverStationAllianceStationId,
    setDriverStationAutonomous,
    setDriverStationDsAttached,
    setDriverStationEStop,
    setDriverStationEnabled,
    setDriverStationFmsAttached,
    setDriverStationMatchTime,
    setDriverStationTest,
    setDutyCycleFrequency,
    setDutyCycleInitialized,
    setDutyCycleOutput,
    setEncoderCount,
    setEncoderDirection,
    setEncoderDistance,
    setEncoderDistancePerPulse,
    setEncoderInitialized,
    setEncoderMaxPeriod,
    setEncoderPeriod,
    setEncoderRate,
    setEncoderReset,
    setEncoderReverseDirection,
    setEncoderSamplesToAverage,
    setEventName,
    setGameSpecificMessage,
    setJoystickAxes,
    setJoystickAxis,
    setJoystickAxisCount,
    setJoystickAxisType,
    setJoystickButton,
    setJoystickButtonCount,
    setJoystickButtons,
    setJoystickButtonsValue,
    setJoystickDescriptor,
    setJoystickIsXbox,
    setJoystickName,
    setJoystickOutputs,
    setJoystickPOV,
    setJoystickPOVCount,
    setJoystickPOVs,
    setJoystickType,
    setMatchInfo,
    setMatchNumber,
    setMatchType,
    setPCMAllSolenoids,
    setPCMAnySolenoidInitialized,
    setPCMClosedLoopEnabled,
    setPCMCompressorCurrent,
    setPCMCompressorInitialized,
    setPCMCompressorOn,
    setPCMPressureSwitch,
    setPCMSolenoidInitialized,
    setPCMSolenoidOutput,
    setPDPAllCurrents,
    setPDPCurrent,
    setPDPInitialized,
    setPDPTemperature,
    setPDPVoltage,
    setPWMInitialized,
    setPWMPeriodScale,
    setPWMPosition,
    setPWMRawValue,
    setPWMSpeed,
    setPWMZeroLatch,
    setProgramStarted,
    setRelayForward,
    setRelayInitializedForward,
    setRelayInitializedReverse,
    setRelayReverse,
    setReplayNumber,
    setRoboRioFPGAButton,
    setRoboRioUserActive3V3,
    setRoboRioUserActive5V,
    setRoboRioUserActive6V,
    setRoboRioUserCurrent3V3,
    setRoboRioUserCurrent5V,
    setRoboRioUserCurrent6V,
    setRoboRioUserFaults3V3,
    setRoboRioUserFaults5V,
    setRoboRioUserFaults6V,
    setRoboRioUserVoltage3V3,
    setRoboRioUserVoltage5V,
    setRoboRioUserVoltage6V,
    setRoboRioVInCurrent,
    setRoboRioVInVoltage,
    setRuntimeType,
    setSPIAccelerometerActive,
    setSPIAccelerometerRange,
    setSPIAccelerometerX,
    setSPIAccelerometerY,
    setSPIAccelerometerZ,
    setSimDeviceEnabled,
    stepTiming,
    stepTimingAsync,
    waitForProgramStart,
)

__all__ = [
    "AnalogTriggerMode",
    "NotifierInfo",
    "cancelAccelerometerActiveCallback",
    "cancelAccelerometerRangeCallback",
    "cancelAccelerometerXCallback",
    "cancelAccelerometerYCallback",
    "cancelAccelerometerZCallback",
    "cancelAddressableLEDDataCallback",
    "cancelAddressableLEDInitializedCallback",
    "cancelAddressableLEDLengthCallback",
    "cancelAddressableLEDOutputPortCallback",
    "cancelAddressableLEDRunningCallback",
    "cancelAnalogGyroAngleCallback",
    "cancelAnalogGyroInitializedCallback",
    "cancelAnalogGyroRateCallback",
    "cancelAnalogInAccumulatorCenterCallback",
    "cancelAnalogInAccumulatorCountCallback",
    "cancelAnalogInAccumulatorDeadbandCallback",
    "cancelAnalogInAccumulatorInitializedCallback",
    "cancelAnalogInAccumulatorValueCallback",
    "cancelAnalogInAverageBitsCallback",
    "cancelAnalogInInitializedCallback",
    "cancelAnalogInOversampleBitsCallback",
    "cancelAnalogInVoltageCallback",
    "cancelAnalogOutInitializedCallback",
    "cancelAnalogOutVoltageCallback",
    "cancelAnalogTriggerInitializedCallback",
    "cancelAnalogTriggerTriggerLowerBoundCallback",
    "cancelAnalogTriggerTriggerModeCallback",
    "cancelAnalogTriggerTriggerUpperBoundCallback",
    "cancelDIOFilterIndexCallback",
    "cancelDIOInitializedCallback",
    "cancelDIOIsInputCallback",
    "cancelDIOPulseLengthCallback",
    "cancelDIOValueCallback",
    "cancelDigitalPWMDutyCycleCallback",
    "cancelDigitalPWMInitializedCallback",
    "cancelDigitalPWMPinCallback",
    "cancelDriverStationAllianceStationIdCallback",
    "cancelDriverStationAutonomousCallback",
    "cancelDriverStationDsAttachedCallback",
    "cancelDriverStationEStopCallback",
    "cancelDriverStationEnabledCallback",
    "cancelDriverStationFmsAttachedCallback",
    "cancelDriverStationMatchTimeCallback",
    "cancelDriverStationNewDataCallback",
    "cancelDriverStationTestCallback",
    "cancelDutyCycleFrequencyCallback",
    "cancelDutyCycleInitializedCallback",
    "cancelDutyCycleOutputCallback",
    "cancelEncoderCountCallback",
    "cancelEncoderDirectionCallback",
    "cancelEncoderDistancePerPulseCallback",
    "cancelEncoderInitializedCallback",
    "cancelEncoderMaxPeriodCallback",
    "cancelEncoderPeriodCallback",
    "cancelEncoderResetCallback",
    "cancelEncoderReverseDirectionCallback",
    "cancelEncoderSamplesToAverageCallback",
    "cancelJoystickAxesCallback",
    "cancelJoystickButtonsCallback",
    "cancelJoystickDescriptorCallback",
    "cancelJoystickOutputsCallback",
    "cancelJoystickPOVsCallback",
    "cancelMatchInfoCallback",
    "cancelPCMAnySolenoidInitializedCallback",
    "cancelPCMClosedLoopEnabledCallback",
    "cancelPCMCompressorCurrentCallback",
    "cancelPCMCompressorInitializedCallback",
    "cancelPCMCompressorOnCallback",
    "cancelPCMPressureSwitchCallback",
    "cancelPCMSolenoidInitializedCallback",
    "cancelPCMSolenoidOutputCallback",
    "cancelPDPCurrentCallback",
    "cancelPDPInitializedCallback",
    "cancelPDPTemperatureCallback",
    "cancelPDPVoltageCallback",
    "cancelPWMInitializedCallback",
    "cancelPWMPeriodScaleCallback",
    "cancelPWMPositionCallback",
    "cancelPWMRawValueCallback",
    "cancelPWMSpeedCallback",
    "cancelPWMZeroLatchCallback",
    "cancelRelayForwardCallback",
    "cancelRelayInitializedForwardCallback",
    "cancelRelayInitializedReverseCallback",
    "cancelRelayReverseCallback",
    "cancelRoboRioFPGAButtonCallback",
    "cancelRoboRioUserActive3V3Callback",
    "cancelRoboRioUserActive5VCallback",
    "cancelRoboRioUserActive6VCallback",
    "cancelRoboRioUserCurrent3V3Callback",
    "cancelRoboRioUserCurrent5VCallback",
    "cancelRoboRioUserCurrent6VCallback",
    "cancelRoboRioUserFaults3V3Callback",
    "cancelRoboRioUserFaults5VCallback",
    "cancelRoboRioUserFaults6VCallback",
    "cancelRoboRioUserVoltage3V3Callback",
    "cancelRoboRioUserVoltage5VCallback",
    "cancelRoboRioUserVoltage6VCallback",
    "cancelRoboRioVInCurrentCallback",
    "cancelRoboRioVInVoltageCallback",
    "cancelSPIAccelerometerActiveCallback",
    "cancelSPIAccelerometerRangeCallback",
    "cancelSPIAccelerometerXCallback",
    "cancelSPIAccelerometerYCallback",
    "cancelSPIAccelerometerZCallback",
    "cancelSimDeviceCreatedCallback",
    "cancelSimDeviceFreedCallback",
    "cancelSimPeriodicAfterCallback",
    "cancelSimPeriodicBeforeCallback",
    "cancelSimValueChangedCallback",
    "cancelSimValueCreatedCallback",
    "cancelSimValueResetCallback",
    "findAddressableLEDForChannel",
    "findAnalogTriggerForChannel",
    "findDigitalPWMForChannel",
    "findDutyCycleForChannel",
    "findEncoderForChannel",
    "getAccelerometerActive",
    "getAccelerometerRange",
    "getAccelerometerX",
    "getAccelerometerY",
    "getAccelerometerZ",
    "getAddressableLEDData",
    "getAddressableLEDInitialized",
    "getAddressableLEDLength",
    "getAddressableLEDOutputPort",
    "getAddressableLEDRunning",
    "getAnalogGyroAngle",
    "getAnalogGyroInitialized",
    "getAnalogGyroRate",
    "getAnalogInAccumulatorCenter",
    "getAnalogInAccumulatorCount",
    "getAnalogInAccumulatorDeadband",
    "getAnalogInAccumulatorInitialized",
    "getAnalogInAccumulatorValue",
    "getAnalogInAverageBits",
    "getAnalogInInitialized",
    "getAnalogInOversampleBits",
    "getAnalogInSimDevice",
    "getAnalogInVoltage",
    "getAnalogOutInitialized",
    "getAnalogOutVoltage",
    "getAnalogTriggerInitialized",
    "getAnalogTriggerTriggerLowerBound",
    "getAnalogTriggerTriggerMode",
    "getAnalogTriggerTriggerUpperBound",
    "getDIOFilterIndex",
    "getDIOInitialized",
    "getDIOIsInput",
    "getDIOPulseLength",
    "getDIOSimDevice",
    "getDIOValue",
    "getDigitalPWMDutyCycle",
    "getDigitalPWMInitialized",
    "getDigitalPWMPin",
    "getDriverStationAllianceStationId",
    "getDriverStationAutonomous",
    "getDriverStationDsAttached",
    "getDriverStationEStop",
    "getDriverStationEnabled",
    "getDriverStationFmsAttached",
    "getDriverStationMatchTime",
    "getDriverStationTest",
    "getDutyCycleDigitalChannel",
    "getDutyCycleFrequency",
    "getDutyCycleInitialized",
    "getDutyCycleOutput",
    "getDutyCycleSimDevice",
    "getEncoderCount",
    "getEncoderDigitalChannelA",
    "getEncoderDigitalChannelB",
    "getEncoderDirection",
    "getEncoderDistance",
    "getEncoderDistancePerPulse",
    "getEncoderInitialized",
    "getEncoderMaxPeriod",
    "getEncoderPeriod",
    "getEncoderRate",
    "getEncoderReset",
    "getEncoderReverseDirection",
    "getEncoderSamplesToAverage",
    "getEncoderSimDevice",
    "getJoystickAxes",
    "getJoystickButtons",
    "getJoystickCounts",
    "getJoystickDescriptor",
    "getJoystickOutputs",
    "getJoystickPOVs",
    "getMatchInfo",
    "getNextNotifierTimeout",
    "getNotifierInfo",
    "getNumNotifiers",
    "getPCMAllSolenoids",
    "getPCMAnySolenoidInitialized",
    "getPCMClosedLoopEnabled",
    "getPCMCompressorCurrent",
    "getPCMCompressorInitialized",
    "getPCMCompressorOn",
    "getPCMPressureSwitch",
    "getPCMSolenoidInitialized",
    "getPCMSolenoidOutput",
    "getPDPAllCurrents",
    "getPDPCurrent",
    "getPDPInitialized",
    "getPDPTemperature",
    "getPDPVoltage",
    "getPWMInitialized",
    "getPWMPeriodScale",
    "getPWMPosition",
    "getPWMRawValue",
    "getPWMSpeed",
    "getPWMZeroLatch",
    "getProgramStarted",
    "getRelayForward",
    "getRelayInitializedForward",
    "getRelayInitializedReverse",
    "getRelayReverse",
    "getRoboRioFPGAButton",
    "getRoboRioUserActive3V3",
    "getRoboRioUserActive5V",
    "getRoboRioUserActive6V",
    "getRoboRioUserCurrent3V3",
    "getRoboRioUserCurrent5V",
    "getRoboRioUserCurrent6V",
    "getRoboRioUserFaults3V3",
    "getRoboRioUserFaults5V",
    "getRoboRioUserFaults6V",
    "getRoboRioUserVoltage3V3",
    "getRoboRioUserVoltage5V",
    "getRoboRioUserVoltage6V",
    "getRoboRioVInCurrent",
    "getRoboRioVInVoltage",
    "getSPIAccelerometerActive",
    "getSPIAccelerometerRange",
    "getSPIAccelerometerX",
    "getSPIAccelerometerY",
    "getSPIAccelerometerZ",
    "getSimDeviceHandle",
    "getSimDeviceName",
    "getSimValueDeviceHandle",
    "getSimValueHandle",
    "isSimDeviceEnabled",
    "isTimingPaused",
    "notifyDriverStationNewData",
    "pauseTiming",
    "resetAccelerometerData",
    "resetAddressableLEDData",
    "resetAnalogGyroData",
    "resetAnalogInData",
    "resetAnalogOutData",
    "resetAnalogTriggerData",
    "resetDIOData",
    "resetDigitalPWMData",
    "resetDriverStationData",
    "resetDutyCycleData",
    "resetEncoderData",
    "resetPCMData",
    "resetPDPData",
    "resetPWMData",
    "resetRelayData",
    "resetRoboRioData",
    "resetSPIAccelerometerData",
    "resetSimDeviceData",
    "restartTiming",
    "resumeTiming",
    "setAccelerometerActive",
    "setAccelerometerRange",
    "setAccelerometerX",
    "setAccelerometerY",
    "setAccelerometerZ",
    "setAddressableLEDData",
    "setAddressableLEDInitialized",
    "setAddressableLEDLength",
    "setAddressableLEDOutputPort",
    "setAddressableLEDRunning",
    "setAnalogGyroAngle",
    "setAnalogGyroInitialized",
    "setAnalogGyroRate",
    "setAnalogInAccumulatorCenter",
    "setAnalogInAccumulatorCount",
    "setAnalogInAccumulatorDeadband",
    "setAnalogInAccumulatorInitialized",
    "setAnalogInAccumulatorValue",
    "setAnalogInAverageBits",
    "setAnalogInInitialized",
    "setAnalogInOversampleBits",
    "setAnalogInVoltage",
    "setAnalogOutInitialized",
    "setAnalogOutVoltage",
    "setAnalogTriggerInitialized",
    "setAnalogTriggerTriggerLowerBound",
    "setAnalogTriggerTriggerMode",
    "setAnalogTriggerTriggerUpperBound",
    "setDIOFilterIndex",
    "setDIOInitialized",
    "setDIOIsInput",
    "setDIOPulseLength",
    "setDIOValue",
    "setDigitalPWMDutyCycle",
    "setDigitalPWMInitialized",
    "setDigitalPWMPin",
    "setDriverStationAllianceStationId",
    "setDriverStationAutonomous",
    "setDriverStationDsAttached",
    "setDriverStationEStop",
    "setDriverStationEnabled",
    "setDriverStationFmsAttached",
    "setDriverStationMatchTime",
    "setDriverStationTest",
    "setDutyCycleFrequency",
    "setDutyCycleInitialized",
    "setDutyCycleOutput",
    "setEncoderCount",
    "setEncoderDirection",
    "setEncoderDistance",
    "setEncoderDistancePerPulse",
    "setEncoderInitialized",
    "setEncoderMaxPeriod",
    "setEncoderPeriod",
    "setEncoderRate",
    "setEncoderReset",
    "setEncoderReverseDirection",
    "setEncoderSamplesToAverage",
    "setEventName",
    "setGameSpecificMessage",
    "setJoystickAxes",
    "setJoystickAxis",
    "setJoystickAxisCount",
    "setJoystickAxisType",
    "setJoystickButton",
    "setJoystickButtonCount",
    "setJoystickButtons",
    "setJoystickButtonsValue",
    "setJoystickDescriptor",
    "setJoystickIsXbox",
    "setJoystickName",
    "setJoystickOutputs",
    "setJoystickPOV",
    "setJoystickPOVCount",
    "setJoystickPOVs",
    "setJoystickType",
    "setMatchInfo",
    "setMatchNumber",
    "setMatchType",
    "setPCMAllSolenoids",
    "setPCMAnySolenoidInitialized",
    "setPCMClosedLoopEnabled",
    "setPCMCompressorCurrent",
    "setPCMCompressorInitialized",
    "setPCMCompressorOn",
    "setPCMPressureSwitch",
    "setPCMSolenoidInitialized",
    "setPCMSolenoidOutput",
    "setPDPAllCurrents",
    "setPDPCurrent",
    "setPDPInitialized",
    "setPDPTemperature",
    "setPDPVoltage",
    "setPWMInitialized",
    "setPWMPeriodScale",
    "setPWMPosition",
    "setPWMRawValue",
    "setPWMSpeed",
    "setPWMZeroLatch",
    "setProgramStarted",
    "setRelayForward",
    "setRelayInitializedForward",
    "setRelayInitializedReverse",
    "setRelayReverse",
    "setReplayNumber",
    "setRoboRioFPGAButton",
    "setRoboRioUserActive3V3",
    "setRoboRioUserActive5V",
    "setRoboRioUserActive6V",
    "setRoboRioUserCurrent3V3",
    "setRoboRioUserCurrent5V",
    "setRoboRioUserCurrent6V",
    "setRoboRioUserFaults3V3",
    "setRoboRioUserFaults5V",
    "setRoboRioUserFaults6V",
    "setRoboRioUserVoltage3V3",
    "setRoboRioUserVoltage5V",
    "setRoboRioUserVoltage6V",
    "setRoboRioVInCurrent",
    "setRoboRioVInVoltage",
    "setRuntimeType",
    "setSPIAccelerometerActive",
    "setSPIAccelerometerRange",
    "setSPIAccelerometerX",
    "setSPIAccelerometerY",
    "setSPIAccelerometerZ",
    "setSimDeviceEnabled",
    "stepTiming",
    "stepTimingAsync",
    "waitForProgramStart",
]
