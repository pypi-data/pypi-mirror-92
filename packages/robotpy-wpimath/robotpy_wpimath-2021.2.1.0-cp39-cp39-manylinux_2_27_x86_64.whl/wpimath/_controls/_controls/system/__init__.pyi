import wpimath._controls._controls.system
import typing
import numpy
import wpimath._controls._controls.controller
import wpimath._controls._controls.estimator
import wpimath._controls._controls.plant
import wpimath.geometry._geometry
import wpimath.kinematics._kinematics
_Shape = typing.Tuple[int, ...]

__all__ = [
    "LinearSystemId",
    "LinearSystemLoop_1_1_1",
    "LinearSystemLoop_2_1_1",
    "LinearSystemLoop_2_2_2",
    "LinearSystem_1_1_1",
    "LinearSystem_1_1_2",
    "LinearSystem_2_1_1",
    "LinearSystem_2_1_2",
    "LinearSystem_2_2_1",
    "LinearSystem_2_2_2",
    "MecanumDrivePoseEstimator"
]


class LinearSystemId():
    def __init__(self) -> None: ...
    @staticmethod
    def drivetrainVelocitySystem(motor: wpimath._controls._controls.plant.DCMotor, m: kilograms, r: meters, rb: meters, J: kilogram_square_meters, G: float) -> LinearSystem_2_2_2: 
        """
        Constructs the state-space model for a drivetrain.

        States: [[left velocity], [right velocity]]
        Inputs: [[left voltage], [right voltage]]
        Outputs: [[left velocity], [right velocity]]

        :param motor: Instance of DCMotor.
        :param m:     Drivetrain mass.
        :param r:     Wheel radius.
        :param rb:    Robot radius.
        :param G:     Gear ratio from motor to wheel.
        :param J:     Moment of inertia.
        """
    @staticmethod
    def elevatorSystem(motor: wpimath._controls._controls.plant.DCMotor, m: kilograms, r: meters, G: float) -> LinearSystem_2_1_1: 
        """
        Constructs the state-space model for an elevator.

        States: [[position], [velocity]]
        Inputs: [[voltage]]
        Outputs: [[position]]

        :param motor: Instance of DCMotor.
        :param m:     Carriage mass.
        :param r:     Pulley radius.
        :param G:     Gear ratio from motor to carriage.
        """
    @staticmethod
    def flywheelSystem(motor: wpimath._controls._controls.plant.DCMotor, J: kilogram_square_meters, G: float) -> LinearSystem_1_1_1: 
        """
        Constructs the state-space model for a flywheel.

        States: [[angular velocity]]
        Inputs: [[voltage]]
        Outputs: [[angular velocity]]

        :param motor: Instance of DCMotor.
        :param J:     Moment of inertia.
        :param G:     Gear ratio from motor to carriage.
        """
    @staticmethod
    def identifyDrivetrainSystem(kVlinear: volt_seconds_per_meter, kAlinear: volt_seconds_squared_per_meter, kVangular: volt_seconds_per_radian, kAangular: volt_seconds_squared_per_radian) -> LinearSystem_2_2_2: 
        """
        Constructs the state-space model for a 2 DOF drivetrain velocity system
        from system identification data.

        States: [[left velocity], [right velocity]]
        Inputs: [[left voltage], [right voltage]]
        Outputs: [[left velocity], [right velocity]]

        :param kVlinear:  The linear velocity gain, in volt seconds per distance.
        :param kAlinear:  The linear acceleration gain, in volt seconds^2 per
                          distance.
        :param kVangular: The angular velocity gain, in volt seconds per angle.
        :param kAangular: The angular acceleration gain, in volt seconds^2 per
                          angle.
        """
    @staticmethod
    def singleJointedArmSystem(motor: wpimath._controls._controls.plant.DCMotor, J: kilogram_square_meters, G: float) -> LinearSystem_2_1_1: 
        """
        Constructs the state-space model for a single-jointed arm.

        States: [[angle], [angular velocity]]
        Inputs: [[voltage]]
        Outputs: [[angle]]

        :param motor: Instance of DCMotor.
        :param J:     Moment of inertia.
        :param G:     Gear ratio from motor to carriage.
        """
    pass
