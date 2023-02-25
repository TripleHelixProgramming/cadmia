import ntcore

class NetworkTablesIO:
    def __init__(self):
        # Initialize NT4 client
        self.inst = ntcore.NetworkTableInstance.getDefault()
        self.table = self.inst.getTable("cadmia")
        self.inst.startClient4("cadmia_client")
        self.inst.setServer("localhost")

        self.publishers = []
        for index in range(5):
            self.publishers.append(self.table.getDoubleArrayTopic("video" + str(index)).publish(
                ntcore.PubSubOptions(periodic=0, sendAll=True, keepDuplicates=True)))

    def get_time(self):
        return ntcore._now()

    def publish_result(self, index, time, corners, ids):
        result = []
        for tag_index in range(len(corners)):
            result.append(ids[tag_index][0])
            for corner in corners[tag_index][0]:
                result.append(corner[0])
                result.append(corner[1])
        self.publishers[index].set(result, time)