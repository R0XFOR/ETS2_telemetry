import mmap
import struct

class SharedMemory:
    def __init__(self) -> None:
        self.map_name = "Local\\SCSTelemetry"
        self.map_size = 22*1024
        self.mmap = None

    def connect(self) -> None:
        self.mmap = mmap.mmap(0, self.map_size, self.map_name, mmap.ACCESS_READ, 0)

    def update(self):
        self.connect()
        updated_data = TelemetryData()

        updated_data.sdkActive = self.get_field("?", 0, 1)
        updated_data.paused = self.get_field("?", 4, 5)

        return updated_data

    def get_field(self, f, start, end):
        field_data = struct.unpack(f, self.mmap[start:end])[0]
        return field_data

    def get_array(self, f, start, end) -> tuple:
        array_data = struct.unpack(f, self.mmap[start:end])
        return array_data

class TelemetryData:
    def __init__(self) -> None:
        #----- START OF FIRST ZONE AT OFFSET 0 -----#

        self.sdkActive = False # display if game / sdk runs
        self.paused = False # check if the game and the telemetry is paused

        # not the game time, only a timestamp. Used to update the values on the other site of the shared memory
        self.time = 0
        self.simulatedTime = 0
        self.renderTime = 0
        self.multiplayerTimeOffset = 0

        #----- END OF FIRST ZONE AT OFFSET 39 -----#
        
        #----- START OF SECOND ZONE AT OFFSET 40 -----#

        self.telemetry_plugin_revision = 0 # Telemetry Plugin Version
        self.version_major = 0 # Game major version
        self.version_minor = 0 # Game minor version
        self.game = 0 # Game identifier (actually 0 for unknown, 1 for ets2 and 2 for ats)
        self.telemetry_version_game_major = 0 # Game telemetry version major
        self.telemetry_version_game_minor = 0 # Game telemetry version minor

        self.time_abs = 0 # In game time in minutes

        self.gears = 0
        self.gears_reverse = 0
        self.retarderStepCount = 0
        self.truckWheelCount = 0
        self.selectorCount = 0
        self.time_abs_delivery = 0
        self.maxTrailerCount = 0
        self.unitCount = 0
        self.plannedDistanceKm = 0

        self.shifterSlot = 0
        self.retarderBrake = 0
        self.lightsAuxFront = 0
        self.lightsAuxRoof = 0
        self.truck_wheelSubstance = 0 # [16]
        self.hshifterPosition = 0 # [32]
        self.hshifterBitmask = 0 # [32]

        self.jobDeliveredDeliveryTime = 0
        self.jobStartingTime = 0
        self.jobFinishedTime = 0

        #----- END OF SECOND ZONE AT OFFSET 499 -----#

        #----- START OF Third ZONE AT OFFSET 500 -----#

        self.restStop = 0

        self.gear = 0
        self.gearDashboard = 0
        self.hshifterResulting = 0 # [32]

        self.jobDeliveredEarnedXp = 0

        #----- END OF third ZONE AT OFFSET 699 -----#

        #----- START OF FOURTH ZONE AT OFFSET 700 -----#

        self.scale = 0.0

        self.fuelCapacity = 0.0
        self.fuelWarningFactor = 0.0
        self.adblueCapacity = 0.0
        self.adblueWarningFactor = 0.0
        self.airPressureWarning = 0.0
        self.airPressurEmergency = 0.0
        self.oilPressureWarning = 0.0
        self.waterTemperatureWarning = 0.0
        self.batteryVoltageWarning = 0.0
        self.engineRpmMax = 0.0
        self.gearDifferential = 0.0
        self.cargoMass = 0.0
        self.truckWheelRadius = 0.0
        self.gearRatiosForward = 0.0
        self.gearRatiosReverse = 0.0
        self.unitMass = 0.0

        self.speed = 0.0
        self.engineRpm = 0.0
        self.userSteer = 0.0
        self.userThrottle = 0.0
        self.userBrake = 0.0
        self.userClutch = 0.0
        self.gameSteer = 0.0
        self.gameThrottle = 0.0
        self.gameBrake = 0.0
        self.gameClutch = 0.0
        self.cruiseControlSpeed = 0.0
        self.airPressure = 0.0
        self.brakeTemperature = 0.0
        self.fuel = 0.0
        self.fuelAvgConsumption = 0.0
        self.fuelRange = 0.0
        self.adblue = 0.0
        self.oilPressure = 0.0
        self.oilTemperature = 0.0
        self.waterTemperature = 0.0
        self.batteryVoltage = 0.0
        self.lightsDashboard = 0.0
        self.wearEngine = 0.0
        self.wearTransmission = 0.0
        self.wearCabin = 0.0
        self.wearChassis = 0.0
        self.wearWheels = 0.0
        self.truckOdometer = 0.0
        self.routeDistance = 0.0
        self.routeTime = 0.0
        self.speedLimit = 0.0
        self.truck_wheelSuspDeflection = 0.0 # [16]
        self.truck_wheelVelocity = 0.0 # [16]
        self.truck_wheelSteering = 0.0 # [16]
        self.truck_wheelRotation = 0.0 # [16]
        self.truck_wheelLift = 0.0 # [16]
        self.truck_wheelLiftOffset = 0.0 # [16]

        self.jobDeliveredCargoDamage = 0.0
        self.jobDeliveredDistanceKm = 0.0
        self.refuelAmount = 0.0

        self.cargoDamage = 0.0

        #----- END OF FOURTH ZONE AT OFFSET 1499 -----#

        #----- START OF FIFTH ZONE AT OFFSET 1500 -----#

        self.truckWheelSteerable = False # [16]
        self.truckWheelSimulated = False # [16]
        self.truckWheelPowered = False # [16]
        self.truckWheelLiftable = False # [16]

        self.isCargoLoaded = False
        self.specialJob = False

        self.parkBrake = False
        self.motorBrake = False
        self.airPressureWarning = False
        self.airPressureEmergency = False
        self.fuelWarning = False
        self.adblueWarning = False
        self.oilPressureWarning = False
        self.waterTemperatureWarning = False
        self.batteryVoltageWarning = False
        self.electricEnabled = False
        self.engineEnabled = False
        self.wipers = False
        self.blinkerLeftActive = False
        self.blinkerRightActive = False
        self.blinkerLeftOn = False
        self.blinkerRightOn = False
        self.lightsParking = False
        self.lightsBeamLow = False
        self.lightsBeamHigh = False
        self.lightsBeacon = False
        self.lightsBrake = False
        self.lightsReverse = False
        self.lightsHazard = False
        self.cruiseControl = False # special field not a sdk field
        self.truck_wheelOnGround = False # [16]
        self.shifterToggle = False # [2]
        self.differentialLock = False
        self.liftAxle = False
        self.liftAxleIndicator = False
        self.trailerLiftAxle = False
        self.trailerLiftAxleIndicator = False

        self.jobDeliveredAutoparkUsed = False
        self.jobDeliveredAutoloadUsed = False

        #----- END OF FIFTH ZONE AT OFFSET 1639 -----#

        #----- START OF SIXTH ZONE AT OFFSET 1640 -----#

        self.cabinPositionX = 0.0
        self.cabinPositionY = 0.0
        self.cabinPositionZ = 0.0
        self.headPositionX = 0.0
        self.headPositionY = 0.0
        self.headPositionZ = 0.0
        self.truckHookPositionX = 0.0
        self.truckHookPositionY = 0.0
        self.truckHookPositionZ = 0.0
        self.truckWheelPositionX = 0.0 # [16]
        self.truckWheelPositionY = 0.0 # [16]
        self.truckWheelPositionZ = 0.0 # [16]

        self.lv_accelerationX = 0.0
        self.lv_accelerationY = 0.0
        self.lv_accelerationZ = 0.0
        self.av_accelerationX = 0.0
        self.av_accelerationY = 0.0
        self.av_accelerationZ = 0.0
        self.accelerationX = 0.0
        self.accelerationY = 0.0
        self.accelerationZ = 0.0
        self.aa_accelerationX = 0.0
        self.aa_accelerationY = 0.0
        self.aa_accelerationZ = 0.0
        self.cabinAVX = 0.0
        self.cabinAVY = 0.0
        self.cabinAVZ = 0.0
        self.cabinAAX = 0.0
        self.cabinAAY = 0.0
        self.cabinAAZ = 0.0

        self.cabinOffsetX = 0.0
        self.cabinOffsetY = 0.0
        self.cabinOffsetZ = 0.0
        self.cabinOffsetrotationX = 0.0
        self.cabinOffsetrotationY = 0.0
        self.cabinOffsetrotationZ = 0.0
        self.headOffsetX = 0.0
        self.headOffsetY = 0.0
        self.headOffsetZ = 0.0
        self.headOffsetrotationX = 0.0
        self.headOffsetrotationY = 0.0
        self.headOffsetrotationZ = 0.0

        #----- END OF 7TH ZONE AT OFFSET 2199 -----#

        #----- START OF 8TH ZONE AT OFFSET 2200 -----#

        self.coordinateX = 0.0
        self.coordinateY = 0.0
        self.coordinateZ = 0.0
        self.rotationX = 0.0
        self.rotationY = 0.0
        self.rotationZ = 0.0

        #----- END OF 8TH ZONE AT OFFSET 2299 -----#

        #----- START OF 9TH ZONE AT OFFSET 2300 -----#

        self.truckBrandId = "" # [stringsize]
        self.truckBrand = "" # [stringsize]
        self.truckId = "" # [stringsize]

        self.truckName = "" # [stringsize]
        self.cargoId = "" # [stringsize]
        self.cargo = "" # [stringsize]
        self.cityDstId = "" # [stringsize]
        self.cityDst = "" # [stringsize]
        self.compDstId = "" # [stringsize]
        self.compDst = "" # [stringsize]
        self.citySrcId = "" # [stringsize]
        self.citySrc = "" # [stringsize]
        self.compSrcId = "" # [stringsize]
        self.compSrc = "" # [stringsize]
        self.shifterType = "" # [16]

        self.truckLicensePlate = "" # [stringsize]
        self.truckLicensePlateCountryId = "" # [stringsize]
        self.truckLicensePlateCountry = "" # [stringsize]

        self.jobMarket = "" # [32]

        self.fineOffence = "" # [32]
        self.ferrySourceName = "" # [stringsize]
        self.ferryTargetName = "" # [stringsize]
        self.ferrySourceId = "" # [stringsize]
        self.ferryTargetId = "" # [stringsize]
        self.trainSourceName = "" # [stringsize]
        self.trainTargetName = "" # [stringsize]
        self.trainSourceId = "" # [stringsize]
        self.trainTargetId = "" # [stringsize]

        #----- END OF 9TH ZONE AT OFFSET 3999 -----#

        #----- START OF 10TH ZONE AT OFFSET 4000 -----#

        self.jobIncome = 0

        #----- END OF 10TH ZONE AT OFFSET 4199 -----#

        #----- START OF 11TH ZONE AT OFFSET 4200 -----#

        self.jobCancelledPenalty = 0
        self.jobDeliveredRevenue = 0
        self.fineAmount = 0
        self.tollgatePayAmount = 0
        self.ferryPayAmount = 0
        self.trainPayAmount = 0

        #----- END OF 11TH ZONE AT OFFSET 4299 -----#

        #----- START OF 12TH ZONE AT OFFSET 4300 -----#

        self.onJob = False
        self.jobFinished = False
        self.jobCancelled = False
        self.jobDelivered = False
        self.fined = False
        self.tollgate = False
        self.ferry = False
        self.train = False
        self.refuel = False
        self.refuelPayed = False

        #----- END OF 12TH ZONE AT OFFSET 4399 -----#

        self.substance = "" #[SUBSTANCE_SIZE][stringsize]

        #----- END OF 13TH ZONE AT OFFSET 5999 -----#

        #----- START OF 14TH ZONE AT OFFSET 6000 -----//

        #scsTrailer_t trailer[10];

        #----- END OF 14TH ZONE AT OFFSET 21619 -----#

if __name__ == "__main__":
    data = SharedMemory().update()
    print(data.sdkActive, data.paused)