class LinearSystemLoop_1_1_1():
    """
    Combines a controller, feedforward, and observer for controlling a mechanism
    with full state feedback.

    For everything in this file, "inputs" and "outputs" are defined from the
    perspective of the plant. This means U is an input and Y is an output
    (because you give the plant U (powers) and it gives you back a Y (sensor
    values). This is the opposite of what they mean from the perspective of the
    controller (U is an output because that's what goes to the motors and Y is an
    input because that's what comes back from the sensors).

    For more on the underlying math, read
    https://file.tavsys.net/control/controls-engineering-in-frc.pdf.
    """
    @typing.overload
    def U(self) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]: 
        """
        Returns the controller's calculated control input u.

        Returns an element of the controller's calculated control input u.

        :param i: Row of u.
        """
    @typing.overload
    def U(self, i: int) -> float: ...
    @typing.overload
    def __init__(self, controller: wpimath._controls._controls.controller.LinearQuadraticRegulator_1_1, feedforward: wpimath._controls._controls.controller.LinearPlantInversionFeedforward_1_1, observer: wpimath._controls._controls.estimator.KalmanFilter_1_1_1, clampFunction: typing.Callable[[numpy.ndarray[numpy.float64, _Shape[1, 1]]], numpy.ndarray[numpy.float64, _Shape[1, 1]]]) -> None: 
        """
        Constructs a state-space loop with the given plant, controller, and
        observer. By default, the initial reference is all zeros. Users should
        call reset with the initial system state before enabling the loop. This
        constructor assumes that the input(s) to this system are voltage.

        :param controller: State-space controller.
        :param observer:   State-space observer.
        :param maxVoltage: The maximum voltage that can be applied. Commonly 12.
        :param dt:         The nominal timestep.

        Constructs a state-space loop with the given plant, controller, and
        observer. By default, the initial reference is all zeros. Users should
        call reset with the initial system state before enabling the loop. This
        constructor assumes that the input(s) to this system are voltage.

        :param plant:         State-space plant.
        :param controller:    State-space controller.
        :param observer:      State-space observer.
        :param clampFunction: The function used to clamp the input vector.
        :param dt:            The nominal timestep.

        Constructs a state-space loop with the given controller, feedforward and
        observer. By default, the initial reference is all zeros. Users should
        call reset with the initial system state.

        :param controller:  State-space controller.
        :param feedforward: Plant inversion feedforward.
        :param observer:    State-space observer.
        :param maxVoltage:  The maximum voltage that can be applied. Assumes
                            that the inputs are voltages.

        Constructs a state-space loop with the given controller, feedforward,
        observer and clamp function. By default, the initial reference is all
        zeros. Users should call reset with the initial system state.

        :param controller:    State-space controller.
        :param feedforward:   Plant-inversion feedforward.
        :param observer:      State-space observer.
        :param clampFunction: The function used to clamp the input vector.
        """
    @typing.overload
    def __init__(self, controller: wpimath._controls._controls.controller.LinearQuadraticRegulator_1_1, feedforward: wpimath._controls._controls.controller.LinearPlantInversionFeedforward_1_1, observer: wpimath._controls._controls.estimator.KalmanFilter_1_1_1, maxVoltage: volts) -> None: ...
    @typing.overload
    def __init__(self, plant: LinearSystem_1_1_1, controller: wpimath._controls._controls.controller.LinearQuadraticRegulator_1_1, observer: wpimath._controls._controls.estimator.KalmanFilter_1_1_1, clampFunction: typing.Callable[[numpy.ndarray[numpy.float64, _Shape[1, 1]]], numpy.ndarray[numpy.float64, _Shape[1, 1]]], dt: seconds) -> None: ...
    @typing.overload
    def __init__(self, plant: LinearSystem_1_1_1, controller: wpimath._controls._controls.controller.LinearQuadraticRegulator_1_1, observer: wpimath._controls._controls.estimator.KalmanFilter_1_1_1, maxVoltage: volts, dt: seconds) -> None: ...
    def clampInput(self, u: numpy.ndarray[numpy.float64, _Shape[1, 1]]) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]: 
        """
        Clamps input vector between system's minimum and maximum allowable input.

        :param u: Input vector to clamp.

        :returns: Clamped input vector.
        """
    def correct(self, y: numpy.ndarray[numpy.float64, _Shape[1, 1]]) -> None: 
        """
        Correct the state estimate x-hat using the measurements in y.

        :param y: Measurement vector.
        """
    def error(self) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]: 
        """
        Returns difference between reference r and current state x-hat.
        """
    @typing.overload
    def nextR(self) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]: 
        """
        Returns the controller's next reference r.

        Returns an element of the controller's next reference r.

        :param i: Row of r.
        """
    @typing.overload
    def nextR(self, i: int) -> float: ...
    def predict(self, dt: seconds) -> None: 
        """
        Sets new controller output, projects model forward, and runs observer
        prediction.

        After calling this, the user should send the elements of u to the
        actuators.

        :param dt: Timestep for model update.
        """
    def reset(self, initialState: numpy.ndarray[numpy.float64, _Shape[1, 1]]) -> None: 
        """
        Zeroes reference r and controller output u. The previous reference
        of the PlantInversionFeedforward and the initial state estimate of
        the KalmanFilter are set to the initial state provided.

        :param initialState: The initial state.
        """
    def setNextR(self, nextR: numpy.ndarray[numpy.float64, _Shape[1, 1]]) -> None: 
        """
        Set the next reference r.

        :param nextR: Next reference.
        """
    @typing.overload
    def setXhat(self, i: int, value: float) -> None: 
        """
        Set the initial state estimate x-hat.

        :param xHat: The initial state estimate x-hat.

        Set an element of the initial state estimate x-hat.

        :param i:     Row of x-hat.
        :param value: Value for element of x-hat.
        """
    @typing.overload
    def setXhat(self, xHat: numpy.ndarray[numpy.float64, _Shape[1, 1]]) -> None: ...
    @typing.overload
    def xhat(self) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]: 
        """
        Returns the observer's state estimate x-hat.

        Returns an element of the observer's state estimate x-hat.

        :param i: Row of x-hat.
        """
    @typing.overload
    def xhat(self, i: int) -> float: ...
    pass
