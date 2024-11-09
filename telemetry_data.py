import mmap
import struct

class SharedMemory:
    def __init__(self) -> None:
        self.map_name = "Local\\SCSTelemetry"
        self.map_size = 32*1024
        self.mmap = None

    def connect(self) -> None:
        self.mmap = mmap.mmap(0, self.map_size, self.map_name, mmap.ACCESS_READ, 0)

    def update(self):
        self.connect()
        updated_data = TelemetryData()

        #----- START OF FIRST ZONE AT OFFSET 0 -----#

        updated_data.sdkActive = self.get_field("?", 0) # display if game / sdk runs
        updated_data.paused = self.get_field("?", 4) # check if the game and the telemetry is paused

        # not the game time, only a timestamp. Used to update the values on the other site of the shared memory
        updated_data.time = self.get_field("Q", 8)
        updated_data.simulatedTime = self.get_field("Q", 16)
        updated_data.renderTime = self.get_field("Q", 24)
        updated_data.multiplayerTimeOffset = self.get_field("Q", 32)

        #----- END OF FIRST ZONE AT OFFSET 39 -----#
        
        #----- START OF SECOND ZONE AT OFFSET 40 -----#

        updated_data.telemetry_plugin_revision = self.get_field("I", 40) # Telemetry Plugin Version
        updated_data.version_major = self.get_field("I", 44) # Game major version
        updated_data.version_minor = self.get_field("I", 48) # Game minor version
        updated_data.game = self.get_field("I", 52) # Game identifier (actually 0 for unknown, 1 for ets2 and 2 for ats)
        updated_data.telemetry_version_game_major = self.get_field("I", 56) # Game telemetry version major
        updated_data.telemetry_version_game_minor = self.get_field("I", 60) # Game telemetry version minor

        #updated_data.time_abs = self.get_field("I", 64, 68) # In game time in minutes
        updated_data.time_abs = self.get_field("I", 64) # In game time in minutes

        updated_data.gears = self.get_field("I", 68)
        updated_data.gears_reverse = self.get_field("I", 72)
        updated_data.retarderStepCount = self.get_field("I", 76)
        updated_data.truckWheelCount = self.get_field("I", 80)
        updated_data.selectorCount = self.get_field("I", 84)
        updated_data.time_abs_delivery = self.get_field("I", 88)
        updated_data.maxTrailerCount = self.get_field("I", 92)
        updated_data.unitCount = self.get_field("I", 96)
        updated_data.plannedDistanceKm = self.get_field("I", 100)

        updated_data.shifterSlot = self.get_field("I", 104)
        updated_data.retarderBrake = self.get_field("I", 108)
        updated_data.lightsAuxFront = self.get_field("I", 112)
        updated_data.lightsAuxRoof = self.get_field("I", 116)
        updated_data.truck_wheelSubstance = self.get_array("16I", 120)
        updated_data.hshifterPosition = self.get_array("32I", 184)
        updated_data.hshifterBitmask = self.get_array("32I", 312)

        updated_data.jobDeliveredDeliveryTime = self.get_field("I", 440)
        updated_data.jobStartingTime = self.get_field("I", 444)
        updated_data.jobFinishedTime = self.get_field("I", 448)

        #----- END OF SECOND ZONE AT OFFSET 499 -----#

        #----- START OF Third ZONE AT OFFSET 500 -----#

        updated_data.restStop = self.get_field("i", 500)

        updated_data.gear = self.get_field("i", 504)
        updated_data.gearDashboard = self.get_field("i", 508)
        updated_data.hshifterResulting = self.get_array("32i", 512)

        updated_data.jobDeliveredEarnedXp = self.get_field("i", 640)

        #----- END OF third ZONE AT OFFSET 699 -----#

        #----- START OF FOURTH ZONE AT OFFSET 700 -----#

        updated_data.scale = self.get_field("f", 700)

        updated_data.fuelCapacity = self.get_field("f", 704)
        updated_data.fuelWarningFactor = self.get_field("f", 708)
        updated_data.adblueCapacity = self.get_field("f", 712)
        updated_data.adblueWarningFactor = self.get_field("f", 716)
        updated_data.airPressureWarning = self.get_field("f", 720)
        updated_data.airPressurEmergency = self.get_field("f", 724)
        updated_data.oilPressureWarning = self.get_field("f", 728)
        updated_data.waterTemperatureWarning = self.get_field("f", 732)
        updated_data.batteryVoltageWarning = self.get_field("f", 736)
        updated_data.engineRpmMax = self.get_field("f", 740)
        updated_data.gearDifferential = self.get_field("f", 744)
        updated_data.cargoMass = self.get_field("f", 748)
        updated_data.truckWheelRadius = self.get_array("16f", 752)
        updated_data.gearRatiosForward = self.get_array("24f", 816)
        updated_data.gearRatiosReverse = self.get_array("8f", 912)
        updated_data.unitMass = self.get_field("f", 944)

        updated_data.speed = self.get_field("f", 948)
        updated_data.engineRpm = self.get_field("f", 952)
        updated_data.userSteer = self.get_field("f", 956)
        updated_data.userThrottle = self.get_field("f", 960)
        updated_data.userBrake = self.get_field("f", 964)
        updated_data.userClutch = self.get_field("f", 968)
        updated_data.gameSteer = self.get_field("f", 972)
        updated_data.gameThrottle = self.get_field("f", 976)
        updated_data.gameBrake = self.get_field("f", 980)
        updated_data.gameClutch = self.get_field("f", 984)
        updated_data.cruiseControlSpeed = self.get_field("f", 988)
        updated_data.airPressure = self.get_field("f", 992)
        updated_data.brakeTemperature = self.get_field("f", 996)
        updated_data.fuel = self.get_field("f", 1000)
        updated_data.fuelAvgConsumption = self.get_field("f", 1004)
        updated_data.fuelRange = self.get_field("f", 1008)
        updated_data.adblue = self.get_field("f", 1012)
        updated_data.oilPressure = self.get_field("f", 1016)
        updated_data.oilTemperature = self.get_field("f", 1020)
        updated_data.waterTemperature = self.get_field("f", 1024)
        updated_data.batteryVoltage = self.get_field("f", 1028)
        updated_data.lightsDashboard = self.get_field("f", 1032)
        updated_data.wearEngine = self.get_field("f", 1036)
        updated_data.wearTransmission = self.get_field("f", 1040)
        updated_data.wearCabin = self.get_field("f", 1044)
        updated_data.wearChassis = self.get_field("f", 1048)
        updated_data.wearWheels = self.get_field("f", 1052)
        updated_data.truckOdometer = self.get_field("f", 1056)
        updated_data.routeDistance = self.get_field("f", 1060)
        updated_data.routeTime = self.get_field("f", 1064)
        updated_data.speedLimit = self.get_field("f", 1068)
        updated_data.truck_wheelSuspDeflection = self.get_array("16f", 1072)
        updated_data.truck_wheelVelocity = self.get_array("16f", 1136)
        updated_data.truck_wheelSteering = self.get_array("16f", 1200)
        updated_data.truck_wheelRotation = self.get_array("16f", 1264)
        updated_data.truck_wheelLift = self.get_array("16f", 1328)
        updated_data.truck_wheelLiftOffset = self.get_array("16f", 1392)

        updated_data.jobDeliveredCargoDamage = self.get_field("f", 1456)
        updated_data.jobDeliveredDistanceKm = self.get_field("f", 1460)
        updated_data.refuelAmount = self.get_field("f", 1464)

        updated_data.cargoDamage = self.get_field("f", 1468)

        #----- END OF FOURTH ZONE AT OFFSET 1499 -----#

        #----- START OF FIFTH ZONE AT OFFSET 1500 -----#

        updated_data.truckWheelSteerable = self.get_array("16?", 1500)
        updated_data.truckWheelSimulated = self.get_array("16?", 1516)
        updated_data.truckWheelPowered = self.get_array("16?", 1532)
        updated_data.truckWheelLiftable = self.get_array("16?", 1548)

        updated_data.isCargoLoaded = self.get_field("?", 1564)
        updated_data.specialJob = self.get_field("?", 1565)

        updated_data.parkBrake = self.get_field("?", 1566)
        updated_data.motorBrake = self.get_field("?", 1567)
        updated_data.airPressureWarning = self.get_field("?", 1568)
        updated_data.airPressureEmergency = self.get_field("?", 1569)
        updated_data.fuelWarning = self.get_field("?", 1570)
        updated_data.adblueWarning = self.get_field("?", 1571)
        updated_data.oilPressureWarning = self.get_field("?", 1572)
        updated_data.waterTemperatureWarning = self.get_field("?", 1573)
        updated_data.batteryVoltageWarning = self.get_field("?", 1574)
        updated_data.electricEnabled = self.get_field("?", 1575)
        updated_data.engineEnabled = self.get_field("?", 1576)
        updated_data.wipers = self.get_field("?", 1577)
        updated_data.blinkerLeftActive = self.get_field("?", 1578)
        updated_data.blinkerRightActive = self.get_field("?", 1579)
        updated_data.blinkerLeftOn = self.get_field("?", 1580)
        updated_data.blinkerRightOn = self.get_field("?", 1581)
        updated_data.lightsParking = self.get_field("?", 1582)
        updated_data.lightsBeamLow = self.get_field("?", 1583)
        updated_data.lightsBeamHigh = self.get_field("?", 1584)
        updated_data.lightsBeacon = self.get_field("?", 1585)
        updated_data.lightsBrake = self.get_field("?", 1586)
        updated_data.lightsReverse = self.get_field("?", 1587)
        updated_data.lightsHazard = self.get_field("?", 1588)
        updated_data.cruiseControl = self.get_field("?", 1589) # special field not a sdk field
        updated_data.truck_wheelOnGround = self.get_array("16?", 1590)
        updated_data.shifterToggle = self.get_array("16?", 1606)
        updated_data.differentialLock = self.get_field("?", 1608)
        updated_data.liftAxle = self.get_field("?", 1609)
        updated_data.liftAxleIndicator = self.get_field("?", 1610)
        updated_data.trailerLiftAxle = self.get_field("?", 1611)
        updated_data.trailerLiftAxleIndicator = self.get_field("?", 1612)

        updated_data.jobDeliveredAutoparkUsed = self.get_field("?", 1613)
        updated_data.jobDeliveredAutoloadUsed = self.get_field("?", 1614)

        #----- END OF FIFTH ZONE AT OFFSET 1639 -----#

        #----- START OF SIXTH ZONE AT OFFSET 1640 -----#

        updated_data.cabinPositionX = 0.0
        updated_data.cabinPositionY = 0.0
        updated_data.cabinPositionZ = 0.0
        updated_data.headPositionX = 0.0
        updated_data.headPositionY = 0.0
        updated_data.headPositionZ = 0.0
        updated_data.truckHookPositionX = 0.0
        updated_data.truckHookPositionY = 0.0
        updated_data.truckHookPositionZ = 0.0
        updated_data.truckWheelPositionX = 0.0 # [16]
        updated_data.truckWheelPositionY = 0.0 # [16]
        updated_data.truckWheelPositionZ = 0.0 # [16]

        updated_data.lv_accelerationX = 0.0
        updated_data.lv_accelerationY = 0.0
        updated_data.lv_accelerationZ = 0.0
        updated_data.av_accelerationX = 0.0
        updated_data.av_accelerationY = 0.0
        updated_data.av_accelerationZ = 0.0
        updated_data.accelerationX = 0.0
        updated_data.accelerationY = 0.0
        updated_data.accelerationZ = 0.0
        updated_data.aa_accelerationX = 0.0
        updated_data.aa_accelerationY = 0.0
        updated_data.aa_accelerationZ = 0.0
        updated_data.cabinAVX = 0.0
        updated_data.cabinAVY = 0.0
        updated_data.cabinAVZ = 0.0
        updated_data.cabinAAX = 0.0
        updated_data.cabinAAY = 0.0
        updated_data.cabinAAZ = 0.0

        updated_data.cabinOffsetX = 0.0
        updated_data.cabinOffsetY = 0.0
        updated_data.cabinOffsetZ = 0.0
        updated_data.cabinOffsetrotationX = 0.0
        updated_data.cabinOffsetrotationY = 0.0
        updated_data.cabinOffsetrotationZ = 0.0
        updated_data.headOffsetX = 0.0
        updated_data.headOffsetY = 0.0
        updated_data.headOffsetZ = 0.0
        updated_data.headOffsetrotationX = 0.0
        updated_data.headOffsetrotationY = 0.0
        updated_data.headOffsetrotationZ = 0.0

        #----- END OF 7TH ZONE AT OFFSET 2199 -----#

        #----- START OF 8TH ZONE AT OFFSET 2200 -----#

        updated_data.coordinateX = 0.0
        updated_data.coordinateY = 0.0
        updated_data.coordinateZ = 0.0
        updated_data.rotationX = 0.0
        updated_data.rotationY = 0.0
        updated_data.rotationZ = 0.0

        #----- END OF 8TH ZONE AT OFFSET 2299 -----#

        #----- START OF 9TH ZONE AT OFFSET 2300 -----#

        updated_data.truckBrandId = "" # [stringsize]
        updated_data.truckBrand = "" # [stringsize]
        updated_data.truckId = "" # [stringsize]

        updated_data.truckName = "" # [stringsize]
        updated_data.cargoId = "" # [stringsize]
        updated_data.cargo = "" # [stringsize]
        updated_data.cityDstId = "" # [stringsize]
        updated_data.cityDst = "" # [stringsize]
        updated_data.compDstId = "" # [stringsize]
        updated_data.compDst = "" # [stringsize]
        updated_data.citySrcId = "" # [stringsize]
        updated_data.citySrc = "" # [stringsize]
        updated_data.compSrcId = "" # [stringsize]
        updated_data.compSrc = "" # [stringsize]
        updated_data.shifterType = "" # [16]

        updated_data.truckLicensePlate = "" # [stringsize]
        updated_data.truckLicensePlateCountryId = "" # [stringsize]
        updated_data.truckLicensePlateCountry = "" # [stringsize]

        updated_data.jobMarket = "" # [32]

        updated_data.fineOffence = "" # [32]
        updated_data.ferrySourceName = "" # [stringsize]
        updated_data.ferryTargetName = "" # [stringsize]
        updated_data.ferrySourceId = "" # [stringsize]
        updated_data.ferryTargetId = "" # [stringsize]
        updated_data.trainSourceName = "" # [stringsize]
        updated_data.trainTargetName = "" # [stringsize]
        updated_data.trainSourceId = "" # [stringsize]
        updated_data.trainTargetId = "" # [stringsize]

        #----- END OF 9TH ZONE AT OFFSET 3999 -----#

        #----- START OF 10TH ZONE AT OFFSET 4000 -----#

        updated_data.jobIncome = 0

        #----- END OF 10TH ZONE AT OFFSET 4199 -----#

        #----- START OF 11TH ZONE AT OFFSET 4200 -----#

        updated_data.jobCancelledPenalty = 0
        updated_data.jobDeliveredRevenue = 0
        updated_data.fineAmount = 0
        updated_data.tollgatePayAmount = 0
        updated_data.ferryPayAmount = 0
        updated_data.trainPayAmount = 0

        #----- END OF 11TH ZONE AT OFFSET 4299 -----#

        #----- START OF 12TH ZONE AT OFFSET 4300 -----#

        updated_data.onJob = False
        updated_data.jobFinished = False
        updated_data.jobCancelled = False
        updated_data.jobDelivered = False
        updated_data.fined = False
        updated_data.tollgate = False
        updated_data.ferry = False
        updated_data.train = False
        updated_data.refuel = False
        updated_data.refuelPayed = False

        #----- END OF 12TH ZONE AT OFFSET 4399 -----#

        updated_data.substance = "" #[SUBSTANCE_SIZE][stringsize]

        #----- END OF 13TH ZONE AT OFFSET 5999 -----#

        #----- START OF 14TH ZONE AT OFFSET 6000 -----//

        updated_data.trailer = SCS_Trailer() # [10]

        #----- END OF 14TH ZONE AT OFFSET 21619 -----#

        return updated_data
    
    def get_field(self, f, start):
        field_data = struct.unpack(f, self.mmap[start:(start + struct.calcsize(f))])[0]
        return field_data
    
    def get_array(self, f, start) -> list:
        array_data = list(struct.unpack(f, self.mmap[start:(start + struct.calcsize(f))]))
        return array_data

