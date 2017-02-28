from networktables import NetworkTables 

TABLE_NAME = 'ImageProc'
DO_WORK_NAME = 'calculate'
HORIZONTAL_DATA_NAME = 'horizontal'
VERTICAL_DATA_NAME = 'vertical'

class TableManager:
    def __init__(self):
        self.startup()

        self.vision_table = NetworkTables.getTable(TABLE_NAME)
        self.do_work = self.vision_table.getBoolean(DO_WORK_NAME, False)
        self.vision_table.addTableListener(self.do_work_changed, True, DO_WORK_NAME, False)

    def startup(self):
        """Connection and setup of the networktables"""
        NetworkTables.initialize(server='10.43.20.2')

    def publish_target_data(self, horizontal_distance, horizontal_vector, vertical_distance):
        """
        Publish navigation data to target

        Publish the data needed to navigate to the target

        Parameters
        ----------
        horizontal_distance : int
            The horizontal distance to the target
        horizontal_vector : string
            The side to the target. L for left, R for right
        vertical_distance : int
            The vertical distance to the target

        Returns
        -------
        void
        """
        self.vision_table.putString(HORIZONTAL_DATA_NAME, horizontal_vector + str(horizontal_distance))
        self.vision_table.putNumber(VERTICAL_DATA_NAME, vertical_distance)

    def is_do_work(self):
        """Return True if the robot requesting calculation for target navigation"""
        return self.do_work

    def do_work_changed(self, table, key, value, isNew):
        """Handle change in the work request indicator"""
        if key == DO_WORK_NAME:
            self.do_work = value