class LinearSystemLoop_2_1_1():
    """
    Combines a controller, feedforward, and observer for controlling a mechanism
    with full state feedback.

    For everything in this file, "inputs" and "outputs" are defined from the
    perspective of the plant. This means U is an input and Y is an output
    (because you give the plant U (powers) and it gives you back a Y (sensor
    values). This is the opposite of what they mean from the perspective of the
    controller (U is an output because that's what goes to the motors and Y is an
    input because that's what comes back from the sensors).

    For more on the underlying math, read
    https://file.tavsys.net/control/controls-engineering-in-frc.pdf.
    """
    @typing.overload
    def U(self) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]: 
        """
        Returns the controller's calculated control input u.

        Returns an element of the controller's calculated control input u.

        :param i: Row of u.
        """
    @typing.overload
    def U(self, i: int) -> float: ...
    @typing.overload
    def __init__(self, controller: wpimath._controls._controls.controller.LinearQuadraticRegulator_2_1, feedforward: wpimath._controls._controls.controller.LinearPlantInversionFeedforward_2_1, observer: wpimath._controls._controls.estimator.KalmanFilter_2_1_1, clampFunction: typing.Callable[[numpy.ndarray[numpy.float64, _Shape[1, 1]]], numpy.ndarray[numpy.float64, _Shape[1, 1]]]) -> None: 
        """
        Constructs a state-space loop with the given plant, controller, and
        observer. By default, the initial reference is all zeros. Users should
        call reset with the initial system state before enabling the loop. This
        constructor assumes that the input(s) to this system are voltage.

        :param controller: State-space controller.
        :param observer:   State-space observer.
        :param maxVoltage: The maximum voltage that can be applied. Commonly 12.
        :param dt:         The nominal timestep.

        Constructs a state-space loop with the given plant, controller, and
        observer. By default, the initial reference is all zeros. Users should
        call reset with the initial system state before enabling the loop. This
        constructor assumes that the input(s) to this system are voltage.

        :param plant:         State-space plant.
        :param controller:    State-space controller.
        :param observer:      State-space observer.
        :param clampFunction: The function used to clamp the input vector.
        :param dt:            The nominal timestep.

        Constructs a state-space loop with the given controller, feedforward and
        observer. By default, the initial reference is all zeros. Users should
        call reset with the initial system state.

        :param controller:  State-space controller.
        :param feedforward: Plant inversion feedforward.
        :param observer:    State-space observer.
        :param maxVoltage:  The maximum voltage that can be applied. Assumes
                            that the inputs are voltages.

        Constructs a state-space loop with the given controller, feedforward,
        observer and clamp function. By default, the initial reference is all
        zeros. Users should call reset with the initial system state.

        :param controller:    State-space controller.
        :param feedforward:   Plant-inversion feedforward.
        :param observer:      State-space observer.
        :param clampFunction: The function used to clamp the input vector.
        """
    @typing.overload
    def __init__(self, controller: wpimath._controls._controls.controller.LinearQuadraticRegulator_2_1, feedforward: wpimath._controls._controls.controller.LinearPlantInversionFeedforward_2_1, observer: wpimath._controls._controls.estimator.KalmanFilter_2_1_1, maxVoltage: volts) -> None: ...
    @typing.overload
    def __init__(self, plant: LinearSystem_2_1_1, controller: wpimath._controls._controls.controller.LinearQuadraticRegulator_2_1, observer: wpimath._controls._controls.estimator.KalmanFilter_2_1_1, clampFunction: typing.Callable[[numpy.ndarray[numpy.float64, _Shape[1, 1]]], numpy.ndarray[numpy.float64, _Shape[1, 1]]], dt: seconds) -> None: ...
    @typing.overload
    def __init__(self, plant: LinearSystem_2_1_1, controller: wpimath._controls._controls.controller.LinearQuadraticRegulator_2_1, observer: wpimath._controls._controls.estimator.KalmanFilter_2_1_1, maxVoltage: volts, dt: seconds) -> None: ...
    def clampInput(self, u: numpy.ndarray[numpy.float64, _Shape[1, 1]]) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]: 
        """
        Clamps input vector between system's minimum and maximum allowable input.

        :param u: Input vector to clamp.

        :returns: Clamped input vector.
        """
    def correct(self, y: numpy.ndarray[numpy.float64, _Shape[1, 1]]) -> None: 
        """
        Correct the state estimate x-hat using the measurements in y.

        :param y: Measurement vector.
        """
    def error(self) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Returns difference between reference r and current state x-hat.
        """
    @typing.overload
    def nextR(self) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Returns the controller's next reference r.

        Returns an element of the controller's next reference r.

        :param i: Row of r.
        """
    @typing.overload
    def nextR(self, i: int) -> float: ...
    def predict(self, dt: seconds) -> None: 
        """
        Sets new controller output, projects model forward, and runs observer
        prediction.

        After calling this, the user should send the elements of u to the
        actuators.

        :param dt: Timestep for model update.
        """
    def reset(self, initialState: numpy.ndarray[numpy.float64, _Shape[2, 1]]) -> None: 
        """
        Zeroes reference r and controller output u. The previous reference
        of the PlantInversionFeedforward and the initial state estimate of
        the KalmanFilter are set to the initial state provided.

        :param initialState: The initial state.
        """
    def setNextR(self, nextR: numpy.ndarray[numpy.float64, _Shape[2, 1]]) -> None: 
        """
        Set the next reference r.

        :param nextR: Next reference.
        """
    @typing.overload
    def setXhat(self, i: int, value: float) -> None: 
        """
        Set the initial state estimate x-hat.

        :param xHat: The initial state estimate x-hat.

        Set an element of the initial state estimate x-hat.

        :param i:     Row of x-hat.
        :param value: Value for element of x-hat.
        """
    @typing.overload
    def setXhat(self, xHat: numpy.ndarray[numpy.float64, _Shape[2, 1]]) -> None: ...
    @typing.overload
    def xhat(self) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Returns the observer's state estimate x-hat.

        Returns an element of the observer's state estimate x-hat.

        :param i: Row of x-hat.
        """
    @typing.overload
    def xhat(self, i: int) -> float: ...
    pass
class LinearSystemLoop_2_2_2():
    """
    Combines a controller, feedforward, and observer for controlling a mechanism
    with full state feedback.

    For everything in this file, "inputs" and "outputs" are defined from the
    perspective of the plant. This means U is an input and Y is an output
    (because you give the plant U (powers) and it gives you back a Y (sensor
    values). This is the opposite of what they mean from the perspective of the
    controller (U is an output because that's what goes to the motors and Y is an
    input because that's what comes back from the sensors).

    For more on the underlying math, read
    https://file.tavsys.net/control/controls-engineering-in-frc.pdf.
    """
    @typing.overload
    def U(self) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Returns the controller's calculated control input u.

        Returns an element of the controller's calculated control input u.

        :param i: Row of u.
        """
    @typing.overload
    def U(self, i: int) -> float: ...
    @typing.overload
    def __init__(self, controller: wpimath._controls._controls.controller.LinearQuadraticRegulator_2_2, feedforward: wpimath._controls._controls.controller.LinearPlantInversionFeedforward_2_2, observer: wpimath._controls._controls.estimator.KalmanFilter_2_2_2, clampFunction: typing.Callable[[numpy.ndarray[numpy.float64, _Shape[2, 1]]], numpy.ndarray[numpy.float64, _Shape[2, 1]]]) -> None: 
        """
        Constructs a state-space loop with the given plant, controller, and
        observer. By default, the initial reference is all zeros. Users should
        call reset with the initial system state before enabling the loop. This
        constructor assumes that the input(s) to this system are voltage.

        :param controller: State-space controller.
        :param observer:   State-space observer.
        :param maxVoltage: The maximum voltage that can be applied. Commonly 12.
        :param dt:         The nominal timestep.

        Constructs a state-space loop with the given plant, controller, and
        observer. By default, the initial reference is all zeros. Users should
        call reset with the initial system state before enabling the loop. This
        constructor assumes that the input(s) to this system are voltage.

        :param plant:         State-space plant.
        :param controller:    State-space controller.
        :param observer:      State-space observer.
        :param clampFunction: The function used to clamp the input vector.
        :param dt:            The nominal timestep.

        Constructs a state-space loop with the given controller, feedforward and
        observer. By default, the initial reference is all zeros. Users should
        call reset with the initial system state.

        :param controller:  State-space controller.
        :param feedforward: Plant inversion feedforward.
        :param observer:    State-space observer.
        :param maxVoltage:  The maximum voltage that can be applied. Assumes
                            that the inputs are voltages.

        Constructs a state-space loop with the given controller, feedforward,
        observer and clamp function. By default, the initial reference is all
        zeros. Users should call reset with the initial system state.

        :param controller:    State-space controller.
        :param feedforward:   Plant-inversion feedforward.
        :param observer:      State-space observer.
        :param clampFunction: The function used to clamp the input vector.
        """
    @typing.overload
    def __init__(self, controller: wpimath._controls._controls.controller.LinearQuadraticRegulator_2_2, feedforward: wpimath._controls._controls.controller.LinearPlantInversionFeedforward_2_2, observer: wpimath._controls._controls.estimator.KalmanFilter_2_2_2, maxVoltage: volts) -> None: ...
    @typing.overload
    def __init__(self, plant: LinearSystem_2_2_2, controller: wpimath._controls._controls.controller.LinearQuadraticRegulator_2_2, observer: wpimath._controls._controls.estimator.KalmanFilter_2_2_2, clampFunction: typing.Callable[[numpy.ndarray[numpy.float64, _Shape[2, 1]]], numpy.ndarray[numpy.float64, _Shape[2, 1]]], dt: seconds) -> None: ...
    @typing.overload
    def __init__(self, plant: LinearSystem_2_2_2, controller: wpimath._controls._controls.controller.LinearQuadraticRegulator_2_2, observer: wpimath._controls._controls.estimator.KalmanFilter_2_2_2, maxVoltage: volts, dt: seconds) -> None: ...
    def clampInput(self, u: numpy.ndarray[numpy.float64, _Shape[2, 1]]) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Clamps input vector between system's minimum and maximum allowable input.

        :param u: Input vector to clamp.

        :returns: Clamped input vector.
        """
    def correct(self, y: numpy.ndarray[numpy.float64, _Shape[2, 1]]) -> None: 
        """
        Correct the state estimate x-hat using the measurements in y.

        :param y: Measurement vector.
        """
    def error(self) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Returns difference between reference r and current state x-hat.
        """
    @typing.overload
    def nextR(self) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Returns the controller's next reference r.

        Returns an element of the controller's next reference r.

        :param i: Row of r.
        """
    @typing.overload
    def nextR(self, i: int) -> float: ...
    def predict(self, dt: seconds) -> None: 
        """
        Sets new controller output, projects model forward, and runs observer
        prediction.

        After calling this, the user should send the elements of u to the
        actuators.

        :param dt: Timestep for model update.
        """
    def reset(self, initialState: numpy.ndarray[numpy.float64, _Shape[2, 1]]) -> None: 
        """
        Zeroes reference r and controller output u. The previous reference
        of the PlantInversionFeedforward and the initial state estimate of
        the KalmanFilter are set to the initial state provided.

        :param initialState: The initial state.
        """
    def setNextR(self, nextR: numpy.ndarray[numpy.float64, _Shape[2, 1]]) -> None: 
        """
        Set the next reference r.

        :param nextR: Next reference.
        """
    @typing.overload
    def setXhat(self, i: int, value: float) -> None: 
        """
        Set the initial state estimate x-hat.

        :param xHat: The initial state estimate x-hat.

        Set an element of the initial state estimate x-hat.

        :param i:     Row of x-hat.
        :param value: Value for element of x-hat.
        """
    @typing.overload
    def setXhat(self, xHat: numpy.ndarray[numpy.float64, _Shape[2, 1]]) -> None: ...
    @typing.overload
    def xhat(self) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Returns the observer's state estimate x-hat.

        Returns an element of the observer's state estimate x-hat.

        :param i: Row of x-hat.
        """
    @typing.overload
    def xhat(self, i: int) -> float: ...
    pass
class LinearSystem_1_1_1():
    """
    A plant defined using state-space notation.

    A plant is a mathematical model of a system's dynamics.

    For more on the underlying math, read
    https://file.tavsys.net/control/controls-engineering-in-frc.pdf.
    """
    @typing.overload
    def A(self) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]: 
        """
        Returns the system matrix A.

        Returns an element of the system matrix A.

        :param i: Row of A.
        :param j: Column of A.
        """
    @typing.overload
    def A(self, i: int, j: int) -> float: ...
    @typing.overload
    def B(self) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]: 
        """
        Returns the input matrix B.

        Returns an element of the input matrix B.

        :param i: Row of B.
        :param j: Column of B.
        """
    @typing.overload
    def B(self, i: int, j: int) -> float: ...
    @typing.overload
    def C(self) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]: 
        """
        Returns the output matrix C.

        Returns an element of the output matrix C.

        :param i: Row of C.
        :param j: Column of C.
        """
    @typing.overload
    def C(self, i: int, j: int) -> float: ...
    @typing.overload
    def D(self) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]: 
        """
        Returns the feedthrough matrix D.

        Returns an element of the feedthrough matrix D.

        :param i: Row of D.
        :param j: Column of D.
        """
    @typing.overload
    def D(self, i: int, j: int) -> float: ...
    def __init__(self, A: numpy.ndarray[numpy.float64, _Shape[1, 1]], B: numpy.ndarray[numpy.float64, _Shape[1, 1]], C: numpy.ndarray[numpy.float64, _Shape[1, 1]], D: numpy.ndarray[numpy.float64, _Shape[1, 1]]) -> None: 
        """
        Constructs a discrete plant with the given continuous system coefficients.

        :param A: System matrix.
        :param B: Input matrix.
        :param C: Output matrix.
        :param D: Feedthrough matrix.
        """
    def calculateX(self, x: numpy.ndarray[numpy.float64, _Shape[1, 1]], clampedU: numpy.ndarray[numpy.float64, _Shape[1, 1]], dt: seconds) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]: 
        """
        Computes the new x given the old x and the control input.

        This is used by state observers directly to run updates based on state
        estimate.

        :param x:  The current state.
        :param u:  The control input.
        :param dt: Timestep for model update.
        """
    def calculateY(self, x: numpy.ndarray[numpy.float64, _Shape[1, 1]], clampedU: numpy.ndarray[numpy.float64, _Shape[1, 1]]) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]: 
        """
        Computes the new y given the control input.

        This is used by state observers directly to run updates based on state
        estimate.

        :param x:        The current state.
        :param clampedU: The control input.
        """
    pass
