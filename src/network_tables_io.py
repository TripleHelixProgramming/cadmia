import ntcore

class NetworkTablesIO:
    def __init__(self, debug):
        # Initialize NT4 client
        self.inst = ntcore.NetworkTableInstance.getDefault()
        self.table = self.inst.getTable("cadmia")
        self.inst.startClient4("cadmia_client")
        if debug:
            self.inst.setServer("127.0.0.1")
        else:
            self.inst.setServerTeam(2363)

        self.publishers = []
        for index in range(5):
            self.publishers.append(self.table.getDoubleArrayTopic("video" + str(index)).publish(
                ntcore.PubSubOptions(periodic=0, sendAll=True, keepDuplicates=True)))

    def get_time(self):
        return ntcore._now()

    def publish_result(self, index, time, pose):
        print("post")
        t = pose.translation()
        r = pose.rotation()
        result = [t.X(), t.Y(), t.Z(), r.X(), r.Y(), r.Z()]
        self.publishers[index].set(result, time)