import ntcore

class NetworkTablesIO:
    def __init__(self, debug):
        # Initialize NT4 client
        self.inst = ntcore.NetworkTableInstance.getDefault()
        self.table = self.inst.getTable("cadmia")
        self.timetable = self.inst.getTable("time")
        self.inst.startClient4("cadmia_client")
        if debug:
            self.inst.setServer("127.0.0.1")
        else:
            self.inst.setServerTeam(2363)

        self.publishers = []
        for index in range(5):
            self.publishers.append(self.table.getDoubleArrayTopic("video" + str(index)).publish(
                ntcore.PubSubOptions(periodic=0.01, sendAll=True, keepDuplicates=True)))
        self.time_subscriber = self.timetable.getDoubleTopic("timer").subscribe(0.0,
                ntcore.PubSubOptions(periodic=0.01, sendAll=True, keepDuplicates=True))

    def get_time(self):
        return self.time_subscriber.get()

    def publish_result(self, index, time, pose):
        t = pose.translation()
        r = pose.rotation()
        result = [t.X(), t.Y(), t.Z(), r.X(), r.Y(), r.Z(), time]
        self.publishers[index].set(result)