class LinearSystem_1_1_2():
    """
    A plant defined using state-space notation.

    A plant is a mathematical model of a system's dynamics.

    For more on the underlying math, read
    https://file.tavsys.net/control/controls-engineering-in-frc.pdf.
    """
    @typing.overload
    def A(self) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]: 
        """
        Returns the system matrix A.

        Returns an element of the system matrix A.

        :param i: Row of A.
        :param j: Column of A.
        """
    @typing.overload
    def A(self, i: int, j: int) -> float: ...
    @typing.overload
    def B(self) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]: 
        """
        Returns the input matrix B.

        Returns an element of the input matrix B.

        :param i: Row of B.
        :param j: Column of B.
        """
    @typing.overload
    def B(self, i: int, j: int) -> float: ...
    @typing.overload
    def C(self) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Returns the output matrix C.

        Returns an element of the output matrix C.

        :param i: Row of C.
        :param j: Column of C.
        """
    @typing.overload
    def C(self, i: int, j: int) -> float: ...
    @typing.overload
    def D(self) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Returns the feedthrough matrix D.

        Returns an element of the feedthrough matrix D.

        :param i: Row of D.
        :param j: Column of D.
        """
    @typing.overload
    def D(self, i: int, j: int) -> float: ...
    def __init__(self, A: numpy.ndarray[numpy.float64, _Shape[1, 1]], B: numpy.ndarray[numpy.float64, _Shape[1, 1]], C: numpy.ndarray[numpy.float64, _Shape[2, 1]], D: numpy.ndarray[numpy.float64, _Shape[2, 1]]) -> None: 
        """
        Constructs a discrete plant with the given continuous system coefficients.

        :param A: System matrix.
        :param B: Input matrix.
        :param C: Output matrix.
        :param D: Feedthrough matrix.
        """
    def calculateX(self, x: numpy.ndarray[numpy.float64, _Shape[1, 1]], clampedU: numpy.ndarray[numpy.float64, _Shape[1, 1]], dt: seconds) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]: 
        """
        Computes the new x given the old x and the control input.

        This is used by state observers directly to run updates based on state
        estimate.

        :param x:  The current state.
        :param u:  The control input.
        :param dt: Timestep for model update.
        """
    def calculateY(self, x: numpy.ndarray[numpy.float64, _Shape[1, 1]], clampedU: numpy.ndarray[numpy.float64, _Shape[1, 1]]) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Computes the new y given the control input.

        This is used by state observers directly to run updates based on state
        estimate.

        :param x:        The current state.
        :param clampedU: The control input.
        """
    pass
class LinearSystem_2_1_1():
    """
    A plant defined using state-space notation.

    A plant is a mathematical model of a system's dynamics.

    For more on the underlying math, read
    https://file.tavsys.net/control/controls-engineering-in-frc.pdf.
    """
    @typing.overload
    def A(self) -> numpy.ndarray[numpy.float64, _Shape[2, 2]]: 
        """
        Returns the system matrix A.

        Returns an element of the system matrix A.

        :param i: Row of A.
        :param j: Column of A.
        """
    @typing.overload
    def A(self, i: int, j: int) -> float: ...
    @typing.overload
    def B(self) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Returns the input matrix B.

        Returns an element of the input matrix B.

        :param i: Row of B.
        :param j: Column of B.
        """
    @typing.overload
    def B(self, i: int, j: int) -> float: ...
    @typing.overload
    def C(self) -> numpy.ndarray[numpy.float64, _Shape[1, 2]]: 
        """
        Returns the output matrix C.

        Returns an element of the output matrix C.

        :param i: Row of C.
        :param j: Column of C.
        """
    @typing.overload
    def C(self, i: int, j: int) -> float: ...
    @typing.overload
    def D(self) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]: 
        """
        Returns the feedthrough matrix D.

        Returns an element of the feedthrough matrix D.

        :param i: Row of D.
        :param j: Column of D.
        """
    @typing.overload
    def D(self, i: int, j: int) -> float: ...
    def __init__(self, A: numpy.ndarray[numpy.float64, _Shape[2, 2]], B: numpy.ndarray[numpy.float64, _Shape[2, 1]], C: numpy.ndarray[numpy.float64, _Shape[1, 2]], D: numpy.ndarray[numpy.float64, _Shape[1, 1]]) -> None: 
        """
        Constructs a discrete plant with the given continuous system coefficients.

        :param A: System matrix.
        :param B: Input matrix.
        :param C: Output matrix.
        :param D: Feedthrough matrix.
        """
    def calculateX(self, x: numpy.ndarray[numpy.float64, _Shape[2, 1]], clampedU: numpy.ndarray[numpy.float64, _Shape[1, 1]], dt: seconds) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Computes the new x given the old x and the control input.

        This is used by state observers directly to run updates based on state
        estimate.

        :param x:  The current state.
        :param u:  The control input.
        :param dt: Timestep for model update.
        """
    def calculateY(self, x: numpy.ndarray[numpy.float64, _Shape[2, 1]], clampedU: numpy.ndarray[numpy.float64, _Shape[1, 1]]) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]: 
        """
        Computes the new y given the control input.

        This is used by state observers directly to run updates based on state
        estimate.

        :param x:        The current state.
        :param clampedU: The control input.
        """
    pass
class LinearSystem_2_1_2():
    """
    A plant defined using state-space notation.

    A plant is a mathematical model of a system's dynamics.

    For more on the underlying math, read
    https://file.tavsys.net/control/controls-engineering-in-frc.pdf.
    """
    @typing.overload
    def A(self) -> numpy.ndarray[numpy.float64, _Shape[2, 2]]: 
        """
        Returns the system matrix A.

        Returns an element of the system matrix A.

        :param i: Row of A.
        :param j: Column of A.
        """
    @typing.overload
    def A(self, i: int, j: int) -> float: ...
    @typing.overload
    def B(self) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Returns the input matrix B.

        Returns an element of the input matrix B.

        :param i: Row of B.
        :param j: Column of B.
        """
    @typing.overload
    def B(self, i: int, j: int) -> float: ...
    @typing.overload
    def C(self) -> numpy.ndarray[numpy.float64, _Shape[2, 2]]: 
        """
        Returns the output matrix C.

        Returns an element of the output matrix C.

        :param i: Row of C.
        :param j: Column of C.
        """
    @typing.overload
    def C(self, i: int, j: int) -> float: ...
    @typing.overload
    def D(self) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Returns the feedthrough matrix D.

        Returns an element of the feedthrough matrix D.

        :param i: Row of D.
        :param j: Column of D.
        """
    @typing.overload
    def D(self, i: int, j: int) -> float: ...
    def __init__(self, A: numpy.ndarray[numpy.float64, _Shape[2, 2]], B: numpy.ndarray[numpy.float64, _Shape[2, 1]], C: numpy.ndarray[numpy.float64, _Shape[2, 2]], D: numpy.ndarray[numpy.float64, _Shape[2, 1]]) -> None: 
        """
        Constructs a discrete plant with the given continuous system coefficients.

        :param A: System matrix.
        :param B: Input matrix.
        :param C: Output matrix.
        :param D: Feedthrough matrix.
        """
    def calculateX(self, x: numpy.ndarray[numpy.float64, _Shape[2, 1]], clampedU: numpy.ndarray[numpy.float64, _Shape[1, 1]], dt: seconds) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Computes the new x given the old x and the control input.

        This is used by state observers directly to run updates based on state
        estimate.

        :param x:  The current state.
        :param u:  The control input.
        :param dt: Timestep for model update.
        """
    def calculateY(self, x: numpy.ndarray[numpy.float64, _Shape[2, 1]], clampedU: numpy.ndarray[numpy.float64, _Shape[1, 1]]) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Computes the new y given the control input.

        This is used by state observers directly to run updates based on state
        estimate.

        :param x:        The current state.
        :param clampedU: The control input.
        """
    pass
class LinearSystem_2_2_1():
    """
    A plant defined using state-space notation.

    A plant is a mathematical model of a system's dynamics.

    For more on the underlying math, read
    https://file.tavsys.net/control/controls-engineering-in-frc.pdf.
    """
    @typing.overload
    def A(self) -> numpy.ndarray[numpy.float64, _Shape[2, 2]]: 
        """
        Returns the system matrix A.

        Returns an element of the system matrix A.

        :param i: Row of A.
        :param j: Column of A.
        """
    @typing.overload
    def A(self, i: int, j: int) -> float: ...
    @typing.overload
    def B(self) -> numpy.ndarray[numpy.float64, _Shape[2, 2]]: 
        """
        Returns the input matrix B.

        Returns an element of the input matrix B.

        :param i: Row of B.
        :param j: Column of B.
        """
    @typing.overload
    def B(self, i: int, j: int) -> float: ...
    @typing.overload
    def C(self) -> numpy.ndarray[numpy.float64, _Shape[1, 2]]: 
        """
        Returns the output matrix C.

        Returns an element of the output matrix C.

        :param i: Row of C.
        :param j: Column of C.
        """
    @typing.overload
    def C(self, i: int, j: int) -> float: ...
    @typing.overload
    def D(self) -> numpy.ndarray[numpy.float64, _Shape[1, 2]]: 
        """
        Returns the feedthrough matrix D.

        Returns an element of the feedthrough matrix D.

        :param i: Row of D.
        :param j: Column of D.
        """
    @typing.overload
    def D(self, i: int, j: int) -> float: ...
    def __init__(self, A: numpy.ndarray[numpy.float64, _Shape[2, 2]], B: numpy.ndarray[numpy.float64, _Shape[2, 2]], C: numpy.ndarray[numpy.float64, _Shape[1, 2]], D: numpy.ndarray[numpy.float64, _Shape[1, 2]]) -> None: 
        """
        Constructs a discrete plant with the given continuous system coefficients.

        :param A: System matrix.
        :param B: Input matrix.
        :param C: Output matrix.
        :param D: Feedthrough matrix.
        """
    def calculateX(self, x: numpy.ndarray[numpy.float64, _Shape[2, 1]], clampedU: numpy.ndarray[numpy.float64, _Shape[2, 1]], dt: seconds) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Computes the new x given the old x and the control input.

        This is used by state observers directly to run updates based on state
        estimate.

        :param x:  The current state.
        :param u:  The control input.
        :param dt: Timestep for model update.
        """
    def calculateY(self, x: numpy.ndarray[numpy.float64, _Shape[2, 1]], clampedU: numpy.ndarray[numpy.float64, _Shape[2, 1]]) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]: 
        """
        Computes the new y given the control input.

        This is used by state observers directly to run updates based on state
        estimate.

        :param x:        The current state.
        :param clampedU: The control input.
        """
    pass
