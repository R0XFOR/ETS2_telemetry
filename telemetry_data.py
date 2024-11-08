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
        self.truck_wheelSubstance = 0
        self.hshifterPosition = 0
        self.hshifterBitmask = 0

if __name__ == "__main__":
    data = SharedMemory().update()
    print(data.sdkActive, data.paused)