class SCS_Trailer:
    def __init__(self) -> None:
        #----- START OF FIRST ZONE AT OFFSET 0 -----#

        self.wheelSteerable = [False] * 16
        self.wheelSimulated = [False] * 16
        self.wheelPowered = [False] * 16
        self.wheelLiftable = [False] * 16

        self.wheelOnGround = [False] * 16
        self.attached = False

        #----- END OF FIRST ZONE AT OFFSET 83 -----#

	    #----- START OF SECOND ZONE AT OFFSET 84 -----#
         
        self.wheelSubstance = [0] * 16

        self.wheelCount = 0

        #----- END OF SECOND ZONE AT OFFSET 151 -----#

	    #----- START OF THIRD ZONE AT OFFSET 152 -----#
         
        self.cargoDamage = 0.0
        self.wearChassis = 0.0
        self.wearWheels = 0.0
        self.wearBody = 0.0
        self.wheelSuspDeflection = [0.0] * 16
        self.wheelVelocity = [0.0] * 16
        self.wheelSteering = [0.0] * 16
        self.wheelRotation = [0.0] * 16
        self.wheelLift = [0.0] * 16
        self.wheelLiftOffset = [0.0] * 16
        #----- END OF THIRD ZONE AT OFFSET 615 -----#

        #----- START OF 4TH ZONE AT OFFSET 616 -----#
        
        self.linearVelocityX = 0.0
        self.linearVelocityY = 0.0
        self.linearVelocityZ = 0.0
        self.angularVelocityX = 0.0
        self.angularVelocityY = 0.0
        self.angularVelocityZ = 0.0
        self.linearAccelerationX = 0.0
        self.linearAccelerationY = 0.0
        self.linearAccelerationZ = 0.0
        self.angularAccelerationX = 0.0
        self.angularAccelerationY = 0.0
        self.angularAccelerationZ = 0.0

        self.hookPositionX = 0.0
        self.hookPositionY = 0.0
        self.hookPositionZ = 0.0
        self.wheelPositionX = [0.0] * 16
        self.wheelPositionY = [0.0] * 16
        self.wheelPositionZ = [0.0] * 16

        #----- END OF 4TH ZONE AT OFFSET 871 -----#

        #----- START OF 5TH ZONE AT OFFSET 872 -----#
          
        self.worldX = 0.0
        self.worldY = 0.0
        self.worldZ = 0.0
        self.rotationX = 0.0
        self.rotationY = 0.0
        self.rotationZ = 0.0

        #----- END OF 5TH ZONE AT OFFSET 919 -----#

        #----- START OF 6TH ZONE AT OFFSET 920 -----#
          
        self.id = "" # [stringsize]
        self.cargoAcessoryId = "" # [stringsize]
        self.bodyType = "" # [stringsize]
        self.brandId = "" # [stringsize]
        self.brand = "" # [stringsize]
        self.name = "" # [stringsize]
        self.chainType = "" # [stringsize]
        self.licensePlate = "" # [stringsize]
        self.licensePlateCountry = "" # [stringsize]
        self.licensePlateCountryId = "" # [stringsize]

        #----- END OF 6TH ZONE AT OFFSET 1559 -----#

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
        self.truck_wheelSubstance = [0] * 16
        self.hshifterPosition = [0] * 32
        self.hshifterBitmask = [0] * 32

        self.jobDeliveredDeliveryTime = 0
        self.jobStartingTime = 0
        self.jobFinishedTime = 0

        #----- END OF SECOND ZONE AT OFFSET 499 -----#

        #----- START OF Third ZONE AT OFFSET 500 -----#

        self.restStop = 0

        self.gear = 0
        self.gearDashboard = 0
        self.hshifterResulting = [0] * 32

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
        self.truck_wheelSuspDeflection = [0.0] * 16
        self.truck_wheelVelocity = [0.0] * 16
        self.truck_wheelSteering = [0.0] * 16
        self.truck_wheelRotation = [0.0] * 16
        self.truck_wheelLift = [0.0] * 16
        self.truck_wheelLiftOffset = [0.0] * 16

        self.jobDeliveredCargoDamage = 0.0
        self.jobDeliveredDistanceKm = 0.0
        self.refuelAmount = 0.0

        self.cargoDamage = 0.0

        #----- END OF FOURTH ZONE AT OFFSET 1499 -----#

        #----- START OF FIFTH ZONE AT OFFSET 1500 -----#

        self.truckWheelSteerable = [False] * 16
        self.truckWheelSimulated = [False] * 16
        self.truckWheelPowered = [False] * 16
        self.truckWheelLiftable = [False] * 16

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
        self.truck_wheelOnGround = [False] * 16
        self.shifterToggle = [False] * 2
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
        self.truckWheelPositionX = [0.0] * 16
        self.truckWheelPositionY = [0.0] * 16
        self.truckWheelPositionZ = [0.0] * 16

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

        self.trailer = SCS_Trailer() # [10]

        #----- END OF 14TH ZONE AT OFFSET 21619 -----#