class LinearSystem_2_2_2():
    """
    A plant defined using state-space notation.

    A plant is a mathematical model of a system's dynamics.

    For more on the underlying math, read
    https://file.tavsys.net/control/controls-engineering-in-frc.pdf.
    """
    @typing.overload
    def A(self) -> numpy.ndarray[numpy.float64, _Shape[2, 2]]: 
        """
        Returns the system matrix A.

        Returns an element of the system matrix A.

        :param i: Row of A.
        :param j: Column of A.
        """
    @typing.overload
    def A(self, i: int, j: int) -> float: ...
    @typing.overload
    def B(self) -> numpy.ndarray[numpy.float64, _Shape[2, 2]]: 
        """
        Returns the input matrix B.

        Returns an element of the input matrix B.

        :param i: Row of B.
        :param j: Column of B.
        """
    @typing.overload
    def B(self, i: int, j: int) -> float: ...
    @typing.overload
    def C(self) -> numpy.ndarray[numpy.float64, _Shape[2, 2]]: 
        """
        Returns the output matrix C.

        Returns an element of the output matrix C.

        :param i: Row of C.
        :param j: Column of C.
        """
    @typing.overload
    def C(self, i: int, j: int) -> float: ...
    @typing.overload
    def D(self) -> numpy.ndarray[numpy.float64, _Shape[2, 2]]: 
        """
        Returns the feedthrough matrix D.

        Returns an element of the feedthrough matrix D.

        :param i: Row of D.
        :param j: Column of D.
        """
    @typing.overload
    def D(self, i: int, j: int) -> float: ...
    def __init__(self, A: numpy.ndarray[numpy.float64, _Shape[2, 2]], B: numpy.ndarray[numpy.float64, _Shape[2, 2]], C: numpy.ndarray[numpy.float64, _Shape[2, 2]], D: numpy.ndarray[numpy.float64, _Shape[2, 2]]) -> None: 
        """
        Constructs a discrete plant with the given continuous system coefficients.

        :param A: System matrix.
        :param B: Input matrix.
        :param C: Output matrix.
        :param D: Feedthrough matrix.
        """
    def calculateX(self, x: numpy.ndarray[numpy.float64, _Shape[2, 1]], clampedU: numpy.ndarray[numpy.float64, _Shape[2, 1]], dt: seconds) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Computes the new x given the old x and the control input.

        This is used by state observers directly to run updates based on state
        estimate.

        :param x:  The current state.
        :param u:  The control input.
        :param dt: Timestep for model update.
        """
    def calculateY(self, x: numpy.ndarray[numpy.float64, _Shape[2, 1]], clampedU: numpy.ndarray[numpy.float64, _Shape[2, 1]]) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Computes the new y given the control input.

        This is used by state observers directly to run updates based on state
        estimate.

        :param x:        The current state.
        :param clampedU: The control input.
        """
    pass
class MecanumDrivePoseEstimator():
    """
    This class wraps an Unscented Kalman Filter to fuse latency-compensated
    vision measurements with mecanum drive encoder velocity measurements. It will
    correct for noisy measurements and encoder drift. It is intended to be an
    easy but more accurate drop-in for MecanumDriveOdometry.

    Update() should be called every robot loop. If your loops are faster or
    slower than the default of 0.02s, then you should change the nominal delta
    time by specifying it in the constructor.

    AddVisionMeasurement() can be called as infrequently as you want; if you
    never call it, then this class will behave mostly like regular encoder
    odometry.

    Our state-space system is:

    <strong> x = [[x, y, theta]]^T </strong> in the
    field-coordinate system.

    <strong> u = [[vx, vy, omega]]^T </strong> in the field-coordinate system.

    <strong> y = [[x, y, theta]]^T </strong> in field
    coords from vision, or <strong> y = [[theta]]^T
    </strong> from the gyro.
    """
    def __init__(self, gyroAngle: wpimath.geometry._geometry.Rotation2d, initialPose: wpimath.geometry._geometry.Pose2d, kinematics: wpimath.kinematics._kinematics.MecanumDriveKinematics, stateStdDevs: typing.Tuple[float], localMeasurementStdDevs: typing.Tuple[float], visionMeasurementStdDevs: typing.Tuple[float], nominalDt: seconds = 0.02) -> None: 
        """
        Constructs a MecanumDrivePoseEstimator.

        :param gyroAngle:                The current gyro angle.
        :param initialPoseMeters:        The starting pose estimate.
        :param kinematics:               A correctly-configured kinematics object
                                         for your drivetrain.
        :param stateStdDevs:             Standard deviations of model states.
                                         Increase these numbers to trust your
                                         model's state estimates less. This matrix
                                         is in the form [x, y, theta]^T, with units
                                         in meters and radians.
        :param localMeasurementStdDevs:  Standard deviations of the encoder and gyro
                                         measurements. Increase these numbers to
                                         trust sensor readings from encoders
                                         and gyros less. This matrix is in the form
                                         [theta], with units in radians.
        :param visionMeasurementStdDevs: Standard deviations of the vision
                                         measurements. Increase these numbers to
                                         trust global measurements from vision
                                         less. This matrix is in the form
                                         [x, y, theta]^T, with units in meters and
                                         radians.
        :param nominalDt:                The time in seconds between each robot
                                         loop.
        """
    def addVisionMeasurement(self, visionRobotPose: wpimath.geometry._geometry.Pose2d, timestamp: seconds) -> None: 
        """
        Add a vision measurement to the Unscented Kalman Filter. This will correct
        the odometry pose estimate while still accounting for measurement noise.

        This method can be called as infrequently as you want, as long as you are
        calling Update() every loop.

        :param visionRobotPose: The pose of the robot as measured by the vision
                                camera.
        :param timestamp:       The timestamp of the vision measurement in seconds.
                                Note that if you don't use your own time source by
                                calling UpdateWithTime() then you must use a
                                timestamp with an epoch since FPGA startup
                                (i.e. the epoch of this timestamp is the same
                                epoch as Timer#GetFPGATimestamp.) This means
                                that you should use Timer#GetFPGATimestamp as your
                                time source or sync the epochs.
        """
    def getEstimatedPosition(self) -> wpimath.geometry._geometry.Pose2d: 
        """
        Gets the pose of the robot at the current time as estimated by the Extended
        Kalman Filter.

        :returns: The estimated robot pose in meters.
        """
    def resetPosition(self, pose: wpimath.geometry._geometry.Pose2d, gyroAngle: wpimath.geometry._geometry.Rotation2d) -> None: 
        """
        Resets the robot's position on the field.

        You NEED to reset your encoders (to zero) when calling this method.

        The gyroscope angle does not need to be reset in the user's robot code.
        The library automatically takes care of offsetting the gyro angle.

        :param poseMeters: The position on the field that your robot is at.
        :param gyroAngle:  The angle reported by the gyroscope.
        """
    def setVisionMeasurementStdDevs(self, visionMeasurementStdDevs: typing.Tuple[float]) -> None: 
        """
        Sets the pose estimator's trust of global measurements. This might be used
        to change trust in vision measurements after the autonomous period, or to
        change trust as distance to a vision target increases.

        :param visionMeasurementStdDevs: Standard deviations of the vision
                                         measurements. Increase these numbers to
                                         trust global measurements from vision
                                         less. This matrix is in the form
                                         [x, y, theta]^T, with units in meters and
                                         radians.
        """
    def update(self, gyroAngle: wpimath.geometry._geometry.Rotation2d, wheelSpeeds: wpimath.kinematics._kinematics.MecanumDriveWheelSpeeds) -> wpimath.geometry._geometry.Pose2d: 
        """
        Updates the the Unscented Kalman Filter using only wheel encoder
        information. This should be called every loop, and the correct loop period
        must be passed into the constructor of this class.

        :param gyroAngle:   The current gyro angle.
        :param wheelSpeeds: The current speeds of the mecanum drive wheels.

        :returns: The estimated pose of the robot in meters.
        """
    def updateWithTime(self, currentTime: seconds, gyroAngle: wpimath.geometry._geometry.Rotation2d, wheelSpeeds: wpimath.kinematics._kinematics.MecanumDriveWheelSpeeds) -> wpimath.geometry._geometry.Pose2d: 
        """
        Updates the the Unscented Kalman Filter using only wheel encoder
        information. This should be called every loop, and the correct loop period
        must be passed into the constructor of this class.

        :param currentTimeSeconds: Time at which this method was called, in seconds.
        :param gyroAngle:          The current gyroscope angle.
        :param wheelSpeeds:        The current speeds of the mecanum drive wheels.

        :returns: The estimated pose of the robot in meters.
        """
    